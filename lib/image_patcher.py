import os
import io
import re
import json
import zipfile
import tempfile
from pathlib import Path
from PIL import Image

try:
    import UnityPy
    UNITYPY_AVAILABLE = True
except ImportError:
    UNITYPY_AVAILABLE = False

def normalize_bundle_name(b_name: str) -> str:
    """
    Strips dynamic build dates (e.g. -2025-07-02) and build hash numbers (e.g. _assets_all_4288585921)
    to extract the raw semantic bundle family name.
    """
    fn = Path(b_name).name
    base = re.sub(r'\.bundle$', '', fn, flags=re.IGNORECASE)
    # Strip trailing hashes: _assets_all_\d+, _assets_\d+, or trailing _\d+
    base = re.sub(r'_assets_all_\d+$', '', base, flags=re.IGNORECASE)
    base = re.sub(r'_assets_\d+$', '', base, flags=re.IGNORECASE)
    # Strip build dates: -YYYY-MM-DD
    base = re.sub(r'-\d{4}-\d{2}-\d{2}', '', base)
    base = re.sub(r'_\d+$', '', base)
    return base.lower()

class ImagePatcher:
    """
    High-performance in-place Unity AssetBundle texture patcher.
    Applies translated PNG textures directly into the target game's AssetBundles using 
    O(1) lookups from 'image_bundle_map.json' and dynamic pattern matching across game updates.
    """

    @staticmethod
    def is_available() -> bool:
        return UNITYPY_AVAILABLE

    @staticmethod
    def patch(game_path: Path, images_zip_path: Path, map_data: dict, on_progress=None) -> int:
        if not UNITYPY_AVAILABLE:
            raise RuntimeError("UnityPy is not installed. Cannot patch images into game bundles.")

        bundle_to_images = map_data.get("bundle_to_images", {})
        if not bundle_to_images:
            return 0

        # Locate AssetBundles directory
        base_streaming = game_path / "BlueArchive_Data" / "StreamingAssets"
        bundles_dir = base_streaming / "AssetBundles"
        if not bundles_dir.exists():
            bundles_dir = base_streaming

        # 1. Build an in-memory disk index of all local bundle files for O(1) matching
        # (Handles exact filenames, normalized semantic names, and updated build hashes/dates)
        exact_disk_bundles: dict[str, Path] = {}
        normalized_disk_bundles: dict[str, Path] = {}

        if bundles_dir.exists():
            for root, _, files in os.walk(bundles_dir):
                for f in files:
                    if f.lower().endswith(".bundle"):
                        full_p = Path(root) / f
                        f_lower = f.lower()
                        exact_disk_bundles[f_lower] = full_p
                        
                        norm_k = normalize_bundle_name(f)
                        if norm_k not in normalized_disk_bundles:
                            normalized_disk_bundles[norm_k] = full_p

        # 2. Extract images.zip to temporary directory for fast disk access
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with zipfile.ZipFile(images_zip_path, 'r') as zf:
                zf.extractall(temp_path)

            total_bundles = len(bundle_to_images)
            patched_textures_count = 0

            for idx, (bundle_ref, texture_names) in enumerate(bundle_to_images.items(), 1):
                # Resolve target bundle on disk with multi-tier fallback:
                # 1) Exact filename match
                # 2) Normalized semantic pattern match (ignores dynamic dates/hashes)
                # 3) Prefix match
                bundle_fn = Path(bundle_ref).name.lower()
                bundle_file = exact_disk_bundles.get(bundle_fn)

                if not bundle_file:
                    norm_target = normalize_bundle_name(bundle_fn)
                    bundle_file = normalized_disk_bundles.get(norm_target)

                if not bundle_file:
                    # Final prefix scan fallback
                    norm_target = normalize_bundle_name(bundle_fn)
                    for k, p in normalized_disk_bundles.items():
                        if k.startswith(norm_target) or norm_target.startswith(k):
                            bundle_file = p
                            break

                if not bundle_file or not bundle_file.exists():
                    continue

                if on_progress:
                    percent = idx / total_bundles
                    on_progress(f"Patching: Translated Images ({idx}/{total_bundles})", percent)

                # Preload target PNGs for this bundle
                textures_to_apply = {}
                for tex_name in texture_names:
                    png_path = temp_path / f"{tex_name}.png"
                    if png_path.exists():
                        try:
                            textures_to_apply[tex_name.lower()] = Image.open(png_path)
                        except Exception:
                            pass

                if not textures_to_apply:
                    continue

                # Load Unity bundle from bytes in memory to avoid Windows file locks
                try:
                    with open(bundle_file, "rb") as bf:
                        bundle_bytes = bf.read()

                    env = UnityPy.load(bundle_bytes)
                    modified = False

                    for obj in env.objects:
                        if obj.type.name in ["Texture2D", "Sprite"]:
                            try:
                                data = obj.read()
                                obj_name = (getattr(data, "m_Name", None) or getattr(data, "name", "")).lower()
                                if obj_name in textures_to_apply:
                                    data.image = textures_to_apply[obj_name]
                                    data.save()
                                    modified = True
                                    patched_textures_count += 1
                            except Exception:
                                pass

                    if modified:
                        temp_dest = bundle_file.with_suffix(bundle_file.suffix + ".tmp")
                        with open(temp_dest, "wb") as f:
                            f.write(env.file.save(packer="lz4"))
                        
                        if bundle_file.exists():
                            os.remove(bundle_file)
                        os.rename(temp_dest, bundle_file)

                except Exception as e:
                    print(f"Error patching {bundle_file.name}: {e}")

            return patched_textures_count

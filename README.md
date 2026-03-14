
# BA-TL-Launcher
**The official automated patcher for Blue Archive JP English Translation.**

[![Build Status](https://github.com/Special-Operation-Decagrammaton/BA-TL-Launcher/actions/workflows/build.yml/badge.svg)](https://github.com/Special-Operation-Decagrammaton/BA-TL-Launcher/actions)
[![Latest Release](https://img.shields.io/github/v/release/Special-Operation-Decagrammaton/BA-TL-Launcher)](https://github.com/Special-Operation-Decagrammaton/BA-TL-Launcher/releases)

`BA-TL-Launcher` is a GUI utility designed to simplify the patching process for Blue Archive JP. Instead of manual file replacement, this launcher automates the synchronization between your game files and the translated assets maintained by the community.

---

## 🛠️ How it Works
The launcher is designed to be lightweight and efficient:
1.  **Manifest Check:** It fetches the `GameManifest.json` from the [BA-TL-Assets](https://github.com/Special-Operation-Decagrammaton/BA-TL-Assets) release page.
2.  **Version Comparison:** It compares your local files with the manifest to determine which assets need updating.
3.  **Direct Download:** It downloads only the necessary modified assets directly from the latest asset releases.
4.  **Patching:** It applies the translation layer (either "Vanilla Global" or "Community Translation") based on your preference.

---

## 🌐 The Ecosystem
The launcher sits at the end of a three-stage pipeline:

### 📥 [BA-TL-Assets](https://github.com/Special-Operation-Decagrammaton/BA-TL-Assets)
**This is the only repository the Launcher interacts with.** It contains the compiled, game-ready assets.
*   **Main Branch:** Direct port of Global translations to JP (No modifications).
*   **Translation Branch:** Community-enhanced text sourced from `BA-TL-TEXT`.
*   **Releases:** Contains the `GameManifest.json` and the actual patched files used by the GUI.

### 📝 [BA-TL-TEXT](https://github.com/Special-Operation-Decagrammaton/BA-TL-TEXT)
Contains the `.toml` files where the community adds and modifies translations. These files are used to compile the assets found in the `translation` branch of the Assets repo.

### 🔍 [BA-RAW-TEXT](https://github.com/Special-Operation-Decagrammaton/BA-RAW-TEXT)
A repository for raw localization data used by developers and translators to compare versions:
*   `gl`: Full Global text dump.
*   `jp`: Full JP text dump.
*   `main`: Tracks content missing from Global that requires manual translation.

---

## ✨ Launcher Features
- **Automated Updates:** Uses `GameManifest.json` to ensure you always have the latest translation.
- **Branch Selection:** Easily switch between the "Vanilla" Global port and the "Community" enhanced translation.
- **Integrity Check:** Verifies game files to ensure the patch is applied correctly.
- **Modern UI:** Built with `CustomTkinter` for a clean, user-friendly experience.

---

## 🚀 Installation

### Windows
1. Download `BA_TL_Launcher_windows.exe` from the [Releases](https://github.com/Special-Operation-Decagrammaton/BA-TL-Launcher/releases) page.
2. Run the executable and point it to your Blue Archive JP installation folder.

### Linux
1. Download `BA_TL_Launcher_linux` from the [Releases](https://github.com/Special-Operation-Decagrammaton/BA-TL-Launcher/releases) page.
2. Grant execution permissions: `chmod +x BA_TL_Launcher_linux`
3. Run the binary.

---

## ⚠️ Disclaimer
**BA-TL-Launcher** is an unofficial fan tool. 
- We are not affiliated with Nexon, NAT Games, or Yostar.
- Modifying game files carries a theoretical risk of account suspension. Use at your own risk.
- This tool does not distribute game binaries; it only patches text-based assets.

---
*Maintained by the Special Operation Decagrammaton team.*
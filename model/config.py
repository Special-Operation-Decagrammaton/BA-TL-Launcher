from pathlib import Path
from pydantic import BaseModel
from enum import Enum

class Language(Enum):
    EN = "en"

class BuildTag(Enum):
    LATEST = "latest-build"
    TRANSLATION = "translation-build"
    
class Branch(Enum):
    MAIN = "main"
    TRANSLATION = "translation"
    
    @classmethod
    def list_values(cls):
        return [member.value for member in cls]

class LauncherConfig(BaseModel):
    GamePath: Path
    Language: Language
    Branch: Branch
    BuildTag: BuildTag
    CloseOnLaunch: bool
    
def load_config(file_path: Path) -> LauncherConfig:
    return LauncherConfig.model_validate_json(file_path.read_text())

def save_config(config: LauncherConfig, file_path: Path) -> None:
    json_data = config.model_dump_json(indent=4)
    file_path.write_text(json_data)
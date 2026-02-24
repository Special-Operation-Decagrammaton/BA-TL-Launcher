from typing import Any, Protocol
import customtkinter as ctk

from model.config import LauncherConfig
from model.manifest import GameManifest

class AppInterface(Protocol):
    launch_manager: Any
    setting_manager: Any
    update_manager: Any
        
    game_config: LauncherConfig
    game_manifest: GameManifest
    
    github_btn: ctk.CTkButton
    label: ctk.CTkLabel
    description: ctk.CTkLabel
    branch_frame: ctk.CTkFrame
    branch_description: ctk.CTkLabel
    branch_option: ctk.CTkOptionMenu
    status_label: ctk.CTkLabel
    progress_bar: ctk.CTkProgressBar
    
    button_frame: ctk.CTkFrame
    btn_check: ctk.CTkButton
    btn_folder: ctk.CTkButton
    btn_launch: ctk.CTkButton
    btn_update: ctk.CTkButton
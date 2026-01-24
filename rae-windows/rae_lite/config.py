"""
RAE-Lite Configuration.
"""

from pathlib import Path
import sys
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """RAE-Lite settings."""

    # App info
    app_name: str = "RAE-Lite"
    app_version: str = "0.1.0"

    # Server
    server_host: str = "127.0.0.1"
    server_port: int = 8765

    # Storage paths
    data_dir: Path = Path.home() / ".rae-lite" / "data"
    db_path: Path = data_dir / "rae_memory.db"
    vector_db_path: Path = data_dir / "rae_vectors.db"
    graph_db_path: Path = data_dir / "rae_graph.db"

    # Memory engine
    enable_reflections: bool = True
    enable_auto_consolidation: bool = True

    # Hardware & LLM
    selected_profile: str = "A"  # A, B, C, D
    llama_path: Path = Path.home() / ".rae-lite" / "bin" / ("llama-cli.exe" if "win" in sys.platform else "llama-cli")
    model_path: Optional[Path] = None
    
    # UI
    show_notifications: bool = True
    auto_start: bool = False

    class Config:
        env_prefix = "RAE_LITE_"
        case_sensitive = False

    def ensure_data_dir(self) -> None:
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_profile(self) -> None:
        """Load profile from data directory if exists."""
        profile_file = self.data_dir / "profile.json"
        if profile_file.exists():
            import json
            try:
                data = json.loads(profile_file.read_text())
                self.selected_profile = data.get("profile", "A")
                if "model_path" in data:
                    self.model_path = Path(data["model_path"])
            except Exception:
                pass

    def save_profile(self, profile: str, model_path: Optional[str] = None) -> None:
        """Save selected profile to data directory."""
        import json
        self.selected_profile = profile
        if model_path:
            self.model_path = Path(model_path)
        
        profile_file = self.data_dir / "profile.json"
        data = {"profile": profile}
        if self.model_path:
            data["model_path"] = str(self.model_path)
            
        profile_file.write_text(json.dumps(data))


settings = Settings()
settings.ensure_data_dir()

"""
Configuration Management
Load and manage Jarvis configuration
"""

import yaml
import os
from pathlib import Path
from loguru import logger
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for Jarvis"""
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file or self._get_default_config_path()
        self.config = self._load_config()
        logger.info(f"Configuration loaded from {self.config_file}")
    
    def _get_default_config_path(self) -> Path:
        """Get default configuration file path"""
        config_path = Path(__file__).parent.parent.parent / "config" / "settings.yaml"
        
        if not config_path.exists():
            config_path = Path.home() / ".jarvis" / "settings.yaml"
        
        return config_path
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    config = yaml.safe_load(f)
                    return config or {}
            else:
                logger.warning(f"Config file not found: {self.config_file}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "voice": {
                "engine": "google",
                "language": "en-US",
                "rate": 150,
                "volume": 0.9,
            },
            "nlp": {
                "confidence_threshold": 0.6,
            },
            "logging": {
                "level": "INFO",
                "file": str(Path.home() / ".jarvis" / "jarvis.log"),
            },
            "automation": {
                "enabled": True,
                "max_tasks": 100,
            },
            "memory": {
                "storage": "sqlite",
                "db_path": str(Path.home() / ".jarvis" / "memory.db"),
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key (dot notation supported, e.g., "voice.engine")
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Configuration key (dot notation supported)
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.debug(f"Config updated: {key}={value}")
    
    def save(self, config_file: str = None) -> bool:
        """
        Save configuration to file
        
        Args:
            config_file: Path to save config
        
        Returns:
            True if successful
        """
        try:
            path = Path(config_file or self.config_file)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            
            logger.info(f"Configuration saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return self.config.copy()

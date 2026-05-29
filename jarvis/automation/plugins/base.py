"""
Base Plugin Class
Foundation for creating Jarvis plugins
"""

from abc import ABC, abstractmethod
from loguru import logger
from typing import Dict, Any


class Plugin(ABC):
    """Base class for Jarvis plugins"""
    
    def __init__(self, name: str):
        """
        Initialize plugin
        
        Args:
            name: Plugin name
        """
        self.name = name
        self.enabled = True
        logger.info(f"Plugin initialized: {name}")
    
    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        """
        Check if plugin can handle intent
        
        Args:
            intent: Intent to check
        
        Returns:
            True if plugin can handle, False otherwise
        """
        pass
    
    @abstractmethod
    def execute(self, entities: Dict[str, Any]) -> str:
        """
        Execute plugin action
        
        Args:
            entities: Entity dictionary from NLP
        
        Returns:
            Result string
        """
        pass
    
    def setup(self) -> None:
        """Setup plugin (called on initialization)"""
        logger.debug(f"Setting up plugin: {self.name}")
    
    def teardown(self) -> None:
        """Teardown plugin (called on shutdown)"""
        logger.debug(f"Tearing down plugin: {self.name}")
    
    def enable(self) -> None:
        """Enable plugin"""
        self.enabled = True
        logger.info(f"Plugin enabled: {self.name}")
    
    def disable(self) -> None:
        """Disable plugin"""
        self.enabled = False
        logger.info(f"Plugin disabled: {self.name}")
    
    def is_enabled(self) -> bool:
        """Check if plugin is enabled"""
        return self.enabled

"""
Command Parser
Parses and validates commands for execution
"""

from loguru import logger
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class Command:
    """Represents a parsed command"""
    intent: str
    entities: Dict[str, Any]
    confidence: float = 1.0
    raw_text: str = ""


class CommandParser:
    """Parse and validate commands"""
    
    def __init__(self, config=None):
        """
        Initialize command parser
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.custom_commands = {}
        logger.info("CommandParser initialized")
    
    def parse(self, intent: str, entities: Dict[str, Any]) -> Command:
        """
        Parse an intent and entities into a command
        
        Args:
            intent: Intent string
            entities: Dictionary of entities
        
        Returns:
            Parsed Command object
        """
        try:
            # Validate intent
            if not self._validate_intent(intent):
                logger.warning(f"Invalid intent: {intent}")
                return Command(intent="unknown", entities={})
            
            # Validate entities
            validated_entities = self._validate_entities(entities)
            
            # Create command
            command = Command(
                intent=intent,
                entities=validated_entities,
                raw_text=entities.get("raw_text", "")
            )
            
            logger.debug(f"Command parsed: {command}")
            return command
            
        except Exception as e:
            logger.error(f"Error parsing command: {e}")
            return Command(intent="unknown", entities={})
    
    def _validate_intent(self, intent: str) -> bool:
        """
        Validate intent string
        
        Args:
            intent: Intent to validate
        
        Returns:
            True if valid, False otherwise
        """
        if not intent:
            return False
        
        if not isinstance(intent, str):
            return False
        
        if len(intent) > 50:
            return False
        
        return True
    
    def _validate_entities(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean entities
        
        Args:
            entities: Entities dictionary
        
        Returns:
            Validated entities dictionary
        """
        validated = {}
        
        for key, value in entities.items():
            # Remove raw_text from entities
            if key == "raw_text":
                continue
            
            # Validate value types
            if isinstance(value, (str, int, float, bool, list, dict)):
                validated[key] = value
            else:
                logger.warning(f"Skipping invalid entity value: {key}={value}")
        
        return validated
    
    def register_custom_command(self, name: str, handler_func) -> None:
        """
        Register a custom command handler
        
        Args:
            name: Command name
            handler_func: Handler function
        """
        self.custom_commands[name] = handler_func
        logger.info(f"Custom command registered: {name}")
    
    def is_custom_command(self, intent: str) -> bool:
        """
        Check if intent is a custom command
        
        Args:
            intent: Intent to check
        
        Returns:
            True if custom command exists
        """
        return intent in self.custom_commands
    
    def get_custom_command(self, intent: str):
        """
        Get a custom command handler
        
        Args:
            intent: Intent name
        
        Returns:
            Handler function or None
        """
        return self.custom_commands.get(intent)

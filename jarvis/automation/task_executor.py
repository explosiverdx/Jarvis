"""
Task Executor
Executes automation tasks based on intents
"""

from loguru import logger
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import time


class TaskExecutor:
    """Execute automation tasks"""
    
    def __init__(self, config=None):
        """
        Initialize task executor
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.task_handlers = {}
        self._register_default_handlers()
        logger.info("TaskExecutor initialized")
    
    def _register_default_handlers(self):
        """Register default task handlers"""
        # Greeting tasks
        self.register_handler("greeting", self._handle_greeting)
        self.register_handler("goodbye", self._handle_goodbye)
        
        # Information tasks
        self.register_handler("get_time", self._handle_get_time)
        self.register_handler("get_date", self._handle_get_date)
        self.register_handler("show_help", self._handle_show_help)
        
        # Automation tasks
        self.register_handler("set_reminder", self._handle_set_reminder)
        self.register_handler("weather", self._handle_weather)
        self.register_handler("web_search", self._handle_web_search)
        
        # Unknown
        self.register_handler("unknown", self._handle_unknown)
    
    def register_handler(self, intent: str, handler: Callable) -> None:
        """
        Register a task handler
        
        Args:
            intent: Intent name
            handler: Handler function
        """
        self.task_handlers[intent] = handler
        logger.debug(f"Handler registered for intent: {intent}")
    
    def execute(self, intent: str, entities: Dict[str, Any]) -> str:
        """
        Execute a task based on intent
        
        Args:
            intent: Intent name
            entities: Entity dictionary
        
        Returns:
            Result string
        """
        try:
            handler = self.task_handlers.get(intent)
            
            if not handler:
                logger.warning(f"No handler for intent: {intent}")
                return self._handle_unknown(entities)
            
            logger.info(f"Executing task: {intent}")
            result = handler(entities)
            
            return result if result else "Task completed"
            
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            return f"Error executing task: {str(e)}"
    
    # Default handlers
    
    def _handle_greeting(self, entities: Dict[str, Any]) -> str:
        """Handle greeting"""
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What do you need?",
            "Hey! What can I do for you?",
            "Good to see you! What's on your mind?",
        ]
        import random
        return random.choice(greetings)
    
    def _handle_goodbye(self, entities: Dict[str, Any]) -> str:
        """Handle goodbye"""
        return "Goodbye! See you next time. Have a great day!"
    
    def _handle_get_time(self, entities: Dict[str, Any]) -> str:
        """Handle get time request"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}"
    
    def _handle_get_date(self, entities: Dict[str, Any]) -> str:
        """Handle get date request"""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}"
    
    def _handle_show_help(self, entities: Dict[str, Any]) -> str:
        """Handle help request"""
        help_text = """
        I can help you with:
        - Time and date queries
        - Weather information
        - Setting reminders
        - Web searches
        - Task automation
        - And much more!
        
        Just speak naturally and I'll try to help.
        """
        return help_text.strip()
    
    def _handle_set_reminder(self, entities: Dict[str, Any]) -> str:
        """Handle set reminder"""
        reminder_text = entities.get("query", "reminder")
        time_info = entities.get("time", "")
        
        if time_info:
            return f"I'll remind you to {reminder_text} at {time_info}"
        else:
            return f"I'll set a reminder for {reminder_text}"
    
    def _handle_weather(self, entities: Dict[str, Any]) -> str:
        """Handle weather request"""
        location = entities.get("location", "your location")
        return f"Let me check the weather for {location}. Unfortunately, I need API integration for this feature."
    
    def _handle_web_search(self, entities: Dict[str, Any]) -> str:
        """Handle web search"""
        query = entities.get("query", "that")
        return f"Searching for {query}. I would need to connect to a search engine for this."
    
    def _handle_unknown(self, entities: Dict[str, Any]) -> str:
        """Handle unknown intent"""
        responses = [
            "I'm not sure I understood that. Could you rephrase?",
            "Sorry, I didn't catch that. Can you say it again?",
            "I'm not sure how to help with that.",
            "That's not something I can do yet.",
        ]
        import random
        return random.choice(responses)
    
    def list_handlers(self) -> list:
        """Get list of registered handlers"""
        return list(self.task_handlers.keys())

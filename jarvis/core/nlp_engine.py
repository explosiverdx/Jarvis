"""
Natural Language Processing Engine
Handles intent recognition and entity extraction
"""

import json
from pathlib import Path
from loguru import logger
from typing import Tuple, Dict, Any, List
import re


class NLPEngine:
    """Natural Language Processing engine for intent recognition"""
    
    def __init__(self, config=None):
        """
        Initialize NLP engine
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.commands = self._load_commands()
        logger.info("NLPEngine initialized")
    
    def _load_commands(self) -> Dict[str, Any]:
        """Load command definitions from JSON file"""
        try:
            commands_path = Path(__file__).parent.parent.parent / "config" / "commands.json"
            if commands_path.exists():
                with open(commands_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load commands file: {e}")
        
        # Return default commands
        return self._get_default_commands()
    
    def _get_default_commands(self) -> Dict[str, Any]:
        """Get default command definitions"""
        return {
            "greeting": {
                "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
                "responses": ["Hello! How can I assist you?", "Hi there! What do you need?"],
                "intent": "greeting"
            },
            "weather": {
                "patterns": ["weather", "temperature", "forecast", "rain", "sunny"],
                "responses": ["Let me check the weather for you"],
                "intent": "weather"
            },
            "time": {
                "patterns": ["what time", "tell me time", "current time", "time is it"],
                "responses": ["Sure, let me check the time"],
                "intent": "get_time"
            },
            "date": {
                "patterns": ["what date", "today's date", "current date", "day is it"],
                "responses": ["Let me tell you the date"],
                "intent": "get_date"
            },
            "reminder": {
                "patterns": ["remind", "reminder", "set reminder", "remember"],
                "responses": ["I'll set a reminder for you"],
                "intent": "set_reminder"
            },
            "search": {
                "patterns": ["search", "find", "look up", "google"],
                "responses": ["Let me search that for you"],
                "intent": "web_search"
            },
            "help": {
                "patterns": ["help", "what can you do", "help me", "assist"],
                "responses": ["I can help you with many things"],
                "intent": "show_help"
            },
            "goodbye": {
                "patterns": ["goodbye", "bye", "exit", "quit", "stop"],
                "responses": ["Goodbye! See you later"],
                "intent": "goodbye"
            }
        }
    
    def process(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Process natural language input and extract intent and entities
        
        Args:
            text: Input text to process
        
        Returns:
            Tuple of (intent, entities)
        """
        if not text:
            return "unknown", {}
        
        try:
            # Clean text
            text = text.lower().strip()
            
            # Match against known commands
            intent, confidence = self._match_intent(text)
            
            if intent == "unknown":
                logger.warning(f"Unknown intent for: {text}")
            else:
                logger.info(f"Intent matched: {intent} (confidence: {confidence})")
            
            # Extract entities
            entities = self._extract_entities(text, intent)
            
            return intent, entities
            
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            return "unknown", {}
    
    def _match_intent(self, text: str) -> Tuple[str, float]:
        """
        Match text against known intents
        
        Args:
            text: Input text
        
        Returns:
            Tuple of (intent, confidence score)
        """
        best_match = ("unknown", 0.0)
        
        for command_name, command_data in self.commands.items():
            patterns = command_data.get("patterns", [])
            
            for pattern in patterns:
                if pattern in text:
                    # Calculate confidence (longer pattern match = higher confidence)
                    confidence = len(pattern) / len(text)
                    
                    if confidence > best_match[1]:
                        best_match = (command_data.get("intent", command_name), confidence)
        
        return best_match
    
    def _extract_entities(self, text: str, intent: str) -> Dict[str, Any]:
        """
        Extract entities from text based on intent
        
        Args:
            text: Input text
            intent: Identified intent
        
        Returns:
            Dictionary of extracted entities
        """
        entities = {"intent": intent}
        
        # Extract time expressions
        time_patterns = r'\b(\d{1,2}):(\d{2})\s?(am|pm)?\b'
        time_matches = re.findall(time_patterns, text)
        if time_matches:
            entities["time"] = time_matches[0]
        
        # Extract dates
        date_patterns = r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b'
        date_matches = re.findall(date_patterns, text)
        if date_matches:
            entities["date"] = date_matches[0]
        
        # Extract locations
        location_keywords = ["in", "at", "near", "around"]
        for keyword in location_keywords:
            if keyword in text:
                # Simple extraction: get words after location keywords
                parts = text.split(keyword)
                if len(parts) > 1:
                    entities["location"] = parts[1].strip()
                    break
        
        # Extract numbers
        number_patterns = r'\b\d+\b'
        numbers = re.findall(number_patterns, text)
        if numbers:
            entities["numbers"] = numbers
        
        # Extract query (for search operations)
        search_keywords = ["search", "find", "look up", "google"]
        for keyword in search_keywords:
            if keyword in text:
                query = text.split(keyword)[-1].strip()
                entities["query"] = query
                break
        
        return entities
    
    def get_response(self, intent: str) -> str:
        """
        Get a response for an intent
        
        Args:
            intent: Intent name
        
        Returns:
            Response string
        """
        for command_name, command_data in self.commands.items():
            if command_data.get("intent") == intent:
                responses = command_data.get("responses", [])
                if responses:
                    return responses[0]
        
        return "I'm not sure how to respond to that."
    
    def add_custom_intent(self, intent_name: str, patterns: List[str], 
                         responses: List[str]) -> None:
        """
        Add a custom intent
        
        Args:
            intent_name: Name of the intent
            patterns: List of pattern strings
            responses: List of response strings
        """
        self.commands[intent_name] = {
            "patterns": patterns,
            "responses": responses,
            "intent": intent_name
        }
        logger.info(f"Custom intent added: {intent_name}")

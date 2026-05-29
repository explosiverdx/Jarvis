"""
Memory Storage
Persistent storage for user data and interactions
"""

import json
import sqlite3
from pathlib import Path
from loguru import logger
from typing import Dict, List, Any, Optional
from datetime import datetime


class MemoryStorage:
    """Persistent memory storage using SQLite"""
    
    def __init__(self, config=None):
        """
        Initialize memory storage
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.db_path = Path.home() / ".jarvis" / "memory.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._initialize_database()
        logger.info(f"MemoryStorage initialized at {self.db_path}")
    
    def _initialize_database(self):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Interactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    command TEXT NOT NULL,
                    intent TEXT,
                    result TEXT,
                    success BOOLEAN DEFAULT 1
                )
            """)
            
            # User preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL
                )
            """)
            
            # Reminders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed BOOLEAN DEFAULT 0
                )
            """)
            
            # Custom intents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_intents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    patterns TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            logger.debug("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def store_interaction(self, command: str, intent: str, result: str, 
                         success: bool = True) -> int:
        """
        Store a user interaction
        
        Args:
            command: Original command text
            intent: Identified intent
            result: Result of execution
            success: Whether execution was successful
        
        Returns:
            Interaction ID
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO interactions (command, intent, result, success)
                VALUES (?, ?, ?, ?)
            """, (command, intent, result, success))
            
            conn.commit()
            interaction_id = cursor.lastrowid
            conn.close()
            
            logger.debug(f"Interaction stored: {interaction_id}")
            return interaction_id
            
        except Exception as e:
            logger.error(f"Error storing interaction: {e}")
            return -1
    
    def get_interactions(self, limit: int = 100, intent: str = None) -> List[Dict]:
        """
        Get stored interactions
        
        Args:
            limit: Maximum number of interactions to return
            intent: Filter by specific intent
        
        Returns:
            List of interaction dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if intent:
                cursor.execute("""
                    SELECT * FROM interactions 
                    WHERE intent = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (intent, limit))
            else:
                cursor.execute("""
                    SELECT * FROM interactions 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error retrieving interactions: {e}")
            return []
    
    def set_preference(self, key: str, value: str) -> bool:
        """
        Set a user preference
        
        Args:
            key: Preference key
            value: Preference value
        
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO preferences (key, value)
                VALUES (?, ?)
            """, (key, value))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"Preference set: {key}={value}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting preference: {e}")
            return False
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """
        Get a user preference
        
        Args:
            key: Preference key
            default: Default value if not found
        
        Returns:
            Preference value or default
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
            row = cursor.fetchone()
            conn.close()
            
            return row[0] if row else default
            
        except Exception as e:
            logger.error(f"Error getting preference: {e}")
            return default
    
    def add_reminder(self, title: str, description: str = None, 
                    due_date: str = None) -> int:
        """
        Add a reminder
        
        Args:
            title: Reminder title
            description: Reminder description
            due_date: Due date in ISO format
        
        Returns:
            Reminder ID
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO reminders (title, description, due_date)
                VALUES (?, ?, ?)
            """, (title, description, due_date))
            
            conn.commit()
            reminder_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"Reminder added: {reminder_id}")
            return reminder_id
            
        except Exception as e:
            logger.error(f"Error adding reminder: {e}")
            return -1
    
    def get_reminders(self, completed: bool = False) -> List[Dict]:
        """
        Get reminders
        
        Args:
            completed: Filter by completion status
        
        Returns:
            List of reminder dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM reminders 
                WHERE completed = ? 
                ORDER BY due_date
            """, (completed,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error retrieving reminders: {e}")
            return []
    
    def complete_reminder(self, reminder_id: int) -> bool:
        """
        Mark reminder as completed
        
        Args:
            reminder_id: ID of reminder
        
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE reminders 
                SET completed = 1 
                WHERE id = ?
            """, (reminder_id,))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"Reminder completed: {reminder_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error completing reminder: {e}")
            return False

"""
Jarvis Main Entry Point
This is the main script to run the Jarvis voice assistant.
"""

import sys
import signal
from loguru import logger
from jarvis.core.voice_engine import VoiceEngine
from jarvis.core.nlp_engine import NLPEngine
from jarvis.automation.task_executor import TaskExecutor
from jarvis.memory.storage import MemoryStorage
from jarvis.utils.config import Config


class Jarvis:
    """Main Jarvis assistant class"""
    
    def __init__(self):
        """Initialize Jarvis components"""
        logger.info("Initializing Jarvis...")
        
        self.config = Config()
        self.voice_engine = VoiceEngine(self.config)
        self.nlp_engine = NLPEngine(self.config)
        self.task_executor = TaskExecutor(self.config)
        self.memory = MemoryStorage(self.config)
        
        self.running = False
        logger.info("Jarvis initialized successfully")
    
    def start(self):
        """Start the Jarvis assistant"""
        logger.info("Starting Jarvis voice assistant...")
        self.running = True
        
        # Play startup sound
        self.voice_engine.speak("Hello! I'm Jarvis, your personal assistant. How can I help you?")
        
        try:
            self.listen_loop()
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            self.stop()
    
    def listen_loop(self):
        """Main listening loop"""
        while self.running:
            try:
                logger.debug("Listening for command...")
                
                # Listen for voice command
                command = self.voice_engine.listen()
                
                if not command:
                    continue
                
                logger.info(f"Command received: {command}")
                
                # Process with NLP
                intent, entities = self.nlp_engine.process(command)
                logger.debug(f"Intent: {intent}, Entities: {entities}")
                
                # Execute task
                result = self.task_executor.execute(intent, entities)
                
                # Store in memory
                self.memory.store_interaction(command, intent, result)
                
                # Respond with voice
                if result:
                    self.voice_engine.speak(result)
                
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                self.voice_engine.speak("I encountered an error processing that command.")
    
    def stop(self):
        """Stop Jarvis"""
        logger.info("Stopping Jarvis...")
        self.running = False
        self.voice_engine.speak("Goodbye! See you later.")
        logger.info("Jarvis stopped")
        sys.exit(0)


def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.warning("Received shutdown signal")
    sys.exit(0)


def main():
    """Main function"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start Jarvis
    jarvis = Jarvis()
    jarvis.start()


if __name__ == "__main__":
    main()

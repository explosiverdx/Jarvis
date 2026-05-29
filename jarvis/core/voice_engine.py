"""
Voice Recognition and Text-to-Speech Engine
Handles all voice input/output operations
"""

import speech_recognition as sr
import pyttsx3
from loguru import logger
from typing import Optional


class VoiceEngine:
    """Voice recognition and synthesis engine"""
    
    def __init__(self, config=None):
        """
        Initialize voice engine
        
        Args:
            config: Configuration object
        """
        self.config = config
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self._setup_tts()
        
        logger.info("VoiceEngine initialized")
    
    def _setup_tts(self):
        """Configure text-to-speech engine"""
        try:
            # Set voice rate (speech speed)
            self.tts_engine.setProperty('rate', 150)
            
            # Set voice volume
            self.tts_engine.setProperty('volume', 0.9)
            
            # Set voice (0 = male, 1 = female)
            voices = self.tts_engine.getProperty('voices')
            if len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)
            
            logger.debug("TTS engine configured")
        except Exception as e:
            logger.warning(f"Could not configure TTS: {e}")
    
    def listen(self, timeout: int = 10, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input from microphone
        
        Args:
            timeout: Timeout to start listening (seconds)
            phrase_time_limit: Maximum phrase duration (seconds)
        
        Returns:
            Recognized text or None if no speech detected
        """
        try:
            with self.microphone as source:
                logger.debug("Listening for input...")
                
                # Adjust recognizer sensitivity to ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            # Try to recognize speech
            logger.debug("Recognizing speech...")
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            self.speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            self.speak("Sorry, I'm having trouble connecting to the speech service.")
            return None
        except sr.WaitTimeoutError:
            logger.debug("Listening timeout")
            return None
        except Exception as e:
            logger.error(f"Error during listening: {e}")
            return None
    
    def speak(self, text: str, wait: bool = True) -> None:
        """
        Synthesize and play speech
        
        Args:
            text: Text to speak
            wait: Wait for speech to finish playing
        """
        try:
            if not text:
                return
            
            logger.info(f"Speaking: {text}")
            self.tts_engine.say(text)
            
            if wait:
                self.tts_engine.runAndWait()
            else:
                self.tts_engine.startLoop(False)
        except Exception as e:
            logger.error(f"Error during speech synthesis: {e}")
    
    def listen_for_keyword(self, keyword: str, timeout: int = 30) -> bool:
        """
        Listen specifically for a keyword
        
        Args:
            keyword: Keyword to listen for
            timeout: Maximum listening time (seconds)
        
        Returns:
            True if keyword found, False otherwise
        """
        try:
            command = self.listen(timeout=timeout)
            if command and keyword.lower() in command:
                return True
            return False
        except Exception as e:
            logger.error(f"Error listening for keyword: {e}")
            return False
    
    def set_voice_properties(self, rate: int = None, volume: float = None) -> None:
        """
        Set voice properties
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0-1.0)
        """
        try:
            if rate is not None:
                self.tts_engine.setProperty('rate', rate)
            if volume is not None:
                self.tts_engine.setProperty('volume', volume)
            logger.debug("Voice properties updated")
        except Exception as e:
            logger.error(f"Error setting voice properties: {e}")
    
    def stop_speaking(self) -> None:
        """Stop current speech"""
        try:
            self.tts_engine.stop()
            logger.debug("Speech stopped")
        except Exception as e:
            logger.error(f"Error stopping speech: {e}")

"""Base classes for all messengers in SocialConnect."""

from abc import ABC, abstractmethod
from typing import Dict, List, Union, Any
import logging
from ..utils.logger import setup_logger


class BaseMessenger(ABC):
    """Abstract base class for all messenger implementations."""
    
    def __init__(self, logger_name: str = None):
        """
        Initialize base messenger.
        
        Args:
            logger_name: Name for the logger instance
        """
        self.logger = setup_logger(logger_name or self.__class__.__name__)
    
    @abstractmethod
    def send_message(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Send a message. Must be implemented by subclasses.
        
        Returns:
            Dict containing send results and status
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate messenger configuration. Must be implemented by subclasses.
        
        Returns:
            True if configuration is valid
        """
        pass
    
    def _log_success(self, recipient: str, message_type: str = "message"):
        """Log successful message send."""
        self.logger.info(f"{message_type.title()} sent successfully to {recipient}")
    
    def _log_error(self, recipient: str, error: str, message_type: str = "message"):
        """Log message send error."""
        self.logger.error(f"Failed to send {message_type} to {recipient}: {error}")

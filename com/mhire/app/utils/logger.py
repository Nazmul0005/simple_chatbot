import logging
import sys
from typing import Optional
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        
        return super().format(record)


class ChatEndpoint:
    """Logger factory for different components"""
    
    @staticmethod
    def _setup_logger(
        name: str, 
        level: int = logging.INFO,
        use_colors: bool = True
    ) -> logging.Logger:
        """
        Setup a logger with console handler
        
        Args:
            name: Logger name
            level: Logging level
            use_colors: Whether to use colored output
            
        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        
        # Avoid adding handlers multiple times
        if logger.hasHandlers():
            return logger
        
        logger.setLevel(level)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Create formatter
        if use_colors:
            formatter = ColoredFormatter(
                fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            formatter = logging.Formatter(
                fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def setup_chat_logger(debug: bool = False) -> logging.Logger:
        """
        Setup logger for chat service
        
        Args:
            debug: If True, set to DEBUG level
        """
        level = logging.DEBUG if debug else logging.INFO
        return ChatEndpoint._setup_logger('chat_service', level)
    
    @staticmethod
    def setup_router_logger(debug: bool = False) -> logging.Logger:
        """Setup logger for router"""
        level = logging.DEBUG if debug else logging.INFO
        return ChatEndpoint._setup_logger('router', level)
    
    @staticmethod
    def setup_schema_logger(debug: bool = False) -> logging.Logger:
        """Setup logger for schema validation"""
        level = logging.DEBUG if debug else logging.INFO
        return ChatEndpoint._setup_logger('schema', level)
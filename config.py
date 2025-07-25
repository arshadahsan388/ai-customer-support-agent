"""
Configuration module for the Support Agent system.

This module contains all configuration settings including API keys,
model settings, and system parameters.
"""

import os
from typing import Dict, Any

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB3_5qE8XKvpzGucAvtASwKNQTgndveRPg")

# Model Configuration
MODEL_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 0.3,
    "max_tokens": 1000
}

# System Configuration
SYSTEM_CONFIG = {
    "max_retry_attempts": 2,
    "similarity_threshold": 0.4,
    "escalation_log_path": "escalation_log.csv"
}

# Support Categories
SUPPORT_CATEGORIES = [
    "Billing",
    "Technical", 
    "Security",
    "General"
]

def get_model_config() -> Dict[str, Any]:
    """
    Get the model configuration dictionary.
    
    Returns:
        Dict[str, Any]: Model configuration parameters
    """
    return MODEL_CONFIG.copy()

def get_system_config() -> Dict[str, Any]:
    """
    Get the system configuration dictionary.
    
    Returns:
        Dict[str, Any]: System configuration parameters
    """
    return SYSTEM_CONFIG.copy()

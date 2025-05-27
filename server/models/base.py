"""
Base model module providing common functionality for database models.
This module defines the BaseModel abstract class that all models should extend.
"""
# filepath: server/models/base.py
from . import db

class BaseModel(db.Model):
    """
    Abstract base class for database models providing common functionality.
    
    This class provides shared validation and functionality for all models
    in the application. It's set as abstract so it won't create a table.
    """
    __abstract__ = True
    
    @staticmethod
    def validate_string_length(field_name, value, min_length=2, allow_none=False):
        """
        Validates the length of a string field.
        
        Args:
            field_name (str): Name of the field being validated (for error messages)
            value (str): The string value to validate
            min_length (int, optional): Minimum required length. Defaults to 2.
            allow_none (bool, optional): Whether None values are allowed. Defaults to False.
        
        Returns:
            str: The validated string value (or None if allow_none is True and value is None)
        
        Raises:
            ValueError: If the value is None when not allowed, not a string, or too short
        """
        if value is None:
            if allow_none:
                return value
            else:
                raise ValueError(f"{field_name} cannot be empty")
        
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
            
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
            
        return value
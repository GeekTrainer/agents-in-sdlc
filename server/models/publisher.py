"""
Publisher model module for the Tailspin Toys Crowd Funding application.
This module defines the Publisher database model and its relationships.
"""
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    """
    Publisher model representing game publishers in the database.
    
    A Publisher can have multiple games associated with it through
    a one-to-many relationship.
    """
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key, name):
        """
        Validates the publisher name.
        
        Args:
            key (str): Field name being validated
            name (str): The publisher name to validate
        
        Returns:
            str: The validated name
        
        Raises:
            ValueError: If name doesn't meet validation requirements
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        """
        Validates the publisher description.
        
        Args:
            key (str): Field name being validated
            description (str): The publisher description to validate
        
        Returns:
            str: The validated description or None if description is None and allow_none is True
        
        Raises:
            ValueError: If description doesn't meet validation requirements when provided
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self):
        """
        Returns a string representation of the Publisher.
        
        Returns:
            str: A string representing this publisher
        """
        return f'<Publisher {self.name}>'

    def to_dict(self):
        """
        Converts the Publisher model to a dictionary format for API responses.
        
        Returns:
            dict: Dictionary representation of the publisher with its attributes
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }
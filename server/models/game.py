"""
Game model module for the Tailspin Toys Crowd Funding application.
This module defines the Game database model and its relationships with Category and Publisher.
"""
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Game(BaseModel):
    """
    Game model representing boardgames in the database.
    
    A Game belongs to one Category and one Publisher through
    many-to-one relationships.
    """
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    star_rating = db.Column(db.Float, nullable=True)
    
    # Foreign keys for one-to-many relationships
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'), nullable=False)
    
    # One-to-many relationships (many games belong to one category/publisher)
    category = relationship("Category", back_populates="games")
    publisher = relationship("Publisher", back_populates="games")
    
    @validates('title')
    def validate_name(self, key, name):
        """
        Validates the game title.
        
        Args:
            key (str): Field name being validated
            name (str): The game title to validate
        
        Returns:
            str: The validated title
        
        Raises:
            ValueError: If title doesn't meet validation requirements
        """
        return self.validate_string_length('Game title', name, min_length=2)
    
    @validates('description')
    def validate_description(self, key, description):
        """
        Validates the game description.
        
        Args:
            key (str): Field name being validated
            description (str): The game description to validate
        
        Returns:
            str: The validated description or None if description is None and allow_none is True
        
        Raises:
            ValueError: If description doesn't meet validation requirements when provided
        """
        if description is not None:
            return self.validate_string_length('Description', description, min_length=10, allow_none=True)
        return description
    
    def __repr__(self):
        """
        Returns a string representation of the Game.
        
        Returns:
            str: A string representing this game
        """
        return f'<Game {self.title}, ID: {self.id}>'

    def to_dict(self):
        """
        Converts the Game model to a dictionary format for API responses.
        
        Returns:
            dict: Dictionary representation of the game with its attributes and relationships
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'publisher': {'id': self.publisher.id, 'name': self.publisher.name} if self.publisher else None,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'starRating': self.star_rating  # Changed from star_rating to starRating
        }
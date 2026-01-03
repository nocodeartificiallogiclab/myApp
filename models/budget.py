"""Budget model for representing monthly spending limits by category."""

from dataclasses import dataclass


@dataclass
class Budget:
    """Represents a monthly budget limit for a category.
    
    Attributes:
        category: Category name (e.g., 'Food', 'Transportation')
        monthly_limit: Monthly spending limit for this category
    """
    
    category: str
    monthly_limit: float
    
    def __post_init__(self) -> None:
        """Validate budget data after initialization."""
        if not self.category.strip():
            raise ValueError("Category cannot be empty")
        if self.monthly_limit < 0:
            raise ValueError("Monthly limit must be non-negative")
    
    def to_dict(self) -> dict:
        """Convert budget to dictionary for storage.
        
        Returns:
            Dictionary representation of the budget
        """
        return {
            "category": self.category,
            "monthly_limit": self.monthly_limit,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        """Create a Budget instance from a dictionary.
        
        Args:
            data: Dictionary containing budget data
            
        Returns:
            Budget instance
        """
        return cls(
            category=data["category"],
            monthly_limit=data["monthly_limit"],
        )

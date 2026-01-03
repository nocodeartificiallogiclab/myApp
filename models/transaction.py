"""Transaction model for representing income and expense transactions."""

from dataclasses import dataclass, field
from datetime import date
from typing import Literal


@dataclass
class Transaction:
    """Represents a financial transaction (income or expense).
    
    Attributes:
        id: Unique identifier for the transaction
        date: Date of the transaction
        amount: Transaction amount (always positive)
        category: Category of the transaction (e.g., 'Food', 'Salary')
        description: Optional description of the transaction
        type: Type of transaction ('income' or 'expense')
    """
    
    date: date
    amount: float
    category: str
    description: str
    type: Literal["income", "expense"]
    id: str = field(default="")
    
    def __post_init__(self) -> None:
        """Validate transaction data after initialization."""
        if self.amount < 0:
            raise ValueError("Amount must be positive")
        if not self.category.strip():
            raise ValueError("Category cannot be empty")
        if self.type not in ["income", "expense"]:
            raise ValueError("Type must be 'income' or 'expense'")
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary for storage.
        
        Returns:
            Dictionary representation of the transaction
        """
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "type": self.type,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Create a Transaction instance from a dictionary.
        
        Args:
            data: Dictionary containing transaction data
            
        Returns:
            Transaction instance
        """
        return cls(
            id=data.get("id", ""),
            date=date.fromisoformat(data["date"]),
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            type=data["type"],
        )

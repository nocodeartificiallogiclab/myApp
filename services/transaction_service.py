"""Transaction service for managing transaction-related business logic."""

from datetime import date
from typing import List

from models.transaction import Transaction
from storage.storage_handler import StorageHandler


class TransactionService:
    """Service for managing transactions.
    
    This service handles all transaction-related business logic and
    coordinates with the storage layer.
    """
    
    def __init__(self, storage: StorageHandler) -> None:
        """Initialize the transaction service.
        
        Args:
            storage: StorageHandler instance for data persistence
        """
        self.storage = storage
    
    def add_transaction(
        self,
        transaction_date: date,
        amount: float,
        category: str,
        description: str,
        transaction_type: str,
    ) -> Transaction:
        """Add a new transaction.
        
        Args:
            transaction_date: Date of the transaction
            amount: Transaction amount
            category: Category of the transaction
            description: Description of the transaction
            transaction_type: Type of transaction ('income' or 'expense')
            
        Returns:
            Created Transaction object
        """
        transaction = Transaction(
            date=transaction_date,
            amount=amount,
            category=category,
            description=description,
            type=transaction_type,
        )
        self.storage.save_transaction(transaction)
        return transaction
    
    def get_all_transactions(self) -> List[Transaction]:
        """Retrieve all transactions.
        
        Returns:
            List of all Transaction objects
        """
        return self.storage.load_all_transactions()
    
    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        """Filter transactions by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of Transaction objects matching the category
        """
        all_transactions = self.get_all_transactions()
        return [t for t in all_transactions if t.category == category]
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """Filter transactions by type (income or expense).
        
        Args:
            transaction_type: Type to filter by ('income' or 'expense')
            
        Returns:
            List of Transaction objects matching the type
        """
        all_transactions = self.get_all_transactions()
        return [t for t in all_transactions if t.type == transaction_type]
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction by ID.
        
        Args:
            transaction_id: ID of the transaction to delete
            
        Returns:
            True if transaction was deleted, False if not found
        """
        return self.storage.delete_transaction(transaction_id)

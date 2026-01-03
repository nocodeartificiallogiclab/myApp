"""Storage handler for persisting transactions and budgets to JSON files."""

import json
from pathlib import Path
from typing import List

from models.transaction import Transaction
from models.budget import Budget


class StorageHandler:
    """Handles persistence of transactions and budgets using JSON files.
    
    This class encapsulates all file I/O operations and provides a clean
    interface for reading and writing application data.
    """
    
    def __init__(self, data_dir: str = "data") -> None:
        """Initialize the storage handler.
        
        Args:
            data_dir: Directory name where data files will be stored
        """
        self.data_dir = Path(data_dir)
        self.transactions_file = self.data_dir / "transactions.json"
        self.budgets_file = self.data_dir / "budgets.json"
        
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize files if they don't exist
        if not self.transactions_file.exists():
            self._write_json_file(self.transactions_file, [])
        if not self.budgets_file.exists():
            self._write_json_file(self.budgets_file, [])
    
    def _read_json_file(self, file_path: Path) -> List[dict]:
        """Read JSON data from a file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of dictionaries from the JSON file
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_json_file(self, file_path: Path, data: List[dict]) -> None:
        """Write JSON data to a file.
        
        Args:
            file_path: Path to the JSON file
            data: List of dictionaries to write
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_transaction(self, transaction: Transaction) -> None:
        """Save a transaction to storage.
        
        Args:
            transaction: Transaction object to save
        """
        transactions = self.load_all_transactions()
        
        # Generate ID if not present
        if not transaction.id:
            max_id = max(
                (int(t.id) for t in transactions if t.id and t.id.isdigit()),
                default=0
            )
            transaction.id = str(max_id + 1)
        
        # Check if transaction with this ID already exists
        existing_index = None
        for i, t in enumerate(transactions):
            if t.id == transaction.id:
                existing_index = i
                break
        
        if existing_index is not None:
            transactions[existing_index] = transaction
        else:
            transactions.append(transaction)
        
        transactions_data = [t.to_dict() for t in transactions]
        self._write_json_file(self.transactions_file, transactions_data)
    
    def load_all_transactions(self) -> List[Transaction]:
        """Load all transactions from storage.
        
        Returns:
            List of Transaction objects
        """
        data = self._read_json_file(self.transactions_file)
        return [Transaction.from_dict(item) for item in data]
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction by ID.
        
        Args:
            transaction_id: ID of the transaction to delete
            
        Returns:
            True if transaction was deleted, False if not found
        """
        transactions = self.load_all_transactions()
        original_count = len(transactions)
        transactions = [t for t in transactions if t.id != transaction_id]
        
        if len(transactions) < original_count:
            transactions_data = [t.to_dict() for t in transactions]
            self._write_json_file(self.transactions_file, transactions_data)
            return True
        return False
    
    def save_budget(self, budget: Budget) -> None:
        """Save a budget to storage.
        
        Args:
            budget: Budget object to save
        """
        budgets = self.load_all_budgets()
        
        # Update existing budget for this category or add new one
        existing_index = None
        for i, b in enumerate(budgets):
            if b.category == budget.category:
                existing_index = i
                break
        
        if existing_index is not None:
            budgets[existing_index] = budget
        else:
            budgets.append(budget)
        
        budgets_data = [b.to_dict() for b in budgets]
        self._write_json_file(self.budgets_file, budgets_data)
    
    def load_all_budgets(self) -> List[Budget]:
        """Load all budgets from storage.
        
        Returns:
            List of Budget objects
        """
        data = self._read_json_file(self.budgets_file)
        return [Budget.from_dict(item) for item in data]
    
    def delete_budget(self, category: str) -> bool:
        """Delete a budget by category.
        
        Args:
            category: Category of the budget to delete
            
        Returns:
            True if budget was deleted, False if not found
        """
        budgets = self.load_all_budgets()
        original_count = len(budgets)
        budgets = [b for b in budgets if b.category != category]
        
        if len(budgets) < original_count:
            budgets_data = [b.to_dict() for b in budgets]
            self._write_json_file(self.budgets_file, budgets_data)
            return True
        return False

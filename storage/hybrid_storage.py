"""Hybrid storage handler that saves to both local JSON and Supabase."""

from typing import List, Optional

from models.transaction import Transaction
from models.budget import Budget
from storage.storage_handler import StorageHandler
from storage.supabase_storage import SupabaseStorageHandler


class HybridStorageHandler:
    """Hybrid storage handler that saves to both local JSON files and Supabase.
    
    This class provides a unified interface that saves data to both local storage
    (for offline access) and Supabase (for cloud synchronization).
    """
    
    def __init__(
        self,
        data_dir: str = "data",
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        use_supabase: bool = True,
    ) -> None:
        """Initialize the hybrid storage handler.
        
        Args:
            data_dir: Directory name where data files will be stored
            supabase_url: Supabase project URL (optional, uses env var if not provided)
            supabase_key: Supabase anon/public key (optional, uses env var if not provided)
            use_supabase: Whether to use Supabase (defaults to True)
        """
        self.local_storage = StorageHandler(data_dir)
        self.use_supabase = use_supabase
        self.supabase_storage: Optional[SupabaseStorageHandler] = None
        
        if self.use_supabase:
            try:
                self.supabase_storage = SupabaseStorageHandler(supabase_url, supabase_key)
            except (ValueError, Exception) as e:
                # If Supabase is not configured, continue with local storage only
                print(f"Warning: Supabase not available, using local storage only: {e}")
                self.use_supabase = False
    
    def save_transaction(self, transaction: Transaction) -> None:
        """Save a transaction to both local storage and Supabase.
        
        Args:
            transaction: Transaction object to save
        """
        # Save to local storage first
        self.local_storage.save_transaction(transaction)
        
        # Save to Supabase if available
        if self.use_supabase and self.supabase_storage:
            try:
                self.supabase_storage.save_transaction(transaction)
            except Exception as e:
                print(f"Warning: Failed to save transaction to Supabase: {e}")
    
    def load_all_transactions(self) -> List[Transaction]:
        """Load all transactions from Supabase if available, otherwise from local storage.
        
        Returns:
            List of Transaction objects
        """
        if self.use_supabase and self.supabase_storage:
            try:
                return self.supabase_storage.load_all_transactions()
            except Exception as e:
                print(f"Warning: Failed to load transactions from Supabase, using local storage: {e}")
        
        return self.local_storage.load_all_transactions()
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction from both local storage and Supabase.
        
        Args:
            transaction_id: ID of the transaction to delete
            
        Returns:
            True if transaction was deleted, False if not found
        """
        local_result = self.local_storage.delete_transaction(transaction_id)
        
        if self.use_supabase and self.supabase_storage:
            try:
                supabase_result = self.supabase_storage.delete_transaction(transaction_id)
                return local_result or supabase_result
            except Exception as e:
                print(f"Warning: Failed to delete transaction from Supabase: {e}")
        
        return local_result
    
    def save_budget(self, budget: Budget) -> None:
        """Save a budget to both local storage and Supabase.
        
        Args:
            budget: Budget object to save
        """
        # Save to local storage first
        self.local_storage.save_budget(budget)
        
        # Save to Supabase if available
        if self.use_supabase and self.supabase_storage:
            try:
                self.supabase_storage.save_budget(budget)
            except Exception as e:
                print(f"Warning: Failed to save budget to Supabase: {e}")
    
    def load_all_budgets(self) -> List[Budget]:
        """Load all budgets from Supabase if available, otherwise from local storage.
        
        Returns:
            List of Budget objects
        """
        if self.use_supabase and self.supabase_storage:
            try:
                return self.supabase_storage.load_all_budgets()
            except Exception as e:
                print(f"Warning: Failed to load budgets from Supabase, using local storage: {e}")
        
        return self.local_storage.load_all_budgets()
    
    def delete_budget(self, category: str) -> bool:
        """Delete a budget from both local storage and Supabase.
        
        Args:
            category: Category of the budget to delete
            
        Returns:
            True if budget was deleted, False if not found
        """
        local_result = self.local_storage.delete_budget(category)
        
        if self.use_supabase and self.supabase_storage:
            try:
                supabase_result = self.supabase_storage.delete_budget(category)
                return local_result or supabase_result
            except Exception as e:
                print(f"Warning: Failed to delete budget from Supabase: {e}")
        
        return local_result

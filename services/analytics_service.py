"""Analytics service for computing financial summaries and statistics."""

from datetime import date
from typing import Dict, List

from models.transaction import Transaction
from services.transaction_service import TransactionService


class AnalyticsService:
    """Service for computing financial analytics and summaries.
    
    This service handles all calculation and aggregation logic for
    financial data analysis.
    """
    
    def __init__(self, transaction_service: TransactionService) -> None:
        """Initialize the analytics service.
        
        Args:
            transaction_service: TransactionService instance for accessing transactions
        """
        self.transaction_service = transaction_service
    
    def get_total_income(self) -> float:
        """Calculate total income from all income transactions.
        
        Returns:
            Total income amount
        """
        income_transactions = self.transaction_service.get_transactions_by_type("income")
        return sum(t.amount for t in income_transactions)
    
    def get_total_expenses(self) -> float:
        """Calculate total expenses from all expense transactions.
        
        Returns:
            Total expenses amount
        """
        expense_transactions = self.transaction_service.get_transactions_by_type("expense")
        return sum(t.amount for t in expense_transactions)
    
    def get_current_balance(self) -> float:
        """Calculate current balance (income - expenses).
        
        Returns:
            Current balance
        """
        return self.get_total_income() - self.get_total_expenses()
    
    def get_category_summary(self) -> Dict[str, float]:
        """Get spending summary grouped by category.
        
        Returns:
            Dictionary mapping category names to total amounts
        """
        transactions = self.transaction_service.get_all_transactions()
        category_totals: Dict[str, float] = {}
        
        for transaction in transactions:
            category = transaction.category
            if category not in category_totals:
                category_totals[category] = 0.0
            
            if transaction.type == "income":
                category_totals[category] += transaction.amount
            else:  # expense
                category_totals[category] -= transaction.amount
        
        return category_totals
    
    def get_expense_by_category(self) -> Dict[str, float]:
        """Get expense totals grouped by category.
        
        Returns:
            Dictionary mapping category names to total expense amounts
        """
        transactions = self.transaction_service.get_all_transactions()
        category_expenses: Dict[str, float] = {}
        
        for transaction in transactions:
            if transaction.type == "expense":
                category = transaction.category
                if category not in category_expenses:
                    category_expenses[category] = 0.0
                category_expenses[category] += transaction.amount
        
        return category_expenses
    
    def get_income_by_category(self) -> Dict[str, float]:
        """Get income totals grouped by category.
        
        Returns:
            Dictionary mapping category names to total income amounts
        """
        transactions = self.transaction_service.get_all_transactions()
        category_income: Dict[str, float] = {}
        
        for transaction in transactions:
            if transaction.type == "income":
                category = transaction.category
                if category not in category_income:
                    category_income[category] = 0.0
                category_income[category] += transaction.amount
        
        return category_income
    
    def get_monthly_summary(self, year: int, month: int) -> Dict[str, float]:
        """Get financial summary for a specific month.
        
        Args:
            year: Year to filter by
            month: Month to filter by (1-12)
            
        Returns:
            Dictionary with 'income', 'expenses', and 'balance' keys
        """
        transactions = self.transaction_service.get_all_transactions()
        
        monthly_income = 0.0
        monthly_expenses = 0.0
        
        for transaction in transactions:
            if transaction.date.year == year and transaction.date.month == month:
                if transaction.type == "income":
                    monthly_income += transaction.amount
                else:
                    monthly_expenses += transaction.amount
        
        return {
            "income": monthly_income,
            "expenses": monthly_expenses,
            "balance": monthly_income - monthly_expenses,
        }

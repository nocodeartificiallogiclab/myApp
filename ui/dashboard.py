"""Dashboard page showing financial overview."""

import streamlit as st
from datetime import date

from services.transaction_service import TransactionService
from services.analytics_service import AnalyticsService


def show_dashboard(
    transaction_service: TransactionService,
    analytics_service: AnalyticsService,
) -> None:
    """Display the dashboard page with financial overview.
    
    Args:
        transaction_service: TransactionService instance
        analytics_service: AnalyticsService instance
    """
    st.title("📊 Dashboard")
    
    # Calculate key metrics
    total_income = analytics_service.get_total_income()
    total_expenses = analytics_service.get_total_expenses()
    current_balance = analytics_service.get_current_balance()
    
    # Display key metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Income", f"${total_income:,.2f}")
    
    with col2:
        st.metric("Total Expenses", f"${total_expenses:,.2f}")
    
    with col3:
        balance_color = "normal" if current_balance >= 0 else "inverse"
        st.metric("Current Balance", f"${current_balance:,.2f}", delta=None)
    
    st.divider()
    
    # Recent transactions
    st.subheader("Recent Transactions")
    all_transactions = transaction_service.get_all_transactions()
    
    # Sort by date (most recent first)
    sorted_transactions = sorted(
        all_transactions,
        key=lambda t: t.date,
        reverse=True
    )[:10]  # Show last 10 transactions
    
    if sorted_transactions:
        # Display transactions in a table
        transaction_data = []
        for transaction in sorted_transactions:
            transaction_data.append({
                "Date": transaction.date.strftime("%Y-%m-%d"),
                "Type": transaction.type.title(),
                "Category": transaction.category,
                "Amount": f"${transaction.amount:,.2f}",
                "Description": transaction.description,
            })
        
        st.dataframe(
            transaction_data,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No transactions found. Add your first transaction to get started!")

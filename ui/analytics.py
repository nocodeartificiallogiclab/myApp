"""Analytics page showing charts and category breakdowns."""

import streamlit as st
import pandas as pd

from services.analytics_service import AnalyticsService


def show_analytics(analytics_service: AnalyticsService) -> None:
    """Display the analytics page with charts and breakdowns.
    
    Args:
        analytics_service: AnalyticsService instance
    """
    st.title("📈 Analytics")
    
    # Get category summaries
    expense_by_category = analytics_service.get_expense_by_category()
    income_by_category = analytics_service.get_income_by_category()
    
    # Expense breakdown
    if expense_by_category:
        st.subheader("Expenses by Category")
        
        # Create DataFrame for expenses
        expense_df = pd.DataFrame(
            list(expense_by_category.items()),
            columns=["Category", "Amount"]
        ).sort_values("Amount", ascending=False)
        
        # Display bar chart
        st.bar_chart(expense_df.set_index("Category"))
        
        # Display table
        st.dataframe(
            expense_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No expense data available. Add expense transactions to see analytics.")
    
    st.divider()
    
    # Income breakdown
    if income_by_category:
        st.subheader("Income by Category")
        
        # Create DataFrame for income
        income_df = pd.DataFrame(
            list(income_by_category.items()),
            columns=["Category", "Amount"]
        ).sort_values("Amount", ascending=False)
        
        # Display bar chart
        st.bar_chart(income_df.set_index("Category"))
        
        # Display table
        st.dataframe(
            income_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No income data available. Add income transactions to see analytics.")
    
    st.divider()
    
    # Overall category summary
    category_summary = analytics_service.get_category_summary()
    if category_summary:
        st.subheader("Net by Category (Income - Expenses)")
        
        # Create DataFrame
        summary_df = pd.DataFrame(
            list(category_summary.items()),
            columns=["Category", "Net Amount"]
        ).sort_values("Net Amount", ascending=False)
        
        # Display bar chart with different colors for positive/negative
        st.bar_chart(summary_df.set_index("Category"))
        
        # Display table
        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True,
        )

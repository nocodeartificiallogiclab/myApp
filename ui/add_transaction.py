"""Page for adding new transactions."""

import streamlit as st
from datetime import date

from services.transaction_service import TransactionService


def show_add_transaction(transaction_service: TransactionService) -> None:
    """Display the add transaction page with a form.
    
    Args:
        transaction_service: TransactionService instance
    """
    st.title("➕ Add Transaction")
    
    with st.form("add_transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_date = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today(),
            )
            transaction_type = st.selectbox(
                "Type",
                options=["income", "expense"],
                format_func=lambda x: x.title(),
            )
            amount = st.number_input(
                "Amount",
                min_value=0.01,
                step=0.01,
                format="%.2f",
            )
        
        with col2:
            category = st.text_input(
                "Category",
                placeholder="e.g., Food, Salary, Transportation",
            )
            description = st.text_area(
                "Description",
                placeholder="Optional description...",
                height=100,
            )
        
        submitted = st.form_submit_button("Add Transaction", use_container_width=True)
        
        if submitted:
            if not category.strip():
                st.error("Please enter a category")
            else:
                try:
                    transaction = transaction_service.add_transaction(
                        transaction_date=transaction_date,
                        amount=amount,
                        category=category.strip(),
                        description=description.strip(),
                        transaction_type=transaction_type,
                    )
                    st.success(
                        f"Transaction added successfully! "
                        f"{transaction_type.title()} of ${amount:,.2f} in {category}"
                    )
                except ValueError as e:
                    st.error(f"Error adding transaction: {str(e)}")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")

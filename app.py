"""Main Streamlit application entry point."""

import os
import streamlit as st
from dotenv import load_dotenv

from storage.hybrid_storage import HybridStorageHandler
from services.transaction_service import TransactionService
from services.analytics_service import AnalyticsService
from ui import dashboard, add_transaction, analytics

# Load environment variables
load_dotenv()


# Page configuration
st.set_page_config(
    page_title="Money Management App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize services (using session state to persist across reruns)
if "storage_handler" not in st.session_state:
    # Use hybrid storage handler that saves to both local JSON and Supabase
    st.session_state.storage_handler = HybridStorageHandler(
        data_dir="data",
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
        use_supabase=bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY")),
    )

if "transaction_service" not in st.session_state:
    st.session_state.transaction_service = TransactionService(
        st.session_state.storage_handler
    )

if "analytics_service" not in st.session_state:
    st.session_state.analytics_service = AnalyticsService(
        st.session_state.transaction_service
    )


def main() -> None:
    """Main application function."""
    # Sidebar navigation
    st.sidebar.title("💰 Money Management")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigate",
        options=["Dashboard", "Add Transaction", "Analytics"],
        label_visibility="collapsed",
    )
    
    st.sidebar.markdown("---")
    
    # Display current balance in sidebar
    current_balance = st.session_state.analytics_service.get_current_balance()
    balance_color = "🟢" if current_balance >= 0 else "🔴"
    st.sidebar.markdown(
        f"### {balance_color} Current Balance\n"
        f"### ${current_balance:,.2f}"
    )
    
    st.sidebar.markdown("---")
    
    # Quick stats in sidebar
    total_income = st.session_state.analytics_service.get_total_income()
    total_expenses = st.session_state.analytics_service.get_total_expenses()
    
    st.sidebar.metric("Total Income", f"${total_income:,.2f}")
    st.sidebar.metric("Total Expenses", f"${total_expenses:,.2f}")
    
    # Route to appropriate page
    if page == "Dashboard":
        dashboard.show_dashboard(
            st.session_state.transaction_service,
            st.session_state.analytics_service,
        )
    elif page == "Add Transaction":
        add_transaction.show_add_transaction(
            st.session_state.transaction_service,
        )
    elif page == "Analytics":
        analytics.show_analytics(
            st.session_state.analytics_service,
        )


if __name__ == "__main__":
    main()

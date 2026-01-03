# Money Management App

A comprehensive money management application built with Python and Streamlit. This application helps you track income and expenses, analyze spending patterns, and manage your finances.

## Features

- **Dashboard**: Overview of total income, expenses, and current balance with recent transactions
- **Add Transaction**: Easy-to-use form to add income or expense transactions
- **Analytics**: Visual charts and breakdowns of spending by category

## Project Structure

```
money-management-app/
├── app.py                      # Main Streamlit entry point
├── models/                     # Domain models
│   ├── __init__.py
│   ├── transaction.py         # Transaction class
│   └── budget.py              # Budget class
├── services/                   # Business logic layer
│   ├── __init__.py
│   ├── transaction_service.py # Transaction management
│   └── analytics_service.py   # Financial calculations
├── storage/                    # Data persistence layer
│   ├── __init__.py
│   └── storage_handler.py     # JSON file storage
├── ui/                         # Streamlit UI pages
│   ├── __init__.py
│   ├── dashboard.py           # Dashboard page
│   ├── add_transaction.py     # Add transaction page
│   └── analytics.py           # Analytics page
├── data/                       # Data storage directory (created automatically)
│   ├── transactions.json      # Transaction data
│   └── budgets.json           # Budget data
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application using Streamlit:

```bash
streamlit run app.py
```

The application will open in your default web browser. You can:
- View your financial overview on the Dashboard
- Add new transactions using the Add Transaction page
- Analyze your spending patterns on the Analytics page

## Architecture

This application follows a clean architecture pattern with clear separation of concerns:

- **Models**: Domain classes (Transaction, Budget) with validation and serialization
- **Services**: Business logic layer (TransactionService, AnalyticsService)
- **Storage**: Data persistence layer (JSON-based file storage)
- **UI**: UI components that only handle presentation and user interaction

All business logic is contained in the service layer, and the UI never directly accesses the storage layer.

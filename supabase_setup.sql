-- Supabase Database Setup Script
-- Run this SQL in your Supabase SQL Editor to create the required tables

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    category VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL CHECK (type IN ('income', 'expense')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create budgets table
CREATE TABLE IF NOT EXISTS budgets (
    category VARCHAR(255) PRIMARY KEY,
    monthly_limit DECIMAL(10, 2) NOT NULL CHECK (monthly_limit >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);

-- Enable Row Level Security (RLS) - optional, for multi-user scenarios
-- ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE budgets ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust based on your security needs)
-- CREATE POLICY "Enable read access for all users" ON transactions FOR SELECT USING (true);
-- CREATE POLICY "Enable insert access for all users" ON transactions FOR INSERT WITH CHECK (true);
-- CREATE POLICY "Enable update access for all users" ON transactions FOR UPDATE USING (true);
-- CREATE POLICY "Enable delete access for all users" ON transactions FOR DELETE USING (true);
-- CREATE POLICY "Enable read access for all users" ON budgets FOR SELECT USING (true);
-- CREATE POLICY "Enable insert access for all users" ON budgets FOR INSERT WITH CHECK (true);
-- CREATE POLICY "Enable update access for all users" ON budgets FOR UPDATE USING (true);
-- CREATE POLICY "Enable delete access for all users" ON budgets FOR DELETE USING (true);

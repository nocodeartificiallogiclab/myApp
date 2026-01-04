# Supabase Setup Guide

This guide will help you set up Supabase integration for the Money Management App.

## Prerequisites

1. A Supabase account (sign up at https://supabase.com)
2. A Supabase project created

## Step 1: Create Database Tables

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Open the file `supabase_setup.sql` from this project
4. Copy and paste the SQL code into the SQL Editor
5. Click **Run** to execute the SQL

This will create:
- `transactions` table for storing income and expense transactions
- `budgets` table for storing budget limits
- Indexes for better query performance

## Step 2: Get Your Supabase Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (under "Project URL")
   - **anon public key** (under "Project API keys" → "anon" → "public")

## Step 3: Configure Environment Variables

1. Copy the `.env.example` file to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file and add your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-public-key-here
   ```

   Replace `your-project-id` and `your-anon-public-key-here` with the values from Step 2.

## Step 4: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `supabase` - Supabase Python client
- `python-dotenv` - Environment variable management

## Step 5: Run the Application

```bash
streamlit run app.py
```

## How It Works

The app uses a **HybridStorageHandler** that:
- Saves transactions to **both** local JSON files and Supabase
- Loads data from Supabase if available, falls back to local storage if Supabase is unavailable
- Provides redundancy: your data is stored locally and in the cloud

## Troubleshooting

### Supabase Connection Issues

If you see warnings about Supabase not being available:
1. Check that your `.env` file exists and has the correct values
2. Verify your Supabase project is active (not paused)
3. Check that the database tables were created successfully
4. Verify your API keys are correct

### Database Tables Not Found

If you get errors about tables not existing:
1. Go to Supabase SQL Editor
2. Run the `supabase_setup.sql` script again
3. Verify tables exist in **Table Editor**

## Optional: Enable Row Level Security (RLS)

For production use with multiple users, you may want to enable Row Level Security. Uncomment the RLS policies in `supabase_setup.sql` and adjust them based on your authentication needs.

import yfinance as yf
import pandas as pd

results_df = pd.DataFrame(columns=[
    'Ticker', 
    'Assets YoY Difference', 
    'Assets YoY % Change', 
    'Debt YoY Difference', 
    'Debt YoY % Change', 
    'Shares YoY Difference', 
    'Shares YoY % Change', 
    'Assets Change', 
    'Debt Change', 
    'Shares Change',
    'Revenue YoY Difference', 
    'Revenue YoY % Change', 
    'Gross Profit YoY Difference', 
    'Gross Profit YoY % Change', 
    'Net Income YoY Difference', 
    'Net Income YoY % Change', 
    'Operating Expenses YoY Difference', 
    'Operating Expenses YoY % Change', 
    'Total Expenses YoY Difference', 
    'Total Expenses YoY % Change', 
    'Cost of Revenue YoY Difference', 
    'Cost of Revenue YoY % Change', 
    'Revenue Change', 
    'Gross Profit Change', 
    'Net Income Change', 
    'Operating Expenses Change', 
    'Total Expenses Change', 
    'Cost of Revenue Change',
    'Operating Cash Flow YoY Difference', 
    'Operating Cash Flow YoY % Change', 
    'Operating Cash Flow Change',
    'Free Cash Flow YoY Difference', 
    'Free Cash Flow YoY % Change', 
    'Free Cash Flow Change'
])



def get_income_statement_yoy(ticker):
    try:
    
        # Retrieve the income statement
        income_statement = ticker.get_income_stmt()

        # Extract relevant data for analysis
        total_revenue = income_statement.loc['TotalRevenue']
        gross_profit = income_statement.loc['GrossProfit']
        net_income = income_statement.loc['NetIncome']
        operating_expenses = income_statement.loc['OperatingExpense']
        total_expenses = income_statement.loc['TotalExpenses']
        cost_of_revenue = income_statement.loc['CostOfRevenue']

        # Reverse the order for trend analysis
        total_revenue_reversed = total_revenue[::-1]
        gross_profit_reversed = gross_profit[::-1]
        net_income_reversed = net_income[::-1]
        operating_expenses_reversed = operating_expenses[::-1]
        total_expenses_reversed = total_expenses[::-1]
        cost_of_revenue_reversed = cost_of_revenue[::-1]

        # Calculate YoY differences
        revenue_yoy_diff = total_revenue_reversed.diff(periods=1).dropna()[::-1]
        profit_yoy_diff = gross_profit_reversed.diff(periods=1).dropna()[::-1]
        income_yoy_diff = net_income_reversed.diff(periods=1).dropna()[::-1]
        operating_expenses_yoy_diff = operating_expenses_reversed.diff(periods=1).dropna()[::-1]
        total_expenses_yoy_diff = total_expenses_reversed.diff(periods=1).dropna()[::-1]
        cost_of_revenue_yoy_diff = cost_of_revenue_reversed.diff(periods=1).dropna()[::-1]

        # Calculate YoY percentage changes
        revenue_yoy_pct_change = total_revenue_reversed.pct_change(periods=1).dropna() * 100
        profit_yoy_pct_change = gross_profit_reversed.pct_change(periods=1).dropna() * 100
        income_yoy_pct_change = net_income_reversed.pct_change(periods=1).dropna() * 100
        operating_expenses_yoy_pct_change = operating_expenses_reversed.pct_change(periods=1).dropna() * 100
        total_expenses_yoy_pct_change = total_expenses_reversed.pct_change(periods=1).dropna() * 100
        cost_of_revenue_yoy_pct_change = cost_of_revenue_reversed.pct_change(periods=1).dropna() * 100

        # Create a combined DataFrame
        results = pd.DataFrame({
            'Revenue YoY Difference': revenue_yoy_diff,
            'Revenue YoY % Change': revenue_yoy_pct_change,
            'Gross Profit YoY Difference': profit_yoy_diff,
            'Gross Profit YoY % Change': profit_yoy_pct_change,
            'Net Income YoY Difference': income_yoy_diff,
            'Net Income YoY % Change': income_yoy_pct_change,
            'Operating Expenses YoY Difference': operating_expenses_yoy_diff,
            'Operating Expenses YoY % Change': operating_expenses_yoy_pct_change,
            'Total Expenses YoY Difference': total_expenses_yoy_diff,
            'Total Expenses YoY % Change': total_expenses_yoy_pct_change,
            'Cost of Revenue YoY Difference': cost_of_revenue_yoy_diff,
            'Cost of Revenue YoY % Change': cost_of_revenue_yoy_pct_change
        })
        
        # Add columns for indication of increase or decrease
        results['Revenue Change'] = results['Revenue YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
        results['Gross Profit Change'] = results['Gross Profit YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
        results['Net Income Change'] = results['Net Income YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
        results['Operating Expenses Change'] = results['Operating Expenses YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
        results['Total Expenses Change'] = results['Total Expenses YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
        results['Cost of Revenue Change'] = results['Cost of Revenue YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
     
        # Set index based on years (e.g., "2023-2024")
        years = total_revenue_reversed.index.year
        year_ranges = [f"{years[i]}-{years[i+1]}" for i in range(len(years) - 1)]
        
        while len(year_ranges) != results.shape[0]:
            year_ranges.pop(0)

        results.index = year_ranges
        
        # Reverse again to maintain chronological order
        results = results[::-1]
        
        return results
    
    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {e}")
        return None

def get_cashflow_statement_yoy(ticker):
    try:
        # Retrieve the cash flow statement
        cash_flow_statement = ticker.get_cash_flow()
        
        # Extract relevant data for analysis
        operating_cash_flow = cash_flow_statement.loc['OperatingCashFlow']
        free_cash_flow = cash_flow_statement.loc['FreeCashFlow']

        # Reverse the order for trend analysis
        operating_cash_flow_reversed = operating_cash_flow[::-1]
        free_cash_flow_reversed = free_cash_flow[::-1]

        # Calculate YoY differences
        operating_cash_flow_yoy_diff = operating_cash_flow_reversed.diff(periods=1).dropna()[::-1]
        free_cash_flow_yoy_diff = free_cash_flow_reversed.diff(periods=1).dropna()[::-1]

        # Calculate YoY percentage changes
        operating_cash_flow_yoy_pct_change = operating_cash_flow_reversed.pct_change(periods=1).dropna() * 100
        free_cash_flow_yoy_pct_change = free_cash_flow_reversed.pct_change(periods=1).dropna() * 100

        # Create a combined DataFrame
        results = pd.DataFrame({
            'Operating Cash Flow YoY Difference': operating_cash_flow_yoy_diff,
            'Operating Cash Flow YoY % Change': operating_cash_flow_yoy_pct_change,
            'Free Cash Flow YoY Difference': free_cash_flow_yoy_diff,
            'Free Cash Flow YoY % Change': free_cash_flow_yoy_pct_change
        })
        
        # Add columns for indication of increase or decrease
        results['Operating Cash Flow Change'] = results['Operating Cash Flow YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
        results['Free Cash Flow Change'] = results['Free Cash Flow YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')

        # Set index based on years (e.g., "2023-2024")
        years = operating_cash_flow_reversed.index.year
        year_ranges = [f"{years[i]}-{years[i+1]}" for i in range(len(years) - 1)]
        
        while len(year_ranges) != results.shape[0]:
            year_ranges.pop(0)

        results.index = year_ranges
        
        results = results[::-1]
        return results

    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {e}")
        return None


def get_balance_sheet_yoy(ticker):
        balance_sheet = ticker.get_balance_sheet()

        # Extract relevant data for analysis
        total_assets = balance_sheet.loc['TotalAssets']
        long_term_debt = balance_sheet.loc['LongTermDebt']
        share_number = balance_sheet.loc['OrdinarySharesNumber']

        # Reverse the order for trend analysis
        total_assets_reversed = total_assets[::-1]
        total_debt_reversed = long_term_debt[::-1]
        share_number_reversed = share_number[::-1]

        # Calculate YoY differences
        assets_yoy_diff = total_assets_reversed.diff(periods=1).dropna()[::-1]
        debt_yoy_diff = total_debt_reversed.diff(periods=1).dropna()[::-1]
        shares_yoy_diff = share_number_reversed.diff(periods=1).dropna()[::-1]

        # Calculate YoY percentage changes
        assets_yoy_pct_change = total_assets_reversed.pct_change(periods=1).dropna() * 100
        debt_yoy_pct_change = total_debt_reversed.pct_change(periods=1).dropna() * 100
        shares_yoy_pct_change = share_number_reversed.pct_change(periods=1).dropna() * 100

        # Create a combined DataFrame
        results = pd.DataFrame({
            'Assets YoY Difference': assets_yoy_diff,
            'Assets YoY % Change': assets_yoy_pct_change,
            'Debt YoY Difference': debt_yoy_diff,
            'Debt YoY % Change': debt_yoy_pct_change,
            'Shares YoY Difference': shares_yoy_diff,
            'Shares YoY % Change': shares_yoy_pct_change
        })
        
        # Add columns for indication of increase or decrease
        results['Assets Change'] = results['Assets YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
        results['Debt Change'] = results['Debt YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')
        results['Shares Change'] = results['Shares YoY Difference'].apply(lambda x: 'Increase' if x > 0 else 'Decrease' if x < 0 else 'No Change')

        # Set index based on years (e.g., "2023-2024")
        years = total_assets_reversed.index.year
        year_ranges = [f"{years[i]}-{years[i+1]}" for i in range(len(years) - 1)]
        
        while len(year_ranges) != results.shape[0]:
            year_ranges.pop(0)

        results.index = year_ranges
        
        results = results[::-1]
        return results

def get_year_over_year_changes(ticker_symbol):
    try:
        # Get the ticker data
        ticker = yf.Ticker(ticker_symbol)
        results_bs = get_balance_sheet_yoy(ticker)

        results_is= get_income_statement_yoy(ticker)
        results_cf = get_cashflow_statement_yoy(ticker)
        # Get change compared to last year
        latest_changes = pd.concat([results_bs.iloc[0], results_is.iloc[0],results_cf.iloc[0]], axis=0)
        latest_changes['Ticker'] = ticker_symbol
       
        
        return latest_changes

    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {e}")
        return None, None


def all_records_latest_yoy(ticker_symbol):
    try:
        latest_changes = get_year_over_year_changes(ticker_symbol)
        if latest_changes is not None:
            results_df.loc[len(results_df)] = latest_changes
    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {e}")


def get_latest_record(ticker_symbol):
    try:
        # Get the ticker data
        ticker = yf.Ticker(ticker_symbol)

        # Retrieve the latest balance sheet data
        balance_sheet = ticker.get_balance_sheet()

        # Extract relevant data for the latest record
        latest_record = {
            'Total Assets': balance_sheet.loc['TotalAssets'].iloc[0],
            'Long Term Debt': balance_sheet.loc['LongTermDebt'].iloc[0],
            'Ordinary Shares': balance_sheet.loc['OrdinarySharesNumber'].iloc[0]
        }

        return latest_record
    except Exception as e:
        print(f"Error retrieving latest record for {ticker_symbol}: {e}")
        return None

def save_results_to_csv(file_name, store_df):
    store_df.to_csv(file_name, index=False)
    print(f"Results saved to {file_name}")

def select_best_investments(results_df):
    """
    This function selects the best stocks to invest in based on financial performance criteria.
    Args:
        results_df (pd.DataFrame): Merged DataFrame with balance sheet and income statement data.
    Returns:
        best_investments (pd.DataFrame): DataFrame containing only the best investment options.
    """
    
    # Define the criteria for selection
    criteria = (
    # Assets must increase
    (results_df['Assets Change'] == 'Increase') &
    
    # Debt must decrease or stay stable
    (
        (results_df['Debt Change'] == 'Decrease') | 
        (results_df['Debt Change'] == 'No Change')
    ) &
    
    # Revenue should increase by at least 5%
    (results_df['Revenue YoY % Change'] >= 5) &
    
    # Gross Profit and Net Income should increase
    (results_df['Gross Profit Change'] == 'Increase') &
    (results_df['Net Income Change'] == 'Increase') &
    
    # Operating expenses should decrease or increase less than revenue
    (
        (results_df['Operating Expenses Change'] == 'Decrease') | 
        (results_df['Operating Expenses YoY % Change'] < results_df['Revenue YoY % Change'])
    ) &
    
    # Total expenses must increase less than revenue
    (results_df['Total Expenses YoY % Change'] < results_df['Revenue YoY % Change']) &
    
    # Operating cash flow must increase
    (results_df["Operating Cash Flow Change"] == "Increase")
)


    # Filter the merged DataFrame based on the criteria
    best_investments = results_df[criteria]
    
    return best_investments

url = "https://datahub.io/core/s-and-p-500-companies/r/0.csv"  # URL for S&P 500 CSV
sp500_data = pd.read_csv(url)

# Extract the tickers
tickers = sp500_data['Symbol'].tolist()

for ticker_symbol in tickers:
    print(f"Processing {ticker_symbol}...")
    all_records_latest_yoy(ticker_symbol)
    
save_results_to_csv("overall_results.csv", results_df)

# Example usage
identified_records = select_best_investments(results_df)
save_results_to_csv("identified_records.csv", identified_records)

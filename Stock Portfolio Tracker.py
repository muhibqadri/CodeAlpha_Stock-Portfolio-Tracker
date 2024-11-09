import requests

# Replace with your own API key
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://www.alphavantage.co/query'

portfolio = {}

def get_stock_price(symbol):
    """Fetches the latest stock price for a given symbol using Alpha Vantage API."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    try:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        price = data['Time Series (5min)'][last_refreshed]['4. close']
        return float(price)
    except KeyError:
        print(f"Could not retrieve data for {symbol}. Please check the stock symbol and try again.")
        return None

def add_stock(symbol, quantity):
    """Adds a stock to the portfolio with the specified quantity."""
    if symbol in portfolio:
        portfolio[symbol]['quantity'] += quantity
    else:
        price = get_stock_price(symbol)
        if price:
            portfolio[symbol] = {'quantity': quantity, 'price': price}
            print(f"Added {quantity} shares of {symbol} at ${price:.2f} per share.")

def remove_stock(symbol):
    """Removes a stock from the portfolio."""
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Removed {symbol} from the portfolio.")
    else:
        print(f"{symbol} not found in the portfolio.")

def view_portfolio():
    """Displays the current portfolio and the performance of each stock."""
    print("\nYour Portfolio:")
    for symbol, data in portfolio.items():
        current_price = get_stock_price(symbol)
        if current_price:
            initial_value = data['quantity'] * data['price']
            current_value = data['quantity'] * current_price
            profit_loss = current_value - initial_value
            print(f"{symbol}: {data['quantity']} shares")
            print(f" - Bought at: ${data['price']:.2f} | Current Price: ${current_price:.2f}")
            print(f" - Total Value: ${current_value:.2f} | Profit/Loss: ${profit_loss:.2f}\n")

def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
            quantity = int(input("Enter the quantity: "))
            add_stock(symbol, quantity)
        elif choice == '2':
            symbol = input("Enter the stock symbol to remove: ").upper()
            remove_stock(symbol)
        elif choice == '3':
            view_portfolio()
        elif choice == '4':
            print("Exiting the portfolio tracker.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
main()
from fetch_historical import fetch_data
from calculate_indicators import calculate_and_store_indicators

def main():
    fetch_data()
    calculate_and_store_indicators()

if __name__ == "__main__":
    main()

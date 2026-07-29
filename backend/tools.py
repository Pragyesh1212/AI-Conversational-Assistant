import os
import requests

from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.types import interrupt

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch the latest stock price using Alpha Vantage.
    Example:
        AAPL
        TSLA
        MSFT
    """

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey={ALPHA_VANTAGE_API_KEY}"
    )

    response = requests.get(url, timeout=10)

    return response.json()


@tool
def purchase_stock(symbol: str, quantity: int) -> dict:
    """
    Simulate purchasing a stock.
    Human approval is required.
    """

    decision = interrupt(
        f"Approve buying {quantity} shares of {symbol}?"
    )

    if isinstance(decision, str) and decision.lower() == "yes":

        return {
            "status": "success",
            "message": f"Purchased {quantity} shares of {symbol}."
        }

    return {
        "status": "cancelled",
        "message": "Purchase cancelled."
    }


tools = [
    get_stock_price,
    purchase_stock,
]
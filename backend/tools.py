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

    Returns only useful quote fields so the LLM can present the
    information cleanly instead of exposing raw API JSON.

    Example:
        AAPL
        TSLA
        MSFT
    """

    symbol = symbol.strip().upper()

    if not ALPHA_VANTAGE_API_KEY:
        return {
            "status": "error",
            "message": "Alpha Vantage API key is not configured."
        }

    url = (
        "https://www.alphavantage.co/query"
        "?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey={ALPHA_VANTAGE_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        return {
            "status": "error",
            "message": f"Unable to fetch stock data: {exc}"
        }

    quote = data.get("Global Quote", {})

    if not quote:
        return {
            "status": "error",
            "message": (
                data.get("Note")
                or data.get("Information")
                or data.get("Error Message")
                or f"No stock quote found for {symbol}."
            )
        }

    return {
        "status": "success",
        "symbol": quote.get("01. symbol"),
        "open": quote.get("02. open"),
        "high": quote.get("03. high"),
        "low": quote.get("04. low"),
        "price": quote.get("05. price"),
        "volume": quote.get("06. volume"),
        "latest_trading_day": quote.get("07. latest trading day"),
        "previous_close": quote.get("08. previous close"),
        "change": quote.get("09. change"),
        "change_percent": quote.get("10. change percent"),
    }


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
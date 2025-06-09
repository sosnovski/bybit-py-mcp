import os
from typing import Any, Dict, Union

from dotenv import load_dotenv
from pybit.unified_trading import HTTP

from bybit_mcp.models.market_models import (
    FundingRateHistoryResponse,
    InstrumentsInfoResponse,
    InsuranceResponse,
    KlineResponse,
    LongShortRatioResponse,
    OpenInterestResponse,
    OrderBookResponse,
    RecentTradesResponse,
    RiskLimitResponse,
    TickerResponse,
)

# Load environment variables from .env file
load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

bybit_session = HTTP(
    testnet=False,  # Set to False for production
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)


def get_server_time() -> Dict[str, Any]:
    """Get Bybit server time using the Market API."""
    return bybit_session.get_server_time()


def get_tickers(
    symbol: Union[str, None] = None,
    category: str = "linear",
    baseCoin: Union[str, None] = None,
    limit: int | None = None,
    cursor: str | None = None,
) -> TickerResponse:
    """Get market tickers for all or a specific symbol and validate response."""
    params = {"category": category}
    for key, value in [("symbol", symbol), ("baseCoin", baseCoin), ("limit", str(limit) if limit else None), ("cursor", cursor)]:
        if value:
            params[key] = value
    response = bybit_session.get_tickers(**params)
    if isinstance(response, tuple):
        response = response[0]
    return TickerResponse(**response["result"])


def get_order_book(
    symbol: str,
    category: str = "linear",
    limit: int = 50,
    baseCoin: Union[str, None] = None,
    cursor: str | None = None,
) -> OrderBookResponse:
    """Get order book (depth) for a symbol and validate response."""
    params = {"symbol": symbol, "category": category, "limit": limit}
    if baseCoin:
        params["baseCoin"] = baseCoin
    if cursor:
        params["cursor"] = cursor
    response = bybit_session.get_orderbook(**params)
    if isinstance(response, tuple):
        response = response[0]
    return OrderBookResponse(**response["result"])


def get_recent_trades(
    symbol: str,
    category: str = "linear",
    baseCoin: Union[str, None] = None,
    optionType: Union[str, None] = None,
    limit: int = 50,
    cursor: str | None = None,
) -> RecentTradesResponse:
    """Get recent trades for a symbol and validate response."""
    params = {"symbol": symbol, "category": category, "limit": limit}
    if baseCoin:
        params["baseCoin"] = baseCoin
    if optionType:
        params["optionType"] = optionType
    if cursor:
        params["cursor"] = cursor
    response = bybit_session.get_public_trade_history(**params)
    if isinstance(response, tuple):
        response = response[0]
    return RecentTradesResponse(**response["result"])


def get_kline(symbol: str, interval: str, category: str = "linear", limit: int = 200) -> KlineResponse:
    """Get kline (candlestick) data for a symbol and validate response."""
    response = bybit_session.get_kline(symbol=symbol, interval=interval, category=category, limit=limit)
    if isinstance(response, tuple):
        response = response[0]
    return KlineResponse(**response["result"])


def get_mark_price_kline(symbol: str, interval: str, category: str = "linear", limit: int = 200) -> KlineResponse:
    """Get mark price kline data for a symbol and validate response."""
    response = bybit_session.get_mark_price_kline(symbol=symbol, interval=interval, category=category, limit=limit)
    if isinstance(response, tuple):
        response = response[0]
    return KlineResponse(**response["result"])


def get_index_price_kline(symbol: str, interval: str, category: str = "linear", limit: int = 200) -> KlineResponse:
    """Get index price kline data for a symbol and validate response."""
    response = bybit_session.get_index_price_kline(symbol=symbol, interval=interval, category=category, limit=limit)
    if isinstance(response, tuple):
        response = response[0]
    return KlineResponse(**response["result"])


def get_premium_index_price_kline(symbol: str, interval: str, category: str = "linear", limit: int = 200) -> KlineResponse:
    """Get premium index price kline data for a symbol and validate response."""
    response = bybit_session.get_premium_index_price_kline(symbol=symbol, interval=interval, category=category, limit=limit)
    if isinstance(response, tuple):
        response = response[0]
    return KlineResponse(**response["result"])


def get_instruments_info(category: str = "linear", symbol: Union[str, None] = None) -> InstrumentsInfoResponse:
    """Get instruments info (list of trading pairs) and validate response."""
    params = {"category": category}
    if symbol:
        params["symbol"] = symbol
    response = bybit_session.get_instruments_info(**params)
    if isinstance(response, tuple):
        response = response[0]
    return InstrumentsInfoResponse(**response["result"])


def get_funding_rate_history(symbol: str, category: str = "linear", limit: int = 200) -> FundingRateHistoryResponse:
    """Get funding rate history for a symbol and validate response."""
    response = bybit_session.get_funding_rate_history(symbol=symbol, category=category, limit=limit)
    if isinstance(response, tuple):
        response = response[0]
    return FundingRateHistoryResponse(**response["result"])


def get_open_interest(symbol: str, category: str = "linear", interval: str = "5min", limit: int = 200) -> OpenInterestResponse:
    """Get open interest for a symbol and validate response."""
    response = bybit_session.get_open_interest(symbol=symbol, category=category, intervalTime=interval, limit=limit)
    if isinstance(response, tuple):
        response = response[0]
    return OpenInterestResponse(**response["result"])


def get_insurance(
    category: str = "linear",
    baseCoin: Union[str, None] = None,
    quoteCoin: Union[str, None] = None,
    startTime: Union[str, None] = None,
    endTime: Union[str, None] = None,
) -> InsuranceResponse:
    """Get insurance fund history and validate response."""
    params = {"category": category}
    for key, value in [("baseCoin", baseCoin), ("quoteCoin", quoteCoin), ("startTime", startTime), ("endTime", endTime)]:
        if value:
            params[key] = value
    response = bybit_session.get_insurance(**params)
    if isinstance(response, tuple):
        response = response[0]
    return InsuranceResponse(**response["result"])


def get_risk_limit(symbol: str, category: str = "linear") -> RiskLimitResponse:
    """Get risk limit for a symbol and validate response."""
    response = bybit_session.get_risk_limit(symbol=symbol, category=category)
    if isinstance(response, tuple):
        response = response[0]
    return RiskLimitResponse(**response["result"])


def get_long_short_ratio(symbol: str, category: str = "linear", interval: str = "5min", limit: int = 200) -> LongShortRatioResponse:
    """Get long short ratio for a symbol and validate response."""
    response = bybit_session.get_long_short_ratio(symbol=symbol, category=category, period=interval, limit=limit)
    if isinstance(response, tuple):
        response = response[0]
    return LongShortRatioResponse(**response["result"])

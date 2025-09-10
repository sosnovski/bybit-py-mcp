# src/bybit_mcp/position.py
import os
from typing import Optional

from dotenv import load_dotenv
from pybit.unified_trading import HTTP

from bybit_mcp.models.position_models import (
    AddReduceMarginResponse,
    GetClosedPnlResponse,
    GetPositionInfoResponse,
    SetAutoAddMarginResponse,
    SetLeverageResponse,
    SetTradingStopResponse,
    SwitchMarginModeResponse,
    SwitchPositionModeResponse,
)

from .trade import TRADING_ENABLED, _get_trading_disabled_response

# Load environment variables from .env file
load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
USE_TESTNET = os.getenv("BYBIT_TESTNET", "false").lower() in ("true", "1")

bybit_session = HTTP(
    testnet=USE_TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)


def get_position_info(
    category: str,
    settleCoin: str,
    symbol: Optional[str] = None,
    baseCoin: Optional[str] = None,
    limit: Optional[int] = None,
    cursor: Optional[str] = None,
) -> GetPositionInfoResponse:
    """Query real-time position data."""
    params = {
        "category": category,
        "settleCoin": settleCoin,
    }
    if symbol:
        params["symbol"] = symbol
    if baseCoin:
        params["baseCoin"] = baseCoin
    if limit is not None:
        params["limit"] = str(limit)  # Convert limit to string
    if cursor:
        params["cursor"] = cursor

    response = bybit_session.get_positions(**params)
    if isinstance(response, tuple):
        response = response[0]
    return GetPositionInfoResponse(**response)


def set_leverage(
    category: str,
    symbol: str,
    buyLeverage: str,
    sellLeverage: str,
) -> SetLeverageResponse:
    """Set leverage for a position."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(SetLeverageResponse)

    params = {
        "category": category,
        "symbol": symbol,
        "buyLeverage": buyLeverage,
        "sellLeverage": sellLeverage,
    }

    response = bybit_session.set_leverage(**params)
    if isinstance(response, tuple):
        response = response[0]
    return SetLeverageResponse(**response)


def switch_cross_isolated_margin(
    category: str,
    symbol: str,
    tradeMode: int,
    buyLeverage: str,
    sellLeverage: str,
) -> SwitchMarginModeResponse:
    """Switch between cross margin and isolated margin."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(SwitchMarginModeResponse)

    params = {
        "category": category,
        "symbol": symbol,
        "tradeMode": tradeMode,
        "buyLeverage": buyLeverage,
        "sellLeverage": sellLeverage,
    }

    response = bybit_session.switch_margin_mode(**params)
    if isinstance(response, tuple):
        response = response[0]
    return SwitchMarginModeResponse(**response)


def switch_position_mode(
    category: str,
    symbol: Optional[str] = None,
    coin: Optional[str] = None,
    mode: int = 0,
) -> SwitchPositionModeResponse:
    """Switch position mode between one-way and hedge mode."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(SwitchPositionModeResponse)

    params = {
        "category": category,
        "mode": mode,
    }
    if symbol:
        params["symbol"] = symbol
    if coin:
        params["coin"] = coin

    response = bybit_session.switch_position_mode(**params)
    if isinstance(response, tuple):
        response = response[0]
    return SwitchPositionModeResponse(**response)


def set_trading_stop(
    category: str,
    symbol: str,
    tpslMode: str,
    positionIdx: int,
    takeProfit: Optional[str] = None,
    stopLoss: Optional[str] = None,
    trailingStop: Optional[str] = None,
    tpTriggerBy: Optional[str] = None,
    slTriggerBy: Optional[str] = None,
    activePrice: Optional[str] = None,
    tpSize: Optional[str] = None,
    slSize: Optional[str] = None,
    tpLimitPrice: Optional[str] = None,
    slLimitPrice: Optional[str] = None,
    tpOrderType: Optional[str] = None,
    slOrderType: Optional[str] = None,
) -> SetTradingStopResponse:
    """Set trading stop for a position (take profit, stop loss).
    
    Args:
        category: Product category ('linear', 'inverse')
        symbol: Trading pair symbol (e.g., 'BTCUSDT')
        tpslMode: TP/SL mode ('Full' or 'Partial')
        positionIdx: Position index (0=one-way, 1=hedge-buy, 2=hedge-sell)
        takeProfit: Take profit price (optional)
        stopLoss: Stop loss price (optional)
        trailingStop: Trailing stop distance (optional)
        tpTriggerBy: TP trigger price type (optional)
        slTriggerBy: SL trigger price type (optional) 
        activePrice: Trailing stop trigger price (optional)
        tpSize: TP size for partial mode (optional)
        slSize: SL size for partial mode (optional)
        tpLimitPrice: TP limit order price (optional)
        slLimitPrice: SL limit order price (optional)
        tpOrderType: TP order type when triggered (optional)
        slOrderType: SL order type when triggered (optional)
    """
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(SetTradingStopResponse)

    params = {
        "category": category,
        "symbol": symbol,
        "tpslMode": tpslMode,
        "positionIdx": positionIdx,
    }
    optional_params = {
        "takeProfit": takeProfit,
        "stopLoss": stopLoss,
        "trailingStop": trailingStop,
        "tpTriggerBy": tpTriggerBy,
        "slTriggerBy": slTriggerBy,
        "activePrice": activePrice,
        "tpSize": tpSize,
        "slSize": slSize,
        "tpLimitPrice": tpLimitPrice,
        "slLimitPrice": slLimitPrice,
        "tpOrderType": tpOrderType,
        "slOrderType": slOrderType,
    }
    params.update({k: v for k, v in optional_params.items() if v is not None})

    response = bybit_session.set_trading_stop(**params)
    if isinstance(response, tuple):
        response = response[0]
    return SetTradingStopResponse(**response)


def set_auto_add_margin(
    category: str,
    symbol: str,
    autoAddMargin: int,
    positionIdx: Optional[int] = None,
) -> SetAutoAddMarginResponse:
    """Set auto add margin for a position."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(SetAutoAddMarginResponse)

    params = {
        "category": category,
        "symbol": symbol,
        "autoAddMargin": autoAddMargin,
    }
    if positionIdx is not None:
        params["positionIdx"] = str(positionIdx)

    response = bybit_session.set_auto_add_margin(**params)
    if isinstance(response, tuple):
        response = response[0]
    return SetAutoAddMarginResponse(**response)


def modify_position_margin(
    category: str,
    symbol: str,
    margin: str,
    positionIdx: Optional[int] = None,
) -> AddReduceMarginResponse:
    """Add or reduce margin for isolated margin position"""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(AddReduceMarginResponse)

    params = {
        "category": category,
        "symbol": symbol,
        "margin": margin,
    }
    if positionIdx is not None:
        params["positionIdx"] = str(positionIdx)

    response = bybit_session.add_or_reduce_margin(**params)
    if isinstance(response, tuple):
        response = response[0]
    return AddReduceMarginResponse(**response)


def get_closed_pnl(
    category: str,
    symbol: Optional[str] = None,
    startTime: Optional[int] = None,
    endTime: Optional[int] = None,
    limit: Optional[int] = None,
    cursor: Optional[str] = None,
) -> GetClosedPnlResponse:
    """Get closed profit and loss records."""
    params = {"category": category}
    for param, value in [("symbol", symbol), ("startTime", startTime), ("endTime", endTime), ("limit", limit), ("cursor", cursor)]:
        if value is not None:
            params[param] = str(value) if param in ["startTime", "endTime", "limit"] else value

    response = bybit_session.get_closed_pnl(**params)
    if isinstance(response, tuple):
        response = response[0]
    return GetClosedPnlResponse(**response)

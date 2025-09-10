import logging
import os
from typing import List, Type, TypeVar, Union  # Grouped TypeVar

from dotenv import load_dotenv
from pybit.unified_trading import HTTP

from bybit_mcp.models.trade_models import (
    AccountInfoResponse,
    AmendOrderResponse,
    BaseApiResponse,  # For type hinting
    BatchAmendOrderResponse,
    BatchCancelOrderResponse,
    BatchPlaceOrderResponse,
    CancelAllOrdersResponse,
    CancelOrderResponse,
    OpenClosedOrdersResponse,
    OrderHistoryResponse,
    OrderItemResult,  # For constructing error results
    PlaceOrderResponse,
    SingleCoinBalanceResponse,
    SpotBorrowQuotaResponse,  # Added SpotBorrowQuotaResponse
    TradeHistoryResponse,
    WalletBalanceResponse,
)

# Load environment variables from .env file for local development
load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
USE_TESTNET = os.getenv("BYBIT_TESTNET", "false").lower() in ("true", "1")
TRADING_ENABLED = os.getenv("BYBIT_TRADING_ENABLED", "false").lower() in ("true", "1")

# Debug logging for environment variables
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom error code for trading disabled
TRADING_DISABLED_RET_CODE = 40300
TRADING_DISABLED_RET_MSG = "Trading operations are disabled by server configuration."

bybit_session = HTTP(
    testnet=USE_TESTNET,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)

T = TypeVar("T", bound=BaseApiResponse)


def _get_trading_disabled_response(response_model: Type[T]) -> T:
    """Helper to create a trading disabled error response for different models."""
    kwargs = {"retCode": TRADING_DISABLED_RET_CODE, "retMsg": TRADING_DISABLED_RET_MSG}

    # Handle specific known structures for the 'result' field
    if response_model in (PlaceOrderResponse, AmendOrderResponse, CancelOrderResponse):
        kwargs["result"] = OrderItemResult(orderId="", orderLinkId="")
    elif response_model == CancelAllOrdersResponse:
        kwargs["result"] = {"list": []}  # Matches CancelAllOrdersResult structure
    elif response_model in (BatchPlaceOrderResponse, BatchAmendOrderResponse, BatchCancelOrderResponse):
        kwargs["result"] = {"list": []}  # Matches Batch*OrderResult structures
    # For other BaseApiResponse subclasses that might not have a 'result' or have a different one,
    # they will just get retCode and retMsg.
    return response_model(**kwargs)


def place_order(
    category: str,
    symbol: str,
    side: str,
    orderType: str,
    qty: str,
    price: Union[str, None] = None,
    isLeverage: Union[int, None] = None,
    orderLinkId: Union[str, None] = None,
    timeInForce: Union[str, None] = None,
    positionIdx: Union[int, None] = None,
    reduceOnly: Union[bool, None] = None,
    triggerBy: Union[str, None] = None,
    triggerPrice: Union[str, None] = None,
    triggerDirection: Union[int, None] = None,
    takeProfit: Union[str, None] = None,
    stopLoss: Union[str, None] = None,
    tpTriggerBy: Union[str, None] = None,
    slTriggerBy: Union[str, None] = None,
    marketUnit: Union[str, None] = None,
    smpType: Union[str, None] = None,
) -> PlaceOrderResponse:
    """Place a new order with comprehensive risk management and validate response.
    
    Args:
        category: Product category (linear, spot, option, inverse)
        symbol: Trading pair symbol (e.g., 'BTCUSDT')
        side: Order side ('Buy' or 'Sell')
        orderType: Order type ('Market' or 'Limit')
        qty: Order quantity as string
        price: Order price (required for Limit orders)
        isLeverage: Use leverage for spot margin (0 or 1)
        orderLinkId: Custom order ID for tracking
        timeInForce: Execution strategy (GTC, IOC, FOK, PostOnly)
        positionIdx: Position mode index (0=One-way, 1=Hedge Buy, 2=Hedge Sell)
        reduceOnly: Reduce-only order to close position
        triggerBy: Trigger price type for conditional orders
        triggerPrice: Trigger price for conditional orders
        triggerDirection: Trigger direction (1=rise above, 2=fall below)
        takeProfit: Take profit price for automatic profit taking
        stopLoss: Stop loss price for risk management
        tpTriggerBy: Take profit trigger price type
        slTriggerBy: Stop loss trigger price type
        marketUnit: Market order unit (baseCoin or quoteCoin)
        smpType: Self-match prevention type
    
    Returns:
        PlaceOrderResponse: Order placement result with orderId and status
    """
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(PlaceOrderResponse)
    
    # Validate critical parameter combinations for safety
    if orderType == "Limit" and price is None:
        raise ValueError("Price is required for Limit orders")
    
    if triggerPrice is not None and triggerBy is None:
        raise ValueError("triggerBy is required when triggerPrice is specified")
    
    if triggerDirection is not None and triggerPrice is None:
        raise ValueError("triggerPrice is required when triggerDirection is specified")
    
    if takeProfit is not None and tpTriggerBy is None:
        # Default to LastPrice if not specified for safety
        tpTriggerBy = "LastPrice"
    
    if stopLoss is not None and slTriggerBy is None:
        # Default to LastPrice if not specified for safety
        slTriggerBy = "LastPrice"
    
    # Build parameters dict, excluding None values for cleaner API calls
    params = {
        "category": category,
        "symbol": symbol,
        "side": side,
        "orderType": orderType,
        "qty": qty,
    }
    
    # Add optional parameters only if they are provided
    optional_params = {
        "price": price,
        "isLeverage": isLeverage,
        "orderLinkId": orderLinkId,
        "timeInForce": timeInForce,
        "positionIdx": positionIdx,
        "reduceOnly": reduceOnly,
        "triggerBy": triggerBy,
        "triggerPrice": triggerPrice,
        "triggerDirection": triggerDirection,
        "takeProfit": takeProfit,
        "stopLoss": stopLoss,
        "tpTriggerBy": tpTriggerBy,
        "slTriggerBy": slTriggerBy,
        "marketUnit": marketUnit,
        "smpType": smpType,
    }
    
    # Add non-None optional parameters
    for key, value in optional_params.items():
        if value is not None:
            params[key] = value
    
    response = bybit_session.place_order(**params)
    if isinstance(response, tuple):
        response = response[0]
    return PlaceOrderResponse(**response)


def amend_order(
    category: str,
    symbol: str,
    orderId: Union[str, None] = None,
    orderLinkId: Union[str, None] = None,
    orderIv: Union[str, None] = None,
    triggerPrice: Union[str, None] = None,
    qty: Union[str, None] = None,
    price: Union[str, None] = None,
    tpslMode: Union[str, None] = None,
    takeProfit: Union[str, None] = None,
    stopLoss: Union[str, None] = None,
    tpTriggerBy: Union[str, None] = None,
    slTriggerBy: Union[str, None] = None,
    triggerBy: Union[str, None] = None,
    tpLimitPrice: Union[str, None] = None,
    slLimitPrice: Union[str, None] = None,
) -> AmendOrderResponse:
    """Amend an existing order and validate response."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(AmendOrderResponse)
    params = {
        "category": category,
        "symbol": symbol,
    }
    for key, value in [
        ("orderId", orderId),
        ("orderLinkId", orderLinkId),
        ("orderIv", orderIv),
        ("triggerPrice", triggerPrice),
        ("qty", qty),
        ("price", price),
        ("tpslMode", tpslMode),
        ("takeProfit", takeProfit),
        ("stopLoss", stopLoss),
        ("tpTriggerBy", tpTriggerBy),
        ("slTriggerBy", slTriggerBy),
        ("triggerBy", triggerBy),
        ("tpLimitPrice", tpLimitPrice),
        ("slLimitPrice", slLimitPrice),
    ]:
        if value is not None:
            params[key] = value

    response = bybit_session.amend_order(**params)
    if isinstance(response, tuple):
        response = response[0]
    return AmendOrderResponse(**response)


def cancel_order(
    category: str,
    symbol: str,
    orderId: Union[str, None] = None,
    orderLinkId: Union[str, None] = None,
    orderFilter: Union[str, None] = None,
) -> CancelOrderResponse:
    """Cancel an existing order and validate response."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(CancelOrderResponse)
    params = {
        "category": category,
        "symbol": symbol,
    }
    if orderId:
        params["orderId"] = orderId
    if orderLinkId:
        params["orderLinkId"] = orderLinkId
    if orderFilter:
        params["orderFilter"] = orderFilter

    response = bybit_session.cancel_order(**params)
    if isinstance(response, tuple):
        response = response[0]
    return CancelOrderResponse(**response)


def get_open_closed_orders(
    category: str,
    symbol: Union[str, None] = None,
    baseCoin: Union[str, None] = None,
    settleCoin: Union[str, None] = None,
    orderId: Union[str, None] = None,
    orderLinkId: Union[str, None] = None,
    openOnly: Union[int, None] = None,
    orderFilter: Union[str, None] = None,
    limit: Union[int, None] = None,
    cursor: Union[str, None] = None,
) -> OpenClosedOrdersResponse:
    """Get open and closed orders and validate response."""
    params = {"category": category}
    for key, value in [
        ("symbol", symbol),
        ("baseCoin", baseCoin),
        ("settleCoin", settleCoin),
        ("orderId", orderId),
        ("orderLinkId", orderLinkId),
        ("openOnly", openOnly),
        ("orderFilter", orderFilter),
        ("limit", limit),
        ("cursor", cursor),
    ]:
        if value is not None:
            params[key] = value

    response = bybit_session.get_open_orders(**params)
    if isinstance(response, tuple):
        response = response[0]
    return OpenClosedOrdersResponse(**response)


def cancel_all_orders(
    category: str,
    symbol: Union[str, None] = None,
    baseCoin: Union[str, None] = None,
    settleCoin: Union[str, None] = None,
    orderFilter: Union[str, None] = None,
    stopOrderType: Union[str, None] = None,
) -> CancelAllOrdersResponse:
    """Cancel all open orders and validate response."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(CancelAllOrdersResponse)
    params = {"category": category}
    for key, value in [
        ("symbol", symbol),
        ("baseCoin", baseCoin),
        ("settleCoin", settleCoin),
        ("orderFilter", orderFilter),
        ("stopOrderType", stopOrderType),
    ]:
        if value is not None:
            params[key] = value

    response = bybit_session.cancel_all_orders(**params)
    if isinstance(response, tuple):
        response = response[0]
    return CancelAllOrdersResponse(**response)


def get_order_history(
    category: str,
    symbol: Union[str, None] = None,
    baseCoin: Union[str, None] = None,
    settleCoin: Union[str, None] = None,
    orderId: Union[str, None] = None,
    orderLinkId: Union[str, None] = None,
    orderFilter: Union[str, None] = None,
    orderStatus: Union[str, None] = None,
    startTime: Union[int, None] = None,
    endTime: Union[int, None] = None,
    limit: Union[int, None] = None,
    cursor: Union[str, None] = None,
) -> OrderHistoryResponse:
    """Get order history and validate response."""
    params = {"category": category}
    for key, value in [
        ("symbol", symbol),
        ("baseCoin", baseCoin),
        ("settleCoin", settleCoin),
        ("orderId", orderId),
        ("orderLinkId", orderLinkId),
        ("orderFilter", orderFilter),
        ("orderStatus", orderStatus),
        ("startTime", startTime),
        ("endTime", endTime),
        ("limit", limit),
        ("cursor", cursor),
    ]:
        if value is not None:
            params[key] = value
    response = bybit_session.get_order_history(**params)
    if isinstance(response, tuple):
        response = response[0]
    return OrderHistoryResponse(**response)


def get_trade_history(
    category: str,
    symbol: Union[str, None] = None,
    orderId: Union[str, None] = None,
    orderLinkId: Union[str, None] = None,
    baseCoin: Union[str, None] = None,
    startTime: Union[int, None] = None,
    endTime: Union[int, None] = None,
    execType: Union[str, None] = None,
    limit: Union[int, None] = None,
    cursor: Union[str, None] = None,
) -> TradeHistoryResponse:
    """Get trade history and validate response."""
    params = {"category": category}
    for key, value in [
        ("symbol", symbol),
        ("orderId", orderId),
        ("orderLinkId", orderLinkId),
        ("baseCoin", baseCoin),
        ("startTime", startTime),
        ("endTime", endTime),
        ("execType", execType),
        ("limit", limit),
        ("cursor", cursor),
    ]:
        if value is not None:
            params[key] = value

    response = bybit_session.get_executions(**params)
    if isinstance(response, tuple):
        response = response[0]
    return TradeHistoryResponse(**response)


def batch_place_order(
    category: str,
    request: List[dict],
) -> BatchPlaceOrderResponse:
    """Place a batch of new orders and validate response."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(BatchPlaceOrderResponse)
    response = bybit_session.place_batch_order(
        category=category,
        request=request,
    )
    if isinstance(response, tuple):
        response = response[0]
    return BatchPlaceOrderResponse(**response)


def batch_amend_order(
    category: str,
    request: List[dict],
) -> BatchAmendOrderResponse:
    """Amend a batch of existing orders and validate response."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(BatchAmendOrderResponse)
    response = bybit_session.amend_batch_order(
        category=category,
        request=request,
    )
    if isinstance(response, tuple):
        response = response[0]
    return BatchAmendOrderResponse(**response)


def batch_cancel_order(
    category: str,
    request: List[dict],
) -> BatchCancelOrderResponse:
    """Cancel a batch of existing orders and validate response."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(BatchCancelOrderResponse)
    response = bybit_session.cancel_batch_order(
        category=category,
        request=request,
    )
    if isinstance(response, tuple):
        response = response[0]
    return BatchCancelOrderResponse(**response)


def get_spot_borrow_quota(
    category: str,  # Should always be "spot"
    symbol: str,
    side: str,
) -> SpotBorrowQuotaResponse:
    """Query the available balance for Spot trading and Margin trading."""
    # This is a read-only endpoint, no TRADING_ENABLED check needed by default,
    # but if it were for borrowing actions, a check might be warranted.
    params = {
        "category": category,
        "symbol": symbol,
        "side": side,
    }
    response = bybit_session.get_borrow_quota(**params)
    if isinstance(response, tuple):
        response = response[0]
    return SpotBorrowQuotaResponse(**response)


def get_wallet_balance(
    accountType: str,
    coin: Union[str, None] = None,
) -> WalletBalanceResponse:
    """Get wallet balance information."""
    # This is a read-only endpoint, but since it shows balance information
    # which is sensitive for trading, we'll require API keys but not TRADING_ENABLED
    params = {
        "accountType": accountType,
    }
    if coin:
        params["coin"] = coin

    response = bybit_session.get_wallet_balance(**params)
    if isinstance(response, tuple):
        response = response[0]
    return WalletBalanceResponse(**response)


def get_single_coin_balance(
    accountType: str,
    coin: str,
    memberId: Union[str, None] = None,
    toAccountType: Union[str, None] = None,
    toMemberId: Union[str, None] = None,
    withBonus: Union[int, None] = None,
) -> SingleCoinBalanceResponse:
    """Get single coin balance information."""
    # This is a read-only endpoint, but shows balance information
    params = {
        "accountType": accountType,
        "coin": coin,
    }
    for key, value in [
        ("memberId", memberId),
        ("toAccountType", toAccountType),
        ("toMemberId", toMemberId),
        ("withBonus", withBonus),
    ]:
        if value is not None:
            params[key] = value

    response = bybit_session.get_coin_balance(**params)
    if isinstance(response, tuple):
        response = response[0]
    return SingleCoinBalanceResponse(**response)


def get_account_info() -> AccountInfoResponse:
    """Get account information."""
    # This is a read-only endpoint
    response = bybit_session.get_account_info()
    if isinstance(response, tuple):
        response = response[0]
    return AccountInfoResponse(**response)


def place_trigger_order(
    category: str,
    symbol: str,
    side: str,
    orderType: str,
    qty: str,
    triggerPrice: str,
    triggerDirection: int,
    triggerBy: Union[str, None] = None,
    price: Union[str, None] = None,
    orderFilter: Union[str, None] = None,
    timeInForce: Union[str, None] = None,
    reduceOnly: Union[bool, None] = None,
    closeOnTrigger: Union[bool, None] = None,
    positionIdx: Union[int, None] = None,
    orderLinkId: Union[str, None] = None,
) -> PlaceOrderResponse:
    """Place a trigger/conditional order and validate response.

    Args:
        category: Product category (linear, spot, inverse)
        symbol: Trading pair symbol
        side: Buy or Sell
        orderType: Market or Limit
        qty: Order quantity
        triggerPrice: Price that triggers the order
        triggerDirection: 1 for rising, 2 for falling
        triggerBy: Price type for trigger (LastPrice, MarkPrice, IndexPrice)
        price: Order price after trigger (for Limit orders)
        orderFilter: Order filter for spot (Order, StopOrder, tpslOrder)
        timeInForce: Time in force (GTC, IOC, FOK, PostOnly)
        reduceOnly: Whether order can only reduce position
        closeOnTrigger: Whether to close position on trigger
        positionIdx: Position index for hedge mode
        orderLinkId: Custom order ID

    Returns:
        PlaceOrderResponse with order details
    """
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(PlaceOrderResponse)

    # Build parameters dict, only including non-None values
    params = {
        "category": category,
        "symbol": symbol,
        "side": side,
        "orderType": orderType,
        "qty": qty,
        "triggerPrice": triggerPrice,
        "triggerDirection": triggerDirection,
    }

    # Add optional parameters if they are provided
    for key, value in [
        ("triggerBy", triggerBy),
        ("price", price),
        ("orderFilter", orderFilter),
        ("timeInForce", timeInForce),
        ("reduceOnly", reduceOnly),
        ("closeOnTrigger", closeOnTrigger),
        ("positionIdx", positionIdx),
        ("orderLinkId", orderLinkId),
    ]:
        if value is not None:
            params[key] = value

    response = bybit_session.place_order(**params)
    if isinstance(response, tuple):
        response = response[0]
    return PlaceOrderResponse(**response)

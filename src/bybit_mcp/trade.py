import os
from typing import List, Type, TypeVar, Union  # Grouped TypeVar

from dotenv import load_dotenv
from pybit.unified_trading import HTTP

from bybit_mcp.models.trade_models import (
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
    SpotBorrowQuotaResponse,  # Added SpotBorrowQuotaResponse
    TradeHistoryResponse,
)

# Load environment variables from .env file
load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
USE_TESTNET = os.getenv("BYBIT_TESTNET", "false").lower() in ("true", "1")
TRADING_ENABLED = os.getenv("BYBIT_TRADING_ENABLED", "false").lower() in ("true", "1")

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
) -> PlaceOrderResponse:
    """Place a new order and validate response."""
    if not TRADING_ENABLED:
        return _get_trading_disabled_response(PlaceOrderResponse)
    response = bybit_session.place_order(
        category=category,
        symbol=symbol,
        side=side,
        orderType=orderType,
        qty=qty,
        price=price,
        isLeverage=isLeverage,
        orderLinkId=orderLinkId,
    )
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

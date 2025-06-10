from typing import List, Optional

from pydantic import BaseModel


class BaseApiResponse(BaseModel):
    retCode: int
    retMsg: str


class OrderItemResult(BaseModel):
    orderId: str
    orderLinkId: str


class SingleOrderItemApiResponse(BaseApiResponse):
    result: OrderItemResult


class PlaceOrderResponse(SingleOrderItemApiResponse):
    # Add other common response fields if necessary, based on API docs
    pass


class AmendOrderResponse(SingleOrderItemApiResponse):
    # Add other common response fields if necessary, based on API docs
    pass


class CancelOrderResponse(SingleOrderItemApiResponse):
    # Add other common response fields if necessary, based on API docs
    pass


class Order(BaseModel):
    orderId: str
    orderLinkId: str
    blockTradeId: str
    symbol: str
    price: str
    qty: str
    side: str
    isLeverage: str
    positionIdx: int
    orderStatus: str
    createType: Optional[str] = None  # Optional based on category
    cancelType: str
    rejectReason: str
    avgPrice: str
    leavesQty: str
    leavesValue: str
    cumExecQty: str
    cumExecValue: str
    cumExecFee: str
    timeInForce: str
    orderType: str
    stopOrderType: str
    orderIv: str
    # Add other fields from documentation as needed


class PaginatedOrderListResult(BaseModel):  # New consolidated model
    category: str
    nextPageCursor: str
    list: List[Order]


class OpenClosedOrdersResponse(BaseApiResponse):
    result: PaginatedOrderListResult  # Updated to use consolidated model
    # Add other common response fields if necessary


class CancelAllResultItem(OrderItemResult):  # Inherits from OrderItemResult
    success: Optional[str] = None  # Optional based on category


class CancelAllOrdersResult(BaseModel):
    list: List[CancelAllResultItem]


class CancelAllOrdersResponse(BaseApiResponse):
    result: CancelAllOrdersResult
    # Add other common response fields if necessary


class OrderHistoryResponse(BaseApiResponse):
    result: PaginatedOrderListResult  # Updated to use consolidated model
    # Add other common response fields if necessary


class TradeExecutionItem(BaseModel):
    symbol: str
    orderId: str
    orderLinkId: Optional[str] = None  # Optional based on classic account
    side: str
    orderPrice: str
    orderQty: str
    leavesQty: Optional[str] = None  # Optional based on classic spot
    createType: Optional[str] = None  # Optional based on category
    orderType: str
    stopOrderType: Optional[str] = None  # Optional based on classic spot
    execFee: str
    execId: str
    execPrice: str
    execQty: str
    execType: Optional[str] = None  # Optional based on classic spot
    execValue: Optional[str] = None  # Optional based on classic spot
    execTime: str
    feeCurrency: Optional[str] = None  # Optional based on classic spot
    isMaker: bool
    feeRate: Optional[str] = None  # Optional based on classic spot
    tradeIv: Optional[str] = None  # Optional for option
    markIv: Optional[str] = None  # Optional for option
    markPrice: Optional[str] = None  # Optional based on classic spot
    indexPrice: Optional[str] = None  # Optional for option
    underlyingPrice: Optional[str] = None  # Optional for option
    blockTradeId: Optional[str] = None
    closedSize: Optional[str] = None
    seq: Optional[str] = None  # Optional based on classic account Spot
    extraFees: Optional[str] = None  # Optional based on conditions
    # Add other fields from documentation as needed


class TradeHistoryResult(BaseModel):
    category: str
    list: List[TradeExecutionItem]
    nextPageCursor: Optional[str] = None


class TradeHistoryResponse(BaseApiResponse):
    result: TradeHistoryResult
    # Add other common response fields if necessary


class BatchOperationItemBase(OrderItemResult):  # Base for batch item results
    category: str
    symbol: str
    # Error fields, only present if operation failed
    code: Optional[int] = None
    msg: Optional[str] = None


class BatchPlaceOrderItem(BatchOperationItemBase):
    createAt: Optional[str] = None  # Not in docs, but present in pybit example


class BatchPlaceOrderResult(BaseModel):
    list: List[BatchPlaceOrderItem]


class BatchPlaceOrderResponse(BaseApiResponse):
    result: BatchPlaceOrderResult
    # Add other common response fields if necessary


class BatchAmendOrderItemResult(BatchOperationItemBase):
    pass  # Inherits all fields from BatchOperationItemBase


class BatchAmendOrderResult(BaseModel):
    list: List[BatchAmendOrderItemResult]


class BatchAmendOrderResponse(BaseApiResponse):
    result: BatchAmendOrderResult
    # Add other common response fields if necessary


class BatchCancelOrderItemResult(BatchOperationItemBase):
    pass  # Inherits all fields from BatchOperationItemBase


class BatchCancelOrderResult(BaseModel):
    list: List[BatchCancelOrderItemResult]


class BatchCancelOrderResponse(BaseApiResponse):
    result: BatchCancelOrderResult
    # Add other common response fields if necessary


class SpotBorrowQuotaResult(BaseModel):
    symbol: str
    side: str
    maxTradeQty: str
    maxTradeAmount: str
    spotMaxTradeQty: str
    spotMaxTradeAmount: str
    borrowCoin: str


class SpotBorrowQuotaResponse(BaseApiResponse):
    result: SpotBorrowQuotaResult
    # Add other common response fields if necessary

from typing import List, Optional, Union

from pydantic import BaseModel, field_validator


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
    blockTradeId: Optional[str] = None
    symbol: str
    price: str
    qty: str
    side: str
    isLeverage: Optional[str] = None
    positionIdx: Optional[int] = None
    orderStatus: str
    createType: Optional[str] = None  # Optional based on category
    cancelType: Optional[str] = None
    rejectReason: Optional[str] = None
    avgPrice: Optional[str] = None
    leavesQty: Optional[str] = None
    leavesValue: Optional[str] = None
    cumExecQty: Optional[str] = None
    cumExecValue: Optional[str] = None
    cumExecFee: Optional[str] = None
    timeInForce: Optional[str] = None
    orderType: str
    stopOrderType: Optional[str] = None
    orderIv: Optional[str] = None
    triggerPrice: Optional[str] = None
    takeProfit: Optional[str] = None
    stopLoss: Optional[str] = None
    createdTime: Optional[str] = None
    updatedTime: Optional[str] = None
    triggerDirection: Optional[int] = None
    triggerBy: Optional[str] = None
    reduceOnly: Optional[bool] = None
    closeOnTrigger: Optional[bool] = None
    smpType: Optional[str] = None
    smpGroup: Optional[int] = None
    smpOrderId: Optional[str] = None
    tpslMode: Optional[str] = None
    tpLimitPrice: Optional[str] = None
    slLimitPrice: Optional[str] = None
    placeType: Optional[str] = None
    # Additional fields based on official API documentation


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
    seq: Optional[Union[str, int]] = None  # Optional based on classic account Spot - API can return int or str
    extraFees: Optional[str] = None  # Optional based on conditions
    # Add other fields from documentation as needed

    @field_validator("seq", mode="before")
    @classmethod
    def convert_seq_to_str(cls, v):
        """Convert seq field from int to str if needed."""
        if v is not None and isinstance(v, int):
            return str(v)
        return v


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


# Models for Wallet Balance
class CoinBalance(BaseModel):
    coin: str
    equity: str
    usdValue: str
    walletBalance: str
    borrowAmount: str
    availableToBorrow: str
    availableToWithdraw: str
    accruedInterest: str
    totalOrderIM: str
    totalPositionIM: str
    totalPositionMM: str
    unrealisedPnl: str
    cumRealisedPnl: str
    bonus: str
    collateralSwitch: bool
    marginCollateral: bool
    locked: str
    spotHedgingQty: str


class WalletBalance(BaseModel):
    accountType: str
    totalEquity: str
    totalWalletBalance: str
    totalMarginBalance: str
    totalAvailableBalance: str
    totalPerpUPL: str
    totalInitialMargin: str
    totalMaintenanceMargin: str
    accountIMRate: str
    accountMMRate: str
    accountLTV: str
    coin: List[CoinBalance]


class WalletBalanceResult(BaseModel):
    list: List[WalletBalance]


class WalletBalanceResponse(BaseApiResponse):
    result: WalletBalanceResult


# Models for Single Coin Balance
class SingleCoinBalanceResult(BaseModel):
    accountType: str
    bizType: int
    accountId: str
    memberId: str
    balance: CoinBalance


class SingleCoinBalanceResponse(BaseApiResponse):
    result: SingleCoinBalanceResult


# Models for Account Info
class AccountInfo(BaseModel):
    unifiedMarginStatus: int
    marginMode: str
    dcpStatus: str
    timeWindow: int
    smpGroup: int
    isMasterTrader: bool
    spotHedgingStatus: str
    updatedTime: str


class AccountInfoResponse(BaseApiResponse):
    result: AccountInfo

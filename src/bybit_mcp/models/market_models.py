from pydantic import BaseModel


class ServerTimeResponse(BaseModel):
    """Pydantic model for Bybit server time response."""

    timeSecond: str


class TickerItem(BaseModel):
    symbol: str
    bid1Price: str
    bid1Size: str
    ask1Price: str
    ask1Size: str
    lastPrice: str
    prevPrice24h: str
    price24hPcnt: str
    # Add more fields as needed


class TickerResponse(BaseModel):
    category: str
    list: list[TickerItem]


class OrderBookItem(BaseModel):
    price: str
    size: str


class OrderBookResponse(BaseModel):
    s: str  # symbol
    b: list[list[str]]  # bids: [[price, size], ...]
    a: list[list[str]]  # asks: [[price, size], ...]
    ts: int
    u: int
    seq: int
    cts: int


class RecentTradeItem(BaseModel):
    execId: str
    symbol: str
    price: str
    size: str
    side: str
    time: str
    isBlockTrade: bool
    isRPITrade: bool
    # Option fields (optional)
    mP: str | None = None
    iP: str | None = None
    mIv: str | None = None
    iv: str | None = None


class RecentTradesResponse(BaseModel):
    category: str
    list: list[RecentTradeItem]


class KlineItem(BaseModel):
    startTime: str
    openPrice: str
    highPrice: str
    lowPrice: str
    closePrice: str
    volume: str
    turnover: str


class KlineResponse(BaseModel):
    category: str
    symbol: str
    list: list[list[str]]


class LeverageFilter(BaseModel):
    minLeverage: str
    maxLeverage: str
    leverageStep: str


class PriceFilter(BaseModel):
    minPrice: str
    maxPrice: str
    tickSize: str


class LotSizeFilter(BaseModel):
    maxOrderQty: str
    minOrderQty: str
    qtyStep: str
    postOnlyMaxOrderQty: str | None = None
    maxMktOrderQty: str | None = None
    minNotionalValue: str | None = None


class RiskParameters(BaseModel):
    priceLimitRatioX: str | None = None
    priceLimitRatioY: str | None = None


class InstrumentInfoItem(BaseModel):
    symbol: str
    contractType: str
    status: str
    baseCoin: str
    quoteCoin: str
    launchTime: str
    deliveryTime: str
    deliveryFeeRate: str | None = None
    priceScale: str
    leverageFilter: LeverageFilter
    priceFilter: PriceFilter
    lotSizeFilter: LotSizeFilter
    unifiedMarginTrade: bool | None = None
    fundingInterval: int | None = None
    settleCoin: str
    copyTrading: str | None = None
    upperFundingRate: str | None = None
    lowerFundingRate: str | None = None
    isPreListing: bool | None = None
    preListingInfo: dict | None = None
    riskParameters: RiskParameters | None = None
    # Optional fields that may not be present in all categories
    optionType: str | None = None
    volScale: str | None = None


class InstrumentsInfoResponse(BaseModel):
    category: str
    list: list[InstrumentInfoItem]
    nextPageCursor: str | None = None


class FundingRateHistoryItem(BaseModel):
    symbol: str
    fundingRate: str
    fundingRateTimestamp: str
    # Add more fields as needed


class FundingRateHistoryResponse(BaseModel):
    category: str
    list: list[FundingRateHistoryItem]
    nextPageCursor: str | None = None


class OpenInterestItem(BaseModel):
    openInterest: str
    timestamp: str


class OpenInterestResponse(BaseModel):
    symbol: str
    category: str
    list: list[OpenInterestItem]
    nextPageCursor: str | None = None


class InsuranceItem(BaseModel):
    coin: str
    symbols: str
    balance: str
    value: str


class InsuranceResponse(BaseModel):
    updatedTime: str
    list: list[InsuranceItem]


class RiskLimitItem(BaseModel):
    id: int
    symbol: str
    riskLimitValue: str
    # Add more fields as needed


class RiskLimitResponse(BaseModel):
    category: str
    list: list[RiskLimitItem]
    nextPageCursor: str | None = None


class LongShortRatioItem(BaseModel):
    symbol: str
    buyRatio: str
    sellRatio: str
    timestamp: str
    # Add more fields as needed


class LongShortRatioResponse(BaseModel):
    list: list[LongShortRatioItem]
    nextPageCursor: str | None = None
    nextPageCursor: str | None = None

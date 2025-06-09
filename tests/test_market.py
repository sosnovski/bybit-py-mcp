from bybit_mcp.market import (
    get_funding_rate_history,
    get_index_price_kline,
    get_instruments_info,
    get_insurance,
    get_kline,
    get_long_short_ratio,
    get_mark_price_kline,
    get_open_interest,
    get_order_book,
    get_premium_index_price_kline,
    get_recent_trades,
    get_risk_limit,
    get_server_time,
    get_tickers,
)


def test_get_server_time():
    result = get_server_time()
    assert isinstance(result, dict)
    assert "result" in result
    assert "timeSecond" in result["result"]


def test_get_tickers():
    result = get_tickers(symbol="BTCUSDT")
    assert result.category in ("linear", "spot", "inverse", "option")
    assert hasattr(result, "list")
    assert isinstance(result.list, list)


def test_get_order_book():
    result = get_order_book(symbol="BTCUSDT")
    assert hasattr(result, "s")
    assert hasattr(result, "b")
    assert hasattr(result, "a")


def test_get_recent_trades():
    result = get_recent_trades(symbol="BTCUSDT")
    assert hasattr(result, "category")
    assert isinstance(result.list, list)


def test_get_kline():
    result = get_kline(symbol="BTCUSDT", interval="5")
    assert hasattr(result, "category")
    assert hasattr(result, "list")


def test_get_mark_price_kline():
    result = get_mark_price_kline(symbol="BTCUSDT", interval="5")
    assert hasattr(result, "category")
    assert hasattr(result, "list")


def test_get_index_price_kline():
    result = get_index_price_kline(symbol="BTCUSDT", interval="5")
    assert hasattr(result, "category")
    assert hasattr(result, "list")


def test_get_premium_index_price_kline():
    result = get_premium_index_price_kline(symbol="BTCUSDT", interval="5")
    assert hasattr(result, "category")
    assert hasattr(result, "list")


def test_get_instruments_info():
    result = get_instruments_info()
    assert hasattr(result, "category")
    assert hasattr(result, "list")


def test_get_funding_rate_history():
    result = get_funding_rate_history(symbol="BTCUSDT")
    assert hasattr(result, "category")
    assert hasattr(result, "list")


def test_get_open_interest():
    result = get_open_interest(symbol="BTCUSDT", interval="5min")
    assert hasattr(result, "category")
    assert hasattr(result, "list")


def test_get_insurance():
    result = get_insurance()
    assert hasattr(result, "updatedTime")
    assert hasattr(result, "list")


def test_get_risk_limit():
    result = get_risk_limit(symbol="BTCUSDT")
    assert hasattr(result, "category")
    assert hasattr(result, "list")


def test_get_long_short_ratio():
    result = get_long_short_ratio(symbol="BTCUSDT", interval="5min")
    assert hasattr(result, "list")
    assert hasattr(result, "nextPageCursor")

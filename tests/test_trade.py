# tests/test_trade.py
import os

import pytest  # Third-party imports
from dotenv import load_dotenv

from bybit_mcp.models.trade_models import (
    AmendOrderResponse,
    CancelOrderResponse,
    PlaceOrderResponse,
)
from bybit_mcp.trade import (
    amend_order,
    cancel_order,
    place_order,
)

# Load environment variables for tests
load_dotenv()

# Ensure testnet is enabled for these tests - this should be set in your .env for testing
# or configured in your test environment
if os.getenv("BYBIT_TESTNET", "false").lower() not in ("true", "1"):
    print("\nWARNING: BYBIT_TESTNET is not set to true. Trade tests might fail or use live account.")
    print("Please set BYBIT_TESTNET=true in your .env file for testing trade functions.")
    # It's often better to raise an error or skip tests if the environment isn't correctly configured
    # pytest.skip("Trade tests require BYBIT_TESTNET=true", allow_module_level=True)


@pytest.mark.skipif(os.getenv("BYBIT_TESTNET", "false").lower() not in ("true", "1"), reason="Trade tests require BYBIT_TESTNET=true")
def test_place_linear_market_buy_order():
    """Test placing a linear market buy order on the testnet."""
    # Ensure you have a valid API key and secret with trade permissions on testnet
    # and sufficient testnet funds (e.g., USDT for linear)
    category = "linear"
    symbol = "BTCUSDT"  # Changed back to BTCUSDT
    side = "Buy"
    orderType = "Market"
    qty = "0.001"  # Adjust quantity as needed, ensure it's above minimum order size
    orderLinkId = f"test_market_buy_{os.urandom(8).hex()}"  # Unique order link ID

    try:
        response = place_order(category=category, symbol=symbol, side=side, orderType=orderType, qty=qty, orderLinkId=orderLinkId)
        assert isinstance(response, PlaceOrderResponse)
        assert response.retCode == 0, f"API Error: {response.retMsg} (Symbol: {symbol})"
        assert response.result is not None
        assert response.result.orderId is not None
        assert response.result.orderLinkId == orderLinkId
        print(f"\nPlaced order ID: {response.result.orderId}, Link ID: {response.result.orderLinkId} for {symbol}")

    except Exception as e:
        pytest.fail(f"test_place_linear_market_buy_order failed for {symbol}: {e}")


@pytest.mark.skipif(os.getenv("BYBIT_TESTNET", "false").lower() not in ("true", "1"), reason="Trade tests require BYBIT_TESTNET=true")
def test_place_and_cancel_linear_limit_order():
    """Test placing and then cancelling a linear limit order on the testnet."""
    category = "linear"
    symbol = "BTCUSDT"  # Changed back to BTCUSDT
    side = "Buy"
    orderType = "Limit"
    qty = "0.001"
    # Place the limit order far from the current market price to ensure it doesn't fill immediately
    # You might need to adjust this price based on the current market conditions on testnet
    price = "10000.00"  # Example: a price significantly lower than current market for a buy
    orderLinkId = f"test_limit_buy_cancel_{os.urandom(8).hex()}"
    placed_order_id = None

    try:
        # Place the limit order
        place_response = place_order(
            category=category, symbol=symbol, side=side, orderType=orderType, qty=qty, price=price, orderLinkId=orderLinkId
        )
        assert isinstance(place_response, PlaceOrderResponse)
        assert place_response.retCode == 0, f"Place Order API Error: {place_response.retMsg}"
        assert place_response.result is not None
        assert place_response.result.orderId is not None
        placed_order_id = place_response.result.orderId
        print(f"\nPlaced limit order ID: {placed_order_id}, Link ID: {place_response.result.orderLinkId}")

        # Cancel the order
        cancel_response = cancel_order(category=category, symbol=symbol, orderId=placed_order_id)
        assert isinstance(cancel_response, CancelOrderResponse)
        assert cancel_response.retCode == 0, f"Cancel Order API Error: {cancel_response.retMsg}"
        assert cancel_response.result is not None
        assert cancel_response.result.orderId == placed_order_id
        print(f"Cancelled order ID: {cancel_response.result.orderId}")

    except Exception as e:
        pytest.fail(f"test_place_and_cancel_linear_limit_order failed: {e}")
    finally:
        # Ensure cleanup even if assertions fail mid-way, though cancel_order is already tried
        if placed_order_id and ("cancel_response" not in locals() or cancel_response.retCode != 0):
            print(f"Attempting final cleanup for order ID: {placed_order_id}")
            try:
                cleanup_cancel = cancel_order(category=category, symbol=symbol, orderId=placed_order_id)
                if cleanup_cancel.retCode == 0:
                    print(f"Successfully cleaned up order ID: {placed_order_id}")
                else:
                    print(f"Cleanup failed for order ID {placed_order_id}: {cleanup_cancel.retMsg}")
            except Exception as cleanup_e:
                print(f"Error during final cleanup of order ID {placed_order_id}: {cleanup_e}")


@pytest.mark.skipif(os.getenv("BYBIT_TESTNET", "false").lower() not in ("true", "1"), reason="Trade tests require BYBIT_TESTNET=true")
def test_place_amend_and_cancel_linear_limit_order():
    """Test placing, amending, and then cancelling a linear limit order."""
    category = "linear"
    symbol = "BTCUSDT"  # Changed back to BTCUSDT
    side = "Buy"
    orderType = "Limit"
    initial_qty = "0.001"
    initial_price = "10000.00"  # Far from market
    amended_price = "10001.00"
    orderLinkId = f"test_limit_amend_cancel_{os.urandom(8).hex()}"
    placed_order_id = None

    try:
        # 1. Place the initial limit order
        place_response = place_order(
            category=category, symbol=symbol, side=side, orderType=orderType, qty=initial_qty, price=initial_price, orderLinkId=orderLinkId
        )
        assert place_response.retCode == 0, f"Place Order failed: {place_response.retMsg}"
        placed_order_id = place_response.result.orderId
        print(f"\nPlaced order for amend test: {placed_order_id}")

        # 2. Amend the order (e.g., change price)
        amend_response = amend_order(category=category, symbol=symbol, orderId=placed_order_id, price=amended_price)
        assert isinstance(amend_response, AmendOrderResponse)
        assert amend_response.retCode == 0, f"Amend Order failed: {amend_response.retMsg}"
        assert amend_response.result.orderId == placed_order_id
        print(f"Amended order ID: {amend_response.result.orderId} to price {amended_price}")

        # 3. Cancel the amended order
        cancel_response = cancel_order(category=category, symbol=symbol, orderId=placed_order_id)
        assert isinstance(cancel_response, CancelOrderResponse)
        assert cancel_response.retCode == 0, f"Cancel Order failed: {cancel_response.retMsg}"
        assert cancel_response.result.orderId == placed_order_id
        print(f"Cancelled amended order ID: {cancel_response.result.orderId}")

    except Exception as e:
        pytest.fail(f"test_place_amend_and_cancel_linear_limit_order failed: {e}")
    finally:
        if placed_order_id:
            # Attempt to cancel if not already successfully cancelled in the try block
            # This check is a bit simplified; a more robust way would be to check order status
            print(f"Final cleanup attempt for order ID: {placed_order_id}")
            try:
                cleanup_cancel = cancel_order(category=category, symbol=symbol, orderId=placed_order_id)
                # We don't assert here as the order might have been cancelled already or filled
                if cleanup_cancel.retCode == 0:
                    print(f"Successfully cleaned up order ID: {placed_order_id} in finally block.")
                elif cleanup_cancel.retMsg == "Order does not exist.":  # Or similar error for already cancelled/filled
                    print(f"Order {placed_order_id} likely already cancelled or filled.")
                else:
                    print(f"Cleanup failed for order ID {placed_order_id} in finally: {cleanup_cancel.retMsg}")
            except Exception as cleanup_e:
                print(f"Error during final cleanup of order ID {placed_order_id}: {cleanup_e}")


@pytest.mark.skipif(os.getenv("BYBIT_TESTNET", "false").lower() not in ("true", "1"), reason="Trade tests require BYBIT_TESTNET=true")
def test_place_order_with_risk_management():
    """Test placing a limit order with take profit and stop loss for risk management."""
    category = "linear"
    symbol = "BTCUSDT"
    side = "Buy"
    orderType = "Limit"
    qty = "0.001"
    price = "10000.00"  # Far below market price
    takeProfit = "15000.00"  # Take profit at higher price
    stopLoss = "8000.00"   # Stop loss at lower price
    timeInForce = "GTC"  # Good Till Cancel
    reduceOnly = False
    orderLinkId = f"test_risk_mgmt_{os.urandom(8).hex()}"
    placed_order_id = None

    try:
        # Place order with risk management parameters
        place_response = place_order(
            category=category,
            symbol=symbol,
            side=side,
            orderType=orderType,
            qty=qty,
            price=price,
            takeProfit=takeProfit,
            stopLoss=stopLoss,
            timeInForce=timeInForce,
            reduceOnly=reduceOnly,
            orderLinkId=orderLinkId
        )
        
        assert isinstance(place_response, PlaceOrderResponse)
        assert place_response.retCode == 0, f"Place Order with Risk Mgmt failed: {place_response.retMsg}"
        assert place_response.result is not None
        assert place_response.result.orderId is not None
        placed_order_id = place_response.result.orderId
        print(f"\nPlaced order with TP/SL - ID: {placed_order_id}, TP: {takeProfit}, SL: {stopLoss}")

        # Cancel the order for cleanup
        cancel_response = cancel_order(category=category, symbol=symbol, orderId=placed_order_id)
        assert cancel_response.retCode == 0, f"Cancel Order failed: {cancel_response.retMsg}"
        print(f"Cancelled risk management order ID: {placed_order_id}")

    except Exception as e:
        pytest.fail(f"test_place_order_with_risk_management failed: {e}")
    finally:
        if placed_order_id:
            try:
                cleanup_cancel = cancel_order(category=category, symbol=symbol, orderId=placed_order_id)
                if cleanup_cancel.retCode == 0:
                    print(f"Final cleanup successful for order ID: {placed_order_id}")
            except Exception as cleanup_e:
                print(f"Error during final cleanup of order ID {placed_order_id}: {cleanup_e}")


def test_place_order_validation():
    """Test parameter validation for place_order function."""
    
    # Test that price is required for Limit orders
    with pytest.raises(ValueError, match="Price is required for Limit orders"):
        place_order(
            category="linear",
            symbol="BTCUSDT", 
            side="Buy",
            orderType="Limit",
            qty="0.001"
            # Missing required price parameter
        )

    # Test that triggerBy is required when triggerPrice is specified
    with pytest.raises(ValueError, match="triggerBy is required when triggerPrice is specified"):
        place_order(
            category="linear",
            symbol="BTCUSDT",
            side="Buy", 
            orderType="Market",
            qty="0.001",
            triggerPrice="50000"
            # Missing triggerBy parameter
        )

    # Test that triggerPrice is required when triggerDirection is specified  
    with pytest.raises(ValueError, match="triggerPrice is required when triggerDirection is specified"):
        place_order(
            category="linear",
            symbol="BTCUSDT",
            side="Buy",
            orderType="Market", 
            qty="0.001",
            triggerDirection=1
            # Missing triggerPrice parameter
        )

    print("All parameter validation tests passed!")


def test_place_order_default_trigger_types():
    """Test that default trigger types are set for TP/SL when not specified."""
    import bybit_mcp.trade as trade_module
    
    # Mock the bybit_session to capture the parameters passed
    original_trading_enabled = trade_module.TRADING_ENABLED
    original_place_order = trade_module.bybit_session.place_order
    
    captured_params = None
    
    def mock_place_order(**kwargs):
        nonlocal captured_params
        captured_params = kwargs
        # Return a mock response
        return {"retCode": 0, "retMsg": "OK", "result": {"orderId": "test123", "orderLinkId": "test_link"}}
    
    try:
        # Enable trading and mock the place_order function
        trade_module.TRADING_ENABLED = True
        trade_module.bybit_session.place_order = mock_place_order
        
        # Call place_order with TP/SL but without trigger types
        trade_module.place_order(
            category="linear",
            symbol="BTCUSDT",
            side="Buy",
            orderType="Limit",
            qty="0.001",
            price="50000",
            takeProfit="55000",
            stopLoss="45000"
        )
        
        # Check that default trigger types were added
        assert captured_params is not None
        assert captured_params.get("tpTriggerBy") == "LastPrice"
        assert captured_params.get("slTriggerBy") == "LastPrice"
        print("Default trigger types correctly set for TP/SL!")
        
    finally:
        # Restore original values
        trade_module.TRADING_ENABLED = original_trading_enabled
        trade_module.bybit_session.place_order = original_place_order

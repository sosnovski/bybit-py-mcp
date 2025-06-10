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

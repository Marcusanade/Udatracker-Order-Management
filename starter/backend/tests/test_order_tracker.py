import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---
#
def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")

    mock_storage.save_order.assert_called_once_with("ORD001", {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    })

def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    with pytest.raises(ValueError, match="Order with ID 'ORD_EXISTING' already exists."):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")

def test_get_order_by_id(order_tracker, mock_storage):
    """Tests retrieving an existing order by its ID."""
    mock_storage.get_order.return_value = {"order_id": "ORD.MPV.001"}
    order = order_tracker.get_order_by_id("ORD.MPV.001")
    assert order["order_id"] == "ORD.MPV.001"

def test_get_order_by_id_raises_error_if_empty_id(order_tracker, mock_storage):
    """Tests that retrieving a non-existent order raises a ValueError."""
    mock_storage.get_order.return_value = None
    with pytest.raises(ValueError, match="Ei! Order ID must be provided."):
        order_tracker.get_order_by_id("")

def test_get_order_by_id_returns_none_if_not_found(order_tracker, mock_storage):
    """Tests that retrieving a non-existent order returns None."""
    mock_storage.get_order.return_value = None
    order = order_tracker.get_order_by_id("ORD_NOT_EXIST")
    assert order is None

def test_update_order_status(order_tracker, mock_storage):
    """Tests updating the status of an existing order."""
    mock_storage.get_order.return_value = {"order_id": "ORD.MPV.001", "status": "pending"}
    order_tracker.update_order_status("ORD.MPV.001", "shipped")
    mock_storage.save_order.assert_called_once_with("ORD.MPV.001", {"order_id": "ORD.MPV.001", "status": "shipped"})

def test_update_order_status_raises_error_if_order_not_exists(order_tracker, mock_storage):
    """Tests that updating the status of a non-existent order raises a ValueError."""
    mock_storage.get_order.return_value = None
    with pytest.raises(ValueError, match="Order with ID 'ORD_NOT_EXIST' does not exist."):
        order_tracker.update_order_status("ORD_NOT_EXIST", "shipped")

def test_update_order_status_raises_error_if_invalid_status(order_tracker, mock_storage):
    """Tests that updating the status with an invalid status raises a ValueError."""
    mock_storage.get_order.return_value = {"order_id": "ORD.MPV.001", "status": "pending"}
    with pytest.raises(ValueError, match=r"Status must be one of \['pending', 'processing', 'shipped', 'delivered', 'cancelled'\]."):
        order_tracker.update_order_status("ORD.MPV.001", "invalid_status")

def test_update_order_status_raises_error_if_order_id_not_provided(order_tracker, mock_storage):
    """Tests that updating the status without providing an order ID raises a ValueError."""
    with pytest.raises(ValueError, match="Order ID must be provided."):
        order_tracker.update_order_status("", "shipped")

def test_list_all_orders(order_tracker, mock_storage):
    """Tests listing all orders."""
    mock_storage.get_all_orders.return_value = {
        "ORD.MPV.001": {"order_id": "ORD.MPV.001", "status": "pending"},
        "ORD.MPV.002": {"order_id": "ORD.MPV.002", "status": "shipped"}
    }
    orders = order_tracker.list_all_orders()
    assert len(orders) == 2
    assert orders[0]["order_id"] == "ORD.MPV.001"
    assert orders[1]["order_id"] == "ORD.MPV.002"

def test_list_orders_by_status(order_tracker, mock_storage):
    """Tests listing orders by their status."""
    mock_storage.get_all_orders.return_value = {
        "ORD.MPV.001": {"order_id": "ORD.MPV.001", "status": "pending"},
        "ORD.MPV.002": {"order_id": "ORD.MPV.002", "status": "shipped"}
    }

    orders = order_tracker.list_orders_by_status("pending")
    assert len(orders) == 1
    assert orders[0]["order_id"] == "ORD.MPV.001"



from flask import Flask, request, jsonify, send_from_directory
from backend.order_tracker import OrderTracker
from backend.in_memory_storage import InMemoryStorage

app = Flask(__name__, static_folder='../frontend')
in_memory_storage = InMemoryStorage()
order_tracker = OrderTracker(in_memory_storage)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/orders', methods=['POST'])
def add_order_api():
    new_order = request.get_json()
    try:
        order_tracker.add_order(
            order_id=new_order["order_id"],
            item_name=new_order["item_name"],
            quantity=new_order["quantity"],
            customer_id=new_order["customer_id"],
            status=new_order.get("status", "pending")
        )
        order_created = order_tracker.get_order_by_id(new_order["order_id"])
        return jsonify(order_created), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/orders/<string:order_id>', methods=['GET'])
def get_order_api(order_id):
    try:
        order = order_tracker.get_order_by_id(order_id)
        if order is None:
            return jsonify({"error": "Order not found."}), 404
        return jsonify(order), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/orders/<string:order_id>/status', methods=['PUT'])
def update_order_status_api(order_id):
    try:
        new_status = request.get_json().get("new_status")
        order_tracker.update_order_status(order_id, new_status)
        updated_order = order_tracker.get_order_by_id(order_id)
        return jsonify(updated_order), 200
    except ValueError as e:
        if "does not exist" in str(e):
            return jsonify({"error": "Order not found."}), 404
        return jsonify({"error": str(e)}), 400

@app.route('/api/orders', methods=['GET'])
def list_orders_api():
    try:
        status = request.args.get("status")
        if status:
            orders = order_tracker.list_orders_by_status(status)
        else:
            orders = order_tracker.list_all_orders()
        return jsonify(orders), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

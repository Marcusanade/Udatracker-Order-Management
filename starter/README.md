# Udatracker Order Management by Marcusanade

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```

## Reflection

- **Design decision:** In `update_order_status`, validations are ordered intentionally — empty ID first, then invalid status, then storage lookup. This "fail fast" approach avoids unnecessary storage calls and makes error messages predictable. The trade-off is that the API distinguishes between `400 Bad Request` and `404 Not Found` by inspecting the error message text, which is a pragmatic but fragile coupling between layers.

- **Testing insight:** The unit tests for `update_order_status` with mock storage drove the decision to validate status before calling `get_order`. Without the test asserting that `save_order` was never called on an invalid status, this ordering would have been easy to miss. The failing test caught this design gap early.

- **Next step:** The most valuable next step would be adding a `DELETE /api/orders/<order_id>` endpoint with its corresponding unit and integration tests, followed by replacing `InMemoryStorage` with a persistent storage backend (e.g., SQLite) to survive server restarts.

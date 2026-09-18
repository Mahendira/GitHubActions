from __future__ import annotations


class OrderManagementService:
    def __init__(self):
        self._orders = {}
        self._images = ["image-1", "image-2", "image-3"]

    def create_order(self, user_name: str, items: list[str] | None = None):
        order_id = f"order-{len(self._orders) + 1}"
        order = {
            "id": order_id,
            "user": user_name,
            "items": items or [],
            "status": "created",
        }
        self._orders[order_id] = order
        return order

    def get_order_status(self, order_id: str) -> str:
        order = self._orders.get(order_id)
        if order is None:
            return "not_found"
        return order["status"]

    def list_images(self) -> list[str]:
        return list(self._images)

    def validate_request(self, user_name: str, items: list[str] | None = None) -> dict:
        if not user_name or not user_name.strip():
            raise ValueError("user name is required")
        normalized_items = items or []
        return {
            "user": user_name.strip(),
            "items": normalized_items,
            "status": "valid",
            "image_count": len(normalized_items) or len(self._images),
        }

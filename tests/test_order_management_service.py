import unittest

from app.order_management_service import OrderManagementService


class TestOrderManagementService(unittest.TestCase):
    def setUp(self):
        self.service = OrderManagementService()

    def test_create_order_sets_status_created(self):
        result = self.service.create_order("demo-user", ["image-1", "image-2"])
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["user"], "demo-user")

    def test_list_images_has_entries(self):
        result = self.service.list_images()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_get_order_status_returns_created(self):
        order = self.service.create_order("demo-user", ["image-1"])
        status = self.service.get_order_status(order["id"])
        self.assertEqual(status, "created")

    def test_validate_request_rejects_empty_user(self):
        with self.assertRaises(ValueError):
            self.service.validate_request(" ")

    def test_get_order_status_returns_not_found_when_missing(self):
        status = self.service.get_order_status("missing-order")
        self.assertEqual(status, "not_found")

    def test_validate_request_accepts_valid_user(self):
        result = self.service.validate_request("demo-user", ["image-1"])
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["user"], "demo-user")
        self.assertEqual(result["image_count"], 1)


if __name__ == "__main__":
    unittest.main()

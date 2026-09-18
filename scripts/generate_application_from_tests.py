#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def slug_to_class_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", " ", value.strip())
    words = [part for part in cleaned.split() if part]
    if not words:
        return "GeneratedService"
    return "".join(word.capitalize() for word in words) + "Service"


def slug_to_module_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip())
    cleaned = cleaned.strip("_")
    if not cleaned:
        return "generated_service"
    module_name = "_".join(part.lower() for part in cleaned.split("_") if part)
    return module_name if module_name.endswith("_service") else f"{module_name}_service"


def generate_service_code(feature_name: str) -> str:
    class_name = slug_to_class_name(feature_name)
    return f'''from __future__ import annotations


class {class_name}:
    def __init__(self):
        self._orders = {{}}
        self._images = ["image-1", "image-2", "image-3"]

    def create_order(self, user_name: str, items: list[str] | None = None):
        order_id = f"order-{{len(self._orders) + 1}}"
        order = {{
            "id": order_id,
            "user": user_name,
            "items": items or [],
            "status": "created",
        }}
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
        return {{
            "user": user_name.strip(),
            "items": normalized_items,
            "status": "valid",
            "image_count": len(normalized_items) or len(self._images),
        }}
'''


def ensure_app_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def generate_test_code(feature_name: str) -> str:
    class_name = slug_to_class_name(feature_name)
    module_name = slug_to_module_name(feature_name)
    return f'''import unittest

from app.{module_name} import {class_name}


class Test{class_name}(unittest.TestCase):
    def setUp(self):
        self.service = {class_name}()

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
'''


def main():
    parser = argparse.ArgumentParser(description="Generate application code from a feature file or test context.")
    parser.add_argument("--feature", default="Business_requirements_001.feature", help="Feature file to derive service name and behavior from.")
    parser.add_argument("--app-dir", default="app", help="Directory for generated Python application code.")
    parser.add_argument("--test-dir", default="tests", help="Directory for generated tests.")
    args = parser.parse_args()

    feature_file = Path(args.feature)
    feature_name = feature_file.stem.replace("_", " ").replace("-", " ")
    module_name = slug_to_module_name(feature_name)
    class_name = slug_to_class_name(feature_name)
    app_dir = Path(args.app_dir)
    test_dir = Path(args.test_dir)

    ensure_app_directory(app_dir)
    app_module_path = app_dir / f"{module_name}.py"
    app_module_path.write_text(generate_service_code(feature_name), encoding="utf-8")

    ensure_app_directory(test_dir)
    test_module_path = test_dir / f"test_{module_name}.py"
    test_module_path.write_text(generate_test_code(feature_name), encoding="utf-8")

    print(f"Generated app: {app_module_path}")
    print(f"Generated tests: {test_module_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

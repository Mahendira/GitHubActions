import tempfile
import unittest
from pathlib import Path

from scripts.generate_tests_from_feature import (
    generate_step_definition_file,
    generate_unittest_file,
    parse_feature_file,
)


class GenerateTestsFromFeatureTests(unittest.TestCase):
    def test_parse_feature_file_extracts_feature_and_steps(self):
        feature_text = '''
Feature: Order management

  Scenario: User creates an order
    Given the user is signed in
    And the cart has an item
    When the user submits the order
    Then the order should be created
'''.strip()

        with tempfile.TemporaryDirectory() as tmp_dir:
            feature_path = Path(tmp_dir) / "Order_management.feature"
            feature_path.write_text(feature_text, encoding="utf-8")

            feature = parse_feature_file(feature_path)

            self.assertEqual(feature["feature_name"], "Order management")
            self.assertEqual(feature["scenario_name"], "User creates an order")
            self.assertEqual(
                feature["steps"],
                [
                    "Given the user is signed in",
                    "And the cart has an item",
                    "When the user submits the order",
                    "Then the order should be created",
                ],
            )

    def test_generate_unittest_file_contains_test_case_and_asserts(self):
        feature = {
            "feature_name": "Order management",
            "scenario_name": "User creates an order",
            "steps": [
                "Given the user is signed in",
                "When the user submits the order",
                "Then the order should be created",
            ],
        }

        generated = generate_unittest_file(feature)

        self.assertIn("class TestOrderManagement(unittest.TestCase):", generated)
        self.assertIn("def test_user_creates_an_order", generated)
        self.assertIn("self.assertIsNotNone", generated)
        self.assertIn("self.assertEqual", generated)
        self.assertNotIn("assertTrue(True)", generated)

    def test_generate_step_definition_file_contains_behave_steps(self):
        feature = {
            "feature_name": "Order management",
            "scenario_name": "User creates an order",
            "steps": [
                "Given the user is signed in",
                "When the user submits the order",
                "Then the order should be created",
            ],
        }

        generated = generate_step_definition_file(feature)

        self.assertIn("from behave import given, then, when", generated)
        self.assertIn("@given('the user is signed in')", generated)
        self.assertIn("@when('the user submits the order')", generated)
        self.assertIn("@then('the order should be created')", generated)
        self.assertIn("assert", generated)
        self.assertNotIn("assert context is not None", generated)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock

from backend.services.defense import quarantine_cascade


class TestCascade(unittest.TestCase):

    @patch("backend.services.defense.graph")
    def test_parent_and_child_are_quarantined(self, mock_graph):
        mock_result = MagicMock()
        mock_result.result_set = [[["parent-1", "child-1"]]]
        mock_graph.query.return_value = mock_result

        result = quarantine_cascade("parent-1", "Compromised")

        self.assertEqual(
            result["quarantined_ids"],
            ["parent-1", "child-1"],
        )

    @patch("backend.services.defense.graph")
    def test_missing_memory(self, mock_graph):
        mock_result = MagicMock()
        mock_result.result_set = []
        mock_graph.query.return_value = mock_result

        result = quarantine_cascade("missing-id", "Test")

        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
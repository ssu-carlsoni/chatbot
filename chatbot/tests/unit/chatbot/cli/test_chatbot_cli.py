import unittest
from unittest.mock import patch

from typer.testing import CliRunner

from chatbot.cli.chatbot_cli import app, container


class TestChatbotCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch.object(container, "knowledge_manager")
    def test_rebuild_knowledge_success(self, mock_manager):
        mock_manager.return_value.rebuild.return_value = True

        result = self.runner.invoke(app, ['knowledge-rebuild'])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Knowledge Update Successful", result.output)


    @patch.object(container, "knowledge_manager")
    def test_rebuild_knowledge_failure(self, mock_manager):
        mock_manager.return_value.update_knowledge.return_value = False

        result = self.runner.invoke(app, ['knowledge-rebuild'])

        self.assertEqual(1, result.exit_code)
        self.assertIn("Knowledge Update Failed", result.output)

if __name__ == '__main__':
    unittest.main()
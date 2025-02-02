import unittest
from unittest.mock import patch

from typer.testing import CliRunner

from chatbot.cli.chatbot_cli import app


class TestChatbotCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("chatbot.cli.chatbot_cli.KnowledgeManager")
    def test_update_knowledge_success(self, mock_knowledge_manager):
        mock_knowledge_manager.return_value.update_knowledge.return_value = True

        result = self.runner.invoke(app, ['update-knowledge'])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Knowledge Update Successful", result.output)


    @patch("chatbot.cli.chatbot_cli.KnowledgeManager")
    def test_update_knowledge_failure(self, mock_knowledge_manager):
        mock_knowledge_manager.return_value.update_knowledge.return_value = False

        result = self.runner.invoke(app, ['update-knowledge'])

        self.assertEqual(1, result.exit_code)
        self.assertIn("Knowledge Update Failed", result.output)

if __name__ == '__main__':
    unittest.main()
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class GeminiSearchTests(unittest.TestCase):
    def test_live_model(self):
        s = (ROOT / "main/conversation_task.cpp").read_text()
        self.assertIn('cfg.model = "gemini-3.8-live";', s)

    def test_search_preserves_local_tools(self):
        s = (ROOT / "components/conversation/gemini_live_client.cpp").read_text()
        a = s.index('cJSON_AddObjectToObject(search_tool, "googleSearch");')
        b = s.index('if (!config_.tools.empty())', a)
        c = s.index('cJSON_AddItemToArray(tools, tool);', b)
        self.assertTrue(a < b < c)

if __name__ == "__main__":
    unittest.main()

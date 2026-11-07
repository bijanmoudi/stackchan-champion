from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class GeminiSearchTests(unittest.TestCase):
    def test_live_model(self):
        s = (ROOT / "main/conversation_task.cpp").read_text()
        self.assertIn('cfg.model = "gemini-3.8-live";', s)

    def test_live_38_session_omits_legacy_thinking_config(self):
        s = (ROOT / "components/conversation/gemini_live_client.cpp").read_text()
        self.assertNotIn('cJSON_AddObjectToObject(gen_cfg, "thinkingConfig")', s)
        self.assertIn('models/gemini-3.8-live', s)

    def test_gemini_quota_stops_reconnect_storm(self):
        ws = (ROOT / "components/conversation/gemini_live_client.cpp").read_text()
        task = (ROOT / "main/conversation_task.cpp").read_text()
        self.assertIn('last_close_reason_.find("exceeded your current quota")', ws)
        self.assertIn('last_close_reason_.find("RESOURCE_EXHAUSTED")', ws)
        self.assertIn('quota_rejected ? "gemini_quota_exceeded" : "websocket closed"', ws)
        self.assertIn('ev.text == "gemini_quota_exceeded"', task)
        self.assertIn('if (quota_limited_) break;', task)
        self.assertIn('if (quota_limited_) {', task)
        self.assertIn('client_->stop();', task)
        self.assertIn('state_.conv.status.store(ConvStatus::Error', task)

    def test_offline_play_ui_and_cloud_pause(self):
        ui = (ROOT / "main/device_ui.cpp").read_text()
        shared = (ROOT / "main/shared_state.hpp").read_text()
        task = (ROOT / "main/conversation_task.cpp").read_text()
        self.assertIn('kPlay = 7', ui)
        self.assertIn('g_cv->drawString("PEEKABOO!"', ui)
        self.assertIn('g_cv->drawString(g_play_color >= 0', ui)
        self.assertIn('std::atomic<bool> play_mode_active{false}', shared)
        self.assertIn('g_state->play_mode_active.store(page == kPlay', ui)
        self.assertIn('state_.play_mode_active.load(std::memory_order_acquire)', task)

    def test_search_preserves_local_tools(self):
        s = (ROOT / "components/conversation/gemini_live_client.cpp").read_text()
        a = s.index('cJSON_AddObjectToObject(search_tool, "googleSearch");')
        b = s.index('if (!config_.tools.empty())', a)
        c = s.index('cJSON_AddItemToArray(tools, tool);', b)
        self.assertTrue(a < b < c)

if __name__ == "__main__":
    unittest.main()

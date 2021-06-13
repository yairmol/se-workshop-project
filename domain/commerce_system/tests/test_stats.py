from unittest import TestCase

from domain.commerce_system.commerce_system_statistics import CommerceSystemStats


class TestStats(TestCase):
    def setUp(self) -> None:
        self.stats = CommerceSystemStats()

    def test_add_action(self):
        self.stats.action_made("a1", "u1")
        actions = self.stats.get_all_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(len(actions["a1"]), 1)
        self.assertEqual(actions["a1"][0].action, "a1")
        self.assertEqual(actions["a1"][0].action_maker, "u1")

    # TODO: Add tests

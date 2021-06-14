from datetime import datetime
from itertools import product
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

    def insert_actions(self, actions, users, timestamps=None):
        timestamps = timestamps if timestamps is not None else [None] * len(actions) * len(users)
        for (action, maker), timestamp in zip(product(actions, users), timestamps):
            self.stats.action_made(action, maker, time=datetime.fromtimestamp(timestamp) if timestamp else timestamp)

    def test_get_actions_in_time_window(self):
        self.insert_actions(["a1", "a2"], ["u1", "u2"], [1000, 1100, 1200, 1400])
        actions = self.stats.get_all_actions((datetime.fromtimestamp(1000), datetime.fromtimestamp(1300)))
        self.assertEqual(3, len(actions["a1"]) + len(actions["a2"]))

    def test_get_user_actions(self):
        self.insert_actions(["a1", "a2"], ["u1", "u2"])
        actions = self.stats.actions_of_user("u1")
        self.assertEqual(2, len(actions["a1"]) + len(actions["a2"]))
        self.assertTrue(
            all([all([r.action_maker == "u1" for r in rs]) for rs in actions.values()])
        )

    def test_get_user_actions_non_existing_user(self):
        self.insert_actions(["a1", "a2"], ["u1", "u2"])
        actions = self.stats.actions_of_user("u3")
        self.assertEqual(0, sum(len(rs) for rs in actions.values()))

    def test_get_action_records(self):
        self.insert_actions(["a1", "a2"], ["u1", "u2"])
        records = self.stats.get_action_records("a1")
        self.assertEqual(len(records), 2)
        self.assertTrue(all([r.action == "a1" for r in records]))

    def test_get_action_records_non_existing_actions(self):
        records = self.stats.get_action_records("a3")
        self.assertEqual(len(records), 0)

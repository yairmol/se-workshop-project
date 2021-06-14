from collections import defaultdict
from datetime import datetime
from typing import Dict, Optional, Tuple, List, Any
from data_model import ActivityReport


TimeWindow = Optional[Tuple[datetime, datetime]]


class Record:
    def __init__(self, action_name: str, action_maker: str, time=None):
        self.action = action_name
        self.action_maker = action_maker
        self.time = datetime.now() if not time else time

    def to_dict(self):
        return {
            ActivityReport.ACTION: self.action,
            ActivityReport.ACTION_MAKER: self.action_maker,
            ActivityReport.TIME: self.time.timestamp(),
        }


class CommerceSystemStats:
    def __init__(self):
        self.actions: Dict[str, List[Record]] = defaultdict(list)

    def action_made(self, action_name: str, action_maker: str, time: Optional[datetime] = None):
        self.actions[action_name].append(Record(action_name, action_maker, time))

    def actions_of_user(self, user: str, time_window: TimeWindow = None):
        return self.apply_time_window_on_dict({
            a: [r for r in rs if r.action_maker == user]
            for a, rs in self.actions.items()
        }, time_window)

    def get_all_actions(self, time_window: TimeWindow = None):
        return self.apply_time_window_on_dict(self.actions, time_window)

    def get_action_records(self, action_name: str, time_window: TimeWindow = None):
        return self.apply_time_window_filter(self.actions.get(action_name, []), time_window)

    @staticmethod
    def apply_time_window_filter(records: List[Record], time_window: TimeWindow):
        if time_window is None:
            return records
        return [r for r in records if time_window[0] <= r.time <= time_window[1]]

    @staticmethod
    def apply_time_window_on_dict(actions: Dict[Any, List[Record]], time_window: TimeWindow):
        return {
            k: CommerceSystemStats.apply_time_window_filter(v, time_window) for k, v in actions.items()
        }

    def get_actions_filtered(self, actions: Optional[List[str]], users: Optional[List[str]], time_window: TimeWindow):
        return self.apply_time_window_on_dict({
            action: [r for r in records if not users or r.action_maker in users]
            for action, records in self.actions.items()
            if not actions or action in actions
        }, time_window)

    def get_action_names(self):
        return list(self.actions.keys())

    def get_users(self):
        return list(set([record.action_maker for records in self.actions.values() for record in records]))

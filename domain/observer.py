from typing import List, Dict, Any


class Observer:
    def send_message(self, msg):
        raise NotImplementedError()


class Observable:
    def __init__(self):
        self.observers: List[Observer] = []
        self.keyed_observers: Dict[Any, Observer] = {}

    def add_observer(self, obs: Observer):
        self.observers.append(obs)

    def remove_observer(self, obs: Observer):
        assert obs in self.observers, "failed to remove observer"
        self.observers.remove(obs)

    def add_keyed_observer(self, key, obs: Observer):
        self.keyed_observers[key] = obs

    def remove_keyed_observer(self, key):
        self.keyed_observers.pop(key)

    def notify_observer(self, key, msg: str):
        self.keyed_observers[key].send_message(msg)

    def notify(self, msg: str):
        print("notifying observers", self.observers, self.keyed_observers)
        for obs in self.observers:
            obs.send_message(msg)

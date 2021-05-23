from __future__ import annotations
from typing import Callable, Optional, Any, Generic, TypeVar, Iterable
T = TypeVar('T')
U = TypeVar('U')


class Action(Generic[T]):
    """
    A class for modeling actions and their reverse
    used for performing purchases and easily reverse them
    in a case of failure
    """
    def __init__(self, action: Callable[[Any], T], *args, **kwargs):
        self.action: Callable[[Any], T] = action
        self.args = args
        self.kwargs = kwargs
        self.reverse_action: Optional[Action[U]] = None
        self.return_value = None
        self.use_return_value = False
        self.return_value_name = None
        self.error_msg = "action failed"

    def set_reverse(
            self, reverse_action: Action[U], use_return_value=False, return_value_name=None
    ) -> Action:
        """
        sets the reverse action of this action.
        :param reverse_action:
        :param use_return_value:
        :param return_value_name::
        :return: this action object, for convenient building
        """
        self.reverse_action = reverse_action
        self.use_return_value = use_return_value
        self.return_value_name = return_value_name
        return self

    def set_error_message(self, error_msg):
        """
        :param error_msg error message to be raised in case of failure (False value returned from action execution)
        """
        self.error_msg = error_msg
        return self

    def preform_action(self):
        self.return_value = self.action(*self.args, **self.kwargs)
        return self.return_value

    def reverse(self):
        if self.use_return_value:
            if self.return_value_name:
                self.reverse_action.add_keyword_argument(self.return_value_name, self.return_value)
            else:
                self.reverse_action.add_positional_argument(0, self.return_value)
        return self.reverse_action.preform_action()

    def add_positional_argument(self, loc: int, arg: Any):
        temp_args = list(self.args)
        temp_args.insert(loc, arg)
        self.args = tuple(temp_args)

    def add_keyword_argument(self, name: str, arg: Any):
        self.kwargs.update({name: arg})


class ActionPool:
    def __init__(self, actions: Iterable[Action]):
        self.actions = actions
        self.successful_actions_stack = []
        self.return_values = []

    def execute_actions(self, do_what_you_can=False):
        """
        executes the pool of actions.
        in case an action fails all performed actions are reversed
        :return: True in case of success, otherwise False
        """
        self.successful_actions_stack = []
        for action in self.actions:
            result, assertion_error, exception = None, None, None
            try:
                result = action.preform_action()
            except AssertionError as e:
                assertion_error = e
            except Exception as e:
                exception = e
            self.return_values.append(result)
            if not result:
                if do_what_you_can and not exception:
                    continue
                self.cancel_actions()
                if exception:
                    raise exception
                if assertion_error:
                    raise assertion_error
                assert result, action.error_msg
            self.successful_actions_stack.append(action)
        return True

    def cancel_actions(self):
        while self.successful_actions_stack:
            action = self.successful_actions_stack.pop()
            action.reverse()

    def get_return_values(self):
        return self.return_values

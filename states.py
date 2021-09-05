from __future__ import annotations

from abc import ABCMeta
from typing import List, Callable, Optional

from aiogram.types import Message

from test_action import test_action


class MachineError(Exception):
    message = "Can't trigger event"


class State(ABCMeta):
    name: str
    action: Optional[Callable]

    @staticmethod
    def get_destinations() -> List[State]:
        raise NotImplementedError()

    def check_can_change(self, state: State) -> bool:
        return state in self.get_destinations()


class BaseState(metaclass=State):
    pass


'''
state realization
'''


class AddText(BaseState):
    name = "add_text"
    action = test_action

    @staticmethod
    def get_destinations():
        return [Menu, WriteText]


class WriteText(BaseState):
    name = "write_text"
    action = test_action

    @staticmethod
    def get_destinations():
        return [Menu, AddText]


class ReadText(BaseState):
    name = "read_text"
    action = test_action

    @staticmethod
    def get_destinations():
        return [Menu, ReadText]


class Menu(BaseState):
    name = "menu"
    action = test_action

    @staticmethod
    def get_destinations():
        return [WriteText, ReadText]


class Start(BaseState):
    name = "start"
    action = test_action

    @staticmethod
    def get_destinations():
        return [Menu, ]


'''
state machine
'''


class StateMachine:
    state: State

    def __init__(self, initial_state: State):
        self.state = initial_state

    async def change_state(self, state: State, message: Message):
        if self.state.check_can_change(state):
            self.state = state
            if self.state.action is not None:
                await self.state.action(state, message)
        else:
            raise MachineError()


state_machine = StateMachine(Start)
states = {state.name: state for state in [Start, Menu, ReadText, WriteText, AddText]}

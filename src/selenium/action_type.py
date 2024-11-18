from enum import Enum


class ActionType(Enum):
    CLICK = 'click'
    INPUT = 'input'
    WAIT_FOR = 'wait_for'
    SLEEP = 'sleep'
    KEYBOARD_SHORTCUT = 'keyboard_shortcut'
    CUSTOM = 'custom'

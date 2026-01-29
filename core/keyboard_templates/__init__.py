"""
Система шаблонов кнопок для повторного использования между ботами
"""

from .base import BaseKeyboardTemplate
from .simple import SimpleTemplate
from .grid import GridTemplate
from .menu import MenuTemplate
from .action import ActionTemplate
from .dynamic import DynamicTemplate

__all__ = [
    'BaseKeyboardTemplate',
    'SimpleTemplate',
    'GridTemplate',
    'MenuTemplate',
    'ActionTemplate',
    'DynamicTemplate'
]

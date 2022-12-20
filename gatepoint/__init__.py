"""
Discord Library API
~~~~~~~~~~~~~~~~~~~

A Discord Library API similar to discord.py.

:copyright: (c) 2022-present BenitzCoding
:license: MIT, see LICENSE for more details.

"""

__title__ = 'gatepoint'
__author__ = 'BenitzCoding'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-present BenitzCoding'
__version__ = '0.1'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import logging
from typing import NamedTuple, Literal

from .gateway import GatewayClient
from .interaction import Interaction, Choice, Option, CommandInteraction, AutoComplete
from .object_types import OptionType

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major = 0,
    minor = 1,
    micro = 0,
    releaselevel = "alpha",
    serial = 0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo
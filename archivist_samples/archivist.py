"""Local Archivist class
"""

# pylint:  disable=missing-docstring
# pylint:  disable=too-few-public-methods

from archivist.archivist import Archivist as _Archivist

from .about import __version__ as VERSION
from .constants import USER_AGENT_PREFIX


class Archivist(_Archivist):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_agent = f"{USER_AGENT_PREFIX}{VERSION}"

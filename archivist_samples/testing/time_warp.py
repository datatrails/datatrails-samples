"""Simulates accelerated time for creating plausible logs quickly"""

import datetime


class TimeWarp:  # pylint: disable=too-few-public-methods
    """Stretches time"""

    def __init__(self, start, ffwd):
        self._start_time = datetime.datetime.now()
        self._origin = start
        self._rate = ffwd

    def now(self):
        """Get the warped time"""
        delta = (datetime.datetime.now() - self._start_time).total_seconds()
        return self._origin + datetime.timedelta(seconds=(delta * self._rate))

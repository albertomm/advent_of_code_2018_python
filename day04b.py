#!/usr/bin/env python3

"""
Example input:

[1518-09-02 00:00] Guard #2137 begins shift
[1518-05-01 00:45] falls asleep
[1518-08-15 00:47] wakes up
"""

from collections import Counter
from collections import defaultdict
import re


class Solver(object):

    GUARD_EXPR = r'\[(\d+)\-(\d+)\-(\d+) (\d+):(\d+)\] Guard #(\d+) begins shift'
    SLEEP_EXPR = r'\[(\d+)\-(\d+)\-(\d+) (\d+):(\d+)\] falls asleep'
    AWAKE_EXPR = r'\[(\d+)\-(\d+)\-(\d+) (\d+):(\d+)\] wakes up'

    def __init__(self, fd):
        """Set up the initial state and begin processing the input data."""

        # Registry of the guards and the minutes in which they sleep
        self.guards = defaultdict(Counter)

        # Current shift's guard
        self.guard = None

        # Current guard's sleep minute start
        self.sleep_minute = None

        self.event_processors = (
            (self.GUARD_EXPR, self._begin_shift),
            (self.SLEEP_EXPR, self._fall_asleep),
            (self.AWAKE_EXPR, self._wake_up),
        )

        # Parse the input
        for event in sorted(fd):
            self._process_event(event)

    def __str__(self):
        """Return the answer."""
        guard, minute = self.find_guard_and_minute()
        return str(guard * minute)

    def _process_event(self, event):
        """Parse the event, find and apply the related action method."""

        for expr, processor in self.event_processors:
            match = re.match(expr, event)
            if match:
                return processor(match)

    def _begin_shift(self, match):
        """Process a shift guard change."""

        _, _, _, _, _, self.guard = map(int, match.groups())
        self.sleep_minute = None

    def _fall_asleep(self, match):
        """The current guard falls asleep."""

        _, _, _, _, self.sleep_minute = map(int, match.groups())

    def _wake_up(self, match):
        """The current guard wakes up."""

        _, _, _, _, awake_minute = map(int, match.groups())
        minutes_asleep = range(self.sleep_minute, awake_minute)
        self.guards[self.guard].update(minutes_asleep)
        self.sleep_minute = None

    def find_guard_and_minute(self):
        """Find the guard which sleeps the most during the same minute."""

        _, minute, guard = max(
            (times_asleep, minute, guard)
            for guard, minutes in self.guards.items()
            for minute, times_asleep in minutes.most_common(1)
        )
        return guard, minute


if __name__ == '__main__':
    with open('day04.txt', 'r') as fd:
        print(Solver(fd))

#!/usr/bin/env python
# vi: set et ts=4:



import unittest
from emtest import EventManagerMock
from uzbl.plugins.config import Config
from uzbl.plugins.mode import ModePlugin
from uzbl.plugins.on_event import OnEventPlugin


class OnEventTest(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManagerMock(
            (), (OnEventPlugin,),
        )
        self.uzbl = self.event_manager.add()

    def test_command(self):
        oe = OnEventPlugin[self.uzbl]
        event, command = 'FOO', 'test test'

        oe.on_event(event, [], command)
        oe.event_handler('', on_event=event)
        self.uzbl.send.assert_called_once_with(command)

    def test_matching_pattern(self):
        oe = OnEventPlugin[self.uzbl]
        event, pattern, command = 'FOO', ['BAR'], 'test test'

        oe.on_event(event, pattern, command)
        oe.event_handler('BAR else', on_event=event)
        self.uzbl.send.assert_called_once_with(command)

    def test_non_matching_pattern(self):
        oe = OnEventPlugin[self.uzbl]
        event, pattern, command = 'FOO', ['BAR'], 'test test'

        oe.on_event(event, pattern, command)
        oe.event_handler('FOO else', on_event=event)
        self.assertFalse(self.uzbl.send.called)

    def test_parse(self):
        oe = OnEventPlugin[self.uzbl]
        event, command = 'FOO', 'test test'

        oe.parse_on_event((event, command))
        self.assertIn(event, oe.events)

    def test_parse_pattern(self):
        oe = OnEventPlugin[self.uzbl]
        event, pattern, command = 'FOO', 'BAR', 'test test'

        oe.parse_on_event((event, '[', pattern, ']', command))
        self.assertIn(event, oe.events)
        commands = oe.events[event]
        self.assertIn(command, commands)
        self.assertEqual(commands[command], [pattern])

# -*- coding: utf-8 -*-
"""
LSTree tests.

"""
from mock import MagicMock, patch
import unittest

from livesource import LiveSource


class LiveSourceTestCase(unittest.TestCase):
    @patch('livesource.livesource.LSTree', MagicMock())
    def setUp(self):
        self.source = LiveSource('test_code')
        self.source.lst.globals = {}
        self.source.lst.locals = {'__livesource_listing': ''}
        self.source.lst.visit = MagicMock(side_effect=lambda x: x)

    @patch('livesource.livesource.LSTree', MagicMock(side_effect=lambda x: x))
    def test_init(self):
        code = 'test_code'
        max_deep = 1

        result = LiveSource(code, max_deep)

        self.assertEqual(result.code, code)
        self.assertEqual(result.lst, max_deep)

    def test_get_values(self):
        self.source._parse = MagicMock(return_value='')

        result = self.source.get_values()

        self.assertEqual(result, '')

    @unittest.skip("Not Implemented")
    def test_set_variable(self):
        pass

    def test_update(self):
        code = 'new_code'

        self.source.update(code)

        self.assertEqual(self.source.code, code)

    @patch('ast.parse', MagicMock(side_effect=lambda x: 'parsed {}'.format(x)))
    @patch('ast.fix_missing_locations', MagicMock(side_effect=lambda x: x))
    def test__parse(self):
        result = self.source._parse()

        self.assertEqual(result, 'parsed test_code')

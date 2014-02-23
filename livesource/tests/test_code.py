#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ComplexNode tests.

"""
import collections
from textwrap import dedent as d
import unittest

from livesource import LiveSource


class CodeTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    a = 1
                 """)
        result = lambda x: collections.deque(x, maxlen=10)
        values = LiveSource(code).get_values()

        self.assertEqual(values[1], result([('a', 1)]))

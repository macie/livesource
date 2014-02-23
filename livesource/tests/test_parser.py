#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ComplexNode tests.

"""
import ast
from textwrap import dedent as d
import unittest

from livesource import LivesourceTree


class AssignTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    a = 1
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a = 1
                    _livesource_listing[1].append(('a', a, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_multiline(self):
        code = d("""\
                    a = 1
                    b = 2
                    c = 3
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a = 1
                    _livesource_listing[1].append(('a', a, ))
                    b = 2
                    _livesource_listing[2].append(('b', b, ))
                    c = 3
                    _livesource_listing[3].append(('c', c, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_parallel(self):
        code = d("""\
                    a, b, c = 1, 2, 3
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a, b, c = 1, 2, 3
                    _livesource_listing[1].append(('a', a, ))
                    _livesource_listing[1].append(('b', b, ))
                    _livesource_listing[1].append(('c', c, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_attribute(self):
        code = d("""\
                    a.x = (2,)
                    a.x.y = [1, 2]
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a.x = (2,)
                    _livesource_listing[1].append(('a.x', a.x, ))
                    a.x.y = [1, 2]
                    _livesource_listing[2].append(('a.x.y', a.x.y, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_chained(self):
        code = d("""\
                    a = b = 1
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a = b = 1
                    _livesource_listing[1].append(('a', a, ))
                    _livesource_listing[1].append(('b', b, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_swap(self):
        code = d("""\
                    a, b = b, a
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a, b = b, a
                    _livesource_listing[1].append(('a', a, ))
                    _livesource_listing[1].append(('b', b, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)


class AugAssignTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    a += 1
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a += 1
                    _livesource_listing[1].append(('a', a, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_multiline(self):
        code = d("""\
                    a += 1
                    b -= 2
                    c *= 3
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a += 1
                    _livesource_listing[1].append(('a', a, ))
                    b -= 2
                    _livesource_listing[2].append(('b', b, ))
                    c *= 3
                    _livesource_listing[3].append(('c', c, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_attribute(self):
        code = d("""\
                    a.x *= 2
                    a.x.y /= 2
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    a.x *= 2
                    _livesource_listing[1].append(('a.x', a.x, ))
                    a.x.y /= 2
                    _livesource_listing[2].append(('a.x.y', a.x.y, ))
                   """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)


class IfTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    if x:
                        pass
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    if x:
                        _livesource_listing[1].append((None, x,))
                        pass
                 """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)


class WhileTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    while x:
                        pass
                 """)
        result = d("""\
                    import collections; _livesource_listing = collections.defaultdict(lambda: collections.deque(maxlen=10))
                    while x:
                        _livesource_listing[1].append((None, x,))
                        pass

                 """)

        parsed_tree = ast.dump(LivesourceTree(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)
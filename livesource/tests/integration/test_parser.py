# -*- coding: utf-8 -*-
"""
Parser tests.

"""
import ast
from textwrap import dedent as d
import unittest

from livesource import LiveSource


class AssignTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    a = 1
                 """)
        result = d("""\
                    a = 1
                    __livesource_listing[1].append(('a', a, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_multiline(self):
        code = d("""\
                    a = 1
                    b = 2
                    c = 3
                 """)
        result = d("""\
                    a = 1
                    __livesource_listing[1].append(('a', a, ))
                    b = 2
                    __livesource_listing[2].append(('b', b, ))
                    c = 3
                    __livesource_listing[3].append(('c', c, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_parallel(self):
        code = d("""\
                    a, b, c = 1, 2, 3
                 """)
        result = d("""\
                    a, b, c = 1, 2, 3
                    __livesource_listing[1].append(('a', a, ))
                    __livesource_listing[1].append(('b', b, ))
                    __livesource_listing[1].append(('c', c, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_attribute(self):
        code = d("""\
                    a.x = (2,)
                    a.x.y = [1, 2]
                 """)
        result = d("""\
                    a.x = (2,)
                    __livesource_listing[1].append(('a.x', a.x, ))
                    a.x.y = [1, 2]
                    __livesource_listing[2].append(('a.x.y', a.x.y, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_chained(self):
        code = d("""\
                    a = b = 1
                 """)
        result = d("""\
                    a = b = 1
                    __livesource_listing[1].append(('a', a, ))
                    __livesource_listing[1].append(('b', b, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_swap(self):
        code = d("""\
                    a, b = b, a
                 """)
        result = d("""\
                    a, b = b, a
                    __livesource_listing[1].append(('a', a, ))
                    __livesource_listing[1].append(('b', b, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)


class AugAssignTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    a += 1
                 """)
        result = d("""\
                    a += 1
                    __livesource_listing[1].append(('a', a, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_multiline(self):
        code = d("""\
                    a += 1
                    b -= 2
                    c *= 3
                 """)
        result = d("""\
                    a += 1
                    __livesource_listing[1].append(('a', a, ))
                    b -= 2
                    __livesource_listing[2].append(('b', b, ))
                    c *= 3
                    __livesource_listing[3].append(('c', c, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_attribute(self):
        code = d("""\
                    a.x *= 2
                    a.x.y /= 2
                 """)
        result = d("""\
                    a.x *= 2
                    __livesource_listing[1].append(('a.x', a.x, ))
                    a.x.y /= 2
                    __livesource_listing[2].append(('a.x.y', a.x.y, ))
                   """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)


class IfTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    if x:
                        pass
                 """)
        result = d("""\
                    if x:
                        __livesource_listing[1].append((None, x,))
                        pass
                 """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)


class PrintTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    print "aaa"
                 """)
        result = d("""\
                    print "aaa"
                    __livesource_listing[1].append((None, "aaa",))

                 """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_comma(self):
        code = d("""\
                    print "a", "b"
                 """)
        result = d("""\
                    print "a", "b"
                    __livesource_listing[1].append((None, ("a", "b"),))

                 """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_concatenate(self):
        code = d("""\
                    print "a" + "b"
                 """)
        result = d("""\
                    print "a" + "b"
                    __livesource_listing[1].append((None, "a" + "b",))

                 """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

    def test_format(self):
        code = d("""\
                    print "a{}".format("b")
                 """)
        result = d("""\
                    print "a{}".format("b")
                    __livesource_listing[1].append((None, "a{}".format("b"),))

                 """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)


class WhileTestCase(unittest.TestCase):
    def test_trivial(self):
        code = d("""\
                    while x:
                        pass
                 """)
        result = d("""\
                    while x:
                        __livesource_listing[1].append((None, x,))
                        pass

                 """)

        parsed_tree = ast.dump(LiveSource(code)._parse())
        expected_tree = ast.dump(ast.parse(result))

        self.assertEqual(parsed_tree, expected_tree)

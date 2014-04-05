# -*- coding: utf-8 -*-
"""
LSTree tests.

"""
import ast
import collections
from mock import MagicMock
import sys
import unittest

from livesource import LSTree


class LSTreeTestCase(unittest.TestCase):
    def setUp(self):
        max_deep = 10
        self.lst = LSTree(max_deep)
        self.listing = collections.defaultdict(
            lambda: collections.deque(maxlen=max_deep))

    def test__add_listener(self):
        lineno, var_name, val = 1, 'test_var', 'test_val'
        result = ast.dump(self.lst._add_listener(lineno, var_name, val))

        expected = ast.dump(
            ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Subscript(
                value=ast.Name(id='__livesource_listing', ctx=ast.Load()),
                slice=ast.Index(value=ast.Num(n=lineno)), ctx=ast.Load()),
                attr='append', ctx=ast.Load()),
                args=[ast.Tuple(elts=[var_name, val, ], ctx=ast.Load()), ],
                keywords=[], starargs=None, kwargs=None),
                lineno=lineno+1, col_offset=-1))

        self.assertEqual(result, expected)


class ExpressionsTestCase(unittest.TestCase):
    def setUp(self):
        self.lst = LSTree()
        self.node = MagicMock()
        self.node.body.return_value = ''

    def test_attribute(self):
        result = self.lst.visit_Attribute(self.node)

        self.assertEqual(result, self.node)

    def test_compare(self):
        result = self.lst.visit_Compare(self.node)

        self.assertEqual(result, self.node)

    def test_name(self):
        result = self.lst.visit_Name(self.node)

        self.assertEqual(result, self.node)


class ModulesTestCase(unittest.TestCase):
    def setUp(self):
        self.lst = LSTree()
        self.node = MagicMock()
        self.node.body.return_value = ''

    def test_expression(self):
        result = ast.dump(self.lst.visit_Expression(self.node))

        expected = ast.dump(ast.Expression(body=[]))

        self.assertEqual(result, expected)

    def test_interactive(self):
        result = ast.dump(self.lst.visit_Interactive(self.node))

        expected = ast.dump(ast.Interactive(body=[]))

        self.assertEqual(result, expected)

    def test_module(self):
        result = ast.dump(self.lst.visit_Module(self.node))

        expected = ast.dump(ast.Module(body=[]))

        self.assertEqual(result, expected)


class StatementsTestCase(unittest.TestCase):
    def setUp(self):
        self.lst = LSTree()
        self.node = MagicMock()
        self.node.body.return_value = ''

    def test_assign(self):
        result = self.lst.visit_Assign(self.node)

        self.assertEqual(result, self.node)

    def test_augassign(self):
        result = self.lst.visit_AugAssign(self.node)

        self.assertEqual(result, self.node)

    def test_if(self):
        result = self.lst.visit_If(self.node)

        self.assertEqual(result, self.node)

    @unittest.skipIf(sys.version_info[0] == 3, 'Not supported in Python 3')
    def test_print(self):
        result = self.lst.visit_Print(self.node)

        self.assertEqual(result, self.node)

    def test_return(self):
        result = self.lst.visit_Return(self.node)

        self.assertEqual(result, self.node)

    def test_while(self):
        result = self.lst.visit_While(self.node)

        self.assertEqual(result, self.node)


class VisitorTestCase(unittest.TestCase):
    def setUp(self):
        self.lst = LSTree()

    def test_block_visit(self):
        obj = MagicMock()
        obj.lineno.return_value = 1
        obj.col_offset.return_value = 0
        self.lst.stack = []
        self.lst.generic_visit = MagicMock(return_value=None)

        fields = [obj]

        result = self.lst.block_visit(fields)

        self.assertEqual(result, fields)

    def test_block_visit_empty(self):
        obj = MagicMock()
        obj.lineno.return_value = 1
        obj.col_offset.return_value = 0
        self.lst.stack = [obj]

        fields = []

        result = self.lst.block_visit(fields)

        self.assertEqual(result, [])

        fields = [obj]

        result = self.lst.block_visit(fields)

        self.assertEqual(result, [])

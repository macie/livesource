#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LiveSource.

"""
import ast


class LivesourceTree(ast.NodeVisitor):
    def __init__(self, code, max_deep=10):
        """

        """
        self.code = code
        self.stack = []
        # TODO: move to livesource_globals
        self.header = [
            # import collections
            ast.Import(names=[ast.alias(name='collections', asname=None)],
                lineno=1),
            # _livesource_listing = collections.defaultdict(
            #    lambda: collections.deque(maxlen=<max_deep>))
            ast.Assign(targets=[ast.Name(id='_livesource_listing',
                ctx=ast.Store())], value=ast.Call(func=ast.Attribute(
                value=ast.Name(id='collections', ctx=ast.Load()),
                attr='defaultdict', ctx=ast.Load()), args=[ast.Lambda(
                args=ast.arguments(args=[], vararg=None, kwarg=None,
                defaults=[]), body=ast.Call(func=ast.Attribute(value=ast.Name(
                id='collections', ctx=ast.Load()), attr='deque', ctx=ast.Load()
                ), args=[], keywords=[ast.keyword(arg='maxlen', value=ast.Num(
                n=max_deep))], starargs=None, kwargs=None))], keywords=[],
                starargs=None, kwargs=None), lineno=1)]

    def get_values(self):
        """
        Returns values for all lines in code.

        Returns:
            collections.defaultdict object.

        """
        livesource_globals = {'collections': __import__('collections')}
        livesource_locals = {}

        # TODO: exceptions handling
        compiled_code = compile(self._parse(), '<livesource>', 'exec')
        exec(compiled_code, livesource_globals, livesource_locals)

        return livesource_locals['_livesource_listing']

    def update(self, code):
        """
        Update source code.

        """
        self.code = code
        self.stack = []

    def _parse(self):
        """
        Parse source code.

        Returns:
            ast tree object.

        """
        tree = ast.parse(self.code)
        parsed_tree = self.visit(tree)
        ast.fix_missing_locations(parsed_tree)
        return parsed_tree

    #
    #  Tree visitors
    #

    def field_visit(self, fields):
        """
        Visit nodes in fields.

        """
        if not isinstance(fields, list):
            fields = [fields]
        self.generic_visit(ast.Expression(body=fields))

    def block_visit(self, fields):
        """
        Visit nodes in fields.

        Returns:
            list of fields sorted by line number

        """
        old_stack = self.stack
        self.stack = []
        self.field_visit(fields)
        if old_stack:
            old_stack.append(self.stack)
            self.stack = old_stack

        fields.extend(self.stack)
        sorted_args = sorted(fields,
                             key=lambda obj: (obj.lineno, obj.col_offset))
        return sorted_args

    #
    #  Modules
    #

    def visit_Expression(self, node):
        tree = self.header[:]
        tree.extend(self.block_visit(node.body))
        return ast.Expression(body=tree)

    def visit_Interactive(self, node):
        tree = self.header[:]
        tree.extend(self.block_visit(node.body))
        return ast.Interactive(body=tree)

    def visit_Module(self, node):
        tree = self.header[:]
        tree.extend(self.block_visit(node.body))
        return ast.Module(body=tree)

    #
    #  Statements
    #

    def visit_Assign(self, node):
        self.field_visit(node.targets)
        return node

    def visit_AugAssign(self, node):
        self.field_visit(node.target)
        return node

    def visit_If(self, node):
        node.body = self.block_visit(node.body)

        lineno = node.lineno
        name = ast.Name(id='None', ctx=ast.Load())  # no name
        value = node.test  # boolean

        body = [self.add_listener(lineno, name, value)]
        body.extend(node.body)
        node.body = body

        return node

    def visit_Print(self, node):  # ONLY Python2
        self.field_visit(node.values)
        return node

    def visit_Return(self, node):
        self.field_visit(node.value)
        return node

    def visit_While(self, node):
        self.block_visit(node.body)

        lineno = node.lineno
        name = ast.Name(id='None', ctx=ast.Load())
        value = node.test

        body = [self.add_listener(lineno, name, value)]
        body.extend(node.body)
        node.body = body

        return node

    #
    # Expressions
    #

    def visit_Attribute(self, node):
        attr_obj = node
        name = attr_obj.attr
        while isinstance(attr_obj.value, ast.Attribute):  # nested attributes
            attr_obj = attr_obj.value
            name = '{0}.{1}'.format(attr_obj.attr, name)
        else:
            name = ast.Str(s='{0}.{1}'.format(attr_obj.value.id, name))

        lineno = node.lineno
        value = ast.Attribute(value=node.value,
                              attr=node.attr,
                              ctx=ast.Load(),
                              lineno=lineno,
                              col_offset=node.col_offset)

        self.stack.append(self.add_listener(lineno, name, value))

        return node

    def visit_Compare(self, node):
        lineno = node.lineno
        name = ast.Name(id='None', ctx=ast.Load())
        value = node

        self.stack.append(self.add_listener(lineno, name, value))

        return node

    def visit_Name(self, node):
        lineno = node.lineno
        name = ast.Str(s=node.id)
        value = ast.Name(id=node.id,
                         ctx=ast.Load(),
                         lineno=lineno,
                         col_offset=node.col_offset)

        self.stack.append(self.add_listener(lineno, name, value))

        return node

    @staticmethod
    def add_listener(lineno, var_name, val):
        """
        Add ... inside livesource listener context.

        Args:
            args - list of arguments for <func_name>,
            func_name - function name from livesource listener context

        Returns:
            ast.Expr object

        """
        # TODO: change data structure to omit multiple inline variable assignment
        # _livesource_listing[lineno].append(var_name, val, )
        return ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Subscript(
               value=ast.Name(id='_livesource_listing', ctx=ast.Load()),
               slice=ast.Index(value=ast.Num(n=lineno)), ctx=ast.Load()),
               attr='append', ctx=ast.Load()), args=[ast.Tuple(elts=[var_name,
               val,], ctx=ast.Load()),], keywords=[], starargs=None,
               kwargs=None), lineno=lineno+1, col_offset=-1)

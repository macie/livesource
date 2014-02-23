#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LiveSource.

"""
import ast


class LiveSource(object):
    """

    Attributes:
        code (str): Source code.
        max_deep (int): Number of cached values at one line.

    """
    def __init__(self, code, max_deep=10):
        self.code = code
        self.lst = LSTree(max_deep)

    def get_values(self):
        """
        Returns values for all lines in code.

        Returns:
            Mapping type object.

        """

        # FIXME: exceptions handling
        compiled_code = compile(self._parse(), '<livesource>', 'exec')
        exec(compiled_code, self.lst.globals, self.lst.locals)

        return self.lst.locals['__livesource_listing']

    def update(self, code):
        """
        Update source code.

        Args:
            code (str): New source code.

        """
        self.code = code

    def _parse(self):
        """
        Parse source code.

        Returns:
            ast tree object.

        """
        tree = ast.parse(self.code)
        self.lst.stack = []  # clear stack (needed?)
        parsed_tree = self.lst.visit(tree)
        ast.fix_missing_locations(parsed_tree)
        return parsed_tree


class LSTree(ast.NodeVisitor):
    """

    Attributes:
        globals (dict): Globals for LSTree.
        locals (dict): Locals for LSTree.
        stack (list): Stack used by tree visitors.

    """
    def __init__(self, max_deep=10):
        """
        __livesource_listing = collections.defaultdict(
            lambda: collections.deque(maxlen=max_deep))

        Args:
            max_deep (int): Number of cached values at one line.

        """
        # NOTE: __livesource_listing is definied inside locals to speedup
        #       name searching
        self.globals = {}
        self.locals = {
            '__livesource_listing': __import__('collections').defaultdict(
                lambda: __import__('collections').deque(maxlen=max_deep))}
        self.stack = []

    #
    #  Tree visitors
    #

    def field_visit(self, field):
        """
        Visit nodes in field.

        Args:
            Field (obj or list): ast node field.

        """
        if not isinstance(field, list):
            field = [field]
        self.generic_visit(ast.Expression(body=field))

    def block_visit(self, fields):
        """
        Visit nodes in fields.

        Returns:
            Sequence of fields sorted by line number.

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
        return ast.Expression(body=self.block_visit(node.body))

    def visit_Interactive(self, node):
        return ast.Interactive(body=self.block_visit(node.body))

    def visit_Module(self, node):
        return ast.Module(body=self.block_visit(node.body))

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
        Assigns watched variable with __livesource_listing.

        Args:
            lineno (int): Line number of watched variable in source code.
            var_name (str): Watched variable name.
            val (ast.expr): Value of watched variable.

        Returns:
            ast node.

        """
        # FIXME: change data structure to fix multiple inline variable assignment
        # __livesource_listing[lineno].append(var_name, val, )
        return ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Subscript(
               value=ast.Name(id='__livesource_listing', ctx=ast.Load()),
               slice=ast.Index(value=ast.Num(n=lineno)), ctx=ast.Load()),
               attr='append', ctx=ast.Load()), args=[ast.Tuple(elts=[var_name,
               val,], ctx=ast.Load()),], keywords=[], starargs=None,
               kwargs=None), lineno=lineno+1, col_offset=-1)

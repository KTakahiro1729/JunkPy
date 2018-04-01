import unittest
import ast
from JunkPyTools import *
from junkpy import *

# abstract test
class TestJunkTypeDirect(object):
    """This tests directly inputs the correct ast type to each junk type."""
    input_ast = None
    junktype = None
    expect = None
    def test_direct(self):
        if type(self.input_ast) != self.junktype.ast_type:
            raise TypeError("{0} is wrong ast type for {1}".format(
                type(self.input_ast),
                self.junktype))
        actual = self.junktype(self.input_ast).output
        self.assertEqual(actual, self.expect)


# real tests
class TestModuleDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = ast.parse("")
    junktype = JunkModule
    expect = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]][0]'
class TestExprDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = ast.parse('"b"').body[0]
    junktype = JunkExpr
    expect = 'if["b"]'
class TestAssignDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = ast.parse('a = 3').body[0]
    junktype = JunkAssign
    expect = 'if[ns.update({"a":3})]'
class TestDictDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = parse_terminal('{1:2,"a":2}')
    junktype = JunkDict
    expect = '{1:2,"a":2}'
class TestNumDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = parse_terminal('3')
    junktype = JunkNum
    expect = '3'
class TestNumDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = parse_terminal('[1,"s",3]')
    junktype = JunkList
    expect = '[1,"s",3]'

class TestStrDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = parse_terminal('"source"')
    junktype = JunkStr
    expect = '"source"'
class TestNameConstantDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = parse_terminal('True')
    junktype = JunkNameConstant
    expect = 'True'
class TestNameDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = ast.parse("a = 3").body[0].targets[0]
    junktype = JunkName
    expect = 'ns["a"]'
class TestIfDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = ast.parse("if True:\n\tprint(1)").body[0]
    junktype = JunkIf
    expect = 'if[[None for ns in[ns]if[ns["print"](1)]]if(True)else[None for ns in[ns]]]or True'
class TestIfDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = ast.parse("if True:\n\tprint(1)").body[0]
    junktype = JunkIf
    expect = 'if[[None for ns in[ns]if[ns["print"](1)]]if(True)else[None for ns in[ns]]]or True'
class TestForDirect(TestJunkTypeDirect, unittest.TestCase):
    input_ast = ast.parse("for i in [1,2,3]:\n\tprint(1)").body[0]
    junktype = JunkFor
    expect = 'if[None for r in [(_ for _ in  [1,2,3])]for li in r if not(ns.update({"i":li}))if[None for ns in[ns]if[ns["print"](1)]]]or True'
if __name__ == "__main__":
    unittest.main()

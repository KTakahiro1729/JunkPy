import unittest
import warnings
# import contextlib
# from string io import StringIO
import textwrap
import ast
from JunkPyTools import *
from junkpy import *


class TestJunkTypeEval(object):
    """this tests by evaluating the rubbish output"""
    source = None
    stdin = None    #TODO: Add stdin mock
    expect_code   = None
    expect_stdout = None #TODO: Add stdout mock
    expect_value  = None
    def test_eval(self):
        #test
        actual_code = JunkModule(self.source).output
        #warning
        if self.expect_code != None and actual_code != self.expect_code:
            warning_line = """\
                Code generated from '{0}' differs from expected
                expected : {1}
                generated: {2}
                """.format(self.__class__.__name__, self.expect_code, actual_code)
            warnings.warn(textwrap.dedent(warning_line))
        try:
            actual_value = eval(actual_code)
        except Exception as e:
            raise e
        self.assertEqual(self.expect_value, actual_value)
class TestEmptyEval(TestJunkTypeEval, unittest.TestCase):
    source = ''
    stdin = None
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]][0]'
    expect_stdout = None
    expect_value = None
class TestNumEval(TestJunkTypeEval, unittest.TestCase):
    source = '3'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[3]]][0]'
    expect_stdout = None
    expect_value = None
class TestStrEval(TestJunkTypeEval, unittest.TestCase):
    source = '"string"'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if["string"]]][0]'
    expect_stdout = None
    expect_value = None
class TestNameConstantEval(TestJunkTypeEval, unittest.TestCase):
    source = 'True'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[True]]][0]'
    expect_stdout = None
    expect_value = None
class TestAssignEval(TestJunkTypeEval, unittest.TestCase):
    source = 'a = 3'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":3})]]][0]'
    expect_stdout = None
    expect_value = None
class TestExpr2Eval(TestJunkTypeEval, unittest.TestCase):
    source = '2\n3'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[2]]if[3]]][0]'
    expect_stdout = None
    expect_value = None
class TestExpr5Eval(TestJunkTypeEval, unittest.TestCase):
    source = '2\n3\n\"ab\"\n3\n1'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[2]]if[3]]if["ab"]]if[3]]if[1]]][0]'
    expect_stdout = None
    expect_value = None
class TestCallEval(TestJunkTypeEval, unittest.TestCase):
    source = 'print(2)'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns["print"](2)]]][0]'
    expect_stdout = 2
    expect_value = None
class TestAddEval(TestJunkTypeEval, unittest.TestCase):
    source = 'a=2\nb=a+1'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":2})]]if[ns.update({"b":ns["a"]+1})]]][0]'
    expect_stdout = None
    expect_value = None
class TestFirstGoalEval(TestJunkTypeEval, unittest.TestCase):
    source = 'a = 7\nb = 2\na = 3\nc = a + b\nprint(c)'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":7})]]if[ns.update({"b":2})]]if[ns.update({"a":3})]]if[ns.update({"c":ns["a"]+ns["b"]})]]if[ns["print"](ns["c"])]]][0]'
    expect_stdout = None
    expect_value = None
class TestIfEval(TestJunkTypeEval, unittest.TestCase):
    source = 'a = False\nif a:\n    print(1)\n    print(2)\nelse:\n    print(2)\n'
    stdin = None
    expect_code = '[None for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":False})]]if[[None for ns in[ns for ns in[ns for ns in[ns]if[ns["print"](1)]]if[ns["print"](2)]]][0]if(ns["a"])else[None for ns in[ns for ns in[ns]if[ns["print"](2)]]][0]]]][0]'
    expect_stdout = None
    expect_value = None



if __name__ == "__main__":
    unittest.main()

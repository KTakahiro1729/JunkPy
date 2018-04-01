import unittest
import warnings
from contextlib import _RedirectStream, redirect_stdout
from io import StringIO
import textwrap
import ast
from JunkPyTools import *
from junkpy import *

class redirect_stdin(_RedirectStream):
    _stream = "stdin"
class TestJunkTypeExec(object):
    """this tests by executing the rubbish output"""
    source = None
    actual_stdin = ''
    expect_code   = None
    expect_stdout = ''
    expect_value  = None
    def execute_stdio(self, code):
        stdin = StringIO()
        stdin.write(self.actual_stdin)
        stdin.seek(0)
        stdout = StringIO()
        try:
            with redirect_stdin(stdin), redirect_stdout(stdout):
                value = exec(code)
        except Exception as e:
            raise e
        stdout = stdout.getvalue()
        return stdout.split('\n'), value
    def test_exec(self):
        self.expect_stdout = self.expect_stdout.split("\n")
        #exec Normal Code
        if self.expect_code != None:
            self.normal_stdout, self.normal_value = self.execute_stdio(self.source)
            if self.normal_stdout != self.expect_stdout:
                warning_line = """\
                    Expected code: {3}
                    gives different stdout at '{0}'
                    expected : {1}
                    generated: {2}
                    """.format(
                        self.__class__.__name__,
                        self.expect_stdout,
                        self.normal_stdout,
                        self.expect_code)
                warnings.warn(textwrap.dedent(warning_line))
        #convert
        self.actual_code = JunkModule(self.source).output
        #warning
        if self.expect_code != None and self.actual_code != self.expect_code:
            warning_line = """\
                Code generated from '{0}' differs from expected
                expected : {1}
                generated: {2}
                """.format(self.__class__.__name__, self.expect_code, self.actual_code)
            warnings.warn(textwrap.dedent(warning_line))
        #exec Junk Code
        self.actual_stdout, self.actual_value = self.execute_stdio(self.actual_code)
        self.assertEqual(
        (self.actual_stdout, self.actual_value),
        (self.expect_stdout, self.expect_value))
class TestEmptyExec(TestJunkTypeExec, unittest.TestCase):
    source = ''
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]][0]'
    expect_stdout = ''
    expect_value = None
class TestNumExec(TestJunkTypeExec, unittest.TestCase):
    source = '3'
    user_input = ""
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[3]][0]'
    expect_stdout = ''
    expect_value = None
class TestStrExec(TestJunkTypeExec, unittest.TestCase):
    source = '"string"'
    user_input = ""
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if["string"]][0]'
    expect_stdout = ''
    expect_value = None
class TestNameConstantExec(TestJunkTypeExec, unittest.TestCase):
    source = 'True'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[True]][0]'
    expect_stdout = ''
    expect_value = None
class TestAssignExec(TestJunkTypeExec, unittest.TestCase):
    source = 'a = 3'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":3})]][0]'
    expect_stdout = ''
    expect_value = None
class TestExpr2Exec(TestJunkTypeExec, unittest.TestCase):
    source = '2\n3'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[2]if[3]][0]'
    expect_stdout = ''
    expect_value = None
class TestExpr5Exec(TestJunkTypeExec, unittest.TestCase):
    source = '2\n3\n\"ab\"\n3\n1'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[2]if[3]if["ab"]if[3]if[1]][0]'
    expect_stdout = ''
    expect_value = None
class TestCallExec(TestJunkTypeExec, unittest.TestCase):
    source = 'print(2)'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns["print"](2)]][0]'
    expect_stdout = '2\n'
    expect_value = None
class TestAddExec(TestJunkTypeExec, unittest.TestCase):
    source = 'a=2\nb=a+1'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":2})]if[ns.update({"b":ns["a"]+1})]][0]'
    expect_stdout = ''
    expect_value = None
class TestFirstGoalExec(TestJunkTypeExec, unittest.TestCase):
    source = 'a = 7\nb = 2\na = 3\nc = a + b\nprint(c)'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":7})]if[ns.update({"b":2})]if[ns.update({"a":3})]if[ns.update({"c":ns["a"]+ns["b"]})]if[ns["print"](ns["c"])]][0]'
    expect_stdout = '5\n'
    expect_value = None
class TestIfExec(TestJunkTypeExec, unittest.TestCase):
    source = 'a = False\nif a:\n    print(1)\n    print(2)\nelse:\n    print(2)\n'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":False})]if[[None for ns in[ns]if[ns["print"](1)]if[ns["print"](2)]]if(ns["a"])else[None for ns in[ns]if[ns["print"](2)]]]or True][0]'
    expect_stdout = '2\n'
    expect_value = None
class TestListExec(TestJunkTypeExec, unittest.TestCase):
    source = '[1,"s",3]'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[[1,"s",3]]][0]'
    expect_stdout = ''
    expect_value = None
class TestForExec(TestJunkTypeExec, unittest.TestCase):
    source = 'print(2)\nfor i in range(3):\n\tprint(1,i)'
    actual_stdin = ''
    expect_code = '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns["print"](1)]if[None for r in [(_ for _ in  ns["range"](3))]for li in r if not(ns.update({"i":li}))if[None for ns in[ns]if[ns["print"](1,ns["i"])]]]or True][0]'
    expect_stdout = '1\n1 0\n1 1\n1 2\n'
    expect_value = None

if __name__ == "__main__":
    unittest.main()

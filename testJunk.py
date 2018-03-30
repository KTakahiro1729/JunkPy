from JunkPyTools import *
from junkpy import *
def create_test_list():
    return [
        ("Module",JunkModule(ast.parse("")).output, '[None for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]][0]', True),
        ("Expr",JunkExpr(ast.parse("'b'").body[0]).output,"for ns in[ns if[\"b\"]]",False),
        ("Assign",JunkAssign(ast.parse("a = 3").body[0]).output, "for ns in[ns if[ns.update({\"a\":3})]]",False),
        ("Dict",JunkDict(parse_terminal("{1:2,\"a\":2}")).output, "{1:2,\"a\":2}",False),
        ("Num",JunkNum(parse_terminal("3")).output, '3',False),
        ("Str",JunkStr(parse_terminal("'source'")).output, "\"source\"",False),
        ("True",JunkNameConstant(parse_terminal("True")).output, 'True', False),
        ("Name",JunkName(ast.parse("a = 3").body[0].targets[0]).output, "ns[\"a\"]",False),
        ("ModuleNum",JunkModule("2").output, '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[2]]][0]', True),
        ("ModuleStr",JunkModule("\"2\"").output, '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if["2"]]][0]', True),
        ("ModuleTrue",JunkModule("True").output, '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[True]]][0]', True),
        ("ModuleAssign",JunkModule("a = 1").output, '[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":1})]]][0]', True),
        ("Expr2", JunkModule("2\n3").output, '[None for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[2]]if[3]]][0]', True),
        ("Expr5", JunkModule("2\n3\n\"ab\"\n3\n1").output,
            '[None for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[2]]if[3]]if["ab"]]if[3]]if[1]]][0]', True),
        ("Call",JunkModule("abs(2)").output,'[None for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns["abs"](2)]]][0]', True),
        ("Add",JunkModule("a=2\nb=a+1").output,'[None for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":2})]]if[ns.update({"b":ns["a"]+1})]]][0]',True),
        ("FirstGoal",JunkModule("a = 7\nb = 2\na = 3\nc = a + b\nabs(c)").output, '[None for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":7})]]if[ns.update({"b":2})]]if[ns.update({"a":3})]]if[ns.update({"c":ns["a"]+ns["b"]})]]if[ns["abs"](ns["c"])]]][0]', True),
    #    ("Call",JunkModule("abs(2,end=\"\\n\")").output,  "[None for ns in[ns for ns in[dict()]if[abs(2,end=\"\n\")]]][0]"),
    ]

def run():
    test_list = create_test_list()
    for test in test_list:
        if not parse_test(*test):
            break
    else:
        print("all correct")

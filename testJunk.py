from JunkPyTools import *
from junkpy import *
def create_test_list():
    return [
        ("Module",JunkModule(ast.parse("")).output, '[None for ns in[globals()["__builtins__"]if(type(globals()["__builtins__"]) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(globals()["__builtins__"])}]][0]'),
        ("Expr",JunkExpr(ast.parse("'b'").body[0]).output,"for ns in[ns if[\"b\"]]"),
        ("Assign",JunkAssign(ast.parse("a = 3").body[0]).output, "for ns in[ns if[ns.update({\"a\":3})]]"),
        ("Dict",JunkDict(parse_terminal("{1:2,\"a\":2}")).output, "{1:2,\"a\":2}"),
        ("Num",JunkNum(parse_terminal("3")).output, '3'),
        ("Str",JunkStr(parse_terminal("'source'")).output, "\"source\""),
        ("Name",JunkName(ast.parse("a = 3").body[0].targets[0]).output, "ns[\"a\"]"),
        ("ModuleNum",JunkModule("2").output, '[None for ns in[ns for ns in[globals()["__builtins__"]if(type(globals()["__builtins__"]) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(globals()["__builtins__"])}]if[2]]][0]'),
        ("ModuleStr",JunkModule("\"2\"").output, '[None for ns in[ns for ns in[globals()["__builtins__"]if(type(globals()["__builtins__"]) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(globals()["__builtins__"])}]if["2"]]][0]'),
        ("ModuleAssign",JunkModule("a = 1").output, '[None for ns in[ns for ns in[globals()["__builtins__"]if(type(globals()["__builtins__"]) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(globals()["__builtins__"])}]if[ns.update({"a":1})]]][0]'),
        ("Expr2", JunkModule("2\n3").output, '[None for ns in[ns for ns in[ns for ns in[globals()["__builtins__"]if(type(globals()["__builtins__"]) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(globals()["__builtins__"])}]if[2]]if[3]]][0]'),
        ("Expr5", JunkModule("2\n3\n\"ab\"\n3\n1").output,
            '[None for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[globals()["__builtins__"]if(type(globals()["__builtins__"]) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(globals()["__builtins__"])}]if[2]]if[3]]if["ab"]]if[3]]if[1]]][0]'),
        ("AssignEval",eval(JunkModule("\n3\na=2\nb=3",save_ns = True).output)["a"],2),
        ("AssignEval",eval(JunkModule("\n3\na=2\nb=3",save_ns = True).output)["b"],3),
        ("Call",JunkModule("print(2)").output,'[None for ns in[ns for ns in[globals()["__builtins__"]if(type(globals()["__builtins__"]) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(globals()["__builtins__"])}]if[ns["print"](2)]]][0]'),
        ("Add",JunkModule("a=2\nb=a+1").output,'[None for ns in[ns for ns in[ns for ns in[globals()["__builtins__"]if(type(globals()["__builtins__"]) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(globals()["__builtins__"])}]if[ns.update({"a":2})]]if[ns.update({"b":ns["a"]+1})]]][0]'),
        ("FirstGoal",eval(JunkModule("a = 7\nb = 2\na = 3\nc = a + b\nprint(c)").output),None)
    #    ("Call",JunkModule("print(2,end=\"\\n\")").output,
    #        "[None for ns in[ns for ns in[dict()]if[print(2,end=\"\n\")]]][0]"),
    ]

def run():
    test_list = create_test_list()
    for test in test_list:
        if not parse_test(*test):
            break
    else:
        print("all correct")

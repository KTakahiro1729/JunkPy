#main
import ast
import copy
from collections import namedtuple
import builtins

ChildArg = namedtuple("ChildArg", "nodetype number")

class JunkStruct():
    def __init__(self, head = "", neck = "", shoulder = "", trunk = "", foot = ""):
        self.head = head
        self.neck = neck
        self.shoulder = shoulder
        self.trunk = trunk
        self.foot = foot
        self.order = ["head", "neck", "shoulder", "trunk", "foot"]

    def join(self, connector = ""):
        return connector.join([getattr(self, attr) for attr in self.order])
    def __add__(self, other):
        return JunkStruct(*[getattr(self, attr) + getattr(other, attr) for attr in self.order])

class JunkType():
    @property
    def ast_type(self):
        return ast.AST
    @property
    def child_nodetype(self):
        return dict([])
    def __init__(self, node, struct = None, connector = "", indent = ""):
        if type(node) == str:
            node = ast.parse(node)
        if struct == None:
            struct = JunkStruct()
        self.node = node
        self.struct = copy.deepcopy(struct)
        self.connector = connector
        self.indent = indent
        self.check_ast_type()
        self.junkchild_dict = self.create_junkchild_dict()
        self.deploy_child()
        self.output = self.struct.join(connector)
    def check_ast_type(self):
        if type(self.node) != self.ast_type:
            raise Exception("Wrong Type\nWant : {0}\nNot  : {1}".format(self.ast_type, type(self.node)))
    def create_junkchild_dict(self):
        result = dict([])
        for child_name in self.node._fields:
            field = getattr(self.node, child_name)
            node = self.child_nodetype[child_name]
            if  node.number in ["", "?"]:
                child_node = field
                junktype = self.judge_junktype(child_node, candidate = node.nodetype)
                result[child_name] = junktype(node = child_node, connector = self.connector)
            elif node.number == "*":
                result[child_name] = []
                for child_node in field:
                    junktype = self.judge_junktype(child_node, candidate = node.nodetype)
                    result[child_name].append(junktype(node = child_node, connector = self.connector))
        return result
    def judge_junktype(self, child, candidate):
        ast_type = type(child)
        builtin_types = [getattr(builtins, attr) for attr in dir(builtins)]
        if ast_type in builtin_types:
            return JunkTerminal
        for junktype in candidate:
            if ast_type == junktype.ast_type:
                return junktype
        else:
            raise Exception("{0} not in candidate : {1}".format(type(child),candidate))
    def deploy_child(self):
        pass
    # def make_block(self, exprs):
    #
    #     block_struct = JunkStruct(
    #         head = "[None ",
    #         shoulder = self.connector + self.indent + "for ns in[ns]",
    #         foot="]")
    #     for child in ast.iter_child_nodes(self.node):
    #         block_struct += self.make_junktype(child, self.connector).struct
    #     return block_struct

#terminal
class JunkTerminal():
    def __init__(self, *args, **kwargs):
        pass

#mod
class JunkModule(JunkType):
    ast_type = ast.Module
    @property
    def child_nodetype(self):
        return {"body": ChildArg(stmt, "*")}
    def __init__(self, *args,save_ns = False, **kwargs):
        self.save_ns = save_ns
        super().__init__(*args, **kwargs)
    def deploy_child(self):
        self.struct.head     += "[ns " if self.save_ns else "[None "
        ns_init = "".join([
            "__builtins__ ",
            "if(type(__builtins__) is dict)else",
            "{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}"
        ])
        self.struct.shoulder += "for ns in[{0}]".format(ns_init)
        self.struct.foot     += "][0]"
        for body in self.junkchild_dict["body"]:
            self.struct += body.struct

#stmt
class JunkExpr(JunkType):
    ast_type = ast.Expr
    @property
    def child_nodetype(self):
        return {"value": ChildArg(expr, "")}
    def deploy_child(self):
        self.struct +=  self.junkchild_dict["value"].struct
        self.struct.neck += "for ns in[ns "
        self.struct.trunk = "if[" + self.struct.trunk + "]]" + self.connector

class JunkAssign(JunkType):
    ast_type = ast.Assign
    @property
    def child_nodetype(self):
        return {"targets": ChildArg(expr, "*"), "value": ChildArg(expr, "")}
    def deploy_child(self):
        self.struct.neck = "for ns in[ns "
        key_in_ns = self.junkchild_dict["targets"][0].struct.trunk
        key = key_in_ns[len("ns[\""):len(key_in_ns) - len("\"]")]
        self.struct.trunk = "if[ns.update({{\"{0}\":{1}}})]]{2}".format(
                key,
                self.junkchild_dict["value"].struct.trunk,
                self.connector,)

# class JunkIf(JunkType):
#     ast_type = ast.If
#     @property
#     def child_nodetype(self):
#         return {"test": ChildArg(expr, ""),
#                    "args": ChildArg(operator, "*"),
#                    "orelse": ChildArg(expr, "")}
#     def deploy_child(self):
#         test = self.junkchild_dict["test"]
#         body_block =  self.make_block(self.node.body)
#         orelse_block =  self.make_block(self.node.orelse)
#         self.struct.trunk = "".join([
#         body_block.join(),
#         "if({0})".format(test.struct.join()),
#         orelse_block.join(),
#         ])

#expr
class JunkBinOp(JunkType):
    ast_type = ast.BinOp
    @property
    def child_nodetype(self):
        return {"left": ChildArg(expr, ""),
                   "op": ChildArg(operator, ""),
                   "right": ChildArg(expr, "")}
    def deploy_child(self):
        self.struct.trunk = "{0}{1}{2}".format(
                self.junkchild_dict["left"].struct.trunk,
                self.junkchild_dict["op"].struct.trunk,
                self.junkchild_dict["right"].struct.trunk,)

class JunkDict(JunkType):
    ast_type = ast.Dict
    @property
    def child_nodetype(self):
        return {"keys": ChildArg(expr, "*"),
                   "values": ChildArg(expr, "*")}
    def deploy_child(self):
        zipped = zip(self.junkchild_dict["keys"], self.junkchild_dict["values"])
        self.struct.trunk += "{" + ",".join([k.output + ":" + v.output for k,v in zipped]) + "}"

class JunkCall(JunkType):
    ast_type = ast.Call
    @property
    def child_nodetype(self):
        return {"func": ChildArg(expr, ""),
                   "args": ChildArg(expr, "*"),
                   "keywords": ChildArg(expr, "*")}
    def deploy_child(self):
        args_str = ",".join([arg.struct.trunk for arg in self.junkchild_dict["args"]])
        self.struct.trunk = "{0}({1})".format(
                self.junkchild_dict["func"].struct.trunk,
                args_str,
                self.connector,)

class JunkNum(JunkType):
    ast_type = ast.Num
    @property
    def child_nodetype(self):
        return {"n": ChildArg(JunkTerminal, "")}
    def deploy_child(self):
        self.struct.trunk += str(self.node.n)

class JunkStr(JunkType):
    ast_type = ast.Str
    @property
    def child_nodetype(self):
        return {"s": ChildArg(JunkTerminal, "")}
    def deploy_child(self):
        self.struct.trunk += "\"" + self.node.s + "\""

class JunkNameConstant(JunkType):
    ast_type = ast.NameConstant
    @property
    def child_nodetype(self):
        return {"value": ChildArg(JunkTerminal, "")}
    def deploy_child(self):
        self.struct.trunk = str(self.node.value)


class JunkName(JunkType):
    ast_type = ast.Name
    @property
    def child_nodetype(self):
        return {"id": ChildArg(JunkTerminal, ""), "ctx":ChildArg(expr_context, "")}
    def deploy_child(self):
        self.struct.trunk = "ns[\"{0}\"]".format(self.node.id)

#expr_context
class JunkLoad(JunkType):
    ast_type = ast.Load
    def deploy_child(self):
        pass

class JunkStore(JunkType):
    ast_type = ast.Store
    def deploy_child(self):
        pass

class JunkAdd(JunkType):
    ast_type = ast.Add
    def deploy_child(self):
        self.struct.trunk = "+"

mod = [JunkModule]
stmt = [JunkExpr, JunkAssign]
expr = [JunkBinOp, JunkDict, JunkCall, JunkNum, JunkStr, JunkNameConstant, JunkName]
expr_context = [JunkLoad, JunkStore]
operator = [JunkAdd]

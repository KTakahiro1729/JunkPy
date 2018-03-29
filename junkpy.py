#main
import ast
import copy
from collections import namedtuple

Node = namedtuple("Node", "nodetype number")

#terminal
class identifier():
    pass
class string():
    pass
class singleton():
    pass
class constant():
    pass

class JunkStruct():
    def __init__(self, head = "", neck = "", shoulder = "", body = "", foot = ""):
        self.head = head
        self.neck = neck
        self.shoulder = shoulder
        self.body = body
        self.foot = foot
        self.order = ["head", "neck", "shoulder", "body", "foot"]

    def join(self, connector = ""):
        return connector.join([getattr(self, attr) for attr in self.order])
    def __add__(self, other):
        return JunkStruct(*[getattr(self, attr) + getattr(other, attr) for attr in self.order])

class JunkType():
    @property
    def node_type(self):
        return ast.AST
    @property
    def childnode_type(self):
        return dict([])
    def check_node_type(self):
        if type(self.node) != self.node_type:
            raise Exception("Wrong Type\nWant : {0}\nNot  : {1}".format(self.node_type, type(self.node)))
    def __init__(self, node, struct = None, connector = "", indent = ""):
        if struct == None:
            struct = JunkStruct()
        if type(node) == str:
            node = ast.parse(node)
        self.node = node
        self.check_node_type()
        self.struct = copy.deepcopy(struct)
        self.connector = connector
        self.indent = indent
        self.childnodes = self.parse_childnode()
        self.walk_child()
        self.output = self.struct.join(connector)
    def walk_child(self):
        pass
    def make_junk(self, child, lower_node = None):
        for junktype in lower_node:
            if type(child) == junktype.node_type:
                return junktype(node = child, connector = self.connector)
        else:
            raise Exception("{0} not in candidate : {1}".format(type(child),candidate))
    def parse_childnode(self):
        pass
    def make_block(self, exprs):

        block_struct = JunkStruct(
            head = "[None ",
            shoulder = self.connector + self.indent + "for ns in[ns]",
            foot="]")
        for child in ast.iter_child_nodes(self.node):
            block_struct += self.make_junk(child, self.connector).struct
        return block_struct
#mod
class JunkModule(JunkType):
    node_type = ast.Module
    @property
    def childnode_type(self):
        return {"body": Node(stmt, "*")}
    def __init__(self, *args,save_ns = False, **kwargs):
        self.save_ns = save_ns
        super().__init__(*args, **kwargs)
    def walk_child(self):
        self.struct.head     += "[ns " if self.save_ns else "[None "
        ns_init = "".join([
            "__builtins__ ",
            "if(type(__builtins__) is dict)else",
            "{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}"
        ])
        self.struct.shoulder += "for ns in[{0}]".format(ns_init)
        self.struct.foot     += "][0]"
        for child in ast.iter_child_nodes(self.node):
            self.struct += self.make_junk(
                child,
                lower_node = stmt
            ).struct

#stmt
class JunkExpr(JunkType):
    node_type = ast.Expr
    @property
    def childnode_type(self):
        return {"value": Node(expr, "")}
    def walk_child(self):
        value = self.make_junk(self.node.value, expr)
        self.struct +=  value.struct
        self.struct.neck += "for ns in[ns "
        self.struct.body = "if[" + self.struct.body + "]]" + self.connector

class JunkAssign(JunkType):
    node_type = ast.Assign
    @property
    def childnode_type(self):
        return {"targets": Node(expr, "*"), "value": Node(expr, "")}
    def walk_child(self):
        targets = [self.make_junk(target,expr) for target in self.node.targets]
        value = self.make_junk(self.node.value, expr)
        self.struct.neck = "for ns in[ns "
        key_in_ns = targets[0].struct.body
        key = key_in_ns[len("ns[\""):len(key_in_ns) - len("\"]")]
        self.struct.body = "if[ns.update({{\"{0}\":{1}}})]]{2}".format(
                key,
                value.struct.body,
                self.connector,)

class JunkIf(JunkType):
    node_type = ast.If
    @property
    def childnode_type(self):
        return {"test": Node(expr, ""),
                   "args": Node(operator, "*"),
                   "orelse": Node(expr, "")}
    def walk_child(self):
        test = self.make_junk(self.
            node.test,
            lower_node = expr)
        body_block =  self.make_block(self.node.body)
        orelse_block =  self.make_block(self.node.orelse)
        self.struct.body = "".join([
        body_block.join(),
        "if({0})".format(test.struct.join()),
        orelse_block.join(),
        ])

#expr
class JunkBinOp(JunkType):
    node_type = ast.BinOp
    @property
    def childnode_type(self):
        return {"left": Node(expr, ""),
                   "op": Node(operator, ""),
                   "right": Node(expr, "")}
    def walk_child(self):
        left = self.make_junk(self.node.left, expr)
        op = self.make_junk(self.node.op, operator)
        right =self.make_junk(self.node.right, expr)
        self.struct.body = "{0}{1}{2}".format(
                left.struct.body,
                op.struct.body,
                right.struct.body,)

class JunkDict(JunkType):
    node_type = ast.Dict
    @property
    def childnode_type(self):
        return {"keyes": Node(expr, "*"),
                   "values": Node(expr, "*")}
    def walk_child(self):
        keys = [self.make_junk(k, expr) for k in self.node.keys]
        values = [self.make_junk(v, expr) for v in self.node.values]
        zipped = zip(keys, values)
        self.struct.body += "{" + ",".join([k.output + ":" + v.output for k,v in zipped]) + "}"

class JunkCall(JunkType):
    node_type = ast.Call
    @property
    def childnode_type(self):
        return {"func": Node(expr, ""),
                   "args": Node(expr, "*"),
                   "keyword": Node(expr, "*")}
    def walk_child(self):
        func = self.make_junk(self.node.func, expr)
        args = [self.make_junk(arg, expr) for arg in self.node.args]
        args_str = ",".join([arg.struct.body for arg in args])
        self.struct.body = "{0}({1})".format(
                func.struct.body,
                args_str,
                self.connector,)

class JunkNum(JunkType):
    node_type = ast.Num
    @property
    def childnode_type(self):
        return {"n": Node(object, "")}
    def walk_child(self):
        self.struct.body += str(self.node.n)

class JunkStr(JunkType):
    node_type = ast.Str
    @property
    def childnode_type(self):
        return {"s": Node(object, "")}
    def walk_child(self):
        self.struct.body += "\"" + self.node.s + "\""

class JunkNameConstant(JunkType):
    node_type = ast.NameConstant
    @property
    def childnode_type(self):
        return {"value": Node(singleton, "")}
    def walk_child(self):
        self.struct.body = str(self.node.value)


class JunkName(JunkType):
    node_type = ast.Name
    @property
    def childnode_type(self):
        return {"id": Node(idnetifier, ""), "ctx":Node(expr_context, "")}
    def walk_child(self):
        self.struct.body = "ns[\"{0}\"]".format(self.node.id)

#expr_context
class JunkLoad(JunkType):
    node_type = ast.Load
    def walk_child(self):
        pass

class JunkStore(JunkType):
    node_type = ast.Store
    def walk_child(self):
        pass

class JunkAdd(JunkType):
    node_type = ast.Add
    def walk_child(self):
        self.struct.body = "+"

terminal = [identifier, int, string, bytes, object, singleton, constant]
mod = [JunkModule]
stmt = [JunkExpr, JunkAssign, JunkIf]
expr = [JunkBinOp, JunkDict, JunkCall, JunkNum, JunkStr, JunkNameConstant, JunkName]
expr_context = [JunkLoad, JunkStore]
operator = [JunkAdd]

#main
import ast
import copy
from collections import namedtuple
import builtins

Node = namedtuple("Node", "nodetype number")

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
    def child_nodetype(self):
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
        self.deploy_child()
        self.output = self.struct.join(connector)
    def deploy_child(self):
        pass
    def make_junk(self, child, lower_node = None):
        ast_type = type(child)
        builtin_types = [getattr(builtins, attr) for attr in dir(builtins)]
        if ast_type in builtin_types:
            return JunkTerminal()
        for junktype in lower_node:
            if ast_type == junktype.node_type:
                return junktype(node = child, connector = self.connector)
        else:
            raise Exception("{0} not in candidate : {1}".format(type(child),lower_node))
    def parse_childnode(self):
        result = dict([])
        for child_name in self.node._fields:
            field = getattr(self.node, child_name)
            node = self.child_nodetype[child_name]
            if  node.number in ["", "?"]:
                result[child_name] = self.make_junk(field, lower_node = node.nodetype)
            elif node.number == "*":
                result[child_name] = \
                    [self.make_junk(one_node, lower_node = node.nodetype).struct
                        for one_node in field]
        return result
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
    def child_nodetype(self):
        return {"body": Node(stmt, "*")}
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
        for child in ast.iter_child_nodes(self.node):
            self.struct += self.make_junk(
                child,
                lower_node = stmt
            ).struct

#terminal
class JunkTerminal():
    pass

#stmt
class JunkExpr(JunkType):
    node_type = ast.Expr
    @property
    def child_nodetype(self):
        return {"value": Node(expr, "")}
    def deploy_child(self):
        value = self.make_junk(self.node.value, expr)
        self.struct +=  value.struct
        self.struct.neck += "for ns in[ns "
        self.struct.body = "if[" + self.struct.body + "]]" + self.connector

class JunkAssign(JunkType):
    node_type = ast.Assign
    @property
    def child_nodetype(self):
        return {"targets": Node(expr, "*"), "value": Node(expr, "")}
    def deploy_child(self):
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
    def child_nodetype(self):
        return {"test": Node(expr, ""),
                   "args": Node(operator, "*"),
                   "orelse": Node(expr, "")}
    def deploy_child(self):
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
    def child_nodetype(self):
        return {"left": Node(expr, ""),
                   "op": Node(operator, ""),
                   "right": Node(expr, "")}
    def deploy_child(self):
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
    def child_nodetype(self):
        return {"keys": Node(expr, "*"),
                   "values": Node(expr, "*")}
    def deploy_child(self):
        keys = [self.make_junk(k, expr) for k in self.node.keys]
        values = [self.make_junk(v, expr) for v in self.node.values]
        zipped = zip(keys, values)
        self.struct.body += "{" + ",".join([k.output + ":" + v.output for k,v in zipped]) + "}"

class JunkCall(JunkType):
    node_type = ast.Call
    @property
    def child_nodetype(self):
        return {"func": Node(expr, ""),
                   "args": Node(expr, "*"),
                   "keywords": Node(expr, "*")}
    def deploy_child(self):
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
    def child_nodetype(self):
        return {"n": Node(JunkTerminal, "")}
    def deploy_child(self):
        self.struct.body += str(self.node.n)

class JunkStr(JunkType):
    node_type = ast.Str
    @property
    def child_nodetype(self):
        return {"s": Node(JunkTerminal, "")}
    def deploy_child(self):
        self.struct.body += "\"" + self.node.s + "\""

class JunkNameConstant(JunkType):
    node_type = ast.NameConstant
    @property
    def child_nodetype(self):
        return {"value": Node(JunkTerminal, "")}
    def deploy_child(self):
        self.struct.body = str(self.node.value)


class JunkName(JunkType):
    node_type = ast.Name
    @property
    def child_nodetype(self):
        return {"id": Node(JunkTerminal, ""), "ctx":Node(expr_context, "")}
    def deploy_child(self):
        self.struct.body = "ns[\"{0}\"]".format(self.node.id)

#expr_context
class JunkLoad(JunkType):
    node_type = ast.Load
    def deploy_child(self):
        pass

class JunkStore(JunkType):
    node_type = ast.Store
    def deploy_child(self):
        pass

class JunkAdd(JunkType):
    node_type = ast.Add
    def deploy_child(self):
        self.struct.body = "+"

mod = [JunkModule]
stmt = [JunkExpr, JunkAssign, JunkIf]
expr = [JunkBinOp, JunkDict, JunkCall, JunkNum, JunkStr, JunkNameConstant, JunkName]
expr_context = [JunkLoad, JunkStore]
operator = [JunkAdd]

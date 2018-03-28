#main
import ast
import copy
from collections import namedtuple
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
        return None
    @property
    def lower_node(self):
        return []

    def check_node_type(self):
        if type(self.node) != self.node_type:
            raise Exception("Wrong Type\nWant : {0}\nNot  : {1}".format(self.node_type, type(self.node)))
    def __init__(self, node, struct = None, connector = ""):
        if struct == None:
            struct = JunkStruct()
        if type(node) == str:
            node = ast.parse(node)
        self.node = node
        self.check_node_type()
        self.struct = copy.deepcopy(struct)
        self.connector = connector
        self.walk_child()
        self.output = self.struct.join(connector)
    def walk_child(self):
        pass

    def make_junk(self, child, connector=""):
        candidate = self.lower_node
        for junktype in candidate:
            if type(child) == junktype.node_type:
                return junktype(node = child, connector = connector)
        else:
            raise Exception("{0} is Unknown Type".format(type(child)))

#mod
class JunkModule(JunkType):
    node_type = ast.Module
    @property
    def lower_node(self):
        return stmt
    def __init__(self, *args,save_ns = False, **kwargs):
        self.save_ns = save_ns
        super().__init__(*args, **kwargs)
    def walk_child(self):
        self.struct.head     += "[ns " if self.save_ns else "[None "
        self.struct.shoulder += "for ns in[dict()]"
        self.struct.foot     += "][0]"
        for child in ast.iter_child_nodes(self.node):
            self.struct += self.make_junk(child, self.connector).struct


#stmt
class JunkExpr(JunkType):
    node_type = ast.Expr

    @property
    def lower_node(self):
        return expr
    def walk_child(self):
        child = self.node.value
        self.struct +=  self.make_junk(child, self.connector).struct
        self.struct.neck += "for ns in[ns "
        self.struct.body = "if[" + self.struct.body + "]]" + self.connector

class JunkAssign(JunkType):
    node_type = ast.Assign

    @property
    def lower_node(self):
        return expr
    def walk_child(self):
        target = self.node.targets[0]
        value = self.node.value
        body_target = self.make_junk(target).struct.body
        body_value = self.make_junk(value).struct.body
        self.struct.neck = "for ns in[ns "
        self.struct.body = "if[ns.update({\"" + body_target + "\":" + body_value + "})]]" + self.connector
        value = self.node.value

#expr
class JunkDict(JunkType):
    node_type = ast.Dict
    @property
    def lower_node(self):
        return expr
    def walk_child(self):
        keys = [self.make_junk(k, self.connector) for k in self.node.keys]
        values = [self.make_junk(v, self.connector) for v in self.node.values]
        zipped = zip(keys, values)
        self.struct.body += "{" + ",".join([k.output + ":" + v.output for k,v in zipped]) + "}"

class JunkCall(JunkType):
    node_type = ast.Call
    def walk_child(self):
        pass

class JunkNum(JunkType):
    node_type = ast.Num
    def walk_child(self):
        self.struct.body += str(self.node.n)

class JunkStr(JunkType):
    node_type = ast.Str
    def walk_child(self):
        self.struct.body += "\"" + self.node.s + "\""

class JunkName(JunkType):
    node_type = ast.Name
    def walk_child(self):
        self.struct.body = self.node.id

#expr_context
class JunkLoad(JunkType):
    node_type = ast.Load
    def walk_child(self):
        pass

class JunkStore(JunkType):
    node_type = ast.Store
    def walk_child(self):
        pass

mod = [JunkModule]
stmt = [JunkExpr, JunkAssign]
expr = [JunkDict, JunkCall, JunkNum, JunkStr, JunkName]
expr_context = [JunkLoad, JunkStore]

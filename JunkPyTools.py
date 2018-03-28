import ast

def walk(node, indent=0, indent_size = 4):
    if type(node) == str:
        node = ast.parse(node)
    # 入れ子構造をインデントで表現する
    print(' ' * indent, end='')

    # クラス名を表示する
    print(node.__class__, end=':')

    '''# 行数の情報があれば表示する
    if hasattr(node, 'lineno'):
        msg = ': {lineno}'.format(lineno=node.lineno)
        print(msg, end='')
    '''
    print(node._fields,end=':')

    # name,idがあれば表示する
    show = ["name", "id", "n", "s"]
    for i in show:
        if i in node._fields:
            print()
            print(" "*(indent+indent_size),getattr(node,i),end=':')

    # 改行を入れる
    print()

    # 再帰的に実行する
    for child in ast.iter_child_nodes(node):
        walk(child, indent=indent+indent_size, indent_size= indent_size)


def parse_test(topic,output,correct,evaluate):
    if output == correct:
        if evaluate:
            eval(output)
        return True
    else:
        print("{0}\nwrong   : {1} \ncorrect : {2}".format(topic,output,correct))
        return False
def parse_terminal(source):
    ast_object = ast.parse(source)
    obj = ast_object.body[0].value
    return obj

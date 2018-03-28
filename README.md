this script is useful when you want your python to be a one-liner.

run script by

```python3
import junkpy

source = '''
a = 7
b = 2
a = 3
c = a + b
print(c)'''

code = junkpy.JunkModule(source).output
print("code:", code)
```

```console
code: [None for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":7})]]if[ns.update({"b":2})]]if[ns.update({"a":3})]]if[ns.update({"c":ns["a"]+ns["b"]})]]if[ns["print"](ns["c"])]]][0]
```

```python
[None for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[ns for ns in[__builtins__ if(type(__builtins__) is dict)else{attr:getattr(__builtins__,attr)for attr in dir(__builtins__)}]if[ns.update({"a":7})]]if[ns.update({"b":2})]]if[ns.update({"a":3})]]if[ns.update({"c":ns["a"]+ns["b"]})]]if[ns["print"](ns["c"])]]][0]
```

```console
5
```

For more detail read
- https://qiita.com/KTakahiro1729/items/c9cb757473de50652374 (Japanese)
- https://qiita.com/KTakahiro1729/items/2abef90fee3ec7b31e3e (Japanese)

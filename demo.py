from ast_helper import *

# TODO: it would be nice to use type constraints to further constrain the metavars



# TODO: this seems like a nice way to quantify...
# def while_pattern(expr: ast.AST, content: ..., rest: ast.AST):


@aast
def func_def_0_param(func_name: str,
                     content: list):  # TODO: it's unfortunate that this needs knowledge about the AST typing, and als how the ast isn't algbraic, or documented anywhere
    def func_name():
        content


tree = ast.parse("""
def im_a_function():
    return 3
""")
ok, d = func_def_0_param.match(tree)
assert ok
assert d["func_name"] == "im_a_function"
assert len(d["content"]) == 1


@aast
def func_call(func_name: ast.Name, param_list: ast.AST):
    func_name(param_list)


tree = ast.parse("im_a_func(True)")
ok, d = func_call.match(tree)
assert ok
assert d["func_name"].id == "im_a_func"

tree = ast.parse("im_a_func(True,False)")
ok, d = func_call.match(tree)
assert not ok


@aast
def func_call2(func_name: ast.Name, param_list: list):
    func_name(param_list)


tree = ast.parse("im_a_func(True)")
ok, d = func_call.match(tree)
assert ok
assert d["func_name"].id == "im_a_func"

tree = ast.parse("im_a_func(True,False)")  # TODO: this is a big issue!!!!!!!!!
ok, d = func_call.match(tree)


# assert ok

@aast
def thing_pattern(one_line: ast.AST):
    one_line


tree = ast.parse("""
print("WOWOWOW")
""")

ok, d = thing_pattern.match(tree)
assert ok

tree = ast.parse("""
print("WOWOWOW")
print("!!!!!!!")
""")

ok, d = thing_pattern.match(tree)
assert not ok


@aast
def while_pattern(expr: ast.AST, content: list, rest: list):
    while expr:
        print("I")
        content
    rest


tree = ast.parse("""
while True:
    print("I")
    print("like")
    print("looping")
    print()
print("somedey my time will come")
""")

ok, d = while_pattern.match(tree)
assert ok


@aast
def assert_realizer(expression: ast.NameConstant):
    if __debug__:
        if not expression:
            raise AssertionError


tree = ast.parse("""
if __debug__:
    if not False: raise AssertionError
""")

ok, d = assert_realizer.match(tree)
assert ok
assert d["expression"].value is False


@aast
def assert_matcher(exp: ast.AST):
    assert exp


tree = ast.parse("assert False")
ok, d = assert_matcher.match(tree)
assert ok
assert d["exp"].value is False

tree = ast.parse("assert False, 'thing... stuff'")
ok, d = assert_matcher.match(tree)
assert not ok


@aast
def assert_matcher2(exp: ast.AST, msg: ast.AST):
    assert exp, msg


tree = ast.parse("assert False, 'words words'")
ok, d = assert_matcher2.match(tree)
assert ok
assert d["msg"].s == 'words words'
assert d["exp"].value is False


@aast
def and_matcher(exp: ast.AST):
    True and exp


tree = ast.parse("True and (False or True)")
ok, d = and_matcher.match(tree)
assert ok


@aast
def adds_matcher(a: ast.AST, b: ast.AST):
    a + 3 + b


tree = ast.parse("10 + 3 + some_var")
ok, d = adds_matcher.match(tree)
assert ok
assert d['a'].n == 10
assert d['b'].id == "some_var"


@aast
def add(a: ast.Num):
    a + 3


tree = ast.parse("10 + 4")
ok, d = add.match(tree)
assert not ok

tree = ast.parse("10 + 3")
ok, d = add.match(tree)
assert ok
assert d['a'].n == 10

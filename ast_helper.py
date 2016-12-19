import ast
import inspect
import warnings
from typing import List, Dict, Set, Tuple, Union
import copy  # my quite protest of mutability
from type_assert import ta


# am I sure this isn't a thing? look up python mtaprograming, and macros.  looked it up, doesn't exist




# TODO: rename file
# TODO: should play nice with NodeTransformer?


# abstract ast
# TODO: is this to dumn of a name, call it "Pattern"?
# TODO: make AAST callable?
# TODO: inherit from ast.AST?
class AAST:
    # it's easier to turn a list into an AST then the other way around
    # TODO: support scoping over typing.List with type paramiters
    # TODO: create an annotation that injects if __debug__ typecheck asserts on functions
    # TODO: the semantics of list capturing metavars is far more complicated than node captureing metavars, what if 2 list metavars sit next to each other?

    @ta
    def __init__(self, fragment: List[ast.AST], metavars: Dict[str, type]):  # TODO: correct type signature
        self.fragment = fragment
        self.metavars = metavars

    @ta
    def match(self, other_tree: Union[ast.Module, List[ast.AST]]) -> Tuple[bool, Dict[str, Union[ast.AST,List[ast.AST], str]]]:
        def recursive_matcher(solid_tree: List[ast.AST],
                              match_tree: List[ast.AST],
                              match_holes: Set[str],
                              matched_holes: Dict[str, ast.AST]):
            if not solid_tree and not match_tree:
                return (True, match_holes, matched_holes)  # TODO: better return type

            elif not solid_tree and match_tree:
                return (False, match_holes, matched_holes)
            elif solid_tree and not match_tree:
                return (False, match_holes, matched_holes)
            else:
                solid_head, *solid_tail = solid_tree
                match_head, *match_tail = match_tree

                ## TODO: feal a little sketchy about meta var list matching, but why stop now?
                if ast.Name == type(match_head) and match_head.id in match_holes and self.metavars[match_head.id] == list:
                    match_holes.remove(match_head.id)  # bleeehhh so much mutability, TODO: could be passing around 1 thing instead of 2
                    matched_holes[match_head.id] = solid_tree

                    return (True, match_holes, matched_holes)

                # HACK IT TILL IT WORKS!!!!!???
                # TODO: less hacky way to do this
                if ast.Expr == type(match_head) and ast.Name == type(match_head.value) and match_head.value.id in match_holes and self.metavars[
                    match_head.value.id] == list:
                    match_holes.remove(match_head.value.id)  # bleeehhh so much mutability, TODO: could be passing around 1 thing instead of 2
                    matched_holes[match_head.value.id] = solid_tree

                    return (True, match_holes, matched_holes)

                ok, match_holes, matched_holes = recursive_matcher(solid_tail, match_tail, copy.deepcopy(match_holes),
                                                                   copy.deepcopy(matched_holes))
                if not ok:
                    return (False, match_holes, matched_holes)

                # see if wildcard fits
                elif ast.Name == type(match_head) and match_head.id in match_holes:
                    if issubclass(type(solid_head), self.metavars[match_head.id]):
                        match_holes.remove(match_head.id)  # bleeehhh so much mutability
                        matched_holes[match_head.id] = solid_head

                        return (True, match_holes, matched_holes)
                    else:
                        return (False, match_holes, matched_holes)

                # TODO: check "is" the same thing? Can't becuase of subtle name capturing bugs?

                # does the rest of the tree line up?
                elif type(solid_head) == type(match_head):

                    # a more khosher way to get the fields?
                    assert solid_head._fields == match_head._fields, "a type should aways have the same fields"

                    matches = True
                    for field in solid_head._fields:

                        solid_f = getattr(solid_head, field)
                        match_f = getattr(match_head, field)

                        # TODO: metavariables need to be consifdered EVEN if they do not have the normal type
                        if str == type(match_f) and match_f in match_holes:
                            if issubclass(type(solid_f), self.metavars[match_f]):
                                match_holes.remove(match_f)  # bleeehhh so much mutability
                                matched_holes[match_f] = solid_f

                        elif issubclass(type(solid_f), ast.AST) and issubclass(type(match_f), ast.AST):
                            ok, match_holes, matched_holes = recursive_matcher([solid_f],
                                                                               [match_f],
                                                                               copy.deepcopy(match_holes),
                                                                               copy.deepcopy(matched_holes))
                            if not ok:
                                matches = False
                                break

                        # need the combos for matching TODO: remove second check, let metavars eat lists
                        elif issubclass(type(solid_f), list) and issubclass(type(match_f), list):
                            ok, match_holes, matched_holes = recursive_matcher(solid_f,
                                                                               match_f,
                                                                               copy.deepcopy(match_holes),
                                                                               copy.deepcopy(matched_holes))
                            if not ok:
                                matches = False
                                break


                        elif type(solid_f) == type(match_f) and solid_f == match_f:
                            pass
                        else:
                            matches = False
                            break

                    if matches:
                        return True, match_holes, matched_holes
                    else:
                        return False, match_holes, matched_holes

        if isinstance(other_tree, ast.Module):
            ok, match_holes, matched_holes = recursive_matcher(other_tree.body, copy.deepcopy(self.fragment), copy.deepcopy(set(self.metavars.keys())), {})

            return ok, matched_holes
        else:
            ok, match_holes, matched_holes = recursive_matcher(other_tree, copy.deepcopy(self.fragment), copy.deepcopy(set(self.metavars.keys())), {})

            return ok, matched_holes

    # TODO: if anything, this should be the callable semantics, since it is analogous to how a funtction works, it could even use positional arguments!
    @ta
    def generate(self, metavars: Dict[str, ast.Module]):
        # TODO: assert that the metavars match the type scheme

        def recursive_generate(fragment: ast.AST):
            assert issubclass(type(fragment), ast.AST)

            if ast.Name == type(fragment) and fragment.id in self.metavars:
                return copy.deepcopy(metavars[fragment.id])
            else:

                fragment

                # if it's a piece of AST

                # if it's a piece of AST
                # if it's a plain old var

        return ...


# TODO: would be nice to disable warnings

@ta  # TODO: why would this break things??
def aast(func) -> AAST:
    tree = ast.parse(inspect.getsource(func))  # TODO: can give it the right line nubers and stuff?

    assert type(tree) == ast.Module
    assert len(tree.body) == 1

    function_def = tree.body[0]
    assert type(function_def) == ast.FunctionDef

    # only support named args
    # assert not function_def.args.defaults, "does not support defaults"
    # assert not function_def.args.kw_defaults, "does not support defaults"
    # assert not function_def.args.kwarg, "does not support kwargs"
    # assert not function_def.args.kwonlyargs, "does not support kwargs"
    # assert not function_def.args.vararg, "does not support varargs"
    #
    # meta_vars = [arg.arg for arg in function_def.args.args]

    # the choice is a bit fuzzy, when to use ASTs and when to use introspection
    # I think the function deffinition should be introspected and the body treated as an AST,
    #   though there may be some subtle issues with this

    # of course if we used the asts we could give real nice error msgs, linked to the line and everything

    meta_vars, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(func)

    # this is a little extreame but we can be exlpicit till we settle on a good default (is ast.AST a good default?)
    assert set(annotations.keys()) == set(meta_vars), "every metavar needs an annotation"

    # of course scoped meta vars can be validated at "compile" time

    assert not varargs, "only supports named metavars with type hinted scope"
    assert not varkw, "only supports named metavars with type hinted scope"
    assert not defaults, "does not support defaults"  # perhapes defualts with AST for the ast generators is ok?
    assert not kwonlyargs, "only supports named metavars with type hinted scope"
    assert not kwonlydefaults, "only supports named metavars with type hinted scope"

    return AAST(function_def.body, annotations)


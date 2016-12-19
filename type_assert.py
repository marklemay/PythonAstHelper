import inspect
import warnings

# apparently the magic already works for this
# TODO: review type hinting in the wild
# TODO: make sure it is consistent with mypy and other type checkers



# TODO: better name?
#TODO: a version of this that only warns?
#TODO: clearly not recursing into tuples
def ta(func):
    """
    a decorator that will assert correct typing on functions given type hints
    :param func:
    :return:
    """

    sig = inspect.signature(func)

    # TODO: need to infer arg position

    def asserted_func(*args, **keyargs):
        # TODO first assert the type parameters


        # TODO: only if __debug__ is true


        bindings = sig.bind(*args, **keyargs)

        bindings.apply_defaults()  # TODO: does this work?

        for arg_name, arge_value in bindings.arguments.items():
            t = sig.parameters[arg_name].annotation
            if t and not t == sig.empty:
                if not isinstance(t, type):
                    warnings.warn("doesn't support string hints")

                elif not issubclass(type(arge_value), t):
                    # I miss you scala
                    raise TypeError('function arg "' + str(arg_name) + '" has value "' + str(arge_value) + '" which has type ' + str(
                        type(arge_value)) + ' which is not a subclass of ' + str(t))

        ret = func(*args, **keyargs)

        # don't forget to check the return type!
        if sig.return_annotation and not sig.return_annotation == sig.empty:
            if not isinstance(sig.return_annotation, type):
                warnings.warn("doesn't support string hints")

            elif sig.return_annotation and not issubclass(type(ret), sig.return_annotation):
                # I miss you scala
                raise TypeError(
                    'function returns ' + str(ret) + ' which has type ' + str(type(ret)) + ' which is not a subclass of ' + str(sig.return_annotation))

        return ret

    return asserted_func



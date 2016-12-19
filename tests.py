from type_assert import *

@ta
def add(a: int) -> int:
    return a + 3


assert add(1) == 4

# TODO: expect thrown assertions
# print(add(1.2))

assert add(a=4) == 7


@ta
def add2(a: int):
    return a + 3


# TODO: expect thrown assertions
# print(add2("1"))

# TODO: expect thrown assertions
# print(add(1.2))

assert add2(a=4) == 7

# coding: utf-8
def func_list():
    import types
    print([str(f).split()[1] for f in globals().values() if type(f) == types.FunctionType])

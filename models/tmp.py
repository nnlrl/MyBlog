import inspect


class A:

    @classmethod
    def b(cls, id=1):
        return id


if __name__ == '__main__':
    key_pattern = "%s:%s:v2" % ("{cls.__name__}", "{id}")
    print(A.__name__)
    rv = inspect.getfullargspec(A.b)
    arg_names, kwonlydefaults = rv.args, rv.kwonlydefaults
    print(arg_names, kwonlydefaults)

    kw = kwonlydefaults.copy() if kwonlydefaults is not None else {}
    kw.update(zip(arg_names, [A, 1]))
    if callable(key_pattern):
        key = key_pattern(*[kw[name] for name in arg_names])
    else:
        key = key_pattern.format(*[kw[n] for n in arg_names], **kw)
    print(key)

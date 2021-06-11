from functools import wraps
class myClass:

    def __init__(self):
        self.myValue = "Hello"

    def decorator(x):
        print(x)
        def inner(the_func):
            @wraps(the_func)
            def wrapper(*args, **kwargs):
                print(args[0].myValue)
                the_func(*args, **kwargs)
            return wrapper
        return inner
    @decorator("yo")
    def myFunction(self):
        print("World")

foo = myClass()
foo.myFunction()
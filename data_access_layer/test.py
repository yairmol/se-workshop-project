from functools import wraps
class myClass:

    def __init__(self):
        self.myValue = "Hello"

    def decorator(the_func):
        @wraps(the_func)
        def wrapper(*args, **kwargs):
            print(args[0].myValue)
            the_func(*args, **kwargs)
        return wrapper

    @decorator
    def myFunction(self, a, b, c):
        print("World %s %s %s" % (a,b,c))

foo = myClass()
foo.myFunction(1, 2, 3)
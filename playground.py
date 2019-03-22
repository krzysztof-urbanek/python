

def func(*args,**kwargs):
    print(kwargs)

a = (i**2 for i in range(1,10))
print(type(a))

class MyClass:

    def fun(self, x):
        return x+1

    def fun2(x):
        return x**2

print(MyClass.fun(MyClass(),5))
print(MyClass().fun(42))

def global_func(a, b):
    return a.fun(b)

MyClass.global_func = global_func
print(MyClass().global_func(5))
print(MyClass.fun2(11))

class Class_with_constructor:
    def __init__(self, x):
        print('Constructor called with argument = ' + str(x))

Class_with_constructor(33)
Class_with_constructor("Ala ma kota")

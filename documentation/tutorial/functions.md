---
layout: tutorial
---



Functions
=========

Nominine provide functions and methods in the same way that OOPs like Python and JavaScript does.


Simple functions
----------------

The following defines the function 'square':

        fun (: 'square' ( number ) [
          that * ( that )
        ] )

To use this function, write:

        ( square 10 )

Methods
-------

The following defines a method on a number:

        const (: 'other-number' ( class [
          is 0
          does (: 'max' ( number ) [
            this < ( that ) else [ this ]
          ] )
        ] ) )

Notice the use of 'is 0'. This makes the new class a subclass of 'number' by *being* an instance of the built-in 'number' type.
The new number type is interchangeable with other numbers, even for built-in functionality. However, operations on 'number'
instances that return new instances of 'number', will produce simple number instances without the 'max' method.

To use this write something like:

        var (: 'a-number' ( other-number new ) )

        ( a-number max 20 )

This declares a variable named 'a-number' which is an instance of the other-number class. Then the 'max' method is used.


First order functions
---------------------

'function' is the function class. It is a normal class and it has a constructor that takes two parameters.

The following will return 25:

        ( function (: ( number ) [ that * ( that ) ] ) 5 )


Functions as parameters
-----------------------

Functions can be passed as arguments.

The following defines a function that takes a function as a parameter:

        fun (: 'square' ( function ) [
          that ( some-object )
        ] )

Note: Due to current limitations, it is not possible to specify a the type of a function to include
its parameters and return type when using it as a parameter.


Apply
-----

Functions can be connected to an object, which will be called 'this'. When using a method on an object,
this connection is done implicitly. Function objects have an 'apply' method that can be used to
explicitly connect an object to a function.

Notice that named functions and object methods are created on invocation, so 'apply' does not change 'this'
for further usages of that function or method by name.

'this' as used by functions defined in a local scope, is that scope object.

As a rule, 'apply' only work for first order functions. The following statement will create a function
using 'var' and 'function' and then reassign 'this' to 'some-object'.

        var (: 'f' ( function (: ( any ) [ ... ] ) ) )

        ( f assign ( some-object ) .)



---
layout: tutorial
---

Functions
=========

Nominine provide functions and methods much in the same way that OOPs like Python and JavaScript does.
By this, I mean that a function definition basically assigns a function object to a variable and
a method is a function that is *applied* to a specific object.

<hr>

Simple functions
----------------

The following defines the function **square**:

        defun (: 'square' ( number ) [
          that * ( that )
        ] )

To use this function, write:

        ( square 10 )

Notice that **defun** is short for **def** **fun**.
The above function could also be defined by writing:

        def (: 'square' ( fun (: ( number ) [
          that * ( that )
        ] ) ) )

<hr>

Methods
-------

Methods are just functions that are *applied* to some object.
Normally, the application of a function happens implicitly.
If a an object has a method, then **this** will refer to that object within the body of the applied function.

*Warning: the following example uses terminology that has not been discussed yet.*

The following defines a method on a number:

        defact (: 'newnum' ( number ) [

          that

          does (: 'max' ( number ) [
            this < ( that ) else [ this ]
          ] )

        ] )

This defines a new type **newnum** that takes a number as an argument to construct a number with a **max** method.

To use this write something like:

        var (: 'some-newnum' ( newnum( 10 ) ) )

        ( some-newnum max 20 )

This declares a variable named **some-newnum** which is a **newnum**.
Then the **max** method is used.

<hr>

First order functions
---------------------

**fun** is the function type.
Use **fun** to construct first-order functions.

The following yields 25:

        ( fun (: ( number ) [ that * ( that ) ] ) 5 )

<hr>

Functions as parameters
-----------------------

Functions can be passed as arguments.

The following defines a function that takes a function as a parameter:

        fun (: 'square' ( fun ) [
          that ( some-object )
        ] )

*Note: Due to current limitations, it is not possible to specify a the type of a function to include its parameters and return type when using it as a parameter.*

<hr>

Apply
-----

Functions can be connected to an object, which will be called **this** within the function body.
When using a method on an object the application is done implicitly. Function objects have an **apply** method that can be used to
explicitly connect an object to a function.

Notice that methods are created on invocation, so **apply** does not change **this** for further usages of that method by name.

The following statement will create a function using **var** and **fun** and then reassign **this** to **some-object**.

        var (: 'f' ( fun (: ( any ) [ ... ] ) ) )

        ( f ( apply ( some-object ) !) .)

Notice the use of noun to update **f**.
**apply** creates a new object, which consists of the old function wrapped in an **applicator**.

<hr>

Polymorphism
------------

If more than one method with the same name is defined on an object or more than one functions with the same name is defined in scope,
dispatch will match the one with the parameter type matching the parameter object.

The following is a polymorphic function:

        defun (: 'square' ( number ) [
            that * ( that )
        ] )

        defun (: 'square' ( seq ) [
          seq (: ( number ) [
            var (: 'elements' ( that each ) )
            loop [
              square ( elements next else [ stop ] ) throw
            ]
          ] )
        ] )

will define one *square* function that takes a number as parameter as well as a *square* function that takes a sequence as parameter.

        ( square 5 )

yields 25.

        ( square [ 1 2 3 4 ] )

yields a lazy list that calculates the squares of the numbers.

        ( console write ( square [ 1 2 3 4 ] ) newl .)

will output

        [ 1 4 9 16 ]

Polymorphic functions can also be used as methods.



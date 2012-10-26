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

The following is a polymorphic function:

        def (: 'square' (
          fun (: ( number ) [
            that * ( that )
          ] )
          is (
            fun (: ( set ) [
              gen (: ( number ) [
                var (: 'elements' ( that each ) )
                loop [
                  square ( elements next else [ stop ] ) throw
                ]
              )
            ] )
          )
        ) )

*This syntax is not optimal. In the future there may be a more direct way to define polymorphic functions.*

**square** is basically both a function that takes a number as a parameter and at the same time a function that takes a set
as a parameter.

        ( square 5 )

yields 25.

        ( square (: 1 2 3 4 ) )

yields the set of 1, 4, 9 and 16.
Additionally, **square** yields a generator when it gets a set as a parameter.
This means that the numbers are only calculated when needed.
*More on generators later.*

Polymorphic functions can also be used as methods.

<hr>

Don't
-----

Generally, any object can be any other object, so all objects can be a function.

        ( 234 is ( function (: ( string ) [ ( console write that ':' this newl .) this ] ) ) )

yields a number that is also a function.
If the variable **x** held this number, writing

        ( x 'current value' + 1000 )

yield 1234 and output "current value: 234".

*I do not encourage doing this kind of trickery. It is just an example.*


---
layout: tutorial
---

Functions
=========

Nominine provide functions and methods much in the same way that OOPs like Python and JavaScript does.
By this, I mean that methods are functions that are *applied* to a specific object.

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

The following defines a method on a number:

        defact (: 'newnumber' ( number ) [

          that

          does (: 'max' ( number ) [
            this < ( that ) else [ this ]
          ] )

        ] )

This defines a new type **newnumber** that takes a number as an argument to construct a number with a **max** method.

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

The following will return 25:

        ( fun (: ( number ) [ that * ( that ) ] ) 5 )

<hr>

Functions as parameters
-----------------------

Functions can be passed as arguments.

The following defines a function that takes a function as a parameter:

        fun (: 'square' ( fun ) [
          that ( some-object )
        ] )

Note: Due to current limitations, it is not possible to specify a the type of a function to include
its parameters and return type when using it as a parameter.

<hr>

Apply
-----

Functions can be connected to an object, which will be called **this**. When using a method on an object,
this connection is done implicitly. Function objects have an **apply** method that can be used to
explicitly connect an object to a function.

Notice that methods are created on invocation, so **apply** does not change **this**
for further usages of that method by name.

The following statement will create a function using **var** and **fun** and then reassign **this** to **some-object**.

        var (: 'f' ( fun (: ( any ) [ ... ] ) ) )

        ( f ( apply ( some-object ) !) .)

Notice the use of noun to update **f**.
**apply** creates a new object, which consists of the old function wrapped in an **applicator**.


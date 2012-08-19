---
layout: tutorial
---

This part of the tutorial assumes that you know about syntax, semantics and parameters.


Context methods
===============

Context methods are methods that apply to the current closure.
These methods do things like declare variables, throw objects and such.

Context methods typically return the context itself, so that they can be chained.


Variables
---------

To declare a variable, one uses the context method 'var'.

        var (: 'x' ( number ) 7 )

It takes three parameters.

First there is a string containing the name of the new variable.
Then there is an optional class of the variable. Lastly there is the initial value.

The default class is 'any'.

        var (: 'x' ( number ) 7 )
        var (: 'y' ( number ) 8 )

'x' and 'y' can now be used to refer to their respective number object.

'var' creates 'reference' objects.
To change the object referenced by the variable, use a noun-phrase.

        ( x ( 2 !) .)
        ( y ( x !) .)

Now 'x' and 'y' both reference the same new object.
Notice that numbers in Nominine are *ordinary* objects.

Constants
---------

Constants are like variables except one cannot change the object they refer to. Also constants do not have type.

        const (: 'a' 123 )

First argument is the name and the second argument is the object it represent.

It is not strictly correct to call these constants, because the object itself may be mutable.
The different between constants and variables is that constants will always represent the same object,
while variable may be set to point to different objects.

It is can be wise to use 'const' where possible and only use 'var' where necessary.

Function declarations
---------------------

The context method 'fun' is used to declare functions.

        fun (: 'square' ( number ) [ that * ( that ) ] )

'fun' takes three parameters

The first parameter is a string denoting the name of the function.
The second parameter is the parameter class. This defaults to 'any'.
The last parameter is a set denoting the code block of the function.

Functions currently have no return type, because it has no direct use at this point.
It will default to 'any'.

More on functions in the dedicated section.

Return
------

A function returns automatically when evaluation reaches the end of it.
The object used at this point becomes the return value.

To explicitly return from inside a function use 'return'

        ( return 123 .)

Return takes any object as argument. This object is returned.

Retry
-----

In the same styles as 'skip' for loops, functions have 'retry'.

'retry' used inside a function skips to the beginning of the function.

*'retry' is not implemented yet.*

Catch
-----

'catch' is used to create a receiver for objects *thrown* from subsequent scopes.

        catch (: ( number ) [ that * 10 ] )

The first argument is a class, and the second argument is the set representing the code block.

'catch' is very similar to "except" mechanism used in other languages to catch exceptions.
It is different, however, in that it resumes and returns a value.


Def
---

'def' is used to define words in context.

        def (: 'm' [ ... do something ... ] )

The first argument is a string denoting the word to be defined,
and the second argument is a set denoting the code block that defines the word.


Loop
----

If you have boring repetitive work to do, just put it in a loop.

        loop [ ... ]

Loops continue forever.

Loops return the context so they can be chained.

Stop
----

To stop a loop, use the word 'stop'.

'stop' will stop the innermost loop.

This is similar to what is usually called 'break'.

Skip
----

To jump to the top of a loop from inside the loop use 'skip'.

This is similar to what is usually called 'continue'.

*'skip' is not implemented yet.*

Object properties
=================

Object methods are methods that apply to all objects.
These methods do things like adding new attributes or other properties to objects.
Object methods typically return a new object, so that structural properties remain immutable.


Throw
-----

'throw' is used to throw an object in the dynamic/usage context tree, called 'field'.

        ( some-object throw .)

A thrown object can be caught by a 'catch' or by an 'iterator'.

'throw' returns the value returned by 'catch'.
Generators currently does not support return values and will always return 'none'.

Is
--

'is' builds an object that is both the object on which it is applied and its parameter

        some-object is ( some-other-object )

This does not change the object but produces a new object.

*This is a temporary method that is likely to be removed in the future.*


Has
---

'has' builds an object that has an attribute given by the parameter.

        some-object has (: 'x' ( number ) 123 )

The first parameter is a string denoting the name of the attribute.
The second parameter is the class of the attribute.
The last parameter is the initial value.

The new attribute is like a variable, and can be set to reference an other object of correct type using a noun-phrase.

This does not change the object but produces a new object.

*This is a temporary method that is likely to be removed in the future.*


Does
----

'does' builds an object that has a method given by the parameter.

        some-object does (: 'm' ( any ) [ ... ] )

The first parameter is a string denoting the name of the method.
The second parameter is the class of the methods parameter.
The last parameter is a set denoting the code-block of the method.

This does not change the object but produces a new object.

*This is a temporary method that is likely to be removed in the future.*


Param
-----

'param' builds an object that has a parameter attribute.

        some-object param (: 'p' ( any ) ( none ) )

The first parameter is a string denoting the name of the parameter.
The second parameter is the class of the parameter.
The last parameter is the default value of the parameter.

This does not change the object but produces a new object.

*This is a temporary method that is likely to be removed in the future.*

Gets
-----

'gets' builds an object that can receive an object of a specific class of object.

        some-object gets (: ( number ) [ ... ] )

The first parameter is the class of the objects handled.
The second parameter is a set denoting the code that handles the received object.

This does not change the object but produces a new object.

*This is a temporary method that is likely to be removed in the future.*


Defs
-----

'defs' builds an object that defines a word.

        some-object defs (: 'w' [ ... ] )

The first parameter is a string denoting the word.
The second parameter is a set denoting the code that is carried out then the word is received.

This does not change the object but produces a new object.

*This is a temporary method that is likely to be removed in the future.*


Classes
=======

The following are the classes available to the programmer.


Number
------

This is the superset of all numbers. There should also be integers and more limited number types.

Ideally 'number' should be implemented with unlimited size and precision and all the tricks, but currently
it is implemented using double precision float.

Numbers implement the standard operators in the expected way. Factory methods create new numbers while
mutating methods modify the number operated upon:

Factory arithmetic operations: +, -, /, `*`

Factory comparison operations: <, <=, ==, >, >=, !=

Mutating arithmetic operations: +=, -=, /=, `*`=

Assignment: =

Numbers are not bit fields and not booleans, so they do not implement bitwise or logical operations.


String
------

'string' is the general string type. It currently has no operations.


Set
---

'set' is the superclass of things that can generate an iterator using 'each'.

        ( some-set each )

At the time of writing, sub-classing of 'set' does not allow easily user defined sets.
In the future all objects that respond to 'each' will be considered sets.

An empty set may respond with 'none' to an 'each' dispatch.

See section on sets for more information and examples.

List
----

'list' is a 'set'.

Additionally, list have mechanisms for appending elements and merging with other sets.
Lists also have 'length'.

List iterators produce 'none' when the end of the list is used.

The following may be refined in the future:
Empty lists produce 'none' on 'each'.

See section on sets for more information and examples.

Generator
----------

'generator' is a 'set'.

Generators are subprograms that produce elements. Generators are also called lazy lists.

Generators should produce 'none' when there are no more elements.
There can, however, be other mechanism for terminating iteration.

See section on sets for more information and examples.

Iterator
--------

An iterator is an object that has, as a minimum, 'next' defined.

'next' returns an object, and is used to progress the iteration.

Iterators are commonly produced by sending an 'each' to a set.

At the time of writing, sub-classing of 'iterator' does not allow easily user defined iterators.
In the future all objects that respond to 'next' will be considered iterators.

An depleted iterator may respond with 'none' to a 'next' dispatch.

See section on sets for more information and examples.

Class
-----

*Note: The current mechanism for building user-defined classes is ad-hoc, and will be replaced in the future.*

'class' is a 'class'.

        class [ ... ]

'class' has a constructor on 'set'. The parameter describes the default constructor of the class.
This constructor does not take parameters.

To build a parameterized constructor, build a class that is also a function. See the example on user-defined classes.


Function
--------

The 'function' class is used to create first order functions.

        function (: ( number ) [ that / ( that + 1 ) ] )

The first parameter of the constructor is the parameter type of the function.
The second parameter is a set denoting a code-block.

Functions lack return type. Also, when receiving functions as parameters, one cannot express the
parameter nor return type of the function. These problems will be resolved in the future.

Methods are also functions, and 'fun' create functions identical to first order functions,
except 'apply' works differently.

More on functions in the dedicated section.


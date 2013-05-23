---
layout: tutorial
---

Basics
======

<hr>

Hello world!
------------

This is the *hello world* example.

        ( console write 'Hello world!' newl .)

This produces the following output:

        Hello world!

The workings of this program will be explained in the next few sections.

<hr>

Expressions
-----------

A Nominine expression is very much like an expression in any programming language.
A result is calculated and the expression itself represent that result.

For example:

        ( 1 + 2 )

Expressions can be nested in the obvious way:

        ( ( 1 + 2 ) * 3 )

Everything in Nominine is left-associative, so the previous expression can more easily be written

        ( 1 + 2 * 3 )

The result of which is 6.
However

        ( 1 + 2 * 3 + 4 )

yields 10 while

        ( 1 + 2 * ( 3 + 4 ) )

yields 21, because the evaluation order is changed with the introduction of the inner parenthesis.

*Recall that __start-contexts__ also play an important role when using expressions.*

<hr>

Imperatives
-----------

Nominine does not provide a separate syntactic construct for imperatives, like a code block within curly brackets.
Instead, an expression can be used as an imperative by adding a "." at the end.

        ( console write 'hi' .)

The result of an imperative is ignored, as if the expression was not even there.
Imperatives can only have effect on their environment.

        ( 1 + ( console write 'hi' .) 4 )

yields 5, while *also* outputting the word "hi".

<hr>

Output
------

In Nominine, the **console** object is used for input and output.

        ( console write 'hi' .)

outputs "hi" with no trailing newline.
In order to add a newline, one must use the word **newl**.

        ( console write 'hi' newl .)

To output numbers, simply give **write** numbers.

        ( console write 1 2 3 newl .)

outputs "1 2 3" followed by a newline.
There is no special symbol to separate the arguments to **write**, it just outputs everything it gets.

        ( console write '5 * 7 = ' ( 5 * 7 ) newl .)

outputs "5 * 7 = 35" followed by a newline.

In addition to **newl**, there is also **tab**.
These words can be used anywhere in the arguments to **write**

        ( console write
           '2 * 3' tab '=' tab ( 2 * 3 ) newl
           '3 * 3' tab '=' tab ( 3 * 3 ) newl
        .)

outputs

        2 * 3	=	6
        3 * 3	=	9

There is no special formatting characters within strings in Nominine.

<hr>

Strings
-------

Strings in Nominine support implicit concatenation.
This makes strings behave the same way as **console write**.

        ( '5 * 7 = ' ( 5 * 7 ) newl )

yields a new string object with the value "5 * 7 = 35".
The new string object also has a trailing newline.

<hr>

Variables
=========

<hr>

Using variables
---------------

Nominine lets you define variables by writing:

        var (: 'x' 123 )

This defines the variable **x** to refer to the number 123.

**x** can now be used in expressions

        ( x * 10 )

yields 1230.
However

        ( 10 * x )	<--- wrong !!!

does not multiply **x** by 10.
Instead it attempts to access the property **x** of the __\*__ method.
This fails because the multiplication method of a number has no **x** property.
The variable **x** is defined in the local scope, and it can only be accesses at the beginning of an expression.
Recall the discussion on *start-contexts*.
So for the previous expression to yield the expected result, one must write:

        ( 10 * ( x ) )

<hr>

Assignment
----------

Assignment is a method that works on most objects.

        ( x = 5 .)

sets **x** to be 5. Notice that it is an imperative.


<hr>

Input
-----

The console object is used for input as well as output.

         ( console write 'Name please> ' .)

         var (: 'name' ( console read ) )

         ( console write 'Hello, ' ( name ) newl .)

The property **read** of the **console** object, reads a line of input from the console and yields a string object.
The new-line of the input string is not included.
The program will ask for the users name and output a greeting.

This program can be simplified to not use variables:

        ( console write 'Name please> ' ( 'Hello, ' ( console read ) ) .)

<hr>

Logic
=====

Nominine does not use boolean logic.
Instead **none** is roughly the same as *false* and any other object is *true*.

Notice that only **none** is none. There is no empty list, empty string, negative number or zero that is equivalent to *false*.

<hr>

Comparisons
-----------

All comparisons on numbers and other objects return their argument iff the comparison holds.

        ( 0 < ( a ) )

yields **a** iff the value of **a** is greater than 0.
Otherwise the expression yields **none**.

        ( a > 0 )

yields the number 0 iff a is a positive number.
Otherwise the expression yields **none**.

Only **none** is considered *false*.
0 is regarded as *true*.

<hr>

Else and then
-------------

*else* and *then* are used like conditional statements as well as logical operators.
This is somewhat similar to how "&&" and "||" are used in some other languages like JavaScript.

        ( 0 < ( a ) else [ b ] )

yields **a** iff **a** is positive, otherwise it yields **b**.
*Notice the quoted expression `[ b ]`. More on quoted expressions later.*

        ( a > 0 then [ b ] )

yields **b** iff a is positive otherwise it yields **none**.

*then* and *else* can be chained.

        ( a > 0 then [ b ] else [ c ] )

yields **b** if a is greater than zero otherwise it yields **c**.

<hr>

Loops
-----

Nominine only has one loop construct. This is the endless but endable loop.

**loop** gives a simple endless loop that must be terminated using **stop**.

To loop until **condition** is none, do:

        loop [
          ( condition else [ stop ] .)
        ]

The following program outputs the numbers 1 to 10:

        var (: 'i' 0 )

        loop [
          console write ( 10 > ( i ) else [ stop ] += 1 ) newl
        ]

There are two new concepts here:

The loop tests if **i** is less than 10 before increasing it by 1 and printing it.
If **i** is not less than 10, the quoted expression `[ stop ]` will be evaluated causing the loop to stop.
When the loop stops evaluation continues as expected from the point after the loop.

<hr>

Context methods
===============

We have encountered two context methods so far. These are **var** and **loop**.

We have used these methods as if they were imperatives.
To make this tutorial simpler, this has been ignored until now.

**var** and **loop** are methods on contexts.
When **var** is used, it uses its parameters to do some modifications to its context object.
It creates a new variable.
However, when it is done, it returns itself, the context object, as its result.
That way, instead of writing

        ( var (: 'x' 123 ) .)
        ( var (: 'y' 123 ) .)

one can write

        var (: 'x' 123 )
        var (: 'y' 123 )

The same goes for **loop** and most of the other context methods.

This is the same as returning *this* from methods in Python so that one can write ( JavaScript, pseudo code ):

        start_context.var( 'x', 123 ).var( 'y', 123 )

instead of having to write ( JavaScript, pseudo code ):

        start_context.var( 'x', 123 )
        start_context.var( 'y', 123 )

<hr>

Lists
=====

Lists and quoted expressions are the same.

        [ 1 2 3 ]

is the list with elements 1, 2 and 3.
However, expressions in quoted expressions will not be evaluated.
They remain *phrase* objects which is often not what one wants.

Luckily, lists have implicit append.
The normal way to build a list where the elements may be given as expressions is:

        ( [] ( a ) ( b ) ( c ) )

This first creates an empty list *\[\]*,
and then appends the objects *a*, *b* and *c* to that list.

To merge lists, use *merge*:

        ( l1 merge ( l2 ) .)

Merges the list *l2* into l1.
This operation changes *l1*.

Also, assignment on lists are actually copying elements:

        ( l1 = ( l2 ) .)

*l1* now contains the elements of *l2*, but *l1* and *l2* are still separate lists.


<hr>

Iteration
---------

Common to all **seq** objects, is that one can iterate over their elements.

        var (: 'l' ( [] 10 20 30 ) )

        var (: 'elements' ( l each ) )

        loop [
          console write ( elements next else [ stop ] ) newl
        ]

will output

        10
        20
        30

In order to iterate over elements in a **seq**, one must first produce an **iterator**.
To do this one uses the **each** property of the **seq**.

        ( l each )

yields an **iterator**.
An **iterator** has a property, **next**, that fetches the next element in the **seq**.
If the next element is **none**, the end of the **seq** has been reached.

        ( elements next else [ stop ] )

yields the next element in **elements**.
If the iterator is depleted, the closest **loop** is stopped.

<hr>

Join
----

**seq** objects have a **join** method.
It takes a separator **string** as an argument and produces a **string**.

        (: 1 2 3 join ':' )

produces the string "1:2:3".

<hr>

Functions
=========

The context method **defun** defines a **fun** ( function ) object in current scope.

        defun (: 'square' ( number ) [
          that * ( that )
        ] )

defines a function **square** that takes a number as its argument.
**defun** takes three arguments.
The first is a **string** denoting the name of the function,
the second is the **type** of the function argument and the third is a quoted expression denoting the body of the function.

Notice that **that** is the name of the argument of the function.
It is always **that**.

Notice also that the result of the quoted expression is the object returned by the function.
It is also possible to use the context method **return** to return from a function, but more on that later.

        ( square 8 )

yields 64.

<hr>

Parameters
----------

The function **square** took a single parameter.
In order to take more than one parameter it is necessary to use tuples.
In order to have properly named parameters one can use **param**.
**param** is used to build a type.

        ( param (: (: 'a' ( number ) ) (: 'b' ( number ) ) ) )

yields a type that will match a tuple of two numbers and yield an object with properties **a** and **b** referencing the respective numbers.
**param** takes a **tuple** as a parameter.
The **tuple** contains tuples that conform to the following type:

        ( param (: (: 'name' ( string ) ) (: 'type' ( type ) ) ) )

In other words, the tuples in the parameter **tuple** given to **param** has a **string** and a **type**.

        defun (: 'average' ( param (: (: 'a' ( number ) ) (: 'b' ( number ) ) ) ) [
          that a + ( that b ) / 2
        ] )

Notice that **that a** and **that b** are the parameters as seen from inside the function.

        ( average (: 20 30 ) )

yields 25.

*More on functions later.*


---
layout: tutorial
---

Syntax and Semantics
====================

This page explains the key concepts of syntax and semantics using other languages as comparison and examples.
Last on this page there is an example using an oversimplified version of Nominine, named Mininine.

<hr>

Lisp
----

Lisp and Nominine have somewhat similar looking syntax, but the way to read it is very different.
In a Lisp expression, like

        ( f a b c )

it is the first term inside the parenthesis that denotes function or action to be taken.
To get the gist of what is going on, one looks at the first term.

All the remaining parts of the parenthesis are parameters.
The way they are handled is dependent on the function used.

In regular math notation, the above Lisp expression would look like

        f( a, b, c )

<hr>

Python
------

Nominine expressions are more like Python or a similar object-oriented language.

The Nominine expression:

        ( a b c )

is equivalent to the python expression:

        a.b.c

So, the terms in a Nominine expression form a path.
They do not form a parameter list like in Lisp.

Nominine syntax is completely consistent.
There are absolutely no need for special forms.

<hr>

Words are objects
-----------------

Even though words play an important and special role in Nominine,
they are just normal object.

Fetching the property associated with a word is like calling a function with a word as the parameter.

One can imagine that a path can just as well be written:

        a( word( 'b' ))( word( 'c' ) )

<hr>

Parameters
----------

Given the expression

        a.b( 123 )

The equivalent in Nominine is

        ( a b 123 )

This is really a special case, because 123 is a literal.
In order to have a path to fetch a parameter such as

        a.b( c.d )

on must write in Nominine

        ( a b ( c d ) )

to make sure that the result of 'a b' receives the *result* of 'c d' and not the word 'c'.
This is related to what is called a "start-context" which is written about elsewhere in the tutorial.

<hr>

Multiple parameters
-------------------

Nominine does not support multiple parameters directly.
Instead it uses tuples. The word ':' constructs an empty tuple ready to be sent as a parameter.
All you have to do is append objects to it.
Tuples have implicit append, so when a tuple receives an object it appends it to itself.

        ( f (: 1 2 3 ) )

This is equivalent to the JavaScript expression

        f( 1, 2, 3 )

Remember that start contexts also must be taken into consideration when building tuples.

To translate the JavaScript expression

        f( a.b, c.d )

into Nominine, one must write

        ( f (: ( a b ) ( c d ) ) )

It may seem like a lot of parenthesis, but when placing an expression in a context, one can usually loose the outer parenthesis and get

        f (: ( a b ) ( c d ) )

which in my opinion is not bad.

<hr>

Mininine
--------

Mininine is a little example programming language written in JavaScript.
It does not do much,
but it illustrates perfectly the syntax and semantics of Nominine.

The complete source code for Mininine:

        function newNumber( that ) {
          result = function( that ) {
            if ( that.type == 'number' ) {
              return newNumber( arguments.callee.state + that.state )
            } else if ( that.type = 'word' ) {
              if ( that.state == 'output' ) {
                console.log( arguments.callee.state )
                return arguments.callee
              }
            }
          }
          result.type = 'number' ;
          result.state = that ;
          return result ;
        }

        function newWord( that ) {
          result = function( that ) {}
          result.type = 'word' ;
          result.state = that ;
          return result ;
        }


A Mininine object is a function with **type** and **state**.
Type is simply a string denoting the type.
State is the information contained in that object.
The function itself is the objective of that object.

Mininine has only two different types of objects.

- Words serve as containers for strings.

- A number has an integer as its state.
I addition to this, the objective of numbers implement two mechanism.

   - When a number receives a number as a parameter, it will produce a new number which state is the sum of its own state and the parameters state. In better words, addition is implicit.

   - The other mechanism supported by numbers is outputting the state. When a number receives the word 'output', it will simply print the its number to console. After the printing is done, it will return itself as the result so that more operations can be done on it.

Here is an example expression:

        newNumber( 10 )( newNumber( 5 ) )( newWord( 'output' ) )( newNumber( 100 ) )( newWord( 'output' ) )

This expression is actually compiled to JavaScript.
In Nominine, which is interpreted, an expression of the form

        ( 10 5 output 100 output )

is parsed into a list of object, and then there is a loop that gives each object as the parameter of the result of the previous calculation.
Notice that there is an exact one-to-one correspondence between the source code ( syntax ) and what it does ( semantics ).

The result of evaluating this expression is 

        15
        115

<hr>

Adding features
---------------

In order to turn Mininine into a full fletched programming language,
all one has to do is add more types and more properties to those types.

Notice that adding all the different features is not trivial, because a feature does not stand completely on its own.
Nominine is a good balance of advanced and very adaptive features.
Nominine, however, can be extended easily in the exact same way as Mininine, except that so much of the work is already done.

On a side note, I imagine that this approach can be very good for scripting applications or games
where one needs strict control over the complexity of the scripting environment.


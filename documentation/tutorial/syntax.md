---
layout: tutorial
---

Syntax and Semantics
====================

This page explains the key concepts of syntax and semantics using other languages for comparison.

<hr>

Lisp
----

Lisp and Nominine have somewhat similar looking syntax, but the way to read it is very different.
In a Lisp expression, like

        ( f a b c )

it is the first term inside the parenthesis, "f", that denotes function or action to be taken.
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

The terms in a Nominine expression form a *path* like in a typical object-oriented language.
They do not form a parameter list like in Lisp.

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
- Type is a string denoting the type.
- State is the information contained in that object.
- The function itself is the *objective* of that object.

Mininine has only two different types of objects.

- Words

   - The state of a word is a native string.

   - Words do not understand any input.

- Numbers

   - The state of a number is a native number.

   - When a number receives a number, it will produce a new number which state is the sum of its own state and the parameters state. In better words, addition is implicit.

   - When a number receives the word 'output', it will simply print its state to console. After the printing is done, it will return itself as the result so that more operations can be done on it.

Here is an example expression:

        ( 10 5 output 100 output )

In Mininine, this is evaluated by manually translating it to the following:

        newNumber( 10 )( newNumber( 5 ) )( newWord( 'output' ) )( newNumber( 100 ) )( newWord( 'output' ) )

Notice that there is a one-to-one correspondence between the source code ( syntax ) and what it does ( semantics ).

The result of evaluating this expression is 

        15
        115

In Nominine, which is interpreted, an expression is parsed into a list of objects, and then there is a loop that gives each object as the parameter of the result of the previous calculation.

In JavaScript, the loop might look something like:

        current_result = start_context
        for ( parameter in parse( source_code ) ) {
          current_result = current_result( parameter )
        }

Notice that **current_result** is initialized with an object called **start_context**.
**start_context** represents current scope.

In the manually translated Mininine expression above, the start-context is build by newNumber( 10 ).
In Nominine the start-context is always a context object.

<hr>

Words are objects
-----------------

Even though words play an important and special role in Nominine,
they are just normal object.

Fetching the property associated with a word is like calling a function with a word as the parameter.

The path

        ( a b c )

would therefore translate to the following:

        start_context( newWord( 'a' ) )( newWord( 'b' ) )( newWord( 'c' ) )

Notice the use of **start_context** here.
In this example **a** would be a variable in the current scope. **start_context**, representing the current scope,
would behave like it had an attribute named 'a'.

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
One uses parenthesis to access the start-context object which represent the scope.

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


Adding features
---------------

In order to turn Mininine into a full fletched programming language,
all one has to do is add more types and more properties to those types.

Adding all the different features is not trivial, because a feature does not stand completely on its own.
Nominine can be extended as easily as Mininine and Nominine already has a lot of useful features.


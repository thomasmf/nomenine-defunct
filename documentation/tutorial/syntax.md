---
layout: tutorial
---

Syntax and Semantics
====================

This page explains the key concepts of syntax and semantics using other languages for comparison.

Syntax and semantics in Nominine is directly derived from the way objects work in Nominine as described in the previous chapter.

<hr>

Lisp
----

Lisp and Nominine have somewhat similar looking syntax, but the way to read it is very different.
In a Lisp expression, like

        ( f a b c )

it is the first term inside the parenthesis, "f", that denotes the action to be taken.
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

        function newNumber( state ) {
          result = function( that ) {
            if ( that.type == 'number' ) {
              return newNumber( arguments.callee.state + that.state )
            } else if ( that.type = 'word' ) {
              if ( that.state == 'output' ) {
                console.log( arguments.callee.state )
                return arguments.callee
              }
            }
            return none ;
          }
          result.type = 'number' ;
          result.state = state ;
          return result ;
        }

        function newWord( state ) {
          result = none ;
          result.type = 'word' ;
          result.state = state ;
          return result ;
        }

        start_context = function( that ) {
          return that ;
        }

        none = function( that ) {
          return none ;
        }


A Mininine object is a function with **type** and **state**.
- Type is a string denoting the type.
- State is the information contained in that object.
- The function itself is the *objective* of that object.

Mininine has only two types of objects.

- Words

   - The state of a word is a native string.

   - Words do not understand any input.

- Numbers

   - The state of a number is a native number.

   - When a number receives a number, it will produce a new number which state is the sum of its own state and the parameters state. In better words, addition is implicit.

   - When a number receives the word 'output', it will simply print its state to console. After the printing is done, it will return itself as the result so that more operations can be done on it.

In addition to the two types, Mininine has two predefined objects:

- **start_context** just returns its parameter. Other than that **start_context** has no defined words.

- **none** just produces none. This is just to assure that we are always working on actual objects, even when things go wrong.

Here is an example expression:

        ( 10 5 output 100 output )

In Mininine, this is evaluated by manually translating it to the following:

        start_context( newNumber( 10 ) )( newNumber( 5 ) )( newWord( 'output' ) )( newNumber( 100 ) )( newWord( 'output' ) )

Notice that there is a one-to-one correspondence between the source code ( syntax ) and what it does ( semantics ).

The result of evaluating this expression is 

        15
        115

In Nominine, which is interpreted, an expression is parsed into a list of objects,
and then there is a loop that gives each object as the parameter of the result of the previous calculation.

In JavaScript, the loop might look something like:

        current_result = start_context
        for ( parameter in parse( source_code ) ) {
          current_result = current_result( parameter )
        }

It is a bit like one of those bouncy contraptions that people use to maim themselves on Youtube.

Notice that **current_result** is initialized with **start_context**.


<hr>

Start contexts
--------------

Start contexts represent the current scope.
This is where new variables are set and objects are thrown.

Every time a new local scope is created, such as on function invocation,
a new start context is created and linked to the parent start contexts.
The start contexts form the stack of Nominine.

As Nominine expressions are paths, all of these paths start implicitly with the start context that constitute the local scope.
This way one can get access to variables.
Start contexts also provide a number of methods that will be described later.

<hr>

Words are objects
-----------------

Even though words play an important and special role in Nominine,
they are just normal object.

Fetching the property associated with a word is like calling a function with a word as the parameter.

The path

        ( a b c )

would therefore translate to the following ( translated Mininine expression ):

        start_context( newWord( 'a' ) )( newWord( 'b' ) )( newWord( 'c' ) )

In this example **a** would be a variable in the current scope. **start_context** object, representing the current scope,
would behave like it had an attribute named 'a'.

<hr>

Literals
--------

In Nominine there are the following literals and syntax elements:

- Words:

        some-word

- Numbers:

        123.456

- Strings:

        'this is a string'

- Expressions:

        ( this is an expression )

- Quoted expressions/list:

        [ this is a quoted expression ]

Notice that quoted expressions and lists are the same thing.

<hr>

Parameters
----------

Given the expression ( pseudo code ):

        a.b( 123 )

The equivalent in Nominine is

        ( a b 123 )

This is really a special case, because 123 is a literal.
In order to have a path to fetch a parameter such as ( pseudo code ):

        a.b( c.d )

on must write in Nominine

        ( a b ( c d ) )

to make sure that the result of 'a b' receives the *result* of 'c d' and not the word 'c'.
One uses parenthesis to access the start-context object which represent the scope.

This expression could be translated into something like ( translated Mininine expression ):

        start_context( newWord( 'a' ) )( newWord( 'b' ) )(
          start_context( newWord( 'c' ) )( newWord( 'd' ) )
        )

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

This expression could be translated into something like ( translated Mininine expression ):

        start_context( newWord( 'f' ) )(
          start_context
          ( newWord( ':' ) )
          ( start_context( newWord( 'a' ) )( newWord( 'b' ) ) )
          ( start_context( newWord( 'c' ) )( newWord( 'd' ) ) )
        )

Notice that every left parenthesis in the source gets translated into a **start_context**.

<hr>

Adding features
---------------

In order to turn Mininine into a full fletched programming language,
all one has to do is add more types and more properties to those types.

Adding all the different features is not trivial, because features does not stand completely on their own.
Nominine can be extended as easily as Mininine and Nominine already has a lot of useful features.


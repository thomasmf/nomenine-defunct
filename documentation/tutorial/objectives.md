---
layout: tutorial
---


Objects
-------

Nominine is built using a single type of building-block. This building-block is the object.


A Nominine object has both properties similar to functions in FP as well as properties similar to objects in OOP. An object is
a function that has state, somewhat similar to what you get when using static variables in a C function. Unlike C functions,
objects are created at runtime.

Also an object can be seen as closure, where the state is the closed variables. Except there is no scope structure. The object
is simply a flat struct. Pseudo code:

        struct object: {
          objective
          state
        }

The state of an object is simply called 'state', while the procedural part of the object is called the 'objective'.

This is very close to the traditional definition of objects as having identity, state and behavior. It is common, I believe,
to define behavior as a set of methods, but in Nominine behavior is just this single procedure.

Identity is also necessary, but that is a separate issue.

<hr>

General vs specific model
-------------------------

There are two models here that I am trying to explain.

First there is the model where objects have objectives. This model has no syntax and the semantics are completely general to the extent
that there are no semantics either.

Then, in order to use this model, one has to add some level of predictability through the use of a common protocol. This common
protocol is the implementation of Nominine, the specific model.

The specific model introduces noticeable semantic structure, and by sheer luck of discovery, there is a wonderful mapping between
semantics and syntax.

It is difficult to convey the idea that the specific model is somewhat perfect or complete( not in *that* sense ), because it involves
seemingly design decisions. Decisions that others surely disagree with.

But I want the reader of this to understand how the specific model is not really limiting, and whatever X one might want to implement
in the development environment, can be added as easily as X and any supporting features can be added to any development environment.

I believe that the specific model follows from the general model. This is difficult to argue. The less scientific path is to give
examples of how awesome the whole Nominine programming language is. I'm trying to do a little bit of both.

<hr>

Objectives
----------

*It is difficult to discuss in a meaningful way within the general model. Therefore some of the following information, but not everything, is dependent on specifics in Nominine.*

An objective is a special procedure both with regards to its interface to the outside world as well as its expected behavior.

In C syntax, an objective can be defined as a function with the following signature:

        void objective( context ) ;

An objective observes and modifies its context, which is passed as the only argument.
The returning of a result in the general model does not have the significance it has in a pure functional language.
In the specific model **result** is used in the evaluation model.

The context can be any object, but it is practical to have a more specific definition.
In Nominine, context itself is contained in a task object.
The result is contained in the task object in addition to other stuff.

The definition of the context is ( pseudo code ):

        task : {
          reference action ;
          context {
            closure closure ;
            reference this ;
            reference that ;
          } context ;
          reference result ;
          task next ;
          task exit ;
        }

To learn more there is always the source code.

<hr>

What does the objective do?
---------------------------

The task of the objective is to interpret the context and modify it accordingly.
For example if the context describes one object passed to another object,
the objective will first figure out if there is a rule for the specific situation, and if there is, carry out that rule,
producing the expected result.

Note that objectives are not sets of rules.
They are general procedures,
but they do tests on the context to determine what to do or not to do. 

The objective may also have to delegate interpretation to other objectives.

In the specific model, the objective always deals with these kind of interactions between object.
Results are produced and sometimes there are effects.

<hr>

Syntax and semantics
--------------------

Nominine has simple syntax and semantics. A generic expression can look like:

        a b c d

Nominine objects can be viewed as functions, therefore expression can be expressed using standard functional syntax in the
following way

        ( ( a( b ) ) ( c ) )( d )

Notice how the result of **c** applied in the context of `a b` creates the context where **d** is applied.
**d** is applied on the result of the preceding expression.

One can view an object as a data-structure when it sent from one context to another,
but when it is used, it is treated like a function.

Objects are used by *giving* them another object.
This other object is part of the context to the objective.
One can view the other object as the parameter to the object resulting from the previous part of the expression.

Expressions in Nominine are usually lists of objects.
The evaluation model of Nominine is simply: call the result so far with the next object as parameter.

The model is more general than what is used in Nominine.
In theory, objects could receive symbol objects that in turn are combined to words and literals.
Quoting could be dealt with locally to avoid having an extra set of parenthesis.

Instead I have chosen more traditional solutions both for efficiency and to enable gradual implementation.
The beauty of the underlying model is that adding such features would not require a rewrite but simple and extension of existing stuff.

Ultimately every object and class of objects can have their completely independently defined language.
I am not going in that direction with Nominine.
I am going for "predictable".

<hr>

Start-contexts and sub-expressions
----------------------------------

*In Nominine, expressions are objects. When an object receives an expression, the object first evaluates the expression, then it sends the result to itself.*

The following expression adds **a** and **b**.

        ( a + ( b ) )

There are two expressions here. Each expression have an implicit object that starts the expression. This object is called
the start-context. The start-context represent the current scope.

Given the word **a** in the beginning of the first expression, the start-context will return an object which is associated with
that word. In this case, the object is some number.

**+** is also a word and it is associated with a method.

Notice that the second expression is necessary because the method `a +` does not know about the other objects in scope.
The second expression also has a start-context. This start-context represent the same scope as the previous start-context.
**b** is fetched from scope and `a +` gets the result of the second expression as parameter.

Any start-context will return none-word objects.

        ( 1 + 2 )

The number 1 received by the context is not a word object so it is returned and thereafter receives the **+** in the next step.

<hr>

This and that
-------------

**this** and **that** have special meaning.

**this** is the object operated on by a method. Also functions have **this** defined.

**that** is the parameter. When using methods, you have the following form:

        ( <this> <some-method-name> <that> )

Functions have the following form:

        ( <some-function-or-function-name> <that> )

It is also possible to define forms such as:

        ( <this> <some-word> )

Ultimately, everything is on the form:

        ( <this> <that> )

<hr>

Object-context
--------------

The receiver of an expression makes sure that the expression is evaluated, and the result is dispatched in the same context.

The start-context of a sub-expression delegates dispatch of words to the object receiving that sub-expression.

A start-context that represents an object in this way is called an object-context.
The start of a code block will not have object-context, but all sub-expressions will.

Notice that only words will propagate to the object.
Other objects will be treated the same way as in start-contexts, that is, they will be returned.

In an object-context one can view the object as an extension of the scope.
All the properties in the object, associated with words are available in the start-context.

<hr>

Imperatives
-----------

An imperative is an expression which result is discarded.

        ( i += 1 .)

Imperatives uses the **.** punctuation.

Object context is often used with imperatives. This is similar to a code block or a "with"-statement.

        ( some-object ( some-method-1 ( some-parameter-1 ) .) ( some-method-2 ( some-parameter-2 ) .) )

Both **some-method-1** and **some-method-2** are dispatched at **some-object** because of object-context.

The result of the main expression is **some-object** because the sub-expressions are imperatives.

<hr>

Briefly on parameters
---------------------

Nominine only uses single parameter functions/methods.

There are ways to use the single parameter as multiple parameters,
and I have chosen to have **tuple** objects to pass multiple parameters.
In addition to tuples, there is a mechanism available to the programmer as **struct** and **param**
that turns a tuple into an object with named properties representing the elements in the **tuple**.

The following expression calls **some-function** with the parameters 1, 2 and 3. This is similar to "some_function( 1, 2, 3 )" in C.

        ( some-function (: 1 2 3 ) .)

The following code defines a function with two parameters, **x** and **y**. 

        fun (: 'average' ( param (: (: 'x' ( number ) ) (: 'y' ( number ) ) ) ) [
          that x + ( that y ) / 2
        ] )

To use **average**:

        ( average (: 10 20 ) )

The result is 15.

Notice that **param** takes as parameter a set of tuples of the form **string** and **type**.

Notice also that tuples are sets, and sometimes it is convienient to use tuples as regular sets.

As a comparison, the following is a single parameter function.

        fun (: 'square' ( number ) [ that * ( that ) ] )

It is used like this:

        ( square 5 )

<hr>

References and noun-phrases
----------------------------

Nominine has references. When programming in Nominine, one does not have to think about references all the time, but they
are there and they can be useful for controlling certain aspects of code.

It is also important to understand references to understand typing of set elements, variables and parameters.

References are typed but they can have the type **any**.

*I have made a soft decision to avoid references to references. I hope to solve certain problems with other mechanisms in the future.*

A variable in scope is a reference.

        var (: 'a' ( number ) 45 )

Numbers are mutable, but to make **a** reference a completely different number object, one must use a noun phrase. Noun phrases
are constructed using the **!** punctuation.

        ( a ( 55 !) .)

Now, **a** represent a different number object.
The following statement will have no effect because **a** is a number object and not a string.

        ( a ( 'this is a string' !) .)

It is possible to detect that this statement fails.

Notice that, usually, even in languages where "everything" is an object, numbers are not regular objects.
Usually numbers are exclusively "moved" using assigns, and never by reference.
In Nominine, however, one has to deal with the difference between referencing and copying state ( assignment )
also when it comes to numbers.

<hr>

Error-handling
--------------

        ( a ( 'this is also a string' !) else [ some-error-object throw ] .)

Nominine uses decisions on **none** to detect failures. To handle errors in a manner similar to exceptions in other languages, one can
use **throw** and **catch**.

Notice that **throw** and **catch** are resumable general mechanism used also to implement co-routines and similar features.
To terminate execution, use **exit**.

Built-ins, currently, does no throwing or other form of error handling.
All failures silently result in nothing.

In the future, when implementing I/O, there will be a logging stream, such as "stderr".

<hr>

Using objects as structs
------------------------

*This is only an issue if doing modifications to the source code of the Nominine interpreter.*
*This section uses the word "struct" to mean structs in C, not __struct__ types in Nominine.*

In the core of Nominine it is necessary to make assumptions ( that hold ) about the type of an object, so that interaction
between objects at the low level does not require invocation of objectives.

E.g. if two numbers are to be added, knowledge about the internal structure of a number object is used to fetch the two float
numbers directly and adding them.

In other words, one sub-program may interact with the state of an object directly without going through that objects objective. In
practice, this means treating that object as a simple struct. Prior to doing this, it is important to verify/determine the type of
that object. To learn more about this, look at class id's and references in the source.

<hr>

Inheritance
-----------

Nominine uses an inheritance mechanism that fit well with objectives.

Instead of a class inheriting the properties of another class, an object can *represent* another object.

If A inherits B, then all instances of A will contain an instance of B.
If an instance of A cannot interpret a context, it simply delegates the interpretation to its instance of B.

There are also other variations of this mechanism in the implementation.
In general it is about delegating responsibility between objects.

One of the benefits of this type of inheritance is that it allows for seamless specialization of built-in objects.



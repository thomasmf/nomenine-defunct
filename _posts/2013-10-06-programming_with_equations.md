---
layout: post
title: Programming with equations
---

Disclaimer: I do not claim that the following is in anyway new. Actually it's from 2005 but this is my first implementation.

This mechanism is implemented in my programming language Nominine,
but it can be applied to any language.

I do not use Nominine syntax here. Everything here is pseudo code.
The specifics for Nominine is [here](/documentation/tutorial/statics.html).

Equations
---------

Here is an assignment:

        a = b + 1

Here is an equation:

        a = b + 1

The assignments just calculates 'b + 1' and then copies the result into 'a'. 

The equation, on the other hand, says that 'a' is _always_ equal to 'b + 1'.
From a programmers point of view math is somewhat magical.

This blog post describes a simple mechanism to get some of that math magic into programming.

I call this mechanism a _static dependency_.

( This is not the kind of static dependency that has to do with makefiles and linking,
but it is not completely different from it either.
I have used the term for some time and I'll stick to it until something better pops up. )

Also I'm not claiming that any of this is new ( unless it is ).

Problems I do not solve
-----------------------

In the equation above, the following is also implicitly true

        b = a - 1

My solution does not provide this automatically.
One needs to solve the equation both for 'a' and 'b' and create one static dependency for each variable.

Static dependencies vs functions
--------------------------------

It is possible to use functions to do something similar to static dependencies ( pseudo code ).

        a() : { b() + 1 }

but when solving the equation for 'b' and defining it as a function

        b() : { a() - 1 }

one gets an endless recursion.
Static dependencies handle this kind of circularity automatically.


Both state and definition
-------------------------

The key to static dependencies is that they have both a state and a definition.

In the static dependency ( more pseudo code )

        a ==> b + 1

'b + 1' is the definition, while the state is like a cache of that calculation.

When using 'a', the state will be used directly without using the definition to compute it.

'a' will be recalculated iff anything the definition of 'a' depends on *changes*.

In other words 'a' will be recalculated if the cache is invalidated.

Connections
-----------

A static dependency has a list of other objects it depends on, in-dependencies,
as well as objects that depends on it, out-dependencies.

The in-dependencies contains all the things necessary to create the state.

The out-dependencies contains all the things that uses that state.

It is possible to build in- and out-dependencies manually,
but it is much better if the programming language builds these automatically
based on how objects are used in the definition of the static dependency.

Propagating change
------------------

Whenever the state of a static dependency changes,
all out-dependencies will be forced to reevaluate their definitions,
and as a result _maybe_ their state changes and the change propagates onwards.

An example
----------

Here is an example using the equation above.
Notice that it is solved both for 'a' and 'b'.

        a ==> b + 1

        b ==> a - 1

Lets say the initial state of 'a' and 'b' is 'undefined'.

Lets then do

	a = 9

The state of 'a' was 'undefined' and now it has become 9.
This means that the state has changed.
Since 'b' is dependent on 'a', 'b' needs to be recalculated.

The state of 'b' now changes from 'undefined' to 8.
Since 'a' is dependent on 'b', 'a' needs to be recalculated.

At this point it may seem like endless recursion has kicked in.
However, when 'a' is recalculated the result is, 9, the same as it was previously.

Continuing recalculation at this point will add nothing.
When recalculation no longer produces changes, the recursion stops.
Lets call this convergence.


Circularity
-----------

Static dependencies transforms the problem of infinite recursion into a convergence problem.
Any system that converges can be expressed regardless of whether it is circular or not ( this is my guess ).

Notice that there are systems that will not converge.
Such as infinity

        inf ==> inf + 1

or alternating states

        eh ==> not eh


Not really math
---------------

Static dependencies just mimic some of the behavior of math.
It is not math.

On a positive note, static dependencies work with **any** object including user-defined objects, not just numbers.




Optimizing almost-constants
---------------------------

Static dependencies lets a runtime compiler optimize expressions that are almost-constant
as if they were constant.

Instead of having to guarantee or prove that a code transformation preserves every dependency,
one can simply assume it and model the transformation as a static dependency.
In other words, if whatever is assumed to be true no longer is, then the transformation is redone automatically.

Often there are global parameters in a program,
and these parameters may end up being used, for example, inside critical loops.
Such parameters can be almost-constants.

Also, it is worth to mention out-of-band changes.
If two processes run at different paces and they share some state,
then chances are one process uses data often while another process changes that data seldomly.
Using static dependencies such data can be treated as a almost-constant.

To clarify, almost-constants are effectively constants until they change.
It is dynamics ( almost ) for free.
Generally speaking almost-constants are values or results of expressions that are used more
often then their result changes.


Invariants
----------

The following static dependency describes an invariant:

	a ==> f( a )

'f' can be seen as a type.
It decides what part of the object 'a' should be considered structure, what can not change, and what should be considered state, what can change.

Example implementation of 'f':

	f( old_a ) : {
	  var new-a
	  new-a.state = old-a.state
	  new-a.structure = some-hardcoded-data
	}

Here a.state could be changed, but if one tries to change a.structure, the static dependency would cause it to revert to some-hardcoded-value.

Within a static dependency it is not necessarily possible to guarantee that such an invariance is correct,
because the evaluation order may vary.
It may be possible to deal with this problem automatically, but in my implementation I don't even try to do that.


Circularities in programming languages
--------------------------------------

It is common to encounter circularities when designing programming languages.
Because these tend to be design specific, I will use the eval function as an example.
The eval function will always have this circularity I'm trying to explain.

Imagine implementing 'eval' in terms of the language itself.
I'm not talking about _an_ eval function but _the_ eval function.
So, in order to evaluate an expression,
one must also evaluate the definition of eval.

A decent illustration of this recursion is ( though it is not correct, but you get the point ):

	eval( expression )	-->	eval( "eval( expression )" )

This will never terminate.
However, using a compile function instead, we know that it terminates.
It is the same as compiling a compiler with itself.

The problem is that during compilation information is lost.
This loosing of information is roughly related to how an interpreted language is usually more "dynamic" then a compiled language.

Static dependencies can be used to solve this problem in a satisfactory way.
They can be used to build programming languages that behave consistently as if they are being interpreted by themselves.
I'm not talking about a reflective tower but a reflective plane.
A single instance of a self-interpreting language.

The trick is ( in this example ) to replace the eval function with a compile function coupled with a static dependency.
The static dependency will maintain information on what is compiled.

	compile ==> compile( "source code" )

When the compile function is used, the compiled version of it is used so that the circularity problem with eval does not occur.
Every time something that the source code is dependent on changes,
the compile function will recompile itself so that it behaves like eval.

This kind of system will behave as if it is interpreted even though it uses runtime compilation.
Also it is worth to mention that this can also be very highly optimized as I discussed in the section on almost-constants.
Optimization techniques that apply to JIT compilers also apply to this kind of system.

Notice that the eval/compile example is an oversimplification.
In practice this kind of system would have a lot of interconnected static dependencies to model all the different components that are usually treated as built-ins.
Also there would be a bootstrap phase.


Higher order functions
----------------------

Look at the following ( pseudo code ):

        lambda ==> lambda( [ args:map, def:code ], lambda.implementation )

'lambda' is a function that takes a map from argument name to argument type as its first argument,
and a code block with an implementation as its second argument.

'lambda' is a function that returns a function.

Notice that 'lambda' is here defined in terms of itself using a static dependency.

It is perfectly possible to define higher order functions this way using static dependencies
as long as they converge and have an initial state. 

The initial state is like a bootstrap state that is defined in terms of something other than itself.
It is not shown in this example.

After the function has been bootstrapped, the static dependency can be seen as a constraint of that function object.
It is then possible to modify the function within these constraints.
This is the same as I mention in the section on invariants.

To change 'lambda' do an assignment:

        lambda.implementation = { new implementation of lambda }

Notice that this does not change the definition of 'lambda' but only its state.

The assignment will cause the new function first to be built in terms of the old definition,
then again in terms of its new definition,
and so on until rebuilding 'lambda' produces a function object identical to the one that built it.



The state of static dependencies in Nominine
--------------------------------------------

Static dependencies currently only work with numbers, sequences and user defined objects, but not with string or functions. The reason, if I remember correctly, is that there are no assignments on strings or functions at this point. Objects can have properties that are static dependencies.

There are first order static dependencies that can be inserted directly into generated nominine code. Nominine does not compile at this point, so the benefit of this is limited to mabe simplifying the expression of some algorithms.

The current version of Nominine is scrapped. I am rebuilding it from scratch.
I have, however, fixed up the documentation, unit tests and examples so that it is mostly consistent.
It is not an incomplete project, it's just not a very good one.



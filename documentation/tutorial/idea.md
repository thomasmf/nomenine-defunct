---
layout: tutorial
---

The idea
========


<hr>

Objects
-------

Nominine is built using a single type of building-block. This building-block is the object.

A Nominine object has both properties similar to functions in FP as well as properties similar to objects in OOP.
An object is a function that has state.

In practice an object is implemented as a struct that has a procedure and some state. Pseudo code:

        struct object {
          objective
          state
        }

The state of an object is simply called 'state', while the procedural part of the object is called the 'objective'.

This is very close to the traditional definition of objects as having identity, state and behavior. It is common, I believe,
to define behavior as a *set of methods*, but in Nominine behavior is just this single procedure.


<hr>

Objectives
----------

An objective takes a context object as its only argument.

The task of the objective is to interpret the context and modify it accordingly.

Basically an objective is an action and the context object is what the action is operating on.


<hr>

Contexts
--------

In Nominine, which is an object oriented programming language,
contexts contain _this_, information about scope, information about parameters as well as information about tasks and continuations.
Contexts also contain a _result_.

Nominine uses only one type of context, but objectives can be divided into roughly three categories:

- primitive actions that do whatever they need to do
- methods that behave like regular methods
- user-space objects that do dispatch and lookup identifiers

Technically they are all the same, for example user-space-objects behave like methods where the method does dispatch and lookup identifier.

From the viewpoint of functional programming, objects in Nominine are higher order functions.


<hr>

There is more
-------------

Actually there is not, but please read the next chapter for a better explanation of how Nominine works.


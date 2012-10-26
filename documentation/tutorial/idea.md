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

An objective is a special procedure both with regards to its interface to the outside world as well as its expected behavior.

In C syntax, an objective can be defined as a function with the following signature:

        void objective( context ) ;

An objective observes and modifies its context, which is passed as the only argument.

The context can be any object, but it is practical to have a more specific definition.

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

Note that objectives in Nominine takes a task object as a parameter.
This task object contain a context.

<hr>

What the objective does
-----------------------

The task of the objective is to interpret the context and modify it accordingly.

Typically an objective will set the result to some new or existing object
or delegate the responsibility of dealing with the context to some other object.


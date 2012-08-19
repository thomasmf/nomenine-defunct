---
layout: tutorial
---

Output
------

There are currently no output functionality other then those used for debugging.

In the future, there will be IO based on sets and throw/catch.


Delog
-----

**delog** outputs a line of limited info about the object to which it is passed.

        ( 0 delog .)

will output something like

        ::::			[e6c:NUMBER 0.000000]

The four ':'s and tabs are just to make it stand out and line up nicely.

The three digit hex number is part of the objects address. It is used to determine if two objects are the same object or not.

Lastly there is the class name of the object. This only works for built-ins. User-defined classes will typically have 'IS' or 'HAS'.

The last part, '0.000000' is the value of the number. Only numbers and strings have this state data. It is possible to add
nice debug logging for other types of objects, but I have not done so.

The result of **delog** will always be the object to which it was sent.
In practice, this means that one can insert **delog** at any point in the code without it having any effect on the code other than the outputting of the data.


Tron and troff
--------------

To get a more detailed view of what is going on one can use **tron** and **troff**.

**tron** turns on trace output, while **troff** turns it off.

These are not stack traces. There is one line for each task that is carried out. As mentioned before, each task can be considered
a dynamic dispatch, where an objective does some stuff on a context.

Consider the following example. The delog will output the string object "hello world". Tracing is on during the dispatch and
operation of **delog**. Then it is turned off before the punctuation.

        ( 'hello world' tron delog troff .)

The output will look like this:

        *	[446:LISTITERATOR]            [452:REFERENCE]               [54e:WORD 'next']             [544:WORD **delog**]
        *	[437:EVALUATOR]               [64e:CLOSURE]                 [535:PHRASE]                  [53f:NONETYPE]
        *	[445:REFERENCE]               [445:REFERENCE]               [544:WORD **delog**]            [53f:NONETYPE]
        ::::			[537:STRING "hello world"]
        *	[537:STRING "hello world"]    [537:STRING "hello world"]    [544:WORD **delog**]            [537:STRING "hello world"]
        *	[446:LISTITERATOR]            [452:REFERENCE]               [54e:WORD 'next']             [540:WORD 'troff']
        *	[42d:EVALUATOR]               [64e:CLOSURE]                 [535:PHRASE]                  [53f:NONETYPE]

The trace output lines start with '\*', while the log line starts with '::::'.

Each trace line has four columns. The first is the object which objective is operating on the context. This is called the **action**.

The second and third columns are **this** and **that**.

The fourth line is the **result** as it is *after* the task is done.

When doing traces, one will notice that most dispatches start with a task where **action** and **this** are the same object.
Then during the dispatch **result** will remain **none** until a proper understanding of the context is made, and the result is set.
The reason that there are many tasks with the same result object is because objects delegate work to other objects,
for example if there is inheritance involved.

Also one can usually disregard lines where **action** is **listiterator** and then followed by **evaluator**. This are just the
evaluator moving forward in the code to fetch the next object to be dispatched. Also there are similar patterns for
evaluation of subexpressions. Over all traces can contain too much information to be useful.

The following is a digest of the previous trace, where only information about the code carried out is kept.

        ::::			[537:STRING "hello world"]
        *	[537:STRING "hello world"]    [537:STRING "hello world"]    [544:WORD **delog**]            [537:STRING "hello world"]

Notice that the trace line is a capture of the state of the task *after* the dispatch is carried out. Therefore the log line is
printed *before* the trace line.

Here is a more interesting example:

        tron
        ( 'hello world' delog .)
        troff

And here is the output:

        *	[267:LISTITERATOR]            [273:REFERENCE]               [34e:WORD 'next']             [335:PHRASE]
        *	[263:EVALUATOR]               [33f:NONETYPE]                [33f:NONETYPE]                [33f:NONETYPE]
        *	[278:REFERENCE]               [278:REFERENCE]               [335:PHRASE]                  [33f:NONETYPE]
        *	[24c:EVALUATE]                [278:REFERENCE]               [335:PHRASE]                  [33f:NONETYPE]
        *	[290:LIST]                    [290:LIST]                    [34a:WORD 'each']             [23d:LISTITERATOR]
        *	[23d:LISTITERATOR]            [23d:LISTITERATOR]            [34e:WORD 'next']             [337:STRING "hello world"]
        *	[246:EVALUATOR]               [278:REFERENCE]               [335:PHRASE]                  [33f:NONETYPE]
        *	[24f:OCONTEXT]                [24f:OCONTEXT]                [337:STRING "hello world"]    [337:STRING "hello world"]
        *	[23d:LISTITERATOR]            [249:REFERENCE]               [34e:WORD 'next']             [344:WORD **delog**]
        *	[239:EVALUATOR]               [278:REFERENCE]               [335:PHRASE]                  [33f:NONETYPE]
        ::::			[337:STRING "hello world"]
        *	[337:STRING "hello world"]    [337:STRING "hello world"]    [344:WORD **delog**]            [337:STRING "hello world"]
        *	[23d:LISTITERATOR]            [249:REFERENCE]               [34e:WORD 'next']             [3a8:WORD '.']
        *	[22e:EVALUATOR]               [278:REFERENCE]               [335:PHRASE]                  [33f:NONETYPE]
        *	[337:STRING "hello world"]    [337:STRING "hello world"]    [3a8:WORD '.']                [33e:IGNORETYPE]
        *	[23d:LISTITERATOR]            [249:REFERENCE]               [34e:WORD 'next']             [33f:NONETYPE]
        *	[224:EVALUATOR]               [278:REFERENCE]               [335:PHRASE]                  [33e:IGNORETYPE]
        *	[278:REFERENCE]               [278:REFERENCE]               [33e:IGNORETYPE]              [33f:NONETYPE]
        *	[44e:CLOSURE]                 [44e:CLOSURE]                 [33e:IGNORETYPE]              [44e:CLOSURE]
        *	[267:LISTITERATOR]            [273:REFERENCE]               [34e:WORD 'next']             [340:WORD 'troff']
        *	[258:EVALUATOR]               [33f:NONETYPE]                [33f:NONETYPE]                [33f:NONETYPE]

Some of these interactions can be optimized. Also each line represent many heap allocations. These can be optimized also.


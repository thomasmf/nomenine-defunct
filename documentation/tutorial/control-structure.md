---
layout: tutorial
---

Else and then
=============

Nominine does not have booleans. It uses none and not none to manage control flow and decision making.

<hr>

Else
----

**else** is an object method that takes a set as parameter. The set is an expression that will evaluate in the current closure iff the
object is none. The result of **else** is the result of the expression or the object.

        ( condition else [ ... ] ... )

The following expression will return **x** if **x** is defined, otherwise it will return 0.

        ( x else [ 0 ] )

<hr>

Then
----

**then** is the opposite of **else**.

**then** is an object method that takes a set as parameter. The set is an expression that will evaluate in the current closure iff the
object is *not* none. The result of **then** is the result of the expression or the object.

        ( condition then [ ... ] ... )

**else** and **then** can be chained the way one is used to chaining similar concepts in other programming languages.

The following expression will return **x** if **y** is defined, otherwise it will return 0.

        ( y then [ x ] else [ 0 ] )

<hr>

Comparison
----------

Since there are no booleans, comparisons cannot return true or false. Instead, they return, by convention, the last object
mentioned. This is useful, because it allows for chaining of comparisons.

        ( 1 < 2 )

This will return 2.

        ( 1 < ( x ) < 100 )

This will return 100 iff x is between 1 and 100.
If **x** is not with this range then the expression will return **none**.

<hr>

None
----

Notice that only **none** is none. There is no empty list, empty string, negative number or zero that is equivalent to false/none.
Everything except **none** is "true".

The following expression will divide 100 by x if x is not 0, otherwise it will divide by 0.00001.

        ( 100 / ( 0 != ( x ) else [ 0.00001 ] ) )

<hr>

Loops
-----

Nominine only has one loop construct. This is the infinite but stoppable loop.

**loop** gives a simple endless loop that must be terminated using **stop**.

To loop until **condition** is none, do:

        loop [
          ( condition else [ stop ] .)
        ]

Traditionally one uses the word "break" to do this, but Nominine uses **stop**. Also, instead of "continue", Nominine uses **skip**.

        loop [
          ( condition-1 else [ skip ] .)
          ( condition-2 else [ stop ] .)
        ]

<hr>

Errors
------

All failure in Nominine can result in unexpected behavior if not handled properly.

There is no built-in error-handling in Nominine. Built-ins fail silently. This should be fixed in the future.



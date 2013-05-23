---
layout: reference
---

Seq
===

Nominine has different types of sequences.
 - list
 - lazy list
 - tuple

Common for all sequences is that they have an **each** property that produces an **iterator**.

        ( some-seq each )

produces an iterator.

*Notice, however, that a tuple is not recognized as a sequence when passed as a parameter.*

<hr>

List
----

        [ ... ]

produces a **list**.

In addition to being a **seq**, a **list** has the **length** property.

        ( some-list length )

produces the length of **some-list**.

To append elements to a list, simply write:

        ( some-list ( some-element ) ( some-other-element ) .)

To merge elements from one list into another use the *merge* method:

        ( some-list merge ( some-other-list ) .)

<hr>

Tuple
-----

        (: 1 2 3 )

produces a **tuple** with the elements 1, 2 and 3.

Notice that a **tuple** does not classify as a **seq**.
This means that tuples cannot be given as arguments where sequences are expected.

Tuples are basically only used to handle multiple parameters.

<hr>

lazy lists
----------

        ( seq [ ... ] )

produces a lazy list.
**seq** is both the type of sequences as well as the constructor for lazy lists.

A lazy list uses the quoted expression to generate elements.
The elements are "emitted" from the generator using **yield**.



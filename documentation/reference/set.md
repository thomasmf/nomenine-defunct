---
layout: reference
---

Set
===

Nominine has different types of sets.
 - list
 - generator
 - tuple

Common for all sets is that they have an **each** property that produces an **iterator**.

        ( some-set each )

produces an iterator.

<hr>

List
----

        ( list ( some-type ) )

produces a **list** of type **some-type**.

        [ ... ]

produces a **list** of type **any**, but do not confuse quoted expressions with lists.
The elements in them do not behave the same way.

In addition to being a **set**, a **list** has the **length** property.

        ( some-list length )

produces the length of **some-list**.

<hr>

Tuple
-----

        (: 1 2 3 )

produces a **tuple** with the elements 1, 2 and 3.

In addition to being a **set**, a **tuple** has the **length** property.

        ( some-tuple length )

produces the length of **some-list**.

<hr>

Gen
---

        ( gen (: ( some-type ) [ ... ] ) )

produces a generator.
The name of the generator type is **gen**.

A generator uses the quoted expression to generate elements.
The elements are "emitted" from the generator using **throw**.

Thrown objects that are not of the given type, do not count as elements, and are not caught by the sets iterator.


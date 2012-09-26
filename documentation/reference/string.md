---
layout: reference
---

String
======

Strings can be produced by a string literal:

        'string literal'

or by the string constructor:

        ( string '...' )

or by the concatenation of strings:

        ( 'this' ' is' ' a' ' string' )

Strings are immutable.

<hr>

String
------
        ( string '...' )

produces a new **string**.

**string** takes a **string** as a parameter.

<hr>

Merge
-----
        ( 'a' + 'b' )

or

        ( 'a' 'b' )

produces the **string** 'ab'.


<hr>

To-string
-----
        ( some-string to-string )

produces a **string**.

All objects that has a **to-string** that produces a **string** is a **string**.


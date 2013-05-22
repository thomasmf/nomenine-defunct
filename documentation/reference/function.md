---
layout: reference
---

Function
========

The name of the function type is **fun**.

<hr>

Fun
---
        ( fun (: ( some-type ) [ ... ] ) )

produces a **function** takes a parameter of type **some-type**.

        ( some-function ( some-object ) )

calls a function **some-function** with the parameter **some-object**.

<hr>

Apply
-----
        ( f apply ( o ) )

produces a **function** that behaves like a method on the object **o**.
The original function is not modified.



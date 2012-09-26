---
layout: reference
---

Object
======

All objects are of **type** **any** and share a common set of properties.

Everything within Nominine is an **object**,
and all the objects visible to the programmer have the properties listed here.

<hr>

Is
--
        ( some-object is ( some-other-object ) )

produces a new **object** which is both **some-object** *and* **some-other-object**.
The new object will have the properties and state of both of these objects.

*Related types: [string](/documentation/reference/string.html)*

<hr>

Has
---
        ( some-object has (: 'a' ( some-attribute ) ) )

or

        ( some-object has (: 'a' ( some-type ) ( some-attribute ) ) )

produces a new **object** which has an attribute **a**.
If a **type** is specified, then the object refered to by the attribute can must be of that type.

**has** for objects is similar to **var** for contexts.

*Related types: [context](/documentation/reference/context.html)*

<hr>

Does
----
        ( some-object does (: 'm' ( some-function ) ) )

or

        ( some-object does (: 'm' ( some-type ) [ ... ] ) )

produces a new **object** which has method named **m**.

*Related types: [context](/documentation/reference/context.html)*

<hr>

Defs
----
        ( some-object defs (: 'c' ( some-object ) ) )

produces a new **object** where the **c** will always refere to **some-object**.

**defs** for objects is similar to **def** for contexts.

*Related types: [context](/documentation/reference/context.html)*

<hr>

Then
----
        ( some-object then [ ... ] )

evaluates the quoted expression iff **some-object** is not **none**.
The result is either **none** or the result of the quoted expression.

<hr>

Else
----
        ( some-object else [ ... ] )

evaluates the quoted expression iff **some-object** is **none**.
The result is either **some-object** or the result of the quoted expression.



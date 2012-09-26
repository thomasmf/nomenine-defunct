---
layout: reference
---

Type
====

Types are used to discriminate between objects, for example as function parameters.

There are multiple ways to construct types:
 - fact
 - cat
 - struct

<hr>

Fact
----
        ( fact ( some-object ) )

produces a **type** where responds by **some-object** is signed.

Later, the **fact** can be used to denote, for example, function parameters that should only match objects produced in the specified way.

"fact" is short for "factory". **fact** lets you determine if an object was produced by a particular factory.
Usually the parameter is a function:

        ( fact ( fun (: ( some-type ) [ ... ] ) ) )

produces a type object which produces instances when given an object of **some-type** as parameter.

<hr>

Cat
---
        ( cat [ ... ] )

produces a **type** where the quoted expression is used by the underlying dispatch mechanism to determine if an object is of
the particular type.

        ( var (: 'x' ( cat [ 0 < ( that ) ] ) 123 ) .)

produces a variable that can only contain something that is greater than zero.

<hr>

Struct
------
        def (: 't' ( struct (: (: 'i' ( number ) ) (: 's' ( string ) ) ) ) )

produces a **type** which instances has a state with a **number** **i** and **string** **s**.

Additionally the type can construct instances by giving the correct objects in the correct order as parameters.

        ( t (: 123 'abc' ) )

produces an instance of the type **t**.



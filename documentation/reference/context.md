---
layout: reference
---

Context
=======

All expressions start with a **context** object.
The **context** contains information relating to the current **task** in
addition to functionality for altering some of this information.

<hr>

This
----
        ( this )

produces the object to which the current task is applied.

**this** is usually used in methods where it behaves like the keyword "this" of "self" in other OO languages.

*See example on __that__*

*Related types: [object](/documentation/reference/object.html), [function](/documentation/reference/object.html), [type](/documentation/reference/type.html)*



<hr>

That
----
        ( that )

produces what acts as a parameter to the current code block.

**that** is the parameter of a function or method.

The following example will define the object **test-object** that has a method **test-method**.
The method will write **this** and **that** to console.

The last line calls the method.

        var (: 'test-object' ( new
          does (: 'test-method' ( any ) [
            console write ( this ) newl ( that )
          ] )
          noms (: 'to-string' [ 'this is the value of this' ] )
        ) )

        ( test-object test-method ( 'this is the value of that' newl ) .)

The output of the example is

        this is the value of this
        this is the value of that

*Related types: [object](/documentation/reference/object.html), [function](/documentation/reference/object.html), [type](/documentation/reference/type.html)*


<hr>

Var
---

**var** defines a new variable:

        ( var (: 'a' 123 ) .)

Here **a** is defined to be the number 123.

**var** will return the **context** in which it is used.
The above example is therefore equivalent to:

        var (: 'a' 123 )

<hr>

Defun
-----
        ( defun (: 'test-object' ( number ) [ that * ( that ) ] ) .)

defines a new **function** that takes a **number** as parameter and returns the square of that **number**.

**defun** is short hand for:

        ( var (: 'test-object' ( fun (: ( number ) [ that * ( that ) ] ) ) ) .)

**defun** will return the **context** in which it is used.
The above example is therefore equivalent to:

        defun (: 'test-object' ( number ) [ that * ( that ) ] )

*Related types: [function](/documentation/reference/object.html), [type](/documentation/reference/type.html)*

<hr>

Defact
------

**defact** is used to define new types.
Type in nominine can both be used to construct objects as well as discriminating between objects.

        ( defact (: 'test-type' ( number ) [ that * ( that ) ] ) .)

defines a new **type** which constructor takes a **number** as parameter and returns the square of that **number**.
The object produced is "signed".
If, for example, a function is defined to take **test-type** as parameter, then an ordinary **number** will not do.
The parameter object in that situation must be constructed using the specific **test-type** factory.

**defact** is short hand for:

        ( def (: 'test-object' ( fact ( fun (: ( number ) [ that * ( that ) ] ) ) ) ) .)

**defact** will return the **context** in which it is used.
The above example is usually equivalent to:

        defact (: 'test-object' ( number ) [ that * ( that ) ] )

*Related types: [object](/documentation/reference/object.html), [function](/documentation/reference/object.html), [type](/documentation/reference/type.html)*

<hr>

Nom
---
        ( nom (: 'test' [ ... do something here ... ] ) .)

defines a new **word** which is equivalent to writing the quoted expression as an expression,
except that the quoted expression is evaluated in its own context.
Static scoping and closures apply.

**nom** will return the **context** in which it is used.
The above example is usually equivalent to:

        nom (: 'test-object' [   ] )

*Related types:*

<hr>

Loop
----
        ( loop [ ... ] .)

**loop** evaluates the quoted expression repeatedly like in a loop.
The loop will not stop the word **stop** is used.

**loop** will return the **context** in which it is used.
The above example is usually equivalent to:

        loop [ ... ]

The following example writes all the objects produced by the iterator **some-iterator** to console.

        loop [
          console write ( iterator next else [ stop ] )
        ]


*Related types:*

<hr>

Return
------
        ( return ( some-object ) .)

**return** terminates the evaluation of a function or method, and sets the result of that function.

*Related types:*

<hr>

Stop
----
        ( stop )

**stop** terminates loop.

*Related types:*

<hr>

Catch
-----
        ( catch (: ( some-type ) [ ... ] ) )

creates a mechanism where objects thrown in sub-contexts of the specified type causes the evaluation of the quoted expression
with the thrown object as parameter.

The object returned by the quoted expression becomes the return value of the **throw** that caused it.

*Related types:*

<hr>

Throw
-----
        ( throw ( some-object ) )

Throws an object from a context so that it may be caught by a **catch** in a super-context.

The return value of **throw** is the value produced by the **catch**.

*Related types:*

<hr>

Use
---
        ( use ( some-object ) .)

**use** integrates an object, given as parameter, into the current context's scope.
As a result **some-object** plays the role of a first-order module.

**use** is meant to be used with module factory object to fetch modules.

        ( use ( module 'modules/some-module.nom' ) .)

loads some-module and makes the terminology it defines available in the current scope.

*Related types:*


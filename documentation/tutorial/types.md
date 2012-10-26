---
layout: tutorial
---

Types
=====

Nominine has three different mechanisms for building types.
These meta types are:

- **struct**, used for building simple structures.
- **fact**, used for building *factories*.
- **cat**, used for building *categories*, which is used for dependent typing.

Types serve two purposes in Nominine.

First of all they are used to discriminate between objects.
If, for example, a function has a parameter type **string**,
that functions action will only be triggered by giving a **string** as parameter.
Similarly **set** objects in Nominine have element-type.
It is possible to build **list** and **gen** ( generator ) objects that can only contain/throw a particular type of object.

Secondly, types are used as *factories* to build objects.
However, only **struct** and **fact** objects can be used to build other objects.
**cat** objects are only used to discriminate between objects and never as factories.

*There are currently no classes in Nominine. __fact__ is the closes to a class at the moment.*

<hr>

Struct
------

Struct is a meta type or *type factory*, that creates factories for objects that contain only attributes.

        ( struct (: (: 'x' ( number) ) (: 'y' ( number ) ) ) )

yields a type that can be used to build objects with **x** and **y** properties both being numbers.
It is useful to give names to **struct** factories.

        def (: 'vector' ( struct (: (: 'x' ( number) ) (: 'y' ( number ) ) ) ) )

defines **vector** to be a **struct** factory.

        ( vector (: 4 7 ) )

yields a new **vector** object that has properties **x** equal 4 and **y** equal 7.

Notice that __struct__ takes the same parameter as __param__.
This is no coincidence. **struct** takes a **set** of **tuple** objects.
Each **tuple** object has a name that will be used as the name of the attribute,
and a type that will be used as the type of the attribute.

<hr>

Fact
----

**fact** is used to build factories.
A factory is very much like a constructor.
It builds an object given some parameters.
In addition to this factories sign the objects produced.

Usually, one uses functions to do the actual object building.
Factories just wrap around the function, or any object for that matter, and sign produced objects.

        ( fact ( fun (: ( number ) [ that * 2 ] ) ) )

yields a type that can construct numbers that are even.
It is useful to give names to **fact** objects.

        def (: 'even' ( fact ( fun (: ( number ) [ that * 2 ] ) ) ) )

Now, the **even** can be used to build new objects:

        ( even 3 )

yields an object that is **even** and equal to the number 6.
One can than build a function that only takes **even** numbers:

        defun (: 'f' ( even ) [ ... ] )

*Notice that this is really a bad example, because even if an __even__ number is guaranteed to be even when it is created, it is possible to change it afterwards. Also a number can be even without being __even__.*
There is a simplified way to build factories in the same style as **defun**.
It is called **defact** and it defines a named factory.

        defact (: 'my-class' ( some-parameters ) [ ... ] )

There are more interesting and useful factories to build.

        defact (: 'account' ( param (: (: 'holder' ( string ) ) (: 'balance' ( number ) ) ) ) [
          that
          does (: 'deposit' ( number ) [ this balance += ( that ) ] )
          has (: 'e-mail' '' )
        ]

defines **account**.
**account** keeps track of the balance of an account, stores the name of the account holder, and keeps an optional e-mail address.

**does** and **has** are new to this example.
These are *object methods*.
All objects have these methods.

**does** takes the same parameters as **defun**, but instead of defining a function it creates a method.

**has** takes the same parameters as **var**, but instead of creating a variable it creates an attribute.

It is important to understand that, when operating on the level where we change the structure of objects by adding properties,
objects are immutable. One can only really change the state of an object, and not its structure.

**does** and **has** does not *append* properties to an existing object, but create a new object that **is** the old object
while in addition having a new method or attribute.

Notice that the body of the **account** factory starts with **that**.
That is a structure with properties **holder** and **balance**.
It is created by **param** and the passed to the function as the parameter.
Instead of building this structure over again, we just build a method and an attribute on top of it.
This is a useful pattern in Nominine.

To use **account** one can write:

        def (: 'bobs-account' ( account (: 'Bob' 100 ) ) )

To create an account for Bob with a balance of 100.
To set the email, one can write:

        ( bobs-account e-mail ( 'bob@aol.com' !) .)

Notice the use of **!**.
Attributes behave like variables that are connected to an object instead of a scope.

        ( bobs-account deposit 40 .)

adds 40 to bobs balance.

<hr>

Cat
---

**cat** is a category factory.

A category is something that discriminates between objects on other criteria than where the object is produced.
These criteria are user-defined.

Cat takes a quoted expression as its parameter.
This expression is evaluated in order to test if an object matches that category.
If the expression yields **none**, there is no match.
If the expression yields some other object, then that object becomes the parameter.

That last sentence is important.
Categories are not *just* discriminators, but also filters.

        ( cat [ 0 < that ] )

yields the category of all positive numbers.

        ( cat [ sort ( that ) ] )

yields the category of everything that can be sorted, and the object one gets out of it, is that thing is already sorted.
A bad example:

        defun (: 'positive' ( cat [ 0 < that ] ) [ that ] )

can be used as

        positive ( x ) else [ fail ]

If **x** is not positive, **positive** will fail and this failure can be tested for using **else**.

Notice that categories are not invariance.
Even if a number passes the **positive** test, it may later become negative.
Therefore it is not really useful at this point to mix categories and factories.
Categories can not be used as factories.



---
layout: examples
---

User class
----------

The following example implements a user defined class named 'vector'.
The 'vector' class has two attributes 'x' and 'y' and a method named '+'.

In addition to this, 'vector' also has a constructor that takes two parameters.

*Nominine currently lacks good mechanisms for defining user classes, so the techniques used here will be obsoleted in the future.*

In order to build a class that has a constructor, one simply builds a class that *is* also a function.
That way the result can be used both as a class to discriminate objects on type
and as a factory function to build new instances.

        const (: 'vector' (
          class [
            has (: 'x' 0 )
            has (: 'y' 0 )
            does (: '+' ( vector ) [
              ( this x ( + ( that x ) !) .)
              ( this y ( + ( that y ) !) .)
            ] )
          ]
          is (
            function (: ( class [ none param (: 'y' (number) 0 ) param (: 'x' (number) 0 ) ] ) [
              vector new ( x ( that x !) .) ( y ( that y !) .)
            ] )
          )
        ) )

        var (: 'v1' ( vector (: 7 7 ) ) )
        var (: 'v2' ( vector (: 3 4 ) ) )

        ( 'Adding vectors' delog .)

        ( v2 + ( v1 ) .)

        ( v2 x delog .)
        ( v2 y delog .)

Notice that the factory function starts with 'vector new'. This is bad.
The coupling between the class and the function is loose at best.
There are not many solid guarantees here.
There will be much better ways to build user classes in the future.

The output is:

        ::::			[7cd:STRING "Adding vectors"]
        ::::			[424:NUMBER 10.000000]
        ::::			[5d8:NUMBER 11.000000]
        0000	r->value	[742:CLOSURE]




---
layout: tutorial
---


Lists
-----

Lists in Nominine have element type. The element type decides what type of objects can be in the list.

Lists that can contain any type of object, has element type 'any'.

Lists are mutable. Operations on lists normally return the list operated upon.
If there is a type mismatch, a none object is produced.


Incomplete interface and implementation
---------------------------------------

Lists lack proper error reporting. Failures are not handled very well.

Also lists only implements appending, merging, iteration and length.


Building lists
--------------

The easiest way to build a list is the list literal. The following builds a list with three numbers.
A list literal always results in a list with element type 'any'.

        var (: 'some-list' [ 1 2 3 ] )

To build a list with an element type other than 'any', use the list class object as a constructor.

        var (: 'some-list-of-numbers' ( list ( number ) ) )

The constructor takes a class as an argument.
'some-list-of-numbers' is a list that can only contain objects that are of class 'number'
or of a class that is a subclass of 'number'.


Appending elements to lists
---------------------------

To append more elements to a list, simply pass objects of element type to the list.
Appending elements returns the list object.

        ( some-list-of-numbers 4 5 6 )

Since some-list has element type 'any', one can append any object to it.

        ( some-list 'a' 1 ( x ) )

If one tries to do the same with 'some-list-of-numbers', it will fail, since it only accept numbers.


Merging lists
-------------

To merge lists, one uses the merge method. Merge takes a list as an argument.

        ( some-list merge [ 7 8 9 ] .)

It is possible to merge lists with different element type,
but if at any point an element cannot be appended the merge after that point fails.

        ( some-list-of-numbers merge ( some-list ) .)
        ( some-list merge [ 10 11 ] .)

Generators
----------

Generators are programs that produce elements.

        var (: 'some-generator' ( generator (: ( number ) [ ( 1 throw .) ( 2 throw .) ( 3 throw .) ] ) ) )

To produce a generator one uses the 'generator' class as a constructor. It takes as argument the class of elements
generated by the generator and a 'set' representing the code block that defines the generator program. The class is
optional and has a default value of 'any'.

In the future, there will probably be a constructor on set to build generators of 'any' objects.

Notice that the above generator uses 'throw' to emit elements.
'some-generator' is throws the elements 1, 2 and 3.

Sets
----

Lists and generators share the mechanism for iteration. This means that when building e.g. a function that uses a list as
a parameter, it is often better to use the type 'set' instead. That way, the function can receive both lists and generators.

        fun (: 'do-something-to-all-elements' ( set ) [ ... ] )

The 'set' class is only a placeholder and does not add any functionality and cannot be instantiated.

Generator to list
-----------------

Generators do not support 'append' and 'merge', but it is possible to merge a generator into a list.

        ( some-list merge ( some-generator ) .)

This will append all elements generated by some-generator into some-list. The generator needs to terminate for this to work.
This is effectively converts a generator to a static list.

The 'merge' method of lists takes a 'set' as its parameter.

List to generator
-----------------

It can also be useful to combine lists using generators. To combine two lists dynamically one can throw all the elements of
the lists in a generator.

To throw all elements in a set, use 'all' on the set.

        ( generator (: [ ( list-1 all .) ( list-2 all .) ] ) )

The resulting generator will produce different elements dependent on what is in list-1 and list-2 at the time of iteration.

*'all' is not implemented yet.*


Iterating
---------

To iterate over a set, list or generator, one must create an iterator object using the word 'each'.

        var (: 'elements' ( some-set each ) )

Then one can use the word 'next' to get the next element in the list.

        ( elements next )

The class of an iterator is 'iterator'. It is a first class object. It can be useful to pass iterators as arguments.

The following code iterates over all elements of 'some-set' and outputs them using 'delog'.

        const (: 'elements' ( some-set each ) )
        loop [
          ( elements next else [ return ( none ) ] delog .)
        ]

'some-set' can be either a list or a generator, or an other type of set.


Is everything lists?
--------------------

Nope, but expressions are sets. Therefore, when building methods and other operational data, it is common to pass a list
literal as a code block.

It is, however, possible to pass any kind of set, such as a generator.

The following code generates an expression that is used to generate the expression that defines the function do-something.
The generators will not generate the code until it is used, so it may change dynamically from time to time.

        fun (: 'do-something' ( generator (: ( generator (: [ ... ] ) ) ) ) )

To build code by combining other sets one can use list merge to merge sets into the final code block list.

        fun (: 'do-something' ( [ ... ] merge [ ... ] ) )

Yes, this *is* pretty cool.


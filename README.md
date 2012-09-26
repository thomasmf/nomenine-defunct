Nominine
========

Nominine is a simple programming language.

It is an object-oriented language at heart,
but function-like abstractions and sets have come to play an increasingly important role as the project progress.

The syntax is somewhat unusual,
but I think most people will find it to be straight forward
in addition to having tons of expressiveness.

I think semantics can be characterized as a cross between a functional language and an object oriented language.
Not in the sense that it is a hybrid programming language,
but in the sense that the two paradigms combine to form a new paradigm.

It may also be possible to describe the language in words that are not as big as the word *paradigm*.
I am trying to do that in the documentation on the website.

This is all a work in progress.


Goals
-----

The goal is to build a good programming language.
I cannot give a more specific goal than that.

When it comes to programming languages,
Nominine or something along those lines,
is a good path to go down.
That is my opinion and that is the path I am going.


Website
-------

I have a website with tutorial and discussion of some examples at [nominine.org](http://nominine.org/).

I am not satisfied with the documentation so far.
It is not that I need it to look and sound very professional,
but I hope to, over time, mold it into something that explains the different ideas in a simple and direct fashion.
Currently it is mostly bits and pieces.

I really appreciate any feedback on this.


Example
-------

Here is an example of what source code looks like:

        defun (: 'sort' ( set ) [

          def (: 'elements' ( that each ) )
          def (: 'pivot' ( elements next else [ return [] ] ) )
          var (: 'low' [] )
          var (: 'high' [] )

          loop [
            elements next else [ stop ] > ( pivot )
            then [ high ( elements value ) ]
            else [ low ( elements value ) ]
          ]

          sort ( low ) ( pivot ) merge( sort ( high ) )

        ] )

This defines a function 'sort' which can be used to sort a list:

        ( sort (: 5 4 6 3 7 9 6 3 ) )

It returns a sorted list.


Download
---------

Get the source code using git:

        git clone https://github.com/thomasmf/nomininte.git


Compilation
-----------

To compile, go to *nominine* directory and do:

        make

Usage
-----

To run a nominine script file, write:

        ./nominine <script-file.n>

To run the examples write:

        ./nominine examples/hello-world.n

        ./nominine examples/sort.n

        ./nominine examples/user-class.n

        ./nominine examples/primes.n

        ./nominine examples/fibonacci.n


Have fun and feel free to contact me. I appreciate feedback to thomasmf at nominine org.


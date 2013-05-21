Nominine
========

Nominine is a simple programming language.

The syntax is somewhat unusual,
but I think most people will find it to be straight forward
in addition to having tons of expressiveness.

I think semantics can be characterized as a cross between a functional language and an object oriented language.
Not in the sense that it is a hybrid programming language,
but in the sense that the two paradigms combine to form a new paradigm.

It may also be possible to describe the language in words that are not as big as the word *paradigm*.
I am trying to do that in the documentation on the website.

This is all a work in progress.


Website
-------

I have a website with tutorial and discussion of some examples at [nominine.org](http://nominine.org/).


Example
-------

Here is an example of what source code looks like:

        defun (: 'sort' ( seq ) [

          var (: 'elements' ( that each ) )
          var (: 'pivot' ( elements next else [ return [] ] ) )
          var (: 'low' [] )
          var (: 'high' [] )

          loop [
            elements next else [ stop ] > ( pivot )
            then [ high ( elements value ) ]
            else [ low ( elements value ) ]
          ]

          sort ( low ) ( pivot ) merge ( sort ( high ) )

        ] )

This defines a function 'sort' which can be used to sort a list:

        ( console write ( sort [ 5 4 6 3 7 9 6 3 ] ) newl .)

Will output a sorted list to console.


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


Feel free to contact me. I appreciate feedback to thomasmf at nominine org.


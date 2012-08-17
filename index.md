---
layout: default
---

nominine
========
Nominine is a simple programming language.

It is an object-oriented language with the addition of closures, lambdas and co-routines.

Here is an example of what source code looks like:

        fun (: 'sort' ( set ) [

          const (: 'elements' ( that each ) )
          const (: 'pivot' ( elements next else [ return [] ] ) )
          var (: 'low' [] )
          var (: 'high' [] )

          loop [
            elements next else [ stop ] > ( pivot )
            then [ high ( elements value ) ]
            else [ low ( elements value ) ]
          ]

          sort( low ) ( pivot ) merge( sort( high ) )

        ] )

This defines a function 'sort' which can be used to sort a list:

        sort [ 5 4 2 3 1 ]

It returns a sorted list.


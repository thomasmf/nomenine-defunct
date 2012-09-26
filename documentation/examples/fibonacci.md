---
layout: examples
---

Fibonacci
---------

This example calculates the fibonacci numbers.


        def (: 'fib-set' (
          gen (: ( number ) [
            def (: 'n' 1 )
            var (: 'v0' 0 ) var (: 'v1' 1 ) var (: 'v2' 0 )
            loop [
              ( v2 throw .)
              ( v0 ( v1 !) .)
              ( v1 ( v2 !) .)
              ( v2 ( v0 + ( v1 ) !) .)
            ]
          ] )
        ) )

        defun (: 'getn' ( param (: (: 'n' ( number ) ) (: 'the-set' ( set ) ) ) ) [
          gen (: ( number ) [
            def (: 'i' 0 )
            def (: 'elements' ( that the-set each ) )
            loop [
              ( that n >= ( i ++ ) else [ stop ] .)
              ( elements next else [ stop ] throw .)
            ]
          ] )
        ] )

        defun (: 'ceiling' ( param (: (: 'max' ( number ) ) (: 'the-set' ( set ) ) ) ) [
          gen (: ( number ) [
            def (: 'elements' ( that the-set each ) )
            loop [
              that max > ( elements next else [ stop ] ) then [ elements value throw ]
            ]
          ] )
        ] )

        def (: 'first-100' ( getn (: 100 ( fib-set ) ) ) )

        ( console write ( ceiling (: ( 2 pow 52 ) ( first-100 ) ) join ( ',' tab ) ) newl .)

This program produces:

        0,	1,	1,	2,	3,	5,	8,	13,	21,	34,	55,	89,	144,	233,	377,	610,	987,	1597,	2584,	4181,	6765,	10946,	17711,	28657,	46368,	75025,	121393,	196418,	317811,	514229,	832040,	1.34627e+06,	2.17831e+06,	3.52458e+06,	5.70289e+06,	9.22746e+06,	1.49304e+07,	2.41578e+07,	3.90882e+07,	6.3246e+07,	1.02334e+08,	1.6558e+08,	2.67914e+08,	4.33494e+08,	7.01409e+08,	1.1349e+09,	1.83631e+09,	2.97122e+09,	4.80753e+09,	7.77874e+09,	1.25863e+10,	2.0365e+10,	3.29513e+10,	5.33163e+10,	8.62676e+10,	1.39584e+11,	2.25851e+11,	3.65435e+11,	5.91287e+11,	9.56722e+11,	1.54801e+12,	2.50473e+12,	4.05274e+12,	6.55747e+12,	1.06102e+13,	1.71677e+13,	2.77779e+13,	4.49456e+13,	7.27235e+13,	1.17669e+14,	1.90392e+14,	3.08062e+14,	4.98454e+14,	8.06516e+14,	1.30497e+15,	2.11149e+15,	3.41645e+15

*Sorry about the notation. There will be formatting of numbers later*

The following example defines **fib-set** which is the set of all Fibonacci numbers.
It is a generator, aka. lazy list.
**fib-set** uses an endless loop to generate the numbers.

**getn** produce a generator that passes through a number of elements from a set. Notice that generators play well with closures.

**ceiling** ignore numbers above a threshold.


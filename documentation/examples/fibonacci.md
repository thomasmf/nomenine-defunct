---
layout: examples
---

Fibonacci
---------

This example calculates the fibonacci numbers.

        var (: 'fib-seq' (
          seq [
            var (: 'v0' 0 ) var (: 'v1' 1 ) var (: 'v2' 0 )
            loop [
              ( yield ( v2 ) .)
              ( v0 = ( v1 ) .)
              ( v1 = ( v2 ) .)
              ( v2 = ( v0 + ( v1 ) ) .)
            ]
          ]
        ) )
        
        defun (: 'getn' ( param (: (: 'n' ( number ) ) (: 'the-seq' ( seq ) ) ) ) [
          seq [
            var (: 'i' 0 )
            var (: 'elements' ( that the-seq each ) )
            loop [
              ( that n >= ( i ++ ) else [ stop ] .)
              ( yield ( elements next else [ stop ] ).)
            ]
          ]
        ] )
        
        defun (: 'ceiling' ( param (: (: 'max' ( number ) ) (: 'the-seq' ( seq ) ) ) ) [
          seq [
            var (: 'elements' ( that the-seq each ) )
            loop [
              that max > ( elements next else [ stop ] ) then [ yield ( elements value ) ]
            ]
          ]
        ] )
        
        var (: 'first-100' ( getn (: 100 ( fib-seq ) ) ) )
        
        ( console write ( ceiling (: 1000000 ( first-100 ) ) ) newl .)

This program produces:

        [ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040 ]

The following example defines **fib-seq** which is the sequence of all Fibonacci numbers.
It is a lazy list.
**fib-seq** uses an endless loop to generate the numbers.

**getn** produce a generator that passes through a number of elements from a sequence. Notice that lazy lists play well with closures.

**ceiling** ignore numbers above a threshold.


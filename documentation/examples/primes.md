---
layout: examples
---

Primes
------

This example calculates prime numbers.

        defun (: 'until-ceiling' ( param (: (: 'max' ( number ) ) (: 'the-seq' ( seq ) ) ) ) [
          seq [
            var (: 'elements' ( that the-seq each ) )
            loop [
              yield ( that max >= ( elements next else [ stop ] ) else [ stop ] )
            ]
          ]
        ] )
        
        defun (: 'dividable' ( param (: (: 'n' ( number ) ) (: 'the-seq' ( seq ) ) ) ) [
          var (: 'elements' ( that the-seq each ) )
          loop [
            that n mod ( elements next else [ stop ] ) == 0 then [ return ( elements value ) ]
          ]
          none
        ] )
        
        var (: 'primes-seq' (
          seq [
            var (: 'known-primes' ( list ( number ) ) )
            var (: 'i' 1 )
            loop [
              ( i += 1 .)
              ( dividable (: ( i ) ( until-ceiling (: ( i sqrt ) ( known-primes ) ) ) ) else [
                ( known-primes ( i ) .)
                ( yield ( i ) .)
              ] .)
            ]
          ]
        ) )
        
        ( console write ( until-ceiling (: 123 ( primes-seq ) ) ) newl .)

The output of this program is:

        [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113 ]

**primes-seq** is the lazy list of all the primes.

**dividable** checks if a number can be divided by any number in a sequence/list.

**until-ceiling** makes sure iteration stops when reaching a highest number.

The last line prints prime numbers less than 123.


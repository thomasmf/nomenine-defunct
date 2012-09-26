---
layout: examples
---

Primes
------

This example calculates prime numbers.

        defun (: 'until-ceiling' ( param (: (: 'max' ( number ) ) (: 'the-set' ( set ) ) ) ) [
          gen (: ( number ) [
            def (: 'elements' ( that the-set each ) )
            loop [
              that max >= ( elements next else [ stop ] ) else [ stop ] throw
            ]
          ] )
        ] )

        defun (: 'dividable' ( param (: (: 'n' ( number ) ) (: 'the-set' ( set ) ) ) ) [
          def (: 'elements' ( that the-set each ) )
          loop [
            that n mod ( elements next else [ stop ] ) == 0 then [ return ( elements value ) ]
          ]
          none
        ] )

        def (: 'primes-set' (
          gen (: ( number ) [
            def (: 'known-primes' ( list ( number ) ) )
            var (: 'i' 1 )
            loop [
              ( i ( i + 1 !) .)
              ( dividable (: ( i ) ( until-ceiling (: ( i sqrt ) ( known-primes ) ) ) ) else [
                ( known-primes ( i ) .)
                ( i throw .)
              ] .)
            ]
          ] )
        ) )

        ( console write ( until-ceiling (: 123 ( primes-set ) ) ) newl .)

The output of this program is:

        [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113 ]

**primes-set** is a generator that throw numbers that cannot be divided.
It only tests for divisibility by numbers up to the square root of the number tested.
However, it stores *all* primes found.
The **primes-set** is the set of all primes.

**dividable** checks if a number can be divided by any number in a set.
The number and set are parameters.

**until-ceiling** throws onwards the elements in a set until it reaches an element that is higher then the given ceiling.

The two last lines prints prime numbers less than 100.


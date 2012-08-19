---
layout: examples
---

Primes
------

This example calculates prime numbers.

There are two implementations of the set of prime numbers.
Both of which iterate over the natural numbers and test each number for divisibility.

The first implementation is **primes-set**. This is a generator that throw numbers that cannot be divided.
It only tests for divisibility by numbers up to the square root of the number tested.
However, it stores *all* primes found.
The **primes-set** is the set of all primes.

The second implementation is **primes-ceiling-set**.
This is a set factory that produces a generator that will only store known primes
up to the square root of the maximum prime searched for.
**primes-ceiling-set** takes the maximum number as a parameter and will stop when reaching it.

In addition to these two implementations of prime numbers, there are tools for dealing with sets.

**print-all** outputs elements of a set.

**dividable** checks if a number can be divided by any number in a set.
The number and set are parameters.

**until-ceiling** throws onwards the elements in a set until it reaches an element that is higher then the given ceiling.


        fun (: 'print-all' ( set ) [
          ( 'print-all' delog .)
          const (: 'elements' ( that each ) )
          loop [
            elements next else [ return ( none ) ] delog
          ]
          that
        ] )

        fun (: 'until-ceiling' ( class [ none param (: 'max' ( number ) 0 ) param (: 'the-set' ( set ) ) ] ) [
          generator (: ( number ) [
            const (: 'elements' ( that the-set each ) )
            loop [
              ( that max >= ( elements next else [ stop ] ) else [ stop ] .)
              ( elements value throw .)
            ]
          ] )
        ] )

        fun (: 'dividable' ( class [ none param (: 'n' ( number ) 0 ) param (: 'the-set' ( set ) ) ] ) [
          const (: 'elements' ( that the-set each ) )
          loop [
            ( that n mod ( elements next else [ stop ] ) == 0 then [ return ( elements value ) ] .)
          ]
          none
        ] )

        const (: 'primes-set' (
          generator (: ( number ) [
            const (: 'known-primes' ( list ( number ) ) )
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

        fun (: 'primes-ceiling-set' ( number ) [
          generator (: ( number ) [
            const (: 'known-primes' ( list ( number ) ) )
            var (: 'i' 1 )
            loop [
              ( i ( i + 1 !) < ( that sqrt ) else [ stop ] .)
              ( dividable (: ( i ) ( until-ceiling (: ( i sqrt ) ( known-primes ) ) ) ) else [
                ( known-primes ( i ) .)
                ( i throw .)
              ] .)
            ]
            loop [
              ( i ( i + 1 !) < ( that ) else [ stop ] .)
              ( dividable (: ( i ) ( until-ceiling (: ( i sqrt ) ( known-primes ) ) ) ) else [
                ( i throw .)
              ] .)
            ]
          ] )
        ] )

        ( print-all ( until-ceiling (: 100 ( primes-set ) ) ) .)

        ( print-all ( primes-ceiling-set 100 ) .)

The two last lines prints prime numbers less than 100 using the two implementations.

The output of this program is:

        ::::			[71c:STRING "print-all"]
        ::::			[207:NUMBER 2.000000]
        ::::			[aa6:NUMBER 3.000000]
        ::::			[02b:NUMBER 5.000000]
        ::::			[f0c:NUMBER 7.000000]
        ::::			[5be:NUMBER 11.000000]
        ::::			[22a:NUMBER 13.000000]
        ::::			[8be:NUMBER 17.000000]
        ::::			[409:NUMBER 19.000000]
        ::::			[11f:NUMBER 23.000000]
        ::::			[e48:NUMBER 29.000000]
        ::::			[dd8:NUMBER 31.000000]
        ::::			[709:NUMBER 37.000000]
        ::::			[325:NUMBER 41.000000]
        ::::			[3d5:NUMBER 43.000000]
        ::::			[b1f:NUMBER 47.000000]
        ::::			[701:NUMBER 53.000000]
        ::::			[e22:NUMBER 59.000000]
        ::::			[696:NUMBER 61.000000]
        ::::			[0b4:NUMBER 67.000000]
        ::::			[810:NUMBER 71.000000]
        ::::			[6d3:NUMBER 73.000000]
        ::::			[d94:NUMBER 79.000000]
        ::::			[407:NUMBER 83.000000]
        ::::			[415:NUMBER 89.000000]
        ::::			[4e7:NUMBER 97.000000]
        ::::			[71c:STRING "print-all"]
        ::::			[946:NUMBER 2.000000]
        ::::			[0d5:NUMBER 3.000000]
        ::::			[e61:NUMBER 5.000000]
        ::::			[c4b:NUMBER 7.000000]
        ::::			[055:NUMBER 11.000000]
        ::::			[2c9:NUMBER 13.000000]
        ::::			[c03:NUMBER 17.000000]
        ::::			[15a:NUMBER 19.000000]
        ::::			[c4e:NUMBER 23.000000]
        ::::			[a01:NUMBER 29.000000]
        ::::			[0af:NUMBER 31.000000]
        ::::			[df7:NUMBER 37.000000]
        ::::			[2fd:NUMBER 41.000000]
        ::::			[0ac:NUMBER 43.000000]
        ::::			[0a5:NUMBER 47.000000]
        ::::			[101:NUMBER 53.000000]
        ::::			[a69:NUMBER 59.000000]
        ::::			[e33:NUMBER 61.000000]
        ::::			[8eb:NUMBER 67.000000]
        ::::			[c28:NUMBER 71.000000]
        ::::			[219:NUMBER 73.000000]
        ::::			[7df:NUMBER 79.000000]
        ::::			[027:NUMBER 83.000000]
        ::::			[2d6:NUMBER 89.000000]
        ::::			[e31:NUMBER 97.000000]
        0000	r->value	[83a:CLOSURE]



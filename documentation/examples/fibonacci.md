---
layout: examples
---

Fibonacci
---------

The following example defines 'fib-set' which is the set of all Fibonacci numbers.
It is a generator, aka. lazy list.
'fib-set' uses an endless loop to generate the numbers.

Due to limitations on number instances, 'fib-set' will start producing non-Fibonacci numbers after a certain
number of iterations. I am just assuming this. I have not checked it. The example below, handles this using 'ceiling'.
The natural way to handle this would be to put a limit into the generator itself,
but 'number' objects are not supposed to be limited. 'fib-set' is correct and the 'number' class will be
extended to handle arbitrary precision and size of numbers in the future.

There is also, as an alternative, a recursive function, 'fib-rec', that calculates the n'th Fibonacci number.
This is very slow. The mechanism does not store already calculated numbers.

In addition to these two implementations of Fibonacci numbers, there are tools for dealing with sets and functions.

'print-all' outputs elements of a set.

'range' produces a set of numbers within a range. The set is a generator.

'getn' produce a generator that passes through a number of elements from a set. Notice that generators play well with closures.

'ceiling' ignore numbers above a threshold.

'filter' produce a set where the elements are produced by calling a function with elements from a set.
This is like "map" only that the application of the function on the set is not carried out until elements are requested.
It can be used for infinite lists.

These tools are written to work with the example and may fail under other conditions.
Eg. sorted lists of *numbers* are often assumed.


        fun (: 'print-all' ( set ) [
          ( 'print-all' delog .)
          const (: 'elements' ( that each ) )
          loop [
            elements next else [ return ( none ) ] delog
          ]
          that
        ] )

        fun (: 'range' ( class [ none param (: 'to' (number) 0 ) param (: 'from' (number) 0 ) ] ) [
          generator (: ( number ) [
            var (: 'index' ( that from ) )
            loop [
              that to > ( index ++ ) else [ stop ] throw
            ]
          ] )
        ] )

        const (: 'fib-set' (
          generator (: ( number ) [
            const (: 'n' 1 )
            var (: 'v0' ) var (: 'v1' 1 ) var (: 'v2' 0 )
            loop [
              ( v2 throw .)
              ( v0 ( v1 !) .)
              ( v1 ( v2 !) .)
              ( v2 ( v0 + ( v1 ) !) .)
            ]
          ] )
        ) )

        fun (: 'getn' ( class [ none param (: 'n' ( number ) 0 ) param (: 'the-set' ( set ) ) ] ) [
          generator (: ( number ) [
            const (: 'i' 0 )
            const (: 'elements' ( that the-set each ) )
            loop [
              ( that n >= ( i ++ ) else [ stop ] .)
              ( elements next else [ stop ] throw .)
            ]
          ] )
        ] )

        fun (: 'ceiling' ( class [ none param (: 'max' ( number ) 0 ) param (: 'the-set' ( set ) ) ] ) [
          generator (: ( number ) [
            const (: 'elements' ( that the-set each ) )
            loop [
              that max > ( elements next else [ stop ] ) then [ elements value throw ]
            ]
          ] )
        ] )

        fun (: 'fib-rec' ( number ) [
          ( that == 0 else [ that == 1 ] then [ return 1 ] .)
          fib-rec ( that - 1 ) + ( fib-rec ( that - 2 ) )
        ] )

        fun (: 'filter' ( class [ none param (: 'the-function' ( function ) ) param (: 'the-set' ( set ) ) ] ) [
          generator (: ( number ) [
            const (: 'elements' ( that the-set each ) )
            loop [
              that the-function ( elements next else [ stop ] ) throw
            ]
          ] )
        ] )


        const (: 'first-100' ( getn (: 100 ( fib-set ) ) ) )

        ( print-all ( ceiling (: ( 2 pow 52 ) ( first-100 ) ) ) .)

        ( print-all ( filter (: ( fib-rec ) ( range (: 10 15 ) ) ) ) .)

All these generator factories have similar structure.
This can be captured using meta programming, ie. building expressions dynamically.
Currently there is a constructor deficiency, so this cannot be done properly.

Notice the use of 'else' in 'fib-rec'. It acts as a logical *or* rather then a conditional branch.

The result of running this program:

        ::::			[51c:STRING "print-all"]
        ::::			[1ae:NUMBER 0.000000]
        ::::			[96f:NUMBER 1.000000]
        ::::			[245:NUMBER 1.000000]
        ::::			[7ab:NUMBER 2.000000]
        ::::			[c9a:NUMBER 3.000000]
        ::::			[2eb:NUMBER 5.000000]
        ::::			[dc1:NUMBER 8.000000]
        ::::			[697:NUMBER 13.000000]
        ::::			[f6d:NUMBER 21.000000]
        ::::			[554:NUMBER 34.000000]
        ::::			[6c9:NUMBER 55.000000]
        ::::			[cee:NUMBER 89.000000]
        ::::			[0c4:NUMBER 144.000000]
        ::::			[79a:NUMBER 233.000000]
        ::::			[070:NUMBER 377.000000]
        ::::			[557:NUMBER 610.000000]
        ::::			[7cc:NUMBER 987.000000]
        ::::			[cee:NUMBER 1597.000000]
        ::::			[bc4:NUMBER 2584.000000]
        ::::			[49a:NUMBER 4181.000000]
        ::::			[d70:NUMBER 6765.000000]
        ::::			[646:NUMBER 10946.000000]
        ::::			[1e7:NUMBER 17711.000000]
        ::::			[e42:NUMBER 28657.000000]
        ::::			[567:NUMBER 46368.000000]
        ::::			[e3d:NUMBER 75025.000000]
        ::::			[713:NUMBER 121393.000000]
        ::::			[1e8:NUMBER 196418.000000]
        ::::			[e93:NUMBER 317811.000000]
        ::::			[41f:NUMBER 514229.000000]
        ::::			[267:NUMBER 832040.000000]
        ::::			[b3d:NUMBER 1346269.000000]
        ::::			[a13:NUMBER 2178309.000000]
        ::::			[4e8:NUMBER 3524578.000000]
        ::::			[e93:NUMBER 5702887.000000]
        ::::			[71f:NUMBER 9227465.000000]
        ::::			[267:NUMBER 14930352.000000]
        ::::			[e3d:NUMBER 24157817.000000]
        ::::			[713:NUMBER 39088169.000000]
        ::::			[1e8:NUMBER 63245986.000000]
        ::::			[e93:NUMBER 102334155.000000]
        ::::			[41f:NUMBER 165580141.000000]
        ::::			[267:NUMBER 267914296.000000]
        ::::			[b3d:NUMBER 433494437.000000]
        ::::			[a13:NUMBER 701408733.000000]
        ::::			[4e8:NUMBER 1134903170.000000]
        ::::			[e93:NUMBER 1836311903.000000]
        ::::			[71f:NUMBER 2971215073.000000]
        ::::			[267:NUMBER 4807526976.000000]
        ::::			[e3d:NUMBER 7778742049.000000]
        ::::			[713:NUMBER 12586269025.000000]
        ::::			[1e8:NUMBER 20365011074.000000]
        ::::			[e93:NUMBER 32951280099.000000]
        ::::			[41f:NUMBER 53316291173.000000]
        ::::			[267:NUMBER 86267571272.000000]
        ::::			[b3d:NUMBER 139583862445.000000]
        ::::			[a13:NUMBER 225851433717.000000]
        ::::			[4e8:NUMBER 365435296162.000000]
        ::::			[e93:NUMBER 591286729879.000000]
        ::::			[71f:NUMBER 956722026041.000000]
        ::::			[267:NUMBER 1548008755920.000000]
        ::::			[e3d:NUMBER 2504730781961.000000]
        ::::			[713:NUMBER 4052739537881.000000]
        ::::			[1e8:NUMBER 6557470319842.000000]
        ::::			[e93:NUMBER 10610209857723.000000]
        ::::			[41f:NUMBER 17167680177565.000000]
        ::::			[267:NUMBER 27777890035288.000000]
        ::::			[b3d:NUMBER 44945570212853.000000]
        ::::			[a13:NUMBER 72723460248141.000000]
        ::::			[4e8:NUMBER 117669030460994.000000]
        ::::			[e93:NUMBER 190392490709135.000000]
        ::::			[71f:NUMBER 308061521170129.000000]
        ::::			[267:NUMBER 498454011879264.000000]
        ::::			[e3d:NUMBER 806515533049393.000000]
        ::::			[713:NUMBER 1304969544928657.000000]
        ::::			[1e8:NUMBER 2111485077978050.000000]
        ::::			[e93:NUMBER 3416454622906707.000000]
        ::::			[51c:STRING "print-all"]
        ::::			[b94:NUMBER 144.000000]
        ::::			[beb:NUMBER 233.000000]
        ::::			[2dc:NUMBER 377.000000]
        ::::			[137:NUMBER 610.000000]
        0000	r->value	[636:CLOSURE]

Notice how 'first-100' is *not* calculated when it is defined.
This set is a generator and it is generated every time it is used. This also goes for sets produced by 'filter'.
To convert a generator into a list, simply merge it to a list like this:

        ( [] merge ( first-100 ) )

This will produce a new list with the elements from the set.


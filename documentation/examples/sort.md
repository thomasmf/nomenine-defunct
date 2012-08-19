---
layout: examples
---


Sort
----

This is an implementation of the quick-sort sorting algorithm.

        fun (: 'print-all' ( set ) [
          const (: 'elements' ( that each ) )
          loop [
            ( elements next else [ return ( none ) ] delog .)
          ]
          that
        ] )

        fun (: 'sort' ( set ) [

          const (: 'elements' ( that each ) )
          const (: 'pivot' ( elements next else [ return [] ] ) )
          var (: 'low' [] )
          var (: 'high' [] )

          loop [
            elements next else [ stop ] > ( pivot )
            then [ high ( elements value ) ]
            else [ low ( elements value ) ]
          ]

          sort( low ) ( pivot ) merge( sort( high ) )

        ] )

        const (: 'l' [ 3 2 8 2 5 2 1 2 7 2 4 2 3 ] )

        ( 'Unsorted list' delog .)
        ( print-all( l ) .)

        ( 'Sorted list' delog .)
        ( print-all( sort( l ) ) .)

**print-all** iterates through a set printing all elements.

**sort** does the sorting. It takes a set as a parameter.

**elements** is the iterator. Every time a new element is needed, `elements next` is used. The last element is **none**.

The pivot is the first element in the list. This is a bad choice, particularly for already sorted lists, but Nominine
does not have random access to lists yet, so this will have to do.

**low** and **high** are lists to contain the elements lower than and higher than the pivot.

The loop tests each element and puts them in the right list.

Notice the `else [ stop ]` after `elements next`. This makes sure that the loop stops if there are no more elements.
If the comparison, **>**, is reached, we know that there is an element to compare.

The last line of **sort** first sort the **low** list. This produces a sorted list.
Then **pivot** is appended to the list.
Lastly the **high** list is sorted and merged to the final result.
The return is implicit, and the list resulting from all this sorting, appending and merging is returned.

The lines following the definition of **sort** defines **l**, a list, and sorts it.
Both the sorted and unsorted list is printed using **print-all**.

Notice that, since **sort** takes a set as its parameter, it can be used to sort numbers produced by generators as well as lists.
**sort** will, however, always return a list and *not* a generator.

Also notice that the parameter of **sort** is unmodified.


The output is similar to the following.

        ::::			[9c9:STRING "Unsorted list"]
        ::::			[3a8:NUMBER 3.000000]
        ::::			[3fa:NUMBER 2.000000]
        ::::			[be4:NUMBER 8.000000]
        ::::			[b36:NUMBER 2.000000]
        ::::			[087:NUMBER 5.000000]
        ::::			[1d8:NUMBER 2.000000]
        ::::			[12a:NUMBER 1.000000]
        ::::			[37b:NUMBER 2.000000]
        ::::			[5cc:NUMBER 7.000000]
        ::::			[51e:NUMBER 2.000000]
        ::::			[76f:NUMBER 4.000000]
        ::::			[8c0:NUMBER 2.000000]
        ::::			[812:NUMBER 3.000000]
        ::::			[9bf:STRING "Sorted list"]
        ::::			[594:NUMBER 1.000000]
        ::::			[c85:NUMBER 2.000000]
        ::::			[8be:NUMBER 2.000000]
        ::::			[1f6:NUMBER 2.000000]
        ::::			[431:NUMBER 2.000000]
        ::::			[b6a:NUMBER 2.000000]
        ::::			[6ee:NUMBER 2.000000]
        ::::			[fe8:NUMBER 3.000000]
        ::::			[fc3:NUMBER 3.000000]
        ::::			[952:NUMBER 4.000000]
        ::::			[3fc:NUMBER 5.000000]
        ::::			[288:NUMBER 7.000000]
        ::::			[882:NUMBER 8.000000]
        0000	r->value	[942:CLOSURE]





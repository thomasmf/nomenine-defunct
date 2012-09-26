---
layout: examples
---


Sort
----

This is an implementation of the quick-sort sorting algorithm.

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

        def (: 'l' (: 3 2 8 2 5 2 1 2 7 2 4 2 3 ) )

        ( console write
          'Unsorted list' tab	': ' ( l join ', ' )		newl
          'Sorted list' tab	': ' ( sort( l ) join ', ' )	newl
        .)

This program produces the following output:

        Unsorted list	: 3, 2, 8, 2, 5, 2, 1, 2, 7, 2, 4, 2, 3
        Sorted list	: 1, 2, 2, 2, 2, 2, 2, 3, 3, 4, 5, 7, 8

**sort** is a function that takes a **set** as a parameter.

**elements** is the iterator. Every time a new element is needed, `elements next` is used. The last element is **none**.

The pivot is the first element in the list.

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



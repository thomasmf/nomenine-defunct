---
layout: default
---

Nominine
========

Nominine is a simple programming language.

It is an object-oriented language with the addition of closures, lambdas and co-routines.

<hr>

Example
-------

Here is an example of what source code looks like:

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

This defines a function 'sort' which can be used to sort a list:

        ( sort (: 5 4 6 3 7 9 6 3 ) )

It returns a sorted list.

<div class="nom-posts">
  {% for post in site.posts limit 5 %}
    {% include post.html-fragment %}
  {% endfor %}
</div>





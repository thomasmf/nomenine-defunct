---
layout: default
---

Nominine
========

Nominine is a simple programming language.

Example
-------

Here is an example of what source code looks like:

        defun (: 'sort' ( seq ) [

          var (: 'elements' ( that each ) )
          var (: 'pivot' ( elements next else [ return [] ] ) )
          var (: 'low' [] )
          var (: 'high' [] )

          loop [
            elements next else [ stop ] > ( pivot )
            then [ high ( elements value ) ]
            else [ low ( elements value ) ]
          ]

          sort ( low ) ( pivot ) merge ( sort ( high ) )

        ] )

This defines a function 'sort' which can be used to sort a list:

        ( console write ( sort [ 5 4 6 3 7 9 6 3 ] ) newl .)

Will output a sorted list to console.

<div class="nom-posts">
  {% for post in site.posts limit 5 %}
    {% include post.html-fragment %}
  {% endfor %}
</div>





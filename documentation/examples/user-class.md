---
layout: examples
---

User class
----------

The following example implements a user defined class **vector**.
Instances of **vector** has two attributes **x** and **y** and a method **+**.

Nominine currently have no class concept, but one can use **fact** to build the equivalent of classes.
Here, **defact** is used to build the fact type.

        defact (: 'vector' ( param (: (: 'x' ( number ) ) (: 'y' ( number ) ) ) ) [
        
          that
        
          does (: '+' ( vector ) [
            vector (:
              ( this x + ( that x ) )
              ( this y + ( that y ) )
            )
          ] )
        
          noms (: 'to-string' [
            '<' ( this x ) ',' ( this y ) '>'
          ] )
        
        ] )
        
        
        var (: 'v1' ( vector (: 4 7 ) ) )
        
        var (: 'v2' ( vector (: 6 7 ) ) )
        
        var (: 'v3' ( v1 + ( v2 ) ) )
        
        ( console write ( v1 ) ' + ' ( v2 ) ' = ' ( v3 ) newl .)
        
        ( v1 = ( v2 ) .)
        
        ( console write ( v1 ) ' == ' ( v2 ) ( v1 == ( v2 ) then [ ' is true' ] else [ ' is false' ] ) newl .)

The output is:

        <4,7> + <6,7> = <10,14>
        <6,7> == <6,7> is true

Notice that **vector** objects have **+** and **to-string** explisitly defined while **=** and **==** are implisitly defined.


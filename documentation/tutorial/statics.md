---
layout: tutorial
---

Static dependencies
===================

Nominine provide tools for building static dependencies.
Static dependencies are described [here](/2013/10/06/programming_with_equations.html).

Notice that static dependencies as implemented in Nominine currently only connects to other static dependencies.
In other words one cannot use static dependencies on ordinary objects as on-change handlers.
Changes on ordinary objects simply do not propagate. This is a feature and not a bug.

<hr>

Creating a static dependency
----------------------------

One create static dependencies from ordinary objects by using the **en** or **em** object property.
For example:

        var (: 'b' ( 0 em [ a * 10 ] ) )

**em** creates a static dependency with the give expression as its definition and the object as its initial state.

        var (: 'a' ( 123 en ) )

**en** is a simplified form of **em**. **en** does not require an expression, but defines the static dependency to be itself.
The above expression is equivalent to:

        var (: 'a' ( 123 em [ a ] ) )

**en** is used to make changes to an object propagate while not having to give a specific definition.


*For more examples see test/meta.nom and test/dependency.nom.*

*For a more in-depth explanation of static dependencies read [this](/2013/10/06/programming_with_equations.html).*

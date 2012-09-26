---
layout: reference
---

Iterator
========

An **iterator** object is used to access the elements of a set one by one.
An **iterator** cannot be reset.
To start form the first element, one need to have the original set and create a new **iterator** using **each**.

        ( some-set each )

produces an **iterator**.

<hr>

Next
----
        ( some-iterator next )

produces the next element in the **set**.
The type of this element is determined by the **set**.

*Related types: [string](/documentation/reference/string.html)*


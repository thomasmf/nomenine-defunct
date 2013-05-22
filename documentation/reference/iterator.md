---
layout: reference
---

Iterator
========

An **iterator** object is used to access the elements of a sequence one by one.
An **iterator** cannot be reset.
To start form the first element, one need to have the original sequence and create a new **iterator** using **each**.

        ( some-seq each )

produces an **iterator**.

<hr>

Next
----
        ( some-iterator next )

produces the next element in the **seq**.


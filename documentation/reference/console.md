---
layout: reference
---

Console
=======

The **console** object is used for text communication with the user.

<hr>

Read
----
        ( console read )

produces a **string**.

*Related types: [string](/documentation/reference/string.html)*

<hr>

Write
-----
        ( console write 'some string literal' ( some-string-object ) newl .)

writes the words "some string literal" followed by the **string** value of **some-string-object** to the console.

Write will print all the following **string** objects.
If the value of **some-string-object** is '!!!' then the output of the statement would be:

        some string literal!!!

The string is followed by a new line. Notice the use of **newl** in the example.
In order to write special characters like tab and new line, one must use the words **tab** and **newl** as specified by the string type.

The **write** context behaves like a **string**.
The provided **string** objects are not, however, concatenated, and written as a single string at the end,
but written to console immediately as encountered.

*Related types: [string](/documentation/reference/string.html)*

*Related examples: [Hello world!](/documentation/examples/hello-world.html)*

*Related tutorials:*



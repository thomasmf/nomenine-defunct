/*
Copyright (c) 2012, Thomas M. Farrelly

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#define ISTOKENCHAR(x) ( ( x != '[' ) && ( x != ']' ) && ( x != '(' ) && ( x != ')' ) && ( x > 0x20 ) && ( x < 0x7f ) )

ANY listLITERALfactory( ANY list_proto ) ;

ANY numberLITERALfactory( ANY number_proto ) ;

ANY PARSE_string( n_integer *i, n_string source ) ;

ANY PARSE_token( n_integer *i, n_string source ) ;

ANY PARSE( n_integer *i, n_string source ) ;

ANY PARSE_quote( n_integer *i, n_string source ) ;

ANY PARSE( n_integer *i, n_string source ) ;

n_string read_source( n_string filename ) ;


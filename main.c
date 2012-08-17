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

#define _GNU_SOURCE

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <sysexits.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <ctype.h>

#include <gc.h>

#include "core.h"
#include "utils.h"

ANY PARSE_string( n_integer *i, n_string source ) {
  n_character x ;
  n_integer last = (*i) ;
  while( TRUE ) {
    x = source[ (*i)++ ] ;
//    printf( "%d:%c\\n", (*i), x ) ;
    if ( x == 0 ) {
      printf( "Parse error\\n" ) ;
      exit( 1 ) ;
    }
    if ( x == '\'' ) {
      return any( newSTRING( strndup( &(source[ last ]), (*i)-last-1 ) ) ) ;
    }
  }
}

#define ISTOKENCHAR(x) ( ( x != '[' ) && ( x != ']' ) && ( x != '(' ) && ( x != ')' ) && ( x > 0x20 ) && ( x < 0x7f ) )

ANY PARSE_token( n_integer *i, n_string source ) {
  n_character x ;
  n_integer last = (*i)-1 ;
  n_string token ;
  while( TRUE ) {
    x = source[ (*i)++ ] ;
//    printf( "%d:%c\\n", (*i), x ) ;
    if ( x == 0 ) {
      printf( "Parse error\\n" ) ; exit( 1 ) ;
    }
    if ( !ISTOKENCHAR(x) ) {
      (*i)-- ;
      token = strndup( &(source[ last ]), (*i)-last ) ;
      n_string r ;
      n_float n = strtod( token, &r ) ;
      if ( *r == '\0' ) {
        return any(newNUMBERliteral( newNUMBER( n ) )) ;
      } else {
        return any(wordNEW( token )) ;
      }
    }
  }
}

ANY PARSE( n_integer *i, n_string source ) ;

ANY PARSE_quote( n_integer *i, n_string source ) {
  n_character x ;
  LIST tokens = listNEW( ANY_class ) ;
  while( TRUE ) {
    x = source[ (*i)++ ] ;
//    printf( "%d:%c\\n", (*i), x ) ;
    if ( x == 0 ) {
      printf( "Parse error: expected ']'.\n" ) ; exit( 1 ) ;
    } else if ( x == '(' ) {
      listAPPEND( tokens, ref(PARSE( i, source )) ) ;
    } else if ( x == ')' ) {
      printf( "Parse error: unexpected ')'.\n" ) ; exit( 1 ) ;
    } else if ( x == '[' ) {
      listAPPEND( tokens, ref(PARSE_quote( i, source )) ) ;
    } else if ( x == ']' ) {
//      printf( "tokens: %d\\n", tokens->length ) ;
      return any(newLISTliteral( tokens )) ;
    } else if ( x == '\'' ) {
      listAPPEND( tokens, ref(PARSE_string( i, source )) ) ;
    } else if ( ( x > 0x20 ) && ( x < 0x7f ) ) {
      listAPPEND( tokens, ref(PARSE_token( i, source )) ) ;
    }
  }
}

ANY PARSE( n_integer *i, n_string source ) {
  n_character x ;
  LIST tokens = listNEW( ANY_class ) ;
  while( TRUE ) {
//    OUT( parsing stuff ) ;
//    printf( "%d\\n", (*i) ) ;
    x = source[ (*i)++ ] ;
//    printf( "%d:%c\\n", (*i), x ) ;
    if ( x == 0 ) {
      return any(newPHRASE( tokens )) ;
    } else if ( x == '(' ) {
      listAPPEND( tokens, ref(PARSE( i, source )) ) ;
    } else if ( x == ')' ) {
      return any(newPHRASE( tokens )) ;
    } else if ( x == '[' ) {
      listAPPEND( tokens, ref(PARSE_quote( i, source )) ) ;
    } else if ( x == ']' ) {
      printf( "Parse error: unexpected ']'.\n" ) ; exit( 1 ) ;
    } else if ( x == '\'' ) {
      listAPPEND( tokens, ref(PARSE_string( i, source )) ) ;
    } else if ( ( x > 0x20 ) && ( x < 0x7f ) ) {
      listAPPEND( tokens, ref(PARSE_token( i, source )) ) ;
    }
  }
}


n_string read_source( n_string filename ) {
  n_integer size ;
  n_string result ;
  FILE* f = fopen( filename, "r" ) ;
  if ( f == NULL ) {
    printf( "IO error: file '%s' not found.\n", filename ) ; exit( 1 ) ;
  }
  fseek( f, 0, SEEK_END ) ; size = ftell( f ) ; fseek( f, 0, SEEK_SET ) ;
  result = (n_string)malloc( size + 1 ) ;
  if ( size != fread( result, sizeof( n_character ), size, f ) ) {
    printf( "IO error: cannot read from file '%s'.\n", filename ) ; exit( 1 ) ;
  }
  fclose( f ) ;
  result[ size ] = 0 ;
  return result ;
}

#undef CONTINUE
#define CONTINUE continue
#define THIS (PTHIS)
#define THIS_R ref( THIS )

int main( int argc, const char* argv[] ) {

  if ( argc <= 1 ) {
    printf( "Argument error, missing filename.\n" ) ;
    printf( "Usage: %s <filename>\n", argv[ 0 ] ) ;
    exit( EX_USAGE ) ;
  } 

  n_boolean trace_state = FALSE ;

  INITIALIZE_core_CLASSES() ;
  INITIALIZE_core_WORDS() ;

  NONE = newNONETYPE() ;
  IGNORE = newIGNORETYPE() ;
  UNUSED = ref(NONE) ;
  LOOPstop = newLOOPstopTYPE() ;

  ROOT = newCLOSURE( c(CLOSURE,NONE), ref(NONE), ref(NONE), ref(newROOTOBJECT()), ref(NONE) ) ;
  ROOT->parent = ROOT ;

  USERCLASS = any(newGETS( ref(CLASS_class), LIST_class, any(newSETCUSTOMCONSTRUCTOR()) ) ) ;
  LISTCLASS = any(newGETS( ref(LIST_class), CLASS_class, any(newSETCUSTOMLIST()) ) ) ;
  FUNCTIONCLASS = any(newIS( any(APPLICATOR_class), any(newAPPLICATOR( ref(APPLICATOR_class), PARAMcl_class, any(newAPPLICATORCONSTRUCTOR()) )) )) ;
  GENERATORCLASS = any(newIS( any(GENERATOR_class), any(newAPPLICATOR( ref(GENERATOR_class), PARAMcl_class, any(newGENERATORCONSTRUCTOR()) )) )) ;


  n_integer parse_index = 0 ;
  PHRASE program = C( PHRASE, PARSE( &parse_index, read_source( (n_string)argv[ 1 ] ) ) ) ;

  REFERENCE r = ref(NONE) ;

  CONTEXT c1 = newCONTEXT( ROOT->parent, ref(NONE), ref(NONE) ) ;
  TASK t0 = newTASK( ref(newOBJECTIVE( c(SET,program->value), ROOT->view )), c1, r, c(TASK,NONE), c(TASK,NONE) ) ;
  TASK task = newTASK( ref(NONE), c1, ref(NONE), t0, t0 ) ;

  while ( TRUE ) {

    task = task->next ;
    if ( !NOTNONE( task ) ) break ;

    ATTRIB( WI_tron, ( trace_state = TRUE, task->context->this ) ) ;
    ATTRIB( WI_troff, ( trace_state = FALSE, task->context->this ) ) ;

    task->action->value->objective( task ) ;

    if ( trace_state ) {
      printf( "*\t%-30s%-30s%-30s%-30s\n", DEBUG( task->action->value ), DEBUG( task->context->this->value ), DEBUG( task->context->that->value ), DEBUG( task->result->value ) ) ;
    }

  }

  LOG( r->value ) ;

  return EX_OK ;
}


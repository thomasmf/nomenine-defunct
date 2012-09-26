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

#include <stdlib.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <sysexits.h>
#include <stdint.h>
#include <assert.h>
#include <gc.h>

#include "core.h"
#include "utils.h"

inline STRING STRX( n_string fmt, ... ) {
  va_list ap ;
  va_start( ap, fmt ) ;

  n_string s ;
  vasprintf( &s, fmt, ap ) ;

  n_integer l = strlen( s ) ;
  n_string x = (n_string)allocate( l ) ;
  strncpy( x, s, l ) ;
  free( s ) ;
  return( newSTRING( x ) ) ;
}

inline void rdset_f( REFERENCE r, ANY v, ANY sv ) {
  r->value = v ;
  r->svalue = sv ;
}

inline void rset_f( REFERENCE r, ANY v ) {
  r->value = r->svalue = v ;
}

inline void raset_f( REFERENCE r, ANY v ) {
  ERROR( "Failed setting reference. Expected type 'any' but got something else.", ( r->type == ANY_type ) ) ;
  RSET( r, v ) ; 
}

inline void rpset_f( REFERENCE r, ANY v ) {
  ERROR( "Failed setting reference. Got different type than expected.", ( r->type->instance_objective == v->objective ) ) ;
  RSET( r, v ) ;
}

inline void rtset_f( REFERENCE r, TYPE t, ANY v ) {
  ERROR( "Failed setting reference. Got different type than expected.", ( r->type == t ) ) ;
  RSET( r, v ) ; 
}


inline n_integer counter() {
  static n_integer counter = 0 ;
  return counter++ ;
}

inline void* allocate( n_integer n ) {
  void* r = ( void * )GC_MALLOC( n ) ;
  ERROR( "Out of memory!", c(n_boolean,r) ) ;
  return r ;
}

inline REFERENCE refNEW( TYPE c, ANY x ) {
  return newREFERENCE( c, x, x ) ;
}

inline ANY type_error( TYPE c, ANY o, n_string f, n_integer l ) {
  if ( any(c->instance_objective) != any(o->objective) ) {
    printf( "System error in file '%s' at line %d. Object %s is of incorrect type.\n", f, l, DEBUG( o ) ) ;
    exit( 1 ) ;
  }
  return ( o ) ;
}

inline void error( n_string m, n_boolean v, n_string f, n_integer l ) {
  if ( !v ) {
    printf( "System error in file '%s' at line %d: %s\n", f, l, m ) ;
    exit( 1 ) ;
  }
}



inline TASK REC( TASK task, TYPE type, REFERENCE this, REFERENCE action, TASK next ) {
  if ( type == ANY_type ) {
    CONTEXT c1 = newCONTEXT( task->context->closure, this, refNEW( ANY_type, task->context->that->value ) ) ;
    return newTASK( action, c1, task->result, task->exit, task->exit ) ;
  } else if ( type->instance_objective == task->context->that->value->objective ) {
    return RETA( task, action, this, refNEW( type, task->context->that->value ), task->exit ) ;
  } else if ( NOTNONE( type->comparator ) ) {
    REFERENCE r1 = ref(NONE) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, ref(type), task->context->that ) ;
    TASK t1 = newTASK( ref(newTYPETEST( r1, this, action )), task->context, task->result, next, task->exit ) ;
    return newTASK( ref(type->comparator), c1, r1, t1, t1 ) ;
  } else {
    REFERENCE r1 = ref(NONE) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->that, ref(type->id) ) ;
    return newTASK( task->context->that, c1, r1, next,
      newTASK( ref(newTYPETEST( r1, this, action )), task->context/*nope*/, task->result, next, task->exit )
    ) ;
  }
}

inline TASK REP( TASK task, REFERENCE object, TASK next ) {
  return newTASK( object, task->context, task->result, next, task->exit ) ;
}

inline TASK REX( TASK task, REFERENCE object, TASK next ) {
  CONTEXT c1 = newCONTEXT( task->context->closure, object, task->context->that ) ;
  return newTASK( object, c1, task->result, next, task->exit ) ;
}

inline TASK RETO( TASK task, REFERENCE this, REFERENCE that, TASK next ) {
  CONTEXT c1 = newCONTEXT( task->context->closure, this, that ) ;
  return newTASK( this, c1, task->result, next, task->exit ) ;
}

inline TASK RETA( TASK task, REFERENCE action, REFERENCE this, REFERENCE that, TASK next ) {
  CONTEXT c1 = newCONTEXT( task->context->closure, this, that ) ;
  return newTASK( action, c1, task->result, next, task->exit ) ;
}


	////	tuple stuff

inline n_void tupleAPPEND( TUPLE l, REFERENCE e ) {
  n_integer i = l->length++ ;
  l->data = (REFS)GC_REALLOC( l->data, sizeof( n_pointer ) * l->length ) ;
  l->data[ i ] = e ;
  return ;
}

	////	list stuff

inline n_void listAPPEND( LIST l, REFERENCE e ) {
  n_integer i = l->length++ ;
  l->data = (REFS)GC_REALLOC( l->data, sizeof( n_pointer ) * l->length ) ;
  l->data[ i ] = e ;
  return ;
}

inline LIST listMERGE( LIST l1, LIST l2 ) {
  n_integer i ;
  for ( i = 0 ; i < l2->length ; i++ ) {
    listAPPEND( l1, l2->data[ i ] ) ;
  }
  return l1 ;
}


	////	word stuff

inline WORD wordNEW( n_string s ) {
  n_integer i ;
  for ( i = 0 ; i < WORDS->length ; i++ ) {
    if ( strcmp( s, C(WORD,WORDS->data[ i ]->value)->value->data ) == 0 ) {
      return C(WORD,WORDS->data[ i ]->value) ;
    }
  }
  WORD w = newWORD( newSTRING( s ) ) ;
  listAPPEND( WORDS, ref( w ) ) ;
  return w ; 
}


	////	iterator stuff

inline ITERATOR iteratorNEW( TASK task, TYPE type, SET l, CLOSURE closure ) {
  REFERENCE r1 = refNEW( ITERATOR_type, any(NONE) ) ;

  CLOSURE c1 = newCLOSURE( task->context->closure, closure->this, closure->that, closure->view, ref(newGETS( task->context->closure->field, type, any(newITERATORcatch( r1 )) )) ) ;
  CONTEXT c2 = newCONTEXT( c1->parent, ref(NONE), ref(NONE) ) ;

  TASK t1 = newTASK( ref(newITERATORend( r1 )), task->context, task->result, task->next, task->exit ) ;

  RPSET( r1, newITERATOR(
    newTASK( ref(newEVALUATE( c1, ref(c1), l )), c2, ref(NONE), t1, t1 ),
    c(TASK,NONE), ref(NONE)
  ) ) ;

  return C(ITERATOR,r1->value) ;
}


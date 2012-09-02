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

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sysexits.h>
#include <stdint.h>
#include <assert.h>
#include <gc.h>

#include "core.h"
#include "utils.h"


inline n_integer counter() {
  static n_integer counter = 0 ;
  return counter++ ;
}

inline void* allocate( n_integer n ) {
  void* r = ( void * )GC_MALLOC( n ) ;
  ASSERT( r ) ;
  return r ;
}

inline REFERENCE refNEW( CLASS c, ANY x ) {
  return newREFERENCE( c, x, x ) ;
}

inline ANY assert_type( CLASS c, ANY o, n_integer l ) {
  if ( any(c->instance_objective) != any(o->objective) ) {
    printf( "Type error in line %d:\\n", l ) ;
    LOG( o ) ;
    exit( 1 ) ;
  }
  return ( o ) ;
}

inline TASK REC( TASK task, CLASS class, REFERENCE this, REFERENCE action, TASK next ) {
  if ( class->instance_objective == task->context->that->value->objective ) {
    return RETA( task, action, this, refNEW( class, task->context->that->value ), task->exit ) ;
  }
  REFERENCE r1 = ref(NONE) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, task->context->that, ref(class->id) ) ;
  return newTASK( task->context->that, c1, r1, next,
    newTASK( ref(newTYPETEST( r1, this, action )), task->context/*nope*/, task->result, next, task->exit )
  ) ;
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

inline ITERATOR iteratorNEW( TASK task, CLASS class, SET l, CLOSURE closure ) {
  REFERENCE r1 = ref(NONE) ;

  CLOSURE c1 = newCLOSURE( task->context->closure, closure->this, closure->that, closure->view, ref(newGETS( task->context->closure->field, class, any(newITERATORcatch( r1 )) )) ) ;
  CONTEXT c2 = newCONTEXT( c1->parent, ref(NONE), ref(NONE) ) ;

  TASK t1 = newTASK( ref(newITERATORend( r1 )), task->context, task->result, task->next, task->exit ) ;

  r1->value = any(newITERATOR(
    newTASK( ref(newEVALUATE( c1, ref(c1), l )), c2, ref(NONE), t1, t1 ),	// reflexive tower
    c(TASK,NONE), ref(NONE)
  )) ;

  return c(ITERATOR,r1->value) ;
}


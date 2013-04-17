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
    CONTEXT c1 = newCONTEXT( task->context->closure, this, refNEW( type, task->context->that->value ) ) ;
    return newTASK( action, c1, task->result, task->exit, task->exit ) ;
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

inline n_boolean listHASELEMENT( LIST l, REFERENCE e ) {
  n_integer i ;
  for ( i = 0 ; i < l->length ; i++ ) {
    if ( e->value == l->data[ i ]->value ) {
      return TRUE ;
    }
  }
  return FALSE ;
}

inline n_void listREMOVEELEMENT( LIST l, REFERENCE e ) {
  LIST l2 = listNEW( l->type ) ;
  n_integer i ;
  for ( i = 0 ; i < l->length ; i++ ) {
    if ( e->value != l->data[ i ]->value ) {
      listAPPEND( l2, l->data[ i ] ) ;
    }
  }
  l->data = l2->data ;
  l->length = l2->length ;
}


	////	static dependencies


inline OBSERVER obsNEW( OBSERVER o1, REFERENCE o2 ) {
  if ( o1->object->objective == OBSERVER_type->instance_objective ) {
    return newOBSERVER( o1->dep, ref(obsNEW( C(OBSERVER,o1->object->value), o2 )) ) ;
  } else {
    return newOBSERVER( o1->dep, o2 ) ;
  }
}

inline n_void depREEVALUATE( TASK task, DEPENDENCY dep ) {

  REFERENCE r1 = ref(NONE) ;
  REFERENCE r2 = ref(NONE) ;

  REFERENCE r4 = ref(NONE) ;

  REFERENCE r5 = ref(NONE) ;


  task->next = newTASK( ref(newPROPAGATEtest( dep, r5 )), task->context, ref(NONE), task->next, task->next ) ;

  CONTEXT c3 = newCONTEXT( task->context->closure, r2, r1 ) ;
  task->next = newTASK( r2, c3, ref(NONE), task->next, task->next ) ;
  // mabe mute the setment from connect
  CONTEXT c2 = newCONTEXT( task->context->closure, dep->state, ref(WI_EQ) ) ;
  task->next = newTASK( dep->state, c2, r2, task->next, task->next ) ;


  CONTEXT c5 = newCONTEXT( task->context->closure, r4, r1 ) ;
  task->next = newTASK( r4, c5, r5, task->next, task->next ) ;

  CONTEXT c4 = newCONTEXT( task->context->closure, dep->state, ref(WI_EQEQ) ) ;
  task->next = newTASK( dep->state, c4, r4, task->next, task->next ) ;


  CLOSURE c1 = newCLOSURE( task->context->closure, ref(task->context), ref(dep->definition->closure->view), ref(newDEPcatcher( task->context->closure->field, dep )) ) ;
  task->next = newTASK( ref(newEVALUATE( c1, ref(c1), c(SEQ,dep->definition->expression) )), task->context, r1, task->next, task->next ) ;

  task->next = newTASK( ref(newDEPENDENCYreset( dep )), task->context, task->result, task->next, task->next ) ;
}


inline n_void depPROPAGATE( TASK task, DEPENDENCY dep ) {
  n_integer i ;
  for ( i = 0 ; i < dep->out->length ; i++ ) {
    depREEVALUATE( task, C(DEPENDENCY,dep->out->data[ i ]->value) ) ;
  }
}

inline n_void depRESET( DEPENDENCY dep ) {
  n_integer i ;
  for ( i = 0 ; i < dep->in->length ; i++ ) {
    listREMOVEELEMENT( C(DEPENDENCY,dep->in->data[ i ]->value)->out, ref( dep ) ) ;
  }
  dep->in = listNEW( DEPENDENCY_type ) ;
}


	////	wid stuff

inline WID widNEW( n_string s ) {
  n_integer i ;
  for ( i = 0 ; i < WIDS->length ; i++ ) {
    if ( strcmp( s, C(WID,WIDS->data[ i ]->value)->value->data ) == 0 ) {
      return C(WID,WIDS->data[ i ]->value) ;
    }
  }
  WID w = newWID( newSTRING( s ) ) ;
  listAPPEND( WIDS, ref( w ) ) ;
  return w ; 
}


	////	iterator stuff

inline ITERATOR iteratorNEW( TASK task, TYPE type, SEQ l, CLOSURE closure ) {
  REFERENCE r1 = refNEW( ITERATOR_type, any(NONE) ) ;

  CLOSURE c1 = newCLOSURE( task->context->closure, closure->context, closure->view, ref(newGETS( task->context->closure->field, type, any(newITERATORcatch( r1 )) )) ) ;
  CONTEXT c2 = newCONTEXT( c1->parent, ref(NONE), ref(NONE) ) ;

  TASK t1 = newTASK( ref(newITERATORend( r1 )), task->context, task->result, task->next, task->exit ) ;

  RPSET( r1, newITERATOR(
    newTASK( ref(newEVALUATE( c1, ref(c1), l )), c2, ref(NONE), t1, t1 ),
    c(TASK,NONE), ref(NONE)
  ) ) ;

  return C(ITERATOR,r1->value) ;
}


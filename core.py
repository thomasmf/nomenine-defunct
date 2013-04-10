"""
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
"""

# NOTE: This file contains code that will be split into a number of modules once
# there is a system for builtin modules. 

# NOTE: This file contains both c and python code. It is not pretty. To understand
# why this is written in this way, look at core.c and core.h after writing make.

from meta import *

META.NAME = 'core'

############################################################################################################
############################################################################################################
############################################################################################################
#
#	T(
#	  'name of type',
#	  'type of expected task->context->this->value or None if type is "any"',
#	  'type of expected task->context->that->value or None if type is "any"',
#	  (
#	    A( 'type of attribute', 'name of attribute' ),
#	    A( 'type of attribute', 'name of attribute' ),
#	    ...
#	  ),
#	  """ objective written in C """
#	)
#
############################################################################################################
############################################################################################################
############################################################################################################

T( 'ROOTOBJECT', None, None, (), """
  DO_COMMON ;
  ONWID( WI_set, SET_type ) ;
  ONWID( WI_fun, FUNCTION_type ) ;
  ONWID( WI_gen, GENERATOR_type ) ;
  ONWID( WI_number, NUMBER_type ) ;
  ONWID( WI_string, STRING_type ) ;
  ONWID( WI_type, TYPE_type ) ;
  ONWID( WI_fact, FACTfact ) ;
  ONWID( WI_cat, CATfact ) ;
  ONWID( WI_param, PARAMfact ) ;
  ONWID( WI_module, MODULEfact ) ;
  ONWID( WI_static, STATICfact ) ;
  ONWID( WI_word, WORDfact ) ;
  ONWID( WI_phrase, PHRASEfact ) ;
  ONWID( WI_struct, STRUCT_type ) ;
  ONWID( WI_list, LIST_type ) ;
  ONWID( WI_iterator, ITERATOR_type ) ;
  ONWID( WI_any, ANY_type ) ;
  ONWID( WI_none, NONE ) ;
  ONWID( WI_new, newNEWTYPE() ) ;
  ONWID( WI_assort, ASSORTfact ) ;
  ONWID( WI_console, CONSOLEOBJECT ) ;
""" )

############################################################################################################
############################################################################################################
############################################################################################################

W(
  'exit', 'halt', 'error',
  '.', ':', '::', '!', 'clone',
  'head', 'tail',
  'any', 'none', 'else', 'then',
  'number', '=', '+', '-', '*', '/', '+=', '-=', '<', '<=', '==', '!=', '>=', '>', '++', '--', 'mod', 'pow', 'sqrt',
  'string', 'to-string', 'newl', 'tab', 'qt', 'parse',
  'fact', 'new', 'cat',
  'en', 'is', 'has', 'does', 'noms', 'defs', 'inv', 'gets', 'param',
  'const', 'dep', 'var', 'fun', 'nom', 'defun', 'defact',
  'static', 'connect', 'modified',
  'word', 'phrase',
  'this', 'that',
  'name', 'type', 'value',
  'catch', 'throw',
  'console', 'read', 'write',
  'loop', 'stop', 'continue',
  'func', 'return', 'break', 'apply',
  'set', 'gen', 'next', 'list', 'each', 'merge', 'length', 'iterator', 'join', 'eval', 'all',
  'assort', 'struct',
  'delog', 'tron', 'troff',
  'module', 'use',
  'c', 's', 'w', 'f', 'a',
  'info',
)

############################################################################################################
############################################################################################################
############################################################################################################

META.HEADER = """

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <sysexits.h>

#include "core.h"
#include "utils.h"
#include "parser.h"

"""

############################################################################################################
############################################################################################################
############################################################################################################

META.DECL = """

typedef intptr_t n_pointer ;
typedef n_pointer n_integer ;
typedef double n_float ;
typedef char n_character ;
typedef void n_void ;
typedef n_integer n_boolean ;
typedef n_character* n_string ;
typedef n_pointer* n_array ;

typedef n_void (*n_objective)( TASK ) ;
typedef ANY (*n_constructor)( n_void ) ;
typedef ANY (*n_literal)( ANY ) ;
typedef n_string (*n_debug)( ANY ) ;

typedef REFERENCE* REFS ;

"""

############################################################################################################
############################################################################################################
############################################################################################################



	####	special types

T( 'ANY', None, None, (),"""
//  DO_TYPE ;
""" )

T( 'NONETYPE', None, None, (), """
  DO_TYPE ;
""" )

T( 'NEWTYPE', None, None, (), """
  DO_TYPE ;
""" )


T( 'IGNORETYPE' )

T( 'NOUN', None, None, (
  A( 'REFERENCE', 'object' ),
) )



	####	reference

T( 'REFERENCE', None, None, (
  A( 'TYPE', 'type' ),
  A( 'ANY', 'value' ),
  A( 'ANY', 'svalue' ),
), """
//  DO_EVALUATE ;
  DO_TYPE ;
  IFTYPE( NOUN_type,
    CONTEXT c1 = newCONTEXT( task->context->closure, ref(THIS), ref(C(NOUN,PTHAT)->object->value) ) ;
    task->next = newTASK( ref(newSETREFERENCE()), c1, task->result, task->next, task->exit ) ;
  ) ;
  ONWID( WI_clone, ref(THIS->value) ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, THIS, task->context->that ) ;
  task->next = newTASK( THIS, c1, task->result, task->next, task->exit ) ;
""",
  debug = D( ' %s', 'DEBUG( C(REFERENCE,o)->value )' )
)

T( 'REFERENCEset', 'REFERENCE', None,(), """
  RDSET( PSTHIS, PTHAT, PSTHAT ) ;
  RETURN( PTHIS ) ;
""" )

T( 'SETREFERENCE', 'REFERENCE', None, (), """
  task->next = REC( task, PSTHIS->type, ref(PSTHIS), ref(newREFERENCEset()), task->next ) ;
""" )



	####	objective

T( 'OBJECTIVE', None, None, (
  A( 'SET', 'data' ),
  A( 'REFERENCE', 'view' )
), """
  DO_COMMON ;
  NOMOREWIDS ;
  CLOSURE c1 = newCLOSURE( task->context->closure, ref(task->context), ref(THIS->view),
    ref(newOBJECTIVEreturner( task->context->closure->field, task->result, task->exit ))
  ) ;
  task->next = newTASK( ref(newEVALUATE( c1, ref(c1), THIS->data )), task->context, task->result, task->next, task->exit ) ;
""" )

T( 'OBJECTIVEreturn', None, None, (
  A( 'REFERENCE', 'object' ),
), """
  NOMOREWIDS ;
  REFERENCE r1 = ref(THIS->object) ;
  REFERENCE r2 = ref(NONE) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, r1, ref(newNOUN( task->context->that )) ) ;
  task->next = newTASK( r1, c1, r2, task->exit, task->exit ) ;
  RASET( task->result, PTHIS ) ;
""" ) ;

T( 'OBJECTIVEreturner', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'REFERENCE', 'result' ),
  A( 'TASK', 'exit' ),
), """
  IFTYPE( OBJECTIVEreturn_type,
    RASET( THIS->result, C(OBJECTIVEreturn,PTHAT)->object->value ) ;
    task->next = THIS->exit ;
  ) ;
  task->next = newTASK( ref(THIS->rest), task->context, task->result, task->next, task->exit ) ;
""" )



	####	evaluate

T( 'IDENTITY', None, None, (), """
  RETURN( PTHAT ) ;
""" )

T( 'EVALUATE', None, None, (
  A( 'CLOSURE', 'parent' ),
  A( 'REFERENCE', 'start' ),
  A( 'SET', 'list' ),
), """
  REFERENCE r1 = ref(NONE) ;

  CONTEXT c1 = newCONTEXT( THIS->parent, ref(newIDENTITY()), THIS->start ) ;
  task->next = newTASK( ref(newEVALUATOR( c1, r1 )), task->context, task->result, task->next, task->next ) ;

  CONTEXT c3 = newCONTEXT( task->context->closure, ref(THIS->list), ref(WI_each) ) ;
  task->next = newTASK( ref(THIS->list), c3, r1, task->next, task->next ) ;
""" )

T( 'EVALUATOR', None, None, (
  A( 'CONTEXT', 'context' ),
  A( 'REFERENCE', 'iterator' ),
), """

  if ( THIS->context->that->value == any(NONE) ) {
    RETURN( THIS->context->this->value ) ;
  }

  REFERENCE r1 = ref(NONE) ;
  REFERENCE r2 = ref(NONE) ;

  CONTEXT c1 = newCONTEXT( THIS->context->closure, r1, r2 ) ;
  task->next = newTASK( ref(newEVALUATOR( c1, THIS->iterator )), task->context, task->result, task->next, task->next ) ;

  CONTEXT c2 = newCONTEXT( task->context->closure, ref(THIS->iterator), ref(WI_next) ) ;
  task->next = newTASK( ref(THIS->iterator->value), c2, r2, task->next, task->next ) ;

  task->next = newTASK( THIS->context->this, THIS->context, r1, task->next, task->next ) ;

  // warning: reuse of result objects!

  if ( WID_type->instance_objective == THIS->context->that->value->objective ) {

  } else if ( WORD_type->instance_objective == THIS->context->that->value->objective ) {
    THIS->context->that->value = any( C(WORD,THIS->context->that->value)->id ) ;
  } else if ( CLOSURE_type->instance_objective == THIS->context->that->value->objective ) {

  } else {
    CONTEXT c3 = newCONTEXT( task->context->closure, THIS->context->that, ref(WI_clone) ) ;
    task->next = newTASK( THIS->context->that, c3, THIS->context->that, task->next, task->next ) ;

    if ( PHRASE_type->instance_objective == THIS->context->that->value->objective ) {
      REFERENCE r4 = ref(newEVALUATE( THIS->context->closure, ref(THIS->context->closure), c(SET,C(PHRASE,THIS->context->that->value)->value) )) ;
      task->next = newTASK( r4, task->context, THIS->context->that, task->next, task->next ) ;
    }
  }
""" )



	####	typetest

T( 'TYPETEST', None, None, (
  A( 'REFERENCE', 'r' ),
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'action' ),
), """
  if ( THIS->r->value != any(NONE) ) {
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS->this, THIS->r ) ;
    task->next = newTASK( THIS->action, c1, task->result, task->exit, task->exit ) ;
  }
  // else continue to task->next
""" )



	####	result test

T( 'FAILRESULT', None, None, (
  A( 'REFERENCE', 'value' ),
), """
  if ( !NOTNONE( THIS->value->value ) ) {
    RETURN( NONE ) ;
  }
""" )

T( 'REPLACERESULT', None, None, (
  A( 'REFERENCE', 'value' ),
  A( 'ANY', 'result' ),
), """
  if ( NOTNONE( THIS->value->value ) ) {
    RETURN( THIS->result ) ;
  } else {
    RETURN( NONE ) ;
  }
""" )

T( 'SETRESULT', None, None, (
  A( 'ANY', 'result' ),
), """
  RETURN( THIS->result ) ;
""" )



	####	task

T( 'TASK', None, None, (
  A( 'REFERENCE', 'action' ),
  A( 'CONTEXT', 'context' ),
  A( 'REFERENCE', 'result' ),
  A( 'TASK', 'next' ),
  A( 'TASK', 'exit' ),
) )



	####	closure

T( 'CLOSURE', None, None, (
  A( 'CLOSURE', 'parent' ),
  A( 'REFERENCE', 'context' ),
  A( 'REFERENCE', 'view' ),
  A( 'REFERENCE', 'field' ),
), """
  DO_TYPE ;
  ONWID( WI_COLON, tupleNEW() ) ;
  ONWID( WI_this, C(CONTEXT,THIS->context->value)->this->value ) ;
  ONWID( WI_that, C(CONTEXT,THIS->context->value)->that->value ) ;
  METHOD( WI_loop, SET_type, newLOOPaction() ) ;
  METHOD( WI_var, PARAMwa, newVARaction_wa() ) ;
  METHOP( WI_dep, newIS( ref(newFUNCTION( PARAMws, any(newDEPaction_ws()) )), ref(newFUNCTION( PARAMwas, any(newDEPaction_was()) )) ) ) ;
  METHOD( WI_catch, PARAMcs, newCATCHaction() ) ;
  METHOD( WI_defun, PARAMwcs, newDEFUNaction() ) ;
  METHOD( WI_defact, PARAMwcs, newDEFACTaction() ) ;
  METHOD( WI_nom, PARAMws, newNOMaction() ) ;
  METHOD( WI_return, ANY_type, newRETURNaction() ) ;
//  METHOD( WI_exit, NUMBER_type, newEXITaction() ) ;
  IFWID( WI_halt, exit( EX_OK ) ; ) ;
  METHOD( WI_use, ANY_type, newUSEaction() ) ;
  IFWID( WI_stop,
    task->next = newTASK( THIS->field, newCONTEXT( task->context->closure, THIS->field, ref(LOOPstop) ), task->result, task->next, task->exit ) ;
  ) ;
  METHOD( WI_error, STRING_type, newERRORaction() ) ;
  ONWID( WI_clone,  newCLOSURE( THIS->parent, THIS->context, THIS->view, THIS->field ) ) ;
  IFTYPE( WID_type, task->next = newTASK( THIS->view, task->context, task->result, task->next, task->exit ) ; ) ;
  IFTYPE( TID_type ) ;
  RETURN( PTHAT ) ;
""" )



	####	context

T( 'CONTEXT', None, None, (
  A( 'CLOSURE', 'closure' ),
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'that' ),
) )



	####	context methods

	#	error

T( 'ERRORaction', 'CLOSURE', 'STRING', (), """
  printf( "Error: %s\\n", PSTHAT->data ) ;
  RETURN( NONE ) ;
""" )

	#	var (: 'some-symbol' ( some-object ) )

T( 'VARaction_wa', 'CLOSURE', 'PARAMwa_struct', (), """
  RASET( PSTHIS->view, newHAS(
    ref( PSTHIS->view->value ),
    widNEW( C(STRING, PSTHAT->w_ref->svalue)->data  ),
    PSTHAT->a_ref
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	catch (: ( some-type ) [ ... ] )

T( 'CATCHaction', 'CLOSURE', 'PARAMcs_struct', (), """
  RASET( PSTHIS->field, newGETS(
    ref( PSTHIS->field->value ),
    C(TYPE,PSTHAT->c_ref->svalue),
    any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	defun (: 'some-symbol' ( some-type ) [ ... ] )

T( 'DEFUNaction', 'CLOSURE', 'PARAMwcs_struct', (), """
  RASET( PSTHIS->view, newHAS(
    ref( PSTHIS->view->value ),
    widNEW( C(STRING,PSTHAT->w_ref->svalue)->data ),
    ref(newFUNCTION(
      C(TYPE,PSTHAT->c_ref->svalue),
      any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
    ))
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	defact (: 'some-symbol' ( some-type ) [ ... ] )

T( 'DEFACTaction', 'CLOSURE', 'PARAMwcs_struct', (), """
  RASET( PSTHIS->view, newHAS(
    ref( PSTHIS->view->value ),
    widNEW( C(STRING,PSTHAT->w_ref->svalue)->data ),
    ref(newTYPE( newTID(), c(n_objective,NULL), any(newFUNCTION(
      C(TYPE,PSTHAT->c_ref->svalue),
      any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
    )), any(NONE) ))
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	nom (: 'some-symbol' [ ... ] )

T( 'NOMaction', 'CLOSURE', 'PARAMws_struct', (), """
  RASET( PSTHIS->view, newNOMS(
    ref(PSTHIS->view->value),
    widNEW( C(STRING, PSTHAT->w_ref->svalue)->data ),
    any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	return ( some-object )

T( 'RETURNaction', 'CLOSURE', None, (), """
  task->next = newTASK( PSTHIS->field, newCONTEXT( task->context->closure, PSTHIS->field, ref(newOBJECTIVEreturn(task->context->that)) ), task->result, task->next, task->exit ) ;
""" )

	#	exit

#T( 'EXITaction', 'CLOSURE', 'NUMBER', (), """
#  exit( (n_integer)(PSTHAT->data) ) ;
#""" )

	#	loop [ ... ]

T( 'LOOPaction', 'CONTEXT', None, (), """
  CLOSURE c1 = newCLOSURE( task->context->closure, task->context->closure->context, task->context->closure->view,
    ref(newLOOPstopper( task->context->closure->field, task->context->closure, task->result, task->exit ))
  ) ;
  CONTEXT c2 = newCONTEXT( c1, task->context->this, task->context->that ) ;
  task->next = newTASK( ref(newEVALUATE( c1, ref( c1 ), c(SET,PSTHAT) )), c2, task->result, task, task->exit ) ;
""" )

T( 'LOOPstopTYPE' )

T( 'LOOPstopper', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'CLOSURE', 'parent' ),
  A( 'REFERENCE', 'result' ),
  A( 'TASK', 'exit' ),
), """
  IFADDR( LOOPstop,
    RASET( THIS->result, THIS->parent ) ;
    task->next = THIS->exit ;
  ) ;
  task->next = newTASK( ref(THIS->rest), task->context, task->result, task->next, task->exit ) ;
""" )

	#	use ( some-object )

T( 'USEaction', 'CLOSURE', None, (), """
  RASET( PSTHIS->view, newIS(
    ref(PSTHIS->view->value),
    task->context->that
  ) ) ;
  RETURN( PTHIS ) ;
""" )


	####	object methods

	#	else [ ... ]

T( 'ELSEaction', None, None, (), """
  if ( PTHIS != any(NONE) ) RETURN( PTHIS ) ;
  task->next = newTASK( ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,PSTHAT) )), task->context, task->result, task->next, task->exit ) ;
""" )

	#	then [ ... ]

T( 'THENaction', None, None, (), """
  if ( PTHIS == any(NONE) ) RETURN( NONE ) ;
  task->next = newTASK( ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,PSTHAT) )), task->context, task->result, task->next, task->exit ) ;
""" )

	#	has (: 'some-symbol' ( some-object ) )

T( 'HASaction_wa', None, 'PARAMwa_struct', (), """
  RETURN( newHAS( task->context->this, widNEW( C(STRING, PSTHAT->w_ref->svalue)->data ), ref( any(PSTHAT->a_ref->value) ) ) ) ;
""" )

	#	does (: 'some-symbol' ( some-function ) )

T( 'DOESaction_wf', None, 'PARAMwf_struct', (), """
  RETURN( newDOES( task->context->this, widNEW( C(STRING,PSTHAT->w_ref->svalue)->data ), PSTHAT->f_ref->value ) ) ;
""" )

	#	does (: 'some-symbol' ( some-type ) [ ... ] )

T( 'DOESaction_wcs', None, 'PARAMwcs_struct', (), """
  RETURN( newDOES( task->context->this, widNEW( C(STRING,PSTHAT->w_ref->svalue)->data ),
    any(newFUNCTION(
      C(TYPE,PSTHAT->c_ref->svalue),
      any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
    ))
  ) ) ;
""" )

	#	is ( some-object )

T( 'ISaction', None, None, (), """
  RETURN( newIS( task->context->that, task->context->this ) ) ;
""" )

	#	gets (: ( some-type ) [ ... ] )

T( 'GETSaction', None, 'PARAMcs_struct', (), """
  RETURN( newGETS( task->context->this,
    C(TYPE, PSTHAT->c_ref->svalue),
    any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
  ) ) ;
""" )

	#	noms (: 'some-symbol' [ ... ] )

T( 'NOMSaction', None, 'PARAMws_struct', (), """RETURN( newNOMS( task->context->this, widNEW( C(STRING,PSTHAT->w_ref->svalue)->data ), any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view )) ) ) ; """ )



	####	object property extensions

	#	has

T( 'HAS', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WID', 'wid' ),
  A( 'REFERENCE', 'attribute' ),
), """
  DO_COMMON ;
  ONWID( WI_EQ, newHASASSIGNapplicator( newREFERENCE( HAS_type, PTHIS, any(THIS) ) ) ) ;
  ONWID( WI_EQEQ, newHASCOMPAREapplicator( newREFERENCE( HAS_type, PTHIS, any(THIS) ) ) ) ;
  IFWID( WI_clone,
    REFERENCE r1 = ref(NONE) ;
    REFERENCE r2 = ref(NONE) ;
    task->next = newTASK( ref(newSETRESULT( any(newHAS( r1, THIS->wid, r2 )) )), task->context, task->result, task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS->rest, ref(WI_clone) ) ;
    task->next = newTASK( THIS->rest, c1, r1, task->next, task->next ) ;
    CONTEXT c2 = newCONTEXT( task->context->closure, THIS->attribute, ref(WI_clone) ) ;
    task->next = newTASK( THIS->attribute, c2, r2, task->next, task->next ) ;
  ) ;

  if ( PTHIS->objective == OBSERVER_type->instance_objective ) {
    ONWID( THIS->wid, obsNEW( C(OBSERVER,PTHIS), THIS->attribute ) ) ;
  } else {
    ONWID( THIS->wid, THIS->attribute->value ) ;
  }

  task->next = newTASK( THIS->rest, task->context, task->result, task->next, task->exit ) ;
""" )

T( 'HASASSIGNapplicator', None, None, (
  A( 'REFERENCE', 'has' ),
), """
  DO_COMMON ;

  RASET( task->result, THIS->has->value ) ;

  REFERENCE r5 = ref(NONE) ;

  CONTEXT c4 = newCONTEXT( task->context->closure, r5, task->context->that ) ;
  task->next = newTASK( r5, c4, ref(NONE), task->exit, task->exit ) ;

  CONTEXT c5 = newCONTEXT( task->context->closure, C(HAS,THIS->has->svalue)->rest, ref(WI_EQ) ) ;
  task->next = newTASK( C(HAS,THIS->has->svalue)->rest, c5, r5, task->next, task->next ) ;
  // rest reference should maintain observer if any exists

  REFERENCE r2 = ref(NONE) ;
  REFERENCE r3 = ref(NONE) ;

  CONTEXT c1 = newCONTEXT( task->context->closure, r2, r3 ) ;
  task->next = newTASK( r2, c1, ref(NONE), task->next, task->next ) ;

  CONTEXT c2 = newCONTEXT( task->context->closure, C(HAS,THIS->has->svalue)->attribute, ref(WI_EQ) ) ;
  task->next = newTASK( C(HAS,THIS->has->svalue)->attribute, c2, r2, task->next, task->next ) ;
  // attribute reference should maintain observer if any exists

  CONTEXT c3 = newCONTEXT( task->context->closure, task->context->that, ref(C(HAS,THIS->has->svalue)->wid) ) ;
  task->next = newTASK( task->context->that, c3, r3, task->next, task->next ) ;

""" )

T( 'HASCOMPAREapplicator', None, None, (
  A( 'REFERENCE', 'has' ),
), """
  DO_COMMON ;

  REFERENCE r4 = ref(NONE) ;
  REFERENCE r5 = ref(NONE) ;

  TASK t1 = newTASK( ref(newREPLACERESULT( r4, task->context->that->value )), task->context, task->result, task->next, task->exit ) ;

  TASK t2 = newTASK( ref(newSETRESULT( task->context->that->value )), task->context, task->result, task->next, task->exit ) ;

  CONTEXT c4 = newCONTEXT( task->context->closure, r5, task->context->that ) ;
  task->next = newTASK( r5, c4, r4, t2, t1 ) ;

  CONTEXT c5 = newCONTEXT( task->context->closure, C(HAS,THIS->has->svalue)->rest, ref(WI_EQEQ) ) ;
  task->next = newTASK( C(HAS,THIS->has->svalue)->rest, c5, r5, task->next, task->next ) ;

  REFERENCE r1 = ref(NONE) ;
  REFERENCE r2 = ref(NONE) ;
  REFERENCE r3 = ref(NONE) ;

  task->next = newTASK( ref(newFAILRESULT( r1 )), task->context, task->result, task->next, task->exit ) ;

  CONTEXT c1 = newCONTEXT( task->context->closure, r2, r3 ) ;
  task->next = newTASK( r2, c1, r1, task->next, task->next ) ;

  CONTEXT c2 = newCONTEXT( task->context->closure, C(HAS,THIS->has->svalue)->attribute, ref(WI_EQEQ) ) ;
  task->next = newTASK( C(HAS,THIS->has->svalue)->attribute, c2, r2, task->next, task->next ) ;

  CONTEXT c3 = newCONTEXT( task->context->closure, task->context->that, ref(C(HAS,THIS->has->svalue)->wid) ) ;
  task->next = newTASK( task->context->that, c3, r3, task->next, task->next ) ;

""" )

	#	does

T( 'DOES', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WID', 'wid' ),
  A( 'ANY', 'action' ),
), """
  DO_COMMON ;
  IFWID( WI_clone,
    REFERENCE r1 = ref(NONE) ;
    task->next = newTASK( ref(newSETRESULT( any(newDOES( r1, THIS->wid, THIS->action )) )), task->context, task->result, task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS->rest, ref(WI_clone) ) ;
    task->next = newTASK( THIS->rest, c1, r1, task->next, task->next ) ;
  ) ;
  ONWID( THIS->wid, newAPPLICATOR( task->context->this, ref(THIS->action) ) ) ;
  task->next = newTASK( THIS->rest, task->context, task->result, task->next, task->exit ) ;
""" )

	#	is

T( 'IS', None, None, (
  A( 'REFERENCE', 'object_1' ),
  A( 'REFERENCE', 'object_2' ),
), """
  DO_COMMON ;
  IFWID( WI_clone,
    REFERENCE r1 = ref(NONE) ;
    REFERENCE r2 = ref(NONE) ;
    task->next = newTASK( ref(newSETRESULT( any(newIS( r1, r2 )) )), task->context, task->result, task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS->object_1, ref(WI_clone) ) ;
    task->next = newTASK( THIS->object_1, c1, r1, task->next, task->next ) ;
    CONTEXT c2 = newCONTEXT( task->context->closure, THIS->object_2, ref(WI_clone) ) ;
    task->next = newTASK( THIS->object_2, c2, r2, task->next, task->next ) ;
  ) ;
  task->next = newTASK( ref(THIS->object_1->value), task->context, task->result, newTASK( ref(THIS->object_2->value), task->context, task->result, task->next, task->exit ), task->exit ) ;
""" )

	#	gets

T( 'GETS', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'TYPE', 'type' ),
  A( 'ANY', 'action' ),
), """
  DO_COMMON ;
  task->next = REC( task, THIS->type, task->context->this, ref(THIS->action), newTASK( THIS->rest, task->context, task->result, task->next, task->exit ) ) ;
""" )

	#	noms

T( 'NOMS', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WID', 'wid' ),
  A( 'ANY', 'action' ),
), """
  DO_COMMON ;
  IFWID( WI_clone,
    REFERENCE r1 = ref(NONE) ;
    task->next = newTASK( ref(newSETRESULT( any(newNOMS( r1, THIS->wid, THIS->action )) )), task->context, task->result, task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS->rest, ref(WI_clone) ) ;
    task->next = newTASK( THIS->rest, c1, r1, task->next, task->next ) ;
  ) ;
  IFWID( THIS->wid,
    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->this, ref(NONE) ) ;
    task->next = newTASK( ref(THIS->action), c1, task->result, task->exit, task->exit ) ;
  ) ;
  task->next = newTASK( THIS->rest, task->context, task->result, task->next, task->exit ) ;
""" )



	####	static dependencies

T( 'DEPcatcher', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'DEPENDENCY', 'dep' ),
), """
  IFTYPE( DEPENDENCY_type,
    if ( !listHASELEMENT( C(DEPENDENCY,PTHAT)->out, ref(THIS->dep) ) ) {
      listAPPEND( THIS->dep->in, task->context->that ) ;
      listAPPEND( C(DEPENDENCY,PTHAT)->out, ref(THIS->dep) ) ;
    }
  ) ;
  task->next = newTASK( ref(THIS->rest), task->context, task->result, task->next, task->exit ) ;
""" )

	#	dep (: 'some-symbol' [ ... ] )

T( 'DEPaction_ws', 'CLOSURE', 'PARAMws_struct', (), """
  RETURN( NONE ) ;
""" )

	#	dep (: 'some-symbol' ( some-object ) [ ... ] )

T( 'DEPaction_was', 'CLOSURE', 'PARAMwas_struct', (), """
  RASET( PSTHIS->view, newHAS(
    ref( PSTHIS->view->value ),
    widNEW( C(STRING,PSTHAT->w_ref->svalue)->data ),
    ref(newOBSERVER( newDEPENDENCY( listNEW( DEPENDENCY_type ), listNEW( DEPENDENCY_type ), PSTHAT->a_ref,
      newDEFINITION(
        task->context->closure,
        any( PSTHAT->s_ref->svalue )
      ), TRUE
    ), PSTHAT->a_ref ))
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	inv (: 'some-symbol' [ ... ] )

T( 'INVaction_ws', None, 'PARAMws_struct', (), """
  RETURN( NONE ) ;
""" )

	#	inv (: 'some-symbol' ( some-object ) [ ... ] )

T( 'INVaction_was', None, 'PARAMwas_struct', (), """
  RETURN( newHAS(
    ref( task->context->closure->view->value ),
    widNEW( C(STRING,PSTHAT->w_ref->svalue)->data ),
    ref(newOBSERVER( newDEPENDENCY( listNEW( DEPENDENCY_type ), listNEW( DEPENDENCY_type ), PSTHAT->a_ref,
      newDEFINITION(
        task->context->closure,
        any( PSTHAT->s_ref->svalue )
      ), TRUE
    ), PSTHAT->a_ref ))
  ) ) ;
""" )

T( 'DEPENDENCY', None, None, (
  A( 'LIST', 'in' ),
  A( 'LIST', 'out' ),
  A( 'REFERENCE', 'state' ),
  A( 'DEFINITION', 'definition' ),
  A( 'n_boolean', 'initialize' ),
), """
  DO_TYPE ;

  IFWID( WI_modified,
    depPROPAGATE( task, THIS ) ;
  ) ;

  IFWID( WI_connect,
    task->next = newTASK( ref(newSETRESULT( any(newOBSERVER( THIS, THIS->state )) )), task->context, task->result, task->next, task->exit ) ;
    task->next = newTASK( task->context->closure->field, newCONTEXT( task->context->closure, task->context->closure->field, ref(THIS) ), task->result, task->next, task->next ) ;
  ) ;

""" )

T( 'OBSERVER', None, None, (
  A( 'DEPENDENCY', 'dep' ),
  A( 'REFERENCE', 'object' ),
), """
  if ( THIS->dep->initialize ) {
    THIS->dep->initialize = FALSE ;
    task->next = newTASK( task->action, task->context, task->result, task->next, task->exit ) ;
    depREEVALUATE( task, THIS->dep ) ;
    CONTINUE ;
  }

  ONWID( WI_clone, THIS ) ;
  IFWID( WI_EXCLAIM,
    USE_ON( exit, THIS ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS->object, ref(WI_clone) ) ;
    task->next = newTASK( THIS->object, c1, task->result, task->exit, task->exit ) ;
  ) ;
  task->next = newTASK( THIS->object, task->context, task->result, task->next, task->exit ) ;
""" )

T( 'DEFINITION', None, None, (
  A( 'CLOSURE', 'closure' ),
  A( 'ANY', 'expression' ),
), """
""" )

T( 'PROPAGATEtest', None, None, (
  A( 'DEPENDENCY', 'dep' ),
  A( 'REFERENCE', 'result' ),
), """
  if ( !NOTNONE( THIS->result->value ) ) {
    task->next = newTASK( ref(THIS->dep), newCONTEXT( task->context->closure, ref(THIS->dep), ref(WI_modified) ), task->result, task->next, task->next ) ;
  }
""" )

T( 'DEPENDENCYreset', None, None, (
  A( 'DEPENDENCY', 'dep' ),
), """
  depRESET( THIS->dep ) ;
""" )

T( 'STATICconst_s', None, None, (), """
  REFERENCE r1 = ref(NONE) ;
  RETURN(
    newOBSERVER(
      newDEPENDENCY( listNEW( DEPENDENCY_type ), listNEW( DEPENDENCY_type ), r1,
        newDEFINITION(
          task->context->closure,
          PSTHAT
        ), TRUE
      ),
      r1
    )
  ) ;
""" )

T( 'STATICconst_as', None, 'PARAMas_struct', (), """
  RETURN(
    newOBSERVER(
      newDEPENDENCY( listNEW( DEPENDENCY_type ), listNEW( DEPENDENCY_type ), PSTHAT->a_ref,
        newDEFINITION(
          task->context->closure,
          PSTHAT->s_ref->value
        ), TRUE
      ),
      PSTHAT->a_ref
    )
  ) ;
""" )


	####	parameters used by builtins

P( 'as', X( 'a', 'ANY' ), X( 's', 'SET' ) )

P( 'wa', X( 'w', 'STRING' ), X( 'a', 'ANY' ) )
P( 'wc', X( 'w', 'STRING' ), X( 'c', 'TYPE' ) )
P( 'ws', X( 'w', 'STRING' ), X( 's', 'SET' ) )
P( 'wf', X( 'w', 'STRING' ), X( 'f', 'FUNCTION' ) )

P( 'wca', X( 'w', 'STRING' ), X( 'c', 'TYPE' ), X( 'a', 'ANY' ) )
P( 'wcs', X( 'w', 'STRING' ), X( 'c', 'TYPE' ), X( 's', 'SET' ) )

P( 'was', X( 'w', 'STRING' ), X( 'a', 'ANY' ), X( 's', 'SET' ) )

P( 'cs', X( 'c', 'TYPE' ), X( 's', 'SET' ) )



	####	param (: (: 'some-symbol' ( some-type ) ) ... )

T( 'PARAMconst', None, 'TUPLE', (), """
  REFERENCE r1 = ref(NONE) ;
  task->next = newTASK( ref(newPARAMfinnish( r1 )), task->context, task->result, task->next, task->exit ) ;
  task->next = newTASK( ref(newASSORTconst()), task->context, r1, task->next, task->next ) ;
""" )

T( 'PARAMfinnish', None, None, (
  A( 'REFERENCE', 'assorter' ),
), """
  RETURN( newTYPE( newTID(), c(n_objective,NULL), any(NONE), THIS->assorter->value ) ) ;
""" )



	####	struct (: (: 'some-symbol' ( some-type ) ) ... )

T( 'STRUCTconst', None, 'TUPLE', (), """
  REFERENCE r1 = ref(NONE) ;
  task->next = newTASK( ref(newSTRUCTfinnish( r1 )), task->context, task->result, task->next, task->exit ) ;
  task->next = newTASK( ref(newASSORTconst()), task->context, r1, task->next, task->next ) ;
""" )

T( 'STRUCTfinnish', None, None, (
  A( 'REFERENCE', 'assorter' ),
), """
  RETURN( newTYPE( newTID(), c(n_objective,NULL), THIS->assorter->value, any(NONE) ) ) ;
""" )



	####	assort (: (: 'some-symbol' ( some-type ) ) ... )

T( 'ASSORTconst', None, 'TUPLE', (), """
  ASSORTER assorter = newASSORTER( listNEW( PARAMwc_struct_type ) ) ;
  task->next = newTASK( ref(newASSORTfinnish( assorter )), task->context, task->result, task->next, task->exit ) ;
  n_integer i ;
  for ( i = PSTHAT->length-1 ; i >= 0 ; i-- ) {
    REFERENCE r1 = ref(NONE) ;
    task->next = newTASK( ref(newASSORTprocess( assorter, r1 )), task->context, ref(NONE), task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->this/**/, PSTHAT->data[ i ] ) ;
    task->next = newTASK( ref(newPARAMwc_assort()), c1, r1, task->next, task->next ) ;
  }
""" )

T( 'ASSORTprocess', None, None, (
  A( 'ASSORTER', 'assorter' ),
  A( 'REFERENCE', 'e' ),
), """
  if ( NOTNONE( THIS->e->value ) ) {
    listAPPEND( THIS->assorter->elements, THIS->e ) ;
  } else {
    RETURN( NONE ) ;
  }
""" )

T( 'ASSORTfinnish', None, None, (
  A( 'ASSORTER', 'assorter' ),
), """
  RETURN( newFUNCTION( TUPLE_type, any(newFUNCTION( TUPLE_type, any(THIS->assorter) )) ) ) ;
""" )

	#	assorter (: ... )

T( 'ASSORTER', None, 'TUPLE', (
  A( 'LIST', 'elements' ),
), """
  if ( THIS->elements->length == PSTHAT->length ) {
    STRUCT assortment = newSTRUCT( listNEW( PARAMwa_struct_type ) ) ;
    task->next = newTASK( ref(newASSORTERfinnish( assortment )), task->context, task->result, task->next, task->exit ) ;
    n_integer i ;
    for ( i = 0 ; i < THIS->elements->length ; i++ ) {
      REFERENCE e_ref = refNEW( C(TYPE,C(PARAMwc_struct,THIS->elements->data[ i ]->svalue)->c_ref->svalue), any(NONE) ) ;
      REFERENCE e_ref_ref = ref(e_ref) ;
      task->next = newTASK( ref(newASSORTERprocess( assortment, C(PARAMwc_struct,THIS->elements->data[ i ]->svalue)->w_ref, e_ref )), task->context, ref(NONE), task->next, task->exit ) ;
      CONTEXT c1 = newCONTEXT( task->context->closure, e_ref_ref, ref(newNOUN( PSTHAT->data[ i ] )) ) ;
      task->next = newTASK( e_ref_ref, c1, ref(NONE), task->next, task->next ) ;
    }
  }
""" )

T( 'ASSORTERprocess', None, None, (
  A( 'STRUCT', 'assortment' ),
  A( 'REFERENCE', 'w' ),
  A( 'REFERENCE', 'a' ),
), """
  if ( NOTNONE( THIS->a->value ) ) {
    listAPPEND( THIS->assortment->elements, ref(newATTRIBUTE( ref(widNEW( C(STRING,THIS->w->svalue)->data )), THIS->a )) ) ;
  } else {
    RETURN( NONE ) ;
  }
""" )

T( 'ASSORTERfinnish', None, None, (
  A( 'STRUCT', 'assortment' ),
), """
  RETURN( THIS->assortment ) ;
""" )



	####	struct/attribute

T( 'ATTRIBUTE', None, None, (
  A( 'REFERENCE', 'w' ),
  A( 'REFERENCE', 'a' ),
), """
""" )

T( 'STRUCT', None, None, (
  A( 'LIST', 'elements' ),
), """
  DO_TYPE ;
  ONWID( WI_EQ, newSTRUCTASSIGNapplicator( newREFERENCE( HAS_type, PTHIS, any(THIS) ) ) ) ;
  ONWID( WI_EQEQ, newSTRUCTCOMPAREapplicator( newREFERENCE( HAS_type, PTHIS, any(THIS) ) ) ) ;
  IFWID( WI_clone,
    LIST elements = listNEW( ANY_type ) ;
    task->next = newTASK( ref(newSETRESULT( any(newSTRUCT( elements )) )), task->context, task->result, task->next, task->exit ) ;
    n_integer i ;
    for ( i = 0 ; i < THIS->elements->length ; i++ ) {
      REFERENCE r1 = ref(NONE) ;
      listAPPEND( elements, ref(newATTRIBUTE( C(ATTRIBUTE,THIS->elements->data[ i ]->svalue)->w, r1 )) ) ;
      CONTEXT c1 = newCONTEXT( task->context->closure, C(ATTRIBUTE,THIS->elements->data[ i ]->svalue)->a, ref(WI_clone) ) ;
      task->next = newTASK( C(ATTRIBUTE,THIS->elements->data[ i ]->svalue)->a, c1, r1, task->next, task->next ) ;
    }
  ) ;
  n_integer i ;
  for ( i = 0 ; i < THIS->elements->length ; i++ ) {
    ONWID( C(ATTRIBUTE,THIS->elements->data[ i ]->svalue)->w->svalue, C(ATTRIBUTE,THIS->elements->data[ i ]->svalue)->a->value ) ;
  }
""" )

T( 'STRUCTASSIGNapplicator', None, None, (
  A( 'REFERENCE', 'structure' ),
), """
  DO_COMMON ;
  RASET( task->result, THIS->structure->value ) ;
  n_integer i ;
  for ( i = 0 ; i < C(STRUCT,THIS->structure->svalue)->elements->length ; i++ ) {
    task->next = newTASK( ref( newATTRIBUTEassign( C(ATTRIBUTE,C(STRUCT,THIS->structure->svalue)->elements->data[ i ]->svalue) ) ), task->context, ref(NONE), task->next, task->next ) ;
  }
""" )

T( 'ATTRIBUTEassign', None, None, (
  A( 'ATTRIBUTE', 'attribute' ),
), """
  DO_COMMON ;

  REFERENCE r2 = ref(NONE) ;
  REFERENCE r3 = ref(NONE) ;

  CONTEXT c1 = newCONTEXT( task->context->closure, r2, r3 ) ;
  task->next = newTASK( r2, c1, ref(NONE), task->next, task->next ) ;

  CONTEXT c2 = newCONTEXT( task->context->closure, C(ATTRIBUTE,THIS->attribute)->a, ref(WI_EQ) ) ;
  task->next = newTASK( C(ATTRIBUTE,THIS->attribute)->a, c2, r2, task->next, task->next ) ;

  CONTEXT c3 = newCONTEXT( task->context->closure, task->context->that, C(ATTRIBUTE,THIS->attribute)->w ) ;
  task->next = newTASK( task->context->that, c3, r3, task->next, task->next ) ;
""" )

T( 'STRUCTCOMPAREapplicator', None, None, (
  A( 'REFERENCE', 'structure' ),
), """
  DO_COMMON ;
  task->next = newTASK( ref(newSETRESULT( task->context->that->value )), task->context, task->result, task->next, task->exit ) ;
  n_integer i ;
  for ( i = 0 ; i < C(STRUCT,THIS->structure->svalue)->elements->length ; i++ ) {
    task->next = newTASK( ref( newATTRIBUTEcompare( C(ATTRIBUTE,C(STRUCT,THIS->structure->svalue)->elements->data[ i ]->svalue) ) ), task->context, ref(NONE), task->next, task->exit ) ;
  }
""" )

T( 'ATTRIBUTEcompare', None, None, (
  A( 'ATTRIBUTE', 'attribute' ),
), """
  DO_COMMON ;

  REFERENCE r1 = ref(NONE) ;
  REFERENCE r2 = ref(NONE) ;
  REFERENCE r3 = ref(NONE) ;

  task->next = newTASK( ref(newFAILRESULT( r1 )), task->context, task->result, task->next, task->exit ) ;

  CONTEXT c1 = newCONTEXT( task->context->closure, r2, r3 ) ;
  task->next = newTASK( r2, c1, r1, task->next, task->next ) ;

  CONTEXT c2 = newCONTEXT( task->context->closure, C(ATTRIBUTE,THIS->attribute)->a, ref(WI_EQEQ) ) ;
  task->next = newTASK( C(ATTRIBUTE,THIS->attribute)->a, c2, r2, task->next, task->next ) ;

  CONTEXT c3 = newCONTEXT( task->context->closure, task->context->that, C(ATTRIBUTE,THIS->attribute)->w ) ;
  task->next = newTASK( task->context->that, c3, r3, task->next, task->next ) ;

""" )



	####	console

T( 'CONSOLE', None, None, (), """
  DO_TYPE ;
  IFWID( WI_read, task->next = newTASK( ref(newREADaction()), task->context, task->result, task->next, task->exit ) ; ) ;
  ONWID( WI_write, newWRITER() ) ;
""" )

	#	read

T( 'READaction', 'CONSOLE', None, (), """
  size_t buffer_length = 0 ;
  char* buffer ;
  size_t length = getline( &buffer, &buffer_length, stdin ) ;
  if ( length == -1 ) {
    RETURN( NONE ) ;
  } else {
    buffer[ length - 1 ] = 0x00 ;
    RETURN( newSTRING( buffer ) ) ;
  }
""" )

	#	writer

T( 'WRITER', None, None, (), """
  DO_COMMON ;
  task->next = REC( task, STRING_type, ref(NONE), ref(newWRITEaction()), task->next ) ;
""" )

	#	write

T( 'WRITEaction', None, 'STRING', (), """
  printf( "%s", PSTHAT->data ) ;
  RETURN( newWRITER() ) ;
""" )



	####	module

T( 'MODULEconst', None, 'STRING', (), """
  n_integer parse_index = 0 ;
  PHRASE program = C( PHRASE, PARSE( &parse_index, read_source( PSTHAT->data ) ) ) ;

  CONTEXT c1 = newCONTEXT( ROOT->parent, ref(NONE), ref(NONE) ) ;
  task->next = newTASK( ref(newOBJECTIVE( c(SET,program->value), ROOT->view )), c1, task->result, task->next, task->exit ) ;
""" )




	####	applicator

T( 'APPLICATOR', None, None, (
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'action' ),
), """
  DO_TYPE ;
  CONTEXT c1 = newCONTEXT( task->context->closure, THIS->this, task->context->that ) ;
  task->next = newTASK( THIS->action, c1, task->result, task->next, task->exit ) ;
""" )



	####	function

T( 'FUNCTION', None, None, (
  A( 'TYPE', 'type' ),
  A( 'ANY', 'action' ),
), """
  DO_TYPE ;
  METHOD( WI_apply, ANY_type, newAPPLYaction() ) ;
  NOMOREWIDS ;
  task->next = REC( task, THIS->type, task->context->this, ref( THIS->action ), task->next ) ;
""" )

T( 'FUNCTIONconst', 'TYPE', 'PARAMcs_struct', (), """
  RETURN( newFUNCTION(
    C(TYPE,PSTHAT->c_ref->svalue),
    any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
  ) ) ;
""" )

T( 'APPLYaction', 'FUNCTION', None, (), """
  RETURN( newAPPLICATOR( task->context->that, task->context->this ) ) ;
""" )



	####	type

T( 'TYPE', None, None, (
  A( 'TID', 'id' ),
  A( 'n_objective', 'instance_objective' ),
  A( 'ANY', 'constructor' ),
  A( 'ANY', 'comparator' ),
), """
  DO_TYPE ;
  if ( THIS->instance_objective == c(n_objective,NULL) ) {
    REFERENCE r1 = ref(NONE ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS_R, r1 ) ;
    TASK t1 = newTASK( ref(newSIGNATUREconst()), c1, task->result, task->next, task->exit ) ;
    task->next = newTASK( ref(THIS->constructor), task->context, r1, task->next, t1 ) ;
  } else {
    task->next = newTASK( ref(THIS->constructor), task->context, task->result, task->next, task->exit ) ;
  }
""" )

T( 'TID' )

T( 'SIGNATURE', None, None, (
  A( 'TYPE', 'type' ),
  A( 'REFERENCE', 'rest' ),
), """
  DO_TYPE ;
  if ( c( n_integer, PTHAT ) == c( n_integer, THIS->type->id ) ) { RETURN( newREFERENCE( THIS->type, PTHIS, any(THIS) ) ) ; }
  IFWID( WI_clone,
    REFERENCE r1 = ref(NONE) ;
    task->next = newTASK( ref(newSETRESULT( any(newSIGNATURE( THIS->type, r1 )) )), task->context, task->result, task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS->rest, ref(WI_clone) ) ;
    task->next = newTASK( THIS->rest, c1, r1, task->next, task->next ) ;
  ) ;
  task->next = newTASK( THIS->rest, task->context, task->result, task->next, task->exit ) ;
""" )

T( 'SIGNATUREconst', 'TYPE', None, (), """
  RETURN( newSIGNATURE( PSTHIS, task->context->that ) ) ;
""" )

	#	cat [ ... ]

T( 'CATconst', None, None, (), """
  RETURN( newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newOBJECTIVE( c(SET,PSTHAT), task->context->closure->view )) ) ) ;
""" )

	#	fact ( some-object )

T( 'FACTconst', 'TYPE', None, (), """
  RETURN( newTYPE( newTID(), c(n_objective,NULL), PTHAT, any(NONE) ) ) ;
""" )



	####	number

T( 'NUMBER', None, None, (
  A( 'n_float', 'data' ),
), """
  DO_TYPE ;
  IFWID( WI_ADDADD, MOD_ON( exit, PTHIS ) ; THIS->data++ ; RETURN( THIS ) ; ) ;
  IFWID( WI_SUBSUB, MOD_ON( exit, PTHIS ) ; THIS->data-- ; RETURN( THIS ) ; ) ;
  METHOD( WI_EQ,     NUMBER_type, newNUMBERset() ) ;
  METHOD( WI_ADDEQ,  NUMBER_type, newNUMBERaddset() ) ;
  METHOD( WI_SUBEQ,  NUMBER_type, newNUMBERsubset() ) ;
  METHOD( WI_ADD,    NUMBER_type, newNUMBERadd() ) ;
  METHOD( WI_SUB,    NUMBER_type, newNUMBERsub() ) ;
  METHOD( WI_MUL,    NUMBER_type, newNUMBERmul() ) ;
  METHOD( WI_DIV,    NUMBER_type, newNUMBERdiv() ) ;
  METHOD( WI_EXCLAIMEQ,     NUMBER_type, newNUMBERneq() ) ;
  METHOD( WI_EQEQ,   NUMBER_type, newNUMBEReq() ) ;
  METHOD( WI_LTEQ,   NUMBER_type, newNUMBERlteq() ) ;
  METHOD( WI_GTEQ,   NUMBER_type, newNUMBERgteq() ) ;
  METHOD( WI_LT,     NUMBER_type, newNUMBERlt() ) ;
  METHOD( WI_GT,     NUMBER_type, newNUMBERgt() ) ;
  METHOD( WI_mod,    NUMBER_type, newNUMBERmod() ) ;
  METHOD( WI_pow,    NUMBER_type, newNUMBERpow() ) ;
  ONWID( WI_clone,  newNUMBER( THIS->data ) ) ;
  ONWID( WI_sqrt,   newNUMBER( sqrt( THIS->data ) ) ) ;
  ONWID( WI_toSUBstring, STRX( "%g", c(n_float,THIS->data) ) ) ;
""",
debug = D( ' %f', 'c( n_float, C( NUMBER, o )->data )' )
)

	#	number methods

T( 'NUMBEReq',     'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; if ( PSTHIS->data == PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERneq',    'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; if ( PSTHIS->data != PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERlteq',   'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; if ( PSTHIS->data <= PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERgteq',   'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; if ( PSTHIS->data >= PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERlt',     'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; if ( PSTHIS->data < PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERgt',     'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; if ( PSTHIS->data > PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERadd',    'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; RETURN( newNUMBER( PSTHIS->data + PSTHAT->data ) ) ;""" )
T( 'NUMBERsub',    'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; RETURN( newNUMBER( PSTHIS->data - PSTHAT->data ) ) ;""" )
T( 'NUMBERmul',    'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; RETURN( newNUMBER( PSTHIS->data * PSTHAT->data ) ) ;""" )
T( 'NUMBERdiv',    'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; RETURN( newNUMBER( PSTHIS->data / PSTHAT->data ) ) ;""" )
T( 'NUMBERmod',    'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; RETURN( newNUMBER( fmod( PSTHIS->data, PSTHAT->data ) ) ) ;""" )
T( 'NUMBERpow',    'NUMBER', 'NUMBER', (), """USE_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; RETURN( newNUMBER( pow( PSTHIS->data, PSTHAT->data ) ) ) ;""" )

T( 'NUMBERaddset', 'NUMBER', 'NUMBER', (), """if ( PSTHAT->data != 0 ) MOD_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; PSTHIS->data += PSTHAT->data ; RETURN( PTHIS ) ;""" )
T( 'NUMBERsubset', 'NUMBER', 'NUMBER', (), """if ( PSTHAT->data != 0 ) MOD_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; PSTHIS->data -= PSTHAT->data ; RETURN( PTHIS ) ;""" )
T( 'NUMBERset',    'NUMBER', 'NUMBER', (), """if ( PSTHIS->data != PSTHAT->data ) { MOD_ON( exit, PTHIS ) ; USE_ON( exit, PTHAT ) ; PSTHIS->data = PSTHAT->data ; } RETURN( PTHIS ) ;""" )



	####	set

T( 'SET', None, None, (), """
  DO_TYPE ;
  METHOD( WI_EQEQ, SET_type, newSETCOMPAREaction() ) ;
  METHOD( WI_join, STRING_type, newJOINaction() ) ;
  IFWID( WI_toSUBstring, task->next = newTASK( ref(newSETTOSTRaction()), task->context, task->result, task->exit, task->exit ) ; );
  IFWID( WI_all, task->next = newTASK( ref(newSETALLaction()), task->context, task->result, task->exit, task->exit ) ; );
""" )

	#	compare

T( 'SETCOMPAREaction', None, None, (), """
  USE_ON( exit, PTHAT ) ;
  USE_ON( exit, PTHIS ) ;

  REFERENCE r1 = ref(NONE) ;
  REFERENCE r2 = ref(NONE) ;
  REFERENCE r3 = ref(NONE) ;
  REFERENCE r4 = ref(NONE) ;

  task->next = newTASK( ref(newSETCOMPAREiterate( r1, r2, r3, r4 )), task->context, task->result, task->next, task->exit ) ;

  CONTEXT c4 = newCONTEXT( task->context->closure, r3, ref(WI_next) ) ;
  task->next = newTASK( r3, c4, r4, task->next, task->next ) ;
  CONTEXT c3 = newCONTEXT( task->context->closure, ref(PTHAT), ref(WI_each) ) ;
  task->next = newTASK( ref(PTHAT), c3, r3, task->next, task->next ) ;

  CONTEXT c2 = newCONTEXT( task->context->closure, r1, ref(WI_next) ) ;
  task->next = newTASK( r1, c2, r2, task->next, task->next ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, ref(PTHIS), ref(WI_each) ) ;
  task->next = newTASK( ref(PTHIS), c1, r1, task->next, task->next ) ;
""" )

T( 'SETCOMPAREiterate', None, None, (
  A( 'REFERENCE', 'iterator1' ),
  A( 'REFERENCE', 'element1' ),
  A( 'REFERENCE', 'iterator2' ),
  A( 'REFERENCE', 'element2' ),
), """
  if ( NOTNONE( THIS->element1->value ) ) {
    if ( NOTNONE( THIS->element2->value ) ) {
      REFERENCE r1 = ref(NONE) ;
      REFERENCE r2 = ref(NONE) ;
      task->next = newTASK( ref(newSETCOMPAREiterate( THIS->iterator1, r1, THIS->iterator2, r2 )), task->context, task->result, task->next, task->exit ) ;

      CONTEXT c1 = newCONTEXT( task->context->closure, THIS->iterator1, ref(WI_next) ) ;
      task->next = newTASK( THIS->iterator1, c1, r1, task->next, task->next ) ;
      CONTEXT c2 = newCONTEXT( task->context->closure, THIS->iterator2, ref(WI_next) ) ;
      task->next = newTASK( THIS->iterator2, c2, r2, task->next, task->next ) ;

      REFERENCE r3 = ref(NONE) ;
      REFERENCE r4 = ref(NONE) ;

      task->next = newTASK( ref(newFAILRESULT( r4 )), task->context, task->result, task->next, task->exit ) ;

      CONTEXT c4 = newCONTEXT( task->context->closure, r3, THIS->element2 ) ;
      task->next = newTASK( r3, c4, r4, task->next, task->next ) ;

      CONTEXT c3 = newCONTEXT( task->context->closure, THIS->element1, ref(WI_EQEQ) ) ;
      task->next = newTASK( THIS->element1, c3, r3, task->next, task->next ) ;

    } else {
      RETURN( NONE ) ;
    }
  } else {
    if ( NOTNONE( THIS->element2->value ) ) {
      RETURN( NONE ) ;
    } else {
      RETURN( task->context->that->value ) ;
    }
  }
""" )


	#	all

T( 'SETALLaction', None, None, (), """
  REFERENCE r1 = ref(NONE) ;
  REFERENCE r2 = ref(NONE) ;
  task->next = newTASK( ref(newSETALLiterate( r1, r2 )), task->context, task->result, task->next, task->exit ) ;
  CONTEXT c2 = newCONTEXT( task->context->closure, r1, ref(WI_next) ) ;
  task->next = newTASK( r1, c2, r2, task->next, task->next ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, ref(PTHIS), ref(WI_each) ) ;
  task->next = newTASK( ref(PTHIS), c1, r1, task->next, task->next ) ;
""" )

T( 'SETALLiterate', None, None, (
  A( 'REFERENCE', 'iterator' ),
  A( 'REFERENCE', 'element' ),
), """
  if ( NOTNONE( THIS->element->value ) ) {
    REFERENCE r1 = ref(NONE) ;
    task->next = newTASK( ref(newSETALLiterate( THIS->iterator, r1 )), task->context, task->result, task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, THIS->iterator, ref(WI_next) ) ;
    task->next = newTASK( THIS->iterator, c1, r1, task->next, task->next ) ;
    CONTEXT c2 = newCONTEXT( task->context->closure, task->context->closure->field, THIS->element ) ;
    task->next = newTASK( task->context->closure->field, c2, task->result, task->next, task->next ) ;
  } else {
    RETURN( task->context->this->value ) ;
  }
""" )


	#	to-string

T( 'SETTOSTRaction', None, None, (), """
  REFERENCE r1 = ref(NONE) ;
  REFERENCE r2 = ref(NONE) ;

  REFERENCE e_ref = refNEW( STRING_type, any(NONE) ) ;
  REFERENCE e_ref_ref = ref(e_ref) ;

  task->next = newTASK( ref(newSETTOSTRfinnish( e_ref )), task->context, task->result, task->next, task->exit ) ;

  CONTEXT c3 = newCONTEXT( task->context->closure, e_ref_ref, ref(newNOUN( r2 )) ) ;
  task->next = newTASK( e_ref_ref, c3, ref(NONE), task->next, task->next ) ;

  CONTEXT c2 = newCONTEXT( task->context->closure, r1, ref(newSTRING( ", " )) ) ;
  task->next = newTASK( r1, c2, r2, task->next, task->next ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, ref(PTHIS), ref(WI_join) ) ;
  task->next = newTASK( ref(PTHIS), c1, r1, task->next, task->next ) ;
""" )

T( 'SETTOSTRfinnish', None, None, (
  A( 'REFERENCE', 'string' ),
), """
  if ( NOTNONE( THIS->string->value ) ) {
    RETURN( STRX( "[ %s ]", C(STRING,THIS->string->value)->data ) ) ;
  } else {
    RETURN( NONE ) ;
  }
""" )

	#	join ', '

T( 'JOINaction', None, 'STRING', (), """
  REFERENCE r1 = ref(NONE) ;
  task->next = newTASK( ref(newJOINiterate1( r1, ref(newSTRING("")), task->context->that )), task->context, task->result, task->next, task->exit ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, ref(PTHIS), ref(WI_each) ) ;
  task->next = newTASK( ref(PTHIS), c1, r1, task->next, task->next ) ;
""" )

T( 'JOINiterate1', None, None, (
  A( 'REFERENCE', 'iterator' ),
  A( 'REFERENCE', 'string' ),
  A( 'REFERENCE', 'spacer' ),
), """
  REFERENCE r1 = ref(NONE) ;
  task->next = newTASK( ref(newJOINiterate2( THIS->iterator, THIS->string, THIS->spacer, r1 )), task->context, task->result, task->next, task->exit ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, THIS->iterator, ref(WI_next) ) ;
  task->next = newTASK( THIS->iterator, c1, r1, task->next, task->next ) ;
""" )

T( 'JOINiterate2', None, None, (
  A( 'REFERENCE', 'iterator' ),
  A( 'REFERENCE', 'string' ),
  A( 'REFERENCE', 'spacer' ),
  A( 'REFERENCE', 'object' ),
), """
  if ( NOTNONE( THIS->object->value ) ) {
    STRING base ;

    if ( strlen( C(STRING,THIS->string->value)->data ) > 0 ) {
      base = STRX( "%s%s", C(STRING,THIS->string->value)->data, C(STRING,THIS->spacer->value)->data ) ;
    } else {
      base = C(STRING,THIS->string->value) ;
    }

    REFERENCE base_ref = ref(base) ;
    REFERENCE r1 = ref(NONE) ;
    task->next = newTASK( ref(newJOINiterate1( THIS->iterator, r1, THIS->spacer )), task->context, task->result, task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, base_ref, THIS->object ) ;
    task->next = newTASK( base_ref, c1, r1, task->next, task->next ) ;
  } else {
    RETURN( THIS->string->value ) ;
  }
""" )



	####	generator

T( 'GENERATOR', None, None, (
  A( 'TYPE', 'type' ),
  A( 'SET', 'expr' ),
  A( 'CLOSURE', 'closure' ),
), """
  TYPE_RESPONSE( SET_type ) ;
  DO_TYPE ;
  METHOD( WI_EQEQ, SET_type, newSETCOMPAREaction() ) ;
  METHOD( WI_join, STRING_type, newJOINaction() ) ;
  IFWID( WI_toSUBstring, task->next = newTASK( ref(newSETTOSTRaction()), task->context, task->result, task->exit, task->exit ) ; );
  IFWID( WI_eval, task->next = newTASK( ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,THIS) )), task->context, task->result, task->next, task->exit ) ; ) ;
  IFWID( WI_all, task->next = newTASK( ref(newSETALLaction()), task->context, task->result, task->exit, task->exit ) ; );
  ONWID( WI_each, iteratorNEW( task, THIS->type, THIS->expr, THIS->closure ) ) ;
""" )

T( 'GENERATORconst', None, 'PARAMcs_struct', (), """
  RETURN( newGENERATOR( C(TYPE,PSTHAT->c_ref->svalue), c(SET,PSTHAT->s_ref->svalue), task->context->closure ) ) ;
""" )



	####	list

T( 'LIST', None, None, (
  A( 'TYPE', 'type' ),
  A( 'n_integer', 'length' ),
  A( 'REFS', 'data' ),
), """
  TYPE_RESPONSE( SET_type ) ;
  DO_TYPE ;
  METHOD( WI_EQ, SET_type, newLISTset() ) ;
  METHOD( WI_EQEQ, SET_type, newSETCOMPAREaction() ) ;
  METHOD( WI_join, STRING_type, newJOINaction() ) ;
  IFWID( WI_toSUBstring, task->next = newTASK( ref(newSETTOSTRaction()), task->context, task->result, task->exit, task->exit ) ; ) ;
  IFWID( WI_eval, task->next = newTASK( ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,THIS) )), task->context, task->result, task->next, task->exit ) ; ) ;
  IFWID( WI_all, task->next = newTASK( ref(newSETALLaction()), task->context, task->result, task->exit, task->exit ) ; );
  IFWID( WI_clone,
    LIST list = newLIST( THIS->type, 0, c(REFS,NULL) ) ;
    listMERGE( list, THIS ) ;
    RETURN( list ) ;
  ) ;
  IFWID( WI_length, USE_ON( exit, PTHIS ) ; RETURN( newNUMBER( THIS->length ) ) ; ) ;
  IFWID( WI_each, USE_ON( exit, PTHIS ) ; RETURN( newLISTITERATOR( THIS, 0, any(NONE) ) ) ; ) ;
  METHOD( WI_merge, SET_type, newMERGELISTaction() ) ;
  METHOD( WI_ADD, THIS->type, newAPPENDLISTaction() ) ;
  NOMOREWIDS ;
  task->next = REC( task, THIS->type, THIS_R, ref(newAPPENDLISTaction()), task->next ) ;
""" )

T( 'LISTset', 'LIST', None, (), """
    USE_ON( exit, PTHAT ) ;

    REFERENCE oldlist = ref(newLIST( PSTHIS->type, PSTHIS->length, PSTHIS->data )) ;

    PSTHIS->length = 0 ;
    PSTHIS->data = c(REFS,NULL) ;
    RASET( task->result, PTHIS ) ;

    REFERENCE r1 = ref(NONE) ;

    if ( PTHIS->objective == OBSERVER_type->instance_objective ) {

      REFERENCE r2 = ref(NONE) ;
      REFERENCE r3 = ref(NONE) ;

      task->next = newTASK( ref(newPROPAGATEtest( C(OBSERVER,PTHIS)->dep, r3 )), task->context, ref(NONE), task->exit, task->exit ) ;

      CONTEXT c3 = newCONTEXT( task->context->closure, r2, task->context->that ) ;
      task->next = newTASK( r2, c3, r3, task->next, task->next ) ;

      CONTEXT c2 = newCONTEXT( task->context->closure, oldlist, ref(WI_EQ) ) ;
      task->next = newTASK( oldlist, c2, r2, task->next, task->next ) ;

      task->next = newTASK( ref(newMERGELISTiterator( task->context->this, r1 )), task->context, ref(NONE), task->next, task->next ) ;

    } else {

      task->next = newTASK( ref(newMERGELISTiterator( task->context->this, r1 )), task->context, ref(NONE), task->exit, task->exit ) ;

    }

    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->that, ref(WI_each) ) ;
    task->next = newTASK( task->context->that, c1, r1, task->next, task->next ) ;
""" )

T( 'LISTset_dep', 'LIST', None, (
  A( 'REFERENCE', 'cond' ),
), """
    if ( NOTNONE( THIS->cond->value ) ) {
      MOD_ON( exit, PTHIS ) ;
    }
    USE_ON( exit, PTHAT ) ;
    PSTHIS->length = 0 ;
    PSTHIS->data = c(REFS,NULL) ;
    RASET( task->result, PTHIS ) ;
    REFERENCE r1 = ref(NONE) ;
    task->next = newTASK( ref(newMERGELISTiterator( task->context->this, r1 )), task->context, ref(NONE), task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->that, ref(WI_each) ) ;
    task->next = newTASK( task->context->that, c1, r1, task->next, task->next ) ;
""" )


T( 'LISTITERATOR', None, None, (
  A( 'LIST', 'list' ),
  A( 'n_integer', 'index' ),
  A( 'ANY', 'v' ),
), """
  DO_TYPE ;
  ONWID( WI_value, THIS->v ) ;
  IFWID( WI_next,
    if ( THIS->index < THIS->list->length ) {
      THIS->v = any(THIS->list->data[THIS->index++]->value) ;
    } else {
      THIS->v = any(NONE) ;
    }
    RETURN( THIS->v ) ;
  )
""" )

T( 'APPENDLISTaction', 'LIST', None, (), """
    MOD_ON( exit, PTHIS ) ;
    USE_ON( exit, PTHAT ) ;
    listAPPEND( PSTHIS, ref(PTHAT) ) ;
    RETURN( PTHIS ) ;
""" )

T( 'SETCUSTOMLIST', 'TYPE', 'TYPE', (), """
  RETURN( listNEW( PSTHAT ) ) ;
""" )

T( 'MERGELISTaction', 'LIST', None, (), """
    RASET( task->result, PTHIS ) ;
    REFERENCE r1 = ref(NONE) ;
    task->next = newTASK( ref(newMERGELISTiterator( task->context->this, r1 )), task->context, ref(NONE), task->exit, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->that, ref(WI_each) ) ;
    task->next = newTASK( task->context->that, c1, r1, task->next, task->next ) ;
    USE_ON( next, PTHAT ) ;
    MOD_ON( next, PTHIS ) ; /* missing test */
""" )

T( 'MERGELISTiterator', 'LIST', None, (
  A( 'REFERENCE', 'target' ),
  A( 'REFERENCE', 'source' ),
), """
  REFERENCE r1 = ref(NONE) ;
  task->next = newTASK( ref(newMERGELISTappend( task->action, r1 )), task->context, task->result, task->next, task->exit ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, THIS->source, ref(WI_next) ) ;
  task->next = newTASK( THIS->source, c1, r1, task->next, task->next ) ;
""" )

T( 'MERGELISTappend', 'LIST', None, (
  A( 'REFERENCE', 'iterator' ),
  A( 'REFERENCE', 'element' ),
), """
  if ( NOTNONE( THIS->element->value ) ) {
    task->next = newTASK( THIS->iterator, task->context, task->result, task->next, task->exit ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, C(MERGELISTiterator,THIS->iterator->value)->target, THIS->element ) ;
    task->next = newTASK( C(MERGELISTiterator,THIS->iterator->value)->target, c1, task->result, task->next, task->next ) ;
  }
""" )



	####	tuple

T( 'TUPLE', None, None, (
  A( 'TYPE', 'type' ),
  A( 'n_integer', 'length' ),
  A( 'REFS', 'data' ),
), """
  TYPE_RESPONSE( SET_type ) ;
  DO_TYPE ;
  METHOD( WI_EQEQ, SET_type, newSETCOMPAREaction() ) ;
  METHOD( WI_join, STRING_type, newJOINaction() ) ;
  IFWID( WI_toSUBstring, task->next = newTASK( ref(newSETTOSTRaction()), task->context, task->result, task->exit, task->exit ) ; );
  IFWID( WI_all, task->next = newTASK( ref(newSETALLaction()), task->context, task->result, task->exit, task->exit ) ; );

//  METHOD( WI_assort, TUPLE_type, newASSORTaction() ) ;
  ONWID( WI_length, newNUMBER( THIS->length ) ) ;
  ONWID( WI_each, newTUPLEITERATOR( THIS, 0, any(NONE) ) ) ;
  NOMOREWIDS ;
  task->next = REC( task, THIS->type, THIS_R, ref(newAPPENDTUPLEaction()), task->next ) ;
""" )

T( 'TUPLEITERATOR', None, None, (
  A( 'TUPLE', 'tuple' ),
  A( 'n_integer', 'index' ),
  A( 'ANY', 'v' ),
), """
  DO_TYPE ;
  ONWID( WI_value, THIS->v ) ;
  IFWID( WI_next,
    if ( THIS->index < THIS->tuple->length ) {
      THIS->v = any(THIS->tuple->data[THIS->index++]->value) ;
    } else {
      THIS->v = any(NONE) ;
    }
    RETURN( THIS->v ) ;
  )
""" )

T( 'APPENDTUPLEaction', 'TUPLE', None, (), """
  tupleAPPEND( PSTHIS, ref(PTHAT) ) ;
  RETURN( PTHIS ) ;
""" )



	####	iterator

T( 'ITERATOR', None, None, (
  A( 'TASK', 'inner' ),
  A( 'TASK', 'outer' ),
  A( 'REFERENCE', 'v_ref' ),
), """
  DO_TYPE ;
  ONWID( WI_value, THIS->v_ref->value ) ;
  IFWID( WI_next,
    THIS->v_ref = task->result ;
    if ( NOTNONE( THIS->inner ) ) {
      THIS->outer = task->exit ;
      task->next = THIS->inner ;
    }
  )
""" )

T( 'ITERATORcatch', None, None, (
  A( 'REFERENCE', 'iterator' ),
), """
  RASET( C(ITERATOR,THIS->iterator->svalue)->v_ref, PTHAT ) ;
  C(ITERATOR,THIS->iterator->svalue)->inner = task->exit ;
  task->next = C(ITERATOR,THIS->iterator->svalue)->outer ;
""" )

T( 'ITERATORend', None, None, (
  A( 'REFERENCE', 'iterator' ),
), """
  RASET( C(ITERATOR,THIS->iterator->svalue)->v_ref, NONE ) ;
  C(ITERATOR,THIS->iterator->svalue)->inner = c(TASK,NONE) ;
  task->next = C(ITERATOR,THIS->iterator->svalue)->outer ;
""" )



	####	wid

T( 'WID', None, None, (
  A( 'STRING', 'value' ),
), """
  DO_TYPE ;
""",
debug = D( ' \'%s\'', 'c( n_string, C( WID, o )->value->data )' )
)



	####	string

T( 'STRING', None, None, (
  A( 'n_string', 'data' ),
), """
  DO_TYPE ;
  ONWID( WI_toSUBstring, THIS ) ;
  ONWID( WI_clone, STRX( "%s", THIS->data ) ) ;
  IFWID( WI_parse,
    n_integer parse_index = 0 ;
    RETURN( C( PHRASE, PARSE( &parse_index, THIS->data ) )->value ) ;
  ) ;
  task->next = REC( task, STRING_type, THIS_R, ref(newAPPENDSTRINGaction()), task->next ) ;
""",
debug = D( ' \\"%s\\"', 'c( n_string, C( STRING, o )->data )' )
)

T( 'STRINGconst', 'TYPE', 'STRING', (), """
  RETURN( STRX( "%s", PSTHAT->data ) ) ;
""" )

	#	string append

T( 'APPENDSTRINGaction', 'STRING', 'STRING', (), """
  RETURN( STRX( "%s%s", PSTHIS->data, PSTHAT->data ) ) ;
""" )

	#	string category

T( 'STRINGprimitive' )

T( 'STRINGcat', 'CLOSURE', None, (), """
  ONWID( WI_newl, newSTRING( "\\n" ) ) ;
  ONWID( WI_tab, newSTRING( "\\t" ) ) ;
  ONWID( WI_qt, newSTRING( "'" ) ) ;
  REFERENCE r1 = ref(NONE) ;
  REFERENCE e_ref = refNEW( STRINGprimitive_type, any(NONE) ) ;
  REFERENCE e_ref_ref = ref(e_ref) ;
  task->next = newTASK( ref(newSTRINGcontinue( r1 )), task->context, task->result, task->next, task->next ) ;
  task->next = newTASK( ref(newSTRINGfinnish( e_ref )), task->context, task->result, task->next, task->exit ) ;
  CONTEXT c2 = newCONTEXT( task->context->closure, e_ref_ref, ref(newNOUN( r1 )) ) ;
  task->next = newTASK( e_ref_ref, c2, ref(NONE), task->next, task->next ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, task->context->that, ref(WI_toSUBstring) ) ;
  task->next = newTASK( task->context->that, c1, r1, task->next, task->next ) ;
""" )

T( 'STRINGcontinue', None, None, (
  A( 'REFERENCE', 'e_ref' ),
), """
  if ( NOTNONE( THIS->e_ref->value ) ) {
    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->this, THIS->e_ref ) ;    
    task->next = newTASK( ref(newSTRINGcat()), c1, task->result, task->next, task->next ) ;
  } else {
    RETURN( NONE ) ;
  }
""" )

T( 'STRINGfinnish', None, None, (
  A( 'REFERENCE', 'e_ref' ),
), """
  if ( NOTNONE( THIS->e_ref->value ) ) {
    RDSET( task->result, THIS->e_ref->value, THIS->e_ref->svalue ) ;
    task->next = task->exit ;
  }
""" )



	####	word

T( 'WORD', None, None, (
  A( 'WID', 'id' ),
), """
  DO_TYPE ;
  ONWID( WI_toSUBstring, STRX( "%s", THIS->id->value->data ) ) ;
""" )

T( 'WORDconst', None, 'STRING', (), """
  RETURN( newWORD( widNEW( PSTHAT->data ) ) ) ;
""" )


	####	phrase

T( 'PHRASE', None, None, (
  A( 'LIST', 'value' ),
), """
  DO_TYPE ;
""" )

T( 'PHRASEconst', None, None, (), """
  RETURN( newPHRASE( c(LIST,PSTHAT) ) ) ;
""" )



############################################################################################################
############################################################################################################
############################################################################################################

BUILD()


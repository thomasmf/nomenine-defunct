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
  ATTRIB( WI_set, SET_type ) ;
  ATTRIB( WI_fun, FUNCTION_type ) ;
  ATTRIB( WI_gen, GENERATOR_type ) ;
  ATTRIB( WI_number, NUMBER_type ) ;
  ATTRIB( WI_string, STRING_type ) ;
  ATTRIB( WI_type, TYPE_type ) ;
  ATTRIB( WI_fact, FACTfact ) ;
  ATTRIB( WI_cat, CATfact ) ;
  ATTRIB( WI_param, PARAMfact ) ;
  ATTRIB( WI_module, MODULEfact ) ;
  ATTRIB( WI_struct, STRUCT_type ) ;
  ATTRIB( WI_list, LIST_type ) ;
  ATTRIB( WI_iterator, ITERATOR_type ) ;
  ATTRIB( WI_any, ANY_type ) ;
  ATTRIB( WI_none, NONE ) ;
  ATTRIB( WI_assort, ASSORTfact ) ;
  ATTRIB( WI_console, CONSOLEOBJECT ) ;
""" )

############################################################################################################
############################################################################################################
############################################################################################################

W(
  'exit', 'halt',
  '.', '!', ':', '::',
  'head', 'tail',
  'any', 'none', 'else', 'then',
  'number', '=', '+', '-', '*', '/', '+=', '-=', '<', '<=', '==', '!=', '>=', '>', '++', '--', 'mod', 'pow', 'sqrt',
  'string', 'to-string', 'newl', 'tab', 'qt', 'parse',
  'fact', 'new', 'cat',
  'is', 'has', 'does', 'noms', 'defs', 'gets', 'param',
  'const', 'def', 'var', 'fun', 'nom', 'defun', 'defact',
  'this', 'that',
  'name', 'type', 'value',
  'catch', 'throw',
  'console', 'read', 'write',
  'loop', 'stop', 'continue',
  'func', 'return', 'break', 'apply',
  'set', 'gen', 'next', 'list', 'each', 'merge', 'length', 'iterator', 'join', 'eval',
  'assort', 'struct',
  'delog', 'tron', 'troff',
  'module', 'use',
  'c', 's', 'w', 'f', 'a',
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
//  DO_COMMON ;
""" )

T( 'IGNORETYPE' )

T( 'NOUN', None, None, (
  A( 'REFERENCE', 'object' ),
) )

T( 'LITERAL', None, None, (
  A( 'n_literal', 'factory' ),
  A( 'ANY', 'data' ),
), """
  DO_TYPE ;
""" )



	####	reference

T( 'REFERENCE', None, None, (
  A( 'TYPE', 'type' ),
  A( 'ANY', 'value' ),
  A( 'ANY', 'svalue' ),
), """
  DO_EVALUATE ;
  IFTYPE( NOUN_type,
    task->next = RETA( task, ref(newSETREFERENCE()), ref(THIS), ref(C(NOUN,PTHAT)->object), task->next ) ;
  ) ;
  task->next = REX( task, THIS, task->next ) ;
""" )

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
  NOMOREWORDS ;
  CLOSURE c1 = newCLOSURE( task->context->closure, task->context->this, task->context->that, ref(THIS->view),
    ref(newOBJECTIVEreturner( task->context->closure->field, task->result, task->exit ))
  ) ;
  task->next = newTASK( ref(newEVALUATE( c1, ref(c1), THIS->data )), task->context, task->result, task->next, task->exit ) ;
""" )

T( 'OBJECTIVEreturn', None, None, (
  A( 'REFERENCE', 'object' ),
), """
  DO_EVALUATE ;
  DO_DEBUG ;
  NOMOREWORDS ;
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
  task->next = REP( task, ref(THIS->rest), task->next ) ;
""" )



	####	evaluate

T( 'EVALUATE', None, None, (
  A( 'CLOSURE', 'parent' ),
  A( 'REFERENCE', 'start' ),
  A( 'SET', 'list' ),
), """
  REFERENCE r1 = ref(NONE) ;
  REFERENCE r2 = ref(NONE) ;
  CONTEXT c1 = newCONTEXT( THIS->parent, THIS->start, r2 ) ;
  TASK t1 = newTASK( ref(newEVALUATOR( c1, r1 )), task->context, task->result, task->next, task->next ) ;
  CONTEXT c2 = newCONTEXT( task->context->closure, r1, ref(WI_next) ) ;
  TASK t2 = newTASK( r1, c2, r2, t1, t1 ) ;
  CONTEXT c3 = newCONTEXT( task->context->closure, ref(THIS->list), ref(WI_each) ) ;
  TASK t3 = newTASK( ref(THIS->list), c3, r1, t2, t2 ) ;
  task->next = t3 ;
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
  TASK t1 = newTASK( ref(newEVALUATOR( c1, THIS->iterator )), task->context, task->result, task->next, task->next ) ;
  CONTEXT c2 = newCONTEXT( task->context->closure, ref(THIS->iterator), ref(WI_next) ) ;
  TASK t2 = newTASK( ref(THIS->iterator->value), c2, r2, t1, t1 ) ;
  task->next = newTASK( THIS->context->this, THIS->context, r1, t2, t2 ) ;
""" )



	####	typetest

T( 'TYPETEST', None, None, (
  A( 'REFERENCE', 'r' ),
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'action' ),
), """
  if ( THIS->r->value != any(NONE) ) {
    task->next = RETA( task, THIS->action, THIS->this, THIS->r, task->exit /* WARN NOT TESTED*/ ) ;
  }
""" )



	####	object context

T( 'OCONTEXT', None, None, (
  A( 'ANY', 'object_1' ),
  A( 'ANY', 'object_2' ),
), """
  DO_LITERAL ;
  ONWORD( WI_COLON, tupleNEW() ) ;
  task->next = REP( task, ref(THIS->object_1), REP( task, ref(THIS->object_2), task->next ) ) ;
  if ( PTHAT->objective != WORD_type->instance_objective ) RETURN ( PTHAT ) ;
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
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'that' ),
  A( 'REFERENCE', 'view' ),
  A( 'REFERENCE', 'field' ),
), """
  DO_TYPE ;
  ATTRIB( WI_COLON, tupleNEW() ) ;
  ATTRIB( WI_this, THIS->this->value ) ;
  ATTRIB( WI_that, THIS->that->value ) ;
  METHOD( WI_loop, SET_type, newLOOPaction() ) ;
  METHOP( WI_var, newIS( any(newFUNCTION( PARAMwa, any(newVARaction_wa()) )), any(newFUNCTION( PARAMwca, any(newVARaction_wca()) )) ) ) ;
  METHOD( WI_def, PARAMwa, newDEFaction() ) ;
  METHOD( WI_catch, PARAMcs, newCATCHaction() ) ;
  METHOD( WI_defun, PARAMwcs, newDEFUNaction() ) ;
  METHOD( WI_defact, PARAMwcs, newDEFACTaction() ) ;
  METHOD( WI_nom, PARAMws, newNOMaction() ) ;
  METHOD( WI_return, ANY_type, newRETURNaction() ) ;
//  METHOD( WI_exit, NUMBER_type, newEXITaction() ) ;
  IFWORD( WI_halt, exit( EX_OK ) ; ) ;
  METHOD( WI_use, ANY_type, newUSEaction() ) ;
  IFWORD( WI_stop, task->next = RETO( task, THIS->field, ref(LOOPstop), task->next ) ; ) ;
  IFTYPE( WORD_type, task->next = REP( task, THIS->view, task->next ) ; ) ;
  IFTYPE( ID_type ) ;
  RETURN( PTHAT ) ;
""" )



	####	context

T( 'CONTEXT', None, None, (
  A( 'CLOSURE', 'closure' ),
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'that' ),
) )



	####	context methods

	#	var (: 'some-symbol' ( some-object ) )

T( 'VARaction_wa', 'CLOSURE', 'PARAMwa_struct', (), """
  RASET( PSTHIS->view, newHAS(
    ref( PSTHIS->view->value ),
    wordNEW( C(STRING, PSTHAT->w_ref->svalue)->data  ),
    ref(PSTHAT->a_ref->value)
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	var (: 'some-symbol' ( some-type ) ( some-object ) )

T( 'VARaction_wca', 'CLOSURE', 'PARAMwca_struct', (), """
  REFERENCE v_ref = refNEW( C(TYPE,PSTHAT->c_ref->svalue), any(NONE) ) ;
  REFERENCE v_ref_ref = ref(v_ref) ;
  RASET( PSTHIS->view, newHAS( ref( PSTHIS->view->value ), wordNEW( C(STRING, PSTHAT->w_ref->svalue)->data ), v_ref ) ) ;
  task->next = task->exit ;
  RASET( task->result, PTHIS ) ;
  CONTEXT c1 = newCONTEXT( task->context->closure, v_ref_ref, ref(newNOUN( PSTHAT->a_ref )) ) ;
  task->next = newTASK( v_ref_ref, c1, ref(NONE), task->next, task->next ) ;
""" )

	#	def (: 'some-symbol' ( some-object ) )

T( 'DEFaction', 'CLOSURE', 'PARAMwa_struct', (), """
  RASET( PSTHIS->view, newDEFS(
    ref( PSTHIS->view->value ),
    wordNEW( C(STRING, PSTHAT->w_ref->svalue)->data  ),
    any(PSTHAT->a_ref->value)
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
  RASET( PSTHIS->view, newDEFS(
    ref( PSTHIS->view->value ),
    wordNEW( C(STRING,PSTHAT->w_ref->svalue)->data ),
    any(newFUNCTION(
      C(TYPE,PSTHAT->c_ref->svalue),
      any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
    ))
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	defact (: 'some-symbol' ( some-type ) [ ... ] )

T( 'DEFACTaction', 'CLOSURE', 'PARAMwcs_struct', (), """
  RASET( PSTHIS->view, newDEFS(
    ref( PSTHIS->view->value ),
    wordNEW( C(STRING,PSTHAT->w_ref->svalue)->data ),
    any(newTYPE( newID(), c(n_objective,NULL), any(newFUNCTION(
      C(TYPE,PSTHAT->c_ref->svalue),
      any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
    )), any(NONE) ))
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	nom (: 'some-symbol' [ ... ] )

T( 'NOMaction', 'CLOSURE', 'PARAMws_struct', (), """
  RASET( PSTHIS->view, newNOMS(
    PSTHIS->view->value,
    wordNEW( C(STRING, PSTHAT->w_ref->svalue)->data ),
    any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
  ) ) ;
  RETURN( PTHIS ) ;
""" )

	#	return ( some-object )

T( 'RETURNaction', 'CLOSURE', None, (), """
  task->next = RETO( task, PSTHIS->field, ref(newOBJECTIVEreturn(task->context->that)), task->next ) ;
""" )

	#	exit

#T( 'EXITaction', 'CLOSURE', 'NUMBER', (), """
#  exit( (n_integer)(PSTHAT->data) ) ;
#""" )

	#	loop [ ... ]

T( 'LOOPaction', 'CONTEXT', None, (), """
  CLOSURE c1 = newCLOSURE( task->context->closure, task->context->closure->this, task->context->closure->that, task->context->closure->view,
    ref(newLOOPstopper( task->context->closure->field, task->context->closure, task->result, task->exit ))
  ) ;
  CONTEXT c2 = newCONTEXT( c1, c1->this, c1->that ) ;
  task->next = newTASK( ref(newEVALUATE( c1, ref( c1 ), c(SET,PSTHAT) )), c2, task->result, task, task->exit ) ;
""" )

T( 'LOOPstopTYPE', None, None, (), """
  DO_DEBUG ;
""" ) ;

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
  task->next = REP( task, ref(THIS->rest), task->next ) ;
""" )

	#	use ( some-object )

T( 'USEaction', 'CLOSURE', None, (), """
  RASET( PSTHIS->view, newIS(
    PSTHIS->view->value,
    PTHAT
  ) ) ;
  RETURN( PTHIS ) ;
""" )


	####	object methods

	#	else [ ... ]

T( 'ELSEaction', None, None, (), """
  if ( PTHIS != any(NONE) ) RETURN( PTHIS ) ;
  task->next = REP( task, ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,PSTHAT) )), task->next ) ;
""" )

	#	then [ ... ]

T( 'THENaction', None, None, (), """
  if ( PTHIS == any(NONE) ) RETURN( NONE ) ;
  task->next = REP( task, ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,PSTHAT) )), task->next ) ;
""" )

	#	has (: 'some-symbol' ( some-object ) )

T( 'HASaction_wa', None, 'PARAMwa_struct', (), """
  RETURN( newHAS( task->context->this,
    wordNEW( C(STRING, PSTHAT->w_ref->svalue)->data ),
    ref( any(PSTHAT->a_ref->value) )
  ) ) ;
""" )

	#	has (: 'some-symbol' ( some-type ) ( some-object ) )

T( 'HASaction_wca', None, 'PARAMwca_struct', (), """
  REFERENCE v_ref = refNEW( C(TYPE,PSTHAT->c_ref->svalue), any(NONE) ) ;
  REFERENCE v_ref_ref = ref(v_ref) ;
  RASET( task->result, newHAS( task->context->this, wordNEW( C(STRING, PSTHAT->w_ref->svalue)->data ), v_ref ) ) ;
  task->next = task->exit ;
  CONTEXT c1 = newCONTEXT( task->context->closure, v_ref_ref, ref(newNOUN( PSTHAT->a_ref )) ) ;
  task->next = newTASK( v_ref_ref, c1, ref(NONE), task->next, task->next ) ;
""" )

	#	does (: 'some-symbol' ( some-function ) )

T( 'DOESaction_wf', None, 'PARAMwf_struct', (), """
  RETURN( newDOES( task->context->this, wordNEW( C(STRING,PSTHAT->w_ref->svalue)->data ), PSTHAT->f_ref->value ) ) ;
""" )

	#	does (: 'some-symbol' ( some-type ) [ ... ] )

T( 'DOESaction_wcs', None, 'PARAMwcs_struct', (), """
  RETURN( newDOES( task->context->this, wordNEW( C(STRING,PSTHAT->w_ref->svalue)->data ),
    any(newFUNCTION(
      C(TYPE,PSTHAT->c_ref->svalue),
      any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
    ))
  ) ) ;
""" )

	#	is ( some-object )

T( 'ISaction', None, None, (), """
  RETURN( newIS( PTHAT, PTHIS ) ) ;
""" )

	#	gets (: ( some-type ) [ ... ] )

T( 'GETSaction', None, 'PARAMcs_struct', (), """
  RETURN( newGETS( task->context->this,
    C(TYPE, PSTHAT->c_ref->svalue),
    any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
  ) ) ;
""" )

	#	noms (: 'some-symbol' [ ... ] )

T( 'NOMSaction', None, 'PARAMws_struct', (), """RETURN( newNOMS( PTHIS, wordNEW( C(STRING,PSTHAT->w_ref->svalue)->data ), any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view )) ) ) ; """ )



	####	object property extensions

	#	defs

T( 'DEFS', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WORD', 'word' ),
  A( 'ANY', 'attribute' ),
), """
  DO_COMMON ;
  ONWORD( THIS->word, THIS->attribute ) ;
  task->next = REP( task, THIS->rest, task->next ) ;
""" )

	#	has

T( 'HAS', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WORD', 'word' ),
  A( 'REFERENCE', 'attribute' ),
), """
  DO_COMMON ;
  ONWORD( THIS->word, THIS->attribute ) ;
  task->next = REP( task, THIS->rest, task->next ) ;
""" )

	#	does

T( 'DOES', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WORD', 'word' ),
  A( 'ANY', 'object' ),
), """
  DO_COMMON ;
  ONWORD( THIS->word, newAPPLICATOR( task->context->this, ref(THIS->object) ) ) ;
  task->next = REP( task, THIS->rest, task->next ) ;
""" )

	#	is

T( 'IS', None, None, (
  A( 'ANY', 'object_1' ),
  A( 'ANY', 'object_2' ),
), """
  DO_COMMON ;
  task->next = REP( task, ref(THIS->object_1), REP( task, ref(THIS->object_2), task->next ) ) ;
""" )

	#	gets

T( 'GETS', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'TYPE', 'type' ),
  A( 'ANY', 'action' ),
), """
  DO_COMMON ;
  task->next = REC( task, THIS->type, task->context->this, ref(THIS->action), REP( task, THIS->rest, task->next ) ) ;
""" )

	#	noms

T( 'NOMS', None, None, (
  A( 'ANY', 'rest' ),
  A( 'WORD', 'word' ),
  A( 'ANY', 'object' ),
), """
  DO_COMMON ;
  IFWORD( THIS->word,
    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->this, ref(NONE) ) ;
    task->next = newTASK( ref(THIS->object), c1, task->result, task->exit, task->exit ) ;
  ) ;
  task->next = REP( task, ref(THIS->rest), task->next ) ;
""" )



	####	parameters used by builtins

P( 'wa', X( 'w', 'STRING' ), X( 'a', 'ANY' ) )
P( 'wc', X( 'w', 'STRING' ), X( 'c', 'TYPE' ) )
P( 'ws', X( 'w', 'STRING' ), X( 's', 'SET' ) )
P( 'wf', X( 'w', 'STRING' ), X( 'f', 'FUNCTION' ) )

P( 'wca', X( 'w', 'STRING' ), X( 'c', 'TYPE' ), X( 'a', 'ANY' ) )
P( 'wcs', X( 'w', 'STRING' ), X( 'c', 'TYPE' ), X( 's', 'SET' ) )

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
  RETURN( newTYPE( newID(), c(n_objective,NULL), any(NONE), THIS->assorter->value ) ) ;
""" )



	####	struct (: (: 'some-symbol' ( some-type ) ) ... )

T( 'STRUCT', None, None, (
  A( 'LIST', 'elements' ),
), """
  DO_TYPE ;
  n_integer i ;
  for ( i = 0 ; i < THIS->elements->length ; i++ ) {
    ATTRIB( C(ATTRIBUTE,THIS->elements->data[ i ]->svalue)->w->svalue, C(ATTRIBUTE,THIS->elements->data[ i ]->svalue)->a ) ;
  }
""" )

T( 'STRUCTconst', None, 'TUPLE', (), """
  REFERENCE r1 = ref(NONE) ;
  task->next = newTASK( ref(newSTRUCTfinnish( r1 )), task->context, task->result, task->next, task->exit ) ;
  task->next = newTASK( ref(newASSORTconst()), task->context, r1, task->next, task->next ) ;
""" )

T( 'STRUCTfinnish', None, None, (
  A( 'REFERENCE', 'assorter' ),
), """
  RETURN( newTYPE( newID(), c(n_objective,NULL), THIS->assorter->value, any(NONE) ) ) ;
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
    listAPPEND( THIS->assortment->elements, ref(newATTRIBUTE( ref(wordNEW( C(STRING,THIS->w->svalue)->data )), THIS->a )) ) ;
  } else {
    RETURN( NONE ) ;
  }
""" )

T( 'ASSORTERfinnish', None, None, (
  A( 'STRUCT', 'assortment' ),
), """
  RETURN( THIS->assortment ) ;
""" )



	####	console

T( 'CONSOLE', None, None, (), """
  DO_TYPE ;
  IFWORD( WI_read, task->next = newTASK( ref(newREADaction()), task->context, task->result, task->next, task->exit ) ; ) ;
  ONWORD( WI_write, newWRITER() ) ;
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




	####	attribute

T( 'ATTRIBUTE', None, None, (
  A( 'REFERENCE', 'w' ),
  A( 'REFERENCE', 'a' ),
), """
""" )



	####	applicator

T( 'APPLICATOR', None, None, (
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'object' ),
), """
  DO_TYPE ;
//  NOMOREWORDS ;
  CONTEXT c1 = newCONTEXT( task->context->closure, THIS->this, task->context->that ) ;
  task->next = newTASK( THIS->object, c1, task->result, task->next, task->exit ) ;
""" )


	####	function

T( 'FUNCTION', None, None, (
  A( 'TYPE', 'type' ),
  A( 'ANY', 'action' ),
), """
  DO_TYPE ;
  METHOD( WI_apply, ANY_type, newAPPLYaction() ) ;
  NOMOREWORDS ;
  task->next = REC( task, THIS->type, task->context->this, ref( THIS->action ), task->next ) ;
""" )

T( 'FUNCTIONconst', 'TYPE', 'PARAMcs_struct', (), """
  RETURN( newFUNCTION(
    C(TYPE,PSTHAT->c_ref->svalue),
    any(newOBJECTIVE( c(SET,PSTHAT->s_ref->svalue), task->context->closure->view ))
  ) ) ;
""" )

T( 'APPLYaction', 'FUNCTION', None, (), """
  RETURN( newAPPLICATOR( task->context->that, task->context->that ) ) ;
""" )



	####	type

T( 'TYPE', None, None, (
  A( 'ID', 'id' ),
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

T( 'ID' )

T( 'SIGNATURE', None, None, (
  A( 'TYPE', 'type' ),
  A( 'ANY', 'rest' ),
), """
  DO_TYPE ;
  if ( c( n_integer, PTHAT ) == c( n_integer, THIS->type->id ) ) { RETURN( newREFERENCE( THIS->type, PTHIS, any(THIS) ) ) ; }
  task->next = REP( task, ref(THIS->rest), task->next ) ;
""" )

T( 'SIGNATUREconst', 'TYPE', None, (), """
  RETURN( newSIGNATURE( PSTHIS, PTHAT ) ) ;
""" )

	#	cat [ ... ]

T( 'CATconst', None, None, (), """
  RETURN( newTYPE( newID(), c(n_objective,NULL), any(NONE), any(newOBJECTIVE( c(SET,PSTHAT), task->context->closure->view )) ) ) ;
""" )

	#	fact ( some-object )

T( 'FACTconst', 'TYPE', None, (), """
  RETURN( newTYPE( newID(), c(n_objective,NULL), PTHAT, any(NONE) ) ) ;
""" )



	####	number

T( 'NUMBER', None, None, (
  A( 'n_float', 'data' ),
), """
  DO_TYPE ;
  IFWORD( WI_ADDADD, THIS->data++ ; RETURN( THIS ) ; ) ;
  IFWORD( WI_SUBSUB, THIS->data-- ; RETURN( THIS ) ; ) ;
  METHOD( WI_EQ,     NUMBER_type, newNUMBERset() ) ;
  METHOD( WI_EXCLAIMEQ,     NUMBER_type, newNUMBERset() ) ;
  METHOD( WI_ADDEQ,  NUMBER_type, newNUMBERaddset() ) ;
  METHOD( WI_SUBEQ,  NUMBER_type, newNUMBERsubset() ) ;
  METHOD( WI_ADD,    NUMBER_type, newNUMBERadd() ) ;
  METHOD( WI_SUB,    NUMBER_type, newNUMBERsub() ) ;
  METHOD( WI_MUL,    NUMBER_type, newNUMBERmul() ) ;
  METHOD( WI_DIV,    NUMBER_type, newNUMBERdiv() ) ;
  METHOD( WI_EQEQ,   NUMBER_type, newNUMBEReq() ) ;
  METHOD( WI_LTEQ,   NUMBER_type, newNUMBERlteq() ) ;
  METHOD( WI_GTEQ,   NUMBER_type, newNUMBERgteq() ) ;
  METHOD( WI_LT,     NUMBER_type, newNUMBERlt() ) ;
  METHOD( WI_GT,     NUMBER_type, newNUMBERgt() ) ;
  METHOD( WI_mod,    NUMBER_type, newNUMBERmod() ) ;
  METHOD( WI_pow,    NUMBER_type, newNUMBERpow() ) ;
  ONWORD( WI_sqrt,   newNUMBER( sqrt( THIS->data ) ) ) ;
  ONWORD( WI_toSUBstring, STRX( "%g", c(n_float,THIS->data) ) ) ;
""",
debug = D( ' %f', 'c( n_float, C( NUMBER, o )->data )' )
)

	#	number methods

T( 'NUMBEReq',     'NUMBER', 'NUMBER', (), """if ( PSTHIS->data == PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERneq',    'NUMBER', 'NUMBER', (), """if ( PSTHIS->data != PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERlteq',   'NUMBER', 'NUMBER', (), """if ( PSTHIS->data <= PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERgteq',   'NUMBER', 'NUMBER', (), """if ( PSTHIS->data >= PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERlt',     'NUMBER', 'NUMBER', (), """if ( PSTHIS->data < PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERgt',     'NUMBER', 'NUMBER', (), """if ( PSTHIS->data > PSTHAT->data ) RETURN( PTHAT ) else RETURN( NONE ) ;""" )
T( 'NUMBERadd',    'NUMBER', 'NUMBER', (), """RETURN( newNUMBER( PSTHIS->data + PSTHAT->data ) ) ;""" )
T( 'NUMBERsub',    'NUMBER', 'NUMBER', (), """RETURN( newNUMBER( PSTHIS->data - PSTHAT->data ) ) ;""" )
T( 'NUMBERmul',    'NUMBER', 'NUMBER', (), """RETURN( newNUMBER( PSTHIS->data * PSTHAT->data ) ) ;""" )
T( 'NUMBERdiv',    'NUMBER', 'NUMBER', (), """RETURN( newNUMBER( PSTHIS->data / PSTHAT->data ) ) ;""" )
T( 'NUMBERmod',    'NUMBER', 'NUMBER', (), """RETURN( newNUMBER( fmod( PSTHIS->data, PSTHAT->data ) ) ) ;""" )
T( 'NUMBERpow',    'NUMBER', 'NUMBER', (), """RETURN( newNUMBER( pow( PSTHIS->data, PSTHAT->data ) ) ) ;""" )
T( 'NUMBERaddset', 'NUMBER', 'NUMBER', (), """PSTHIS->data += PSTHAT->data ; RETURN( PTHIS ) ;""" )
T( 'NUMBERsubset', 'NUMBER', 'NUMBER', (), """PSTHIS->data -= PSTHAT->data ; RETURN( PTHIS ) ;""" )
T( 'NUMBERset',    'NUMBER', 'NUMBER', (), """PSTHIS->data = PSTHAT->data ; RETURN( PTHIS ) ;""" )


	####	set

T( 'SET', None, None, (), """
  DO_TYPE ;
  METHOD( WI_join, STRING_type, newJOINaction() ) ;
  IFWORD( WI_toSUBstring, task->next = newTASK( ref(newSETTOSTRaction()), task->context, task->result, task->exit, task->exit ) ; );
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
  METHOD( WI_join, STRING_type, newJOINaction() ) ;
  IFWORD( WI_toSUBstring, task->next = newTASK( ref(newSETTOSTRaction()), task->context, task->result, task->exit, task->exit ) ; );
  IFWORD( WI_eval, task->next = REP( task, ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,THIS) )), task->next ) ; ) ;
  ATTRIB( WI_each, iteratorNEW( task, THIS->type, THIS->expr, THIS->closure ) ) ;
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
  METHOD( WI_join, STRING_type, newJOINaction() ) ;
  IFWORD( WI_toSUBstring, task->next = newTASK( ref(newSETTOSTRaction()), task->context, task->result, task->exit, task->exit ) ; ) ;
  IFWORD( WI_eval, task->next = REP( task, ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,THIS) )), task->next ) ; ) ;
  ATTRIB( WI_length, newNUMBER( THIS->length ) ) ;
  ATTRIB( WI_each, newLISTITERATOR( THIS, 0, any(NONE) ) ) ;
  METHOD( WI_merge, SET_type, newMERGELISTaction() ) ;
  METHOD( WI_ADD, THIS->type, newAPPENDLISTaction() ) ;
  NOMOREWORDS ;
  task->next = REC( task, THIS->type, THIS_R, ref(newAPPENDLISTaction()), task->next ) ;
""" )

T( 'LISTITERATOR', None, None, (
  A( 'LIST', 'list' ),
  A( 'n_integer', 'index' ),
  A( 'ANY', 'v' ),
), """
  DO_TYPE ;
  ATTRIB( WI_value, THIS->v ) ;
  IFWORD( WI_next,
    if ( THIS->index < THIS->list->length ) {
      THIS->v = any(THIS->list->data[THIS->index++]->value) ;
    } else {
      THIS->v = any(NONE) ;
    }
    RETURN( THIS->v ) ;
  )
""" )

T( 'APPENDLISTaction', 'LIST', None, (), """
  listAPPEND( PSTHIS, ref(PTHAT) ) ;
  RETURN( PTHIS ) ;
""" )

T( 'SETCUSTOMLIST', 'TYPE', 'TYPE', (), """
  RETURN( listNEW( PSTHAT ) ) ;
""" )

T( 'MERGELISTaction', 'LIST', None, (), """
  RASET( task->result, PTHIS ) ;
  task->next = newTASK( ref(newEVALUATE( task->context->closure, ref(newMETALIST( PSTHIS )), c(SET,PSTHAT) )), task->context, ref(NONE), task->next, task->exit ) ;
""" )

T( 'METALIST', None, None, (
  A( 'LIST', 'list' ),
), """
  task->next = REC( task, THIS->list->type, THIS_R, ref(newMETAAPPENDLISTaction()), task->next ) ;
""" )
T( 'METAAPPENDLISTaction', 'METALIST', None, (), """
  listAPPEND( PSTHIS->list, ref(PTHAT) ) ;
  RETURN( PTHIS ) ;
""" )



	####	tuple

T( 'TUPLE', None, None, (
  A( 'TYPE', 'type' ),
  A( 'n_integer', 'length' ),
  A( 'REFS', 'data' ),
), """
  TYPE_RESPONSE( SET_type ) ;
  DO_TYPE ;
  METHOD( WI_join, STRING_type, newJOINaction() ) ;
  IFWORD( WI_toSUBstring, task->next = newTASK( ref(newSETTOSTRaction()), task->context, task->result, task->exit, task->exit ) ; );

//  METHOD( WI_assort, TUPLE_type, newASSORTaction() ) ;
  ATTRIB( WI_length, newNUMBER( THIS->length ) ) ;
  ATTRIB( WI_each, newTUPLEITERATOR( THIS, 0, any(NONE) ) ) ;
  NOMOREWORDS ;
  task->next = REC( task, THIS->type, THIS_R, ref(newAPPENDTUPLEaction()), task->next ) ;
""" )

T( 'TUPLEITERATOR', None, None, (
  A( 'TUPLE', 'tuple' ),
  A( 'n_integer', 'index' ),
  A( 'ANY', 'v' ),
), """
  DO_TYPE ;
  ATTRIB( WI_value, THIS->v ) ;
  IFWORD( WI_next,
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
  ATTRIB( WI_value, THIS->v_ref->value ) ;
  IFWORD( WI_next,
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



	####	word

T( 'WORD', None, None, (
  A( 'STRING', 'value' ),
), """
  DO_TYPE ;
""",
debug = D( ' \'%s\'', 'c( n_string, C( WORD, o )->value->data )' )
)



	####	string

T( 'STRING', None, None, (
  A( 'n_string', 'data' ),
), """
  DO_TYPE ;
  ONWORD( WI_toSUBstring, THIS ) ;
  IFWORD( WI_parse,
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
  ATTRIB( WI_newl, newSTRING( "\\n" ) ) ;
  ATTRIB( WI_tab, newSTRING( "\\t" ) ) ;
  ATTRIB( WI_qt, newSTRING( "'" ) ) ;
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

	####	phrase

T( 'PHRASE', None, None, (
  A( 'LIST', 'value' ),
), """
  DO_TYPE ;
""" )



############################################################################################################
############################################################################################################
############################################################################################################

BUILD()


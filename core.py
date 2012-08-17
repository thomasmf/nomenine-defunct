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

T( 'ROOTOBJECT', None, None, (), """
  DO_COMMON ;
  ATTRIB( WI_set, SET_class ) ;
  ATTRIB( WI_function, FUNCTIONCLASS ) ;
  ATTRIB( WI_generator, GENERATORCLASS ) ;
  ATTRIB( WI_number, NUMBER_class ) ;
  ATTRIB( WI_class, USERCLASS ) ;
  ATTRIB( WI_list, LISTCLASS ) ;
  ATTRIB( WI_iterator, ITERATOR_class ) ;
  ATTRIB( WI_any, ANY_class ) ;
  ATTRIB( WI_none, NONE ) ;
""" )

############################################################################################################
############################################################################################################
############################################################################################################

W(
  'exit',
  '.', '!', ':',
  'any', 'none', 'else', 'then',
  'number', '=', '+', '-', '*', '/', '+=', '-=', '<', '<=', '==', '!=', '>=', '>', '++', '--', 'mod', 'pow', 'sqrt',
  'class', 'new',
  'is', 'has', 'does', 'defs', 'gets', 'param',
  'const', 'def', 'var', 'fun',
  'this', 'that',
  'name', 'type', 'value',
  'catch', 'throw',
  'loop', 'stop', 'continue',
  'function', 'return', 'break', 'apply',
  'set', 'generator', 'next', 'list', 'each', 'merge', 'length', 'iterator',
  'delog', 'tron', 'troff',
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

#include "core.h"
#include "utils.h"

"""

############################################################################################################
############################################################################################################
############################################################################################################

META.TYPES = """

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
typedef n_string (*n_debug)( ANY ) ;

typedef REFERENCE* REFS ;

"""

############################################################################################################
############################################################################################################
############################################################################################################


	####	semantics

T( 'REFERENCE', None, None, (
  A( 'CLASS', 'type', 'ANY_class' ),
  A( 'ANY', 'value', 'NONE' ),
  A( 'ANY', 'specific_value', 'NONE' ),
), """
  DO_EVALUATE ;
  IFTYPE( NOUN_class,
    task->next = RETA( task, ref(newSETREFERENCE()), ref(THIS), ref(C(NOUN,PTHAT)->object), task->next ) ;
  ) ;
  task->next = REX( task, THIS, task->next ) ;
""" )
T( 'REFERENCEset', 'REFERENCE', None,(), """
  PSTHIS->value = PTHAT ;
  PSTHIS->specific_value = PSTHAT ;
  RETURN( PTHIS ) ;
""" )
T( 'SETREFERENCE', 'REFERENCE', None, (), """
  task->next = REC( task, PSTHIS->type, ref(PSTHIS), ref(newREFERENCEset()), task->next ) ;
""" )

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
  CONTEXT c1 = newCONTEXT( task->context->closure, r1, ref(newNOUN( task->context->that->value )) ) ;
  task->next = newTASK( r1, c1, r2, task->exit, task->exit ) ;
  task->result->value = PTHIS ;
""" ) ;
T( 'OBJECTIVEreturner', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'REFERENCE', 'result' ),
  A( 'TASK', 'exit' ),
), """
  IFTYPE( OBJECTIVEreturn_class,
    THIS->result->value = C(OBJECTIVEreturn,PTHAT)->object->value ;
    task->next = THIS->exit ;
  ) ;
  task->next = REP( task, ref(THIS->rest), task->next ) ;
""" )

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

T( 'APPLICATOR', None, None, (
  A( 'REFERENCE', 'this' ),
  A( 'CLASS', 'class' ),
  A( 'ANY', 'action' ),
), """
  DO_CLASS ;
  IFWORD( WI_COLON,
    task->next = RETO( task, ref(THIS->class), ref(WI_new), task->next ) ;
  ) ;
  METHOD( WI_apply, ANY_class, newAPPLYaction() ) ;
  NOMOREWORDS ;
  task->next = REC( task, THIS->class, THIS->this, ref( THIS->action ), task->next ) ;
""" )
T( 'APPLICATORCONSTRUCTOR', None, 'PARAMcl', (), """
  RETURN( newAPPLICATOR( ref(NONE), C(CLASS,PSTHAT->type->specific_value),
  any(newOBJECTIVE( c(SET,PSTHAT->value->specific_value), task->context->closure->view )) ) ) ;
""" )
T( 'APPLYaction', 'APPLICATOR', None, (), """
  PSTHIS->this->value = PTHAT ;
  RETURN( PTHIS ) ;
""" )

T( 'TYPETEST', None, None, (
  A( 'REFERENCE', 'r' ),
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'action' ),
), """
  if ( THIS->r->value != any(NONE) ) {
    task->next = RETA( task, THIS->action, THIS->this, C(REFERENCE,THIS->r->value), task->next ) ;
  }
""" )

T( 'OCONTEXT', None, None, (
  A( 'ANY', 'object_1' ),
  A( 'ANY', 'object_2' ),
), """
  if ( PTHAT->objective != WORD_class->instance_objective ) { RETURN( PTHAT ) ; } ;
  task->next = REP( task, ref(THIS->object_1), REP( task, ref(THIS->object_2), task->next ) ) ;
""" )


	####	scheduling

T( 'TASK', None, None, (
  A( 'REFERENCE', 'action' ),
  A( 'CONTEXT', 'context' ),
  A( 'REFERENCE', 'result' ),
  A( 'TASK', 'next' ),
  A( 'TASK', 'exit' ),
) )

T( 'CLOSURE', None, None, (
  A( 'CLOSURE', 'parent' ),
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'that' ),
  A( 'REFERENCE', 'view' ),
  A( 'REFERENCE', 'field' ),
), """
  DO_NOB ;
  DO_DEBUG ;
  ATTRIB( WI_this, THIS->this->value ) ;
  ATTRIB( WI_that, THIS->that->value ) ;
  METHOD( WI_loop, LIST_class, newLOOPaction() ) ;
  METHOD( WI_var, PARAMsac_class, newVARaction() ) ;
  METHOD( WI_const, PARAMsa_class, newCONSTaction() ) ;
  METHOD( WI_catch, PARAMcl_class, newCATCHaction() ) ;
  METHOD( WI_fun, PARAMslc_class, newFUNaction() ) ;
  METHOD( WI_def, PARAMsl_class, newDEFaction() ) ;
  METHOD( WI_return, ANY_class, newRETURNaction() ) ;
  METHOD( WI_exit, NUMBER_class, newEXITaction() ) ;
  IFWORD( WI_stop, task->next = RETO( task, THIS->field, ref(LOOPstop), task->next ) ; ) ;
  IFTYPE( WORD_class, task->next = REP( task, THIS->view, task->next ) ; ) ;
  IFTYPE( ID_class ) ;
  RETURN( PTHAT ) ;
""" )

T( 'CONTEXT', None, None, (
  A( 'CLOSURE', 'closure' ),
  A( 'REFERENCE', 'this' ),
  A( 'REFERENCE', 'that' ),
) )

T( 'VARaction', 'CLOSURE', 'PARAMsac', (), """
  PSTHIS->view->value = any(newHAS(
    ref( PSTHIS->view->value ),
    wordNEW( C(STRING, PSTHAT->string->value)->data  ),
    refNEW( C(CLASS, PSTHAT->type->value), any(PSTHAT->value->value) )
  )) ;
  RETURN( PSTHIS ) ;
""" )
T( 'CONSTaction', 'CLOSURE', 'PARAMsa', (), """
  PSTHIS->view->value = any(newCONST(
    ref( PSTHIS->view->value ),
    wordNEW( C(STRING, PSTHAT->string->value)->data  ),
    any(PSTHAT->value->value)
  )) ;
  RETURN( PSTHIS ) ;
""" )
T( 'CATCHaction', 'CLOSURE', 'PARAMcl', (), """
  PSTHIS->field->value = any(newGETS(
    ref( PSTHIS->field->value ),
    C(CLASS,PSTHAT->type->value),
    any(newOBJECTIVE( c(SET,PSTHAT->value->specific_value), task->context->closure->view ))
  )) ;
  RETURN( PSTHIS ) ;
""" )
T( 'FUNaction', 'CLOSURE', 'PARAMslc', (), """
  PSTHIS->view->value = any(newDOES(
    ref( PSTHIS->view->value ),
    wordNEW( C(STRING,PSTHAT->string->specific_value)->data ),
    C(CLASS,PSTHAT->type->specific_value),
    any(newOBJECTIVE( c(SET,PSTHAT->value->specific_value), task->context->closure->view ))
  )) ;
  RETURN( PSTHIS ) ;
""" )
T( 'DEFaction', 'CLOSURE', 'PARAMsl', (), """
  PSTHIS->view->value = any(newDEFS(
    PSTHIS->view->value,
    wordNEW( C(STRING, PSTHAT->string->value)->data ),
    any(newOBJECTIVE( c(SET,PSTHAT->value->specific_value), task->context->closure->view ))
  )) ;
  RETURN( PSTHIS ) ;
""" )
T( 'RETURNaction', 'CLOSURE', None, (), """
  task->next = RETO( task, PSTHIS->field, ref(newOBJECTIVEreturn(task->context->that)), task->next ) ;
""" )
T( 'EXITaction', 'CLOSURE', 'NUMBER', (), """
  exit( (n_integer)(PSTHAT->data) ) ;
""" )


	####	primitive mechanics

T( 'ANY', None, None, (),"""
//  DO_CLASS ;
""" )

T( 'NONETYPE', None, None, (), """
  DO_CLASS ;
//  DO_COMMON ;
""" )

T( 'IGNORETYPE' )
T( 'NOUN', None, None, (
  A( 'ANY', 'object' ),
) )

T( 'ELSEaction', None, None, (), """
  if ( PTHIS != any(NONE) ) RETURN( PTHIS ) ;
  task->next = REP( task, ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,PSTHAT) )), task->next ) ;
""" )

T( 'THENaction', None, None, (), """
  if ( PTHIS == any(NONE) ) RETURN( NONE ) ;
  task->next = REP( task, ref(newEVALUATE( task->context->closure, ref(task->context->closure), c(SET,PSTHAT) )), task->next ) ;
""" )

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
    THIS->result->value = any(THIS->parent) ;
    task->next = THIS->exit ;
  ) ;
  task->next = REP( task, ref(THIS->rest), task->next ) ;
""" )


	####	iterator

T( 'ITERATOR', None, None, (
  A( 'TASK', 'inner' ),
  A( 'TASK', 'outer' ),
  A( 'REFERENCE', 'value' ),
), """
  DO_CLASS ;
  ATTRIB( WI_value, THIS->value->value ) ;
  IFWORD( WI_next,
    THIS->value = task->result ;
    if ( NOTNONE( THIS->inner ) ) {
      THIS->outer = task->exit ;
      task->next = THIS->inner ;
    }
  )
""" )
T( 'ITERATORcatch', None, None, (
  A( 'REFERENCE', 'iterator' ),
), """
  C(ITERATOR,THIS->iterator->value)->value->value = PTHAT ;
  C(ITERATOR,THIS->iterator->value)->inner = task->exit ;
  task->next = C(ITERATOR,THIS->iterator->value)->outer ;
""" )
T( 'ITERATORend', None, None, (
  A( 'REFERENCE', 'iterator' ),
), """
  C(ITERATOR,THIS->iterator->value)->value->value = any(NONE) ;
  C(ITERATOR,THIS->iterator->value)->inner = c(TASK,NONE) ;
  task->next = C(ITERATOR,THIS->iterator->value)->outer ;
""" )


	####	mini mixins

T( 'CONST', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WORD', 'word' ),
  A( 'ANY', 'attribute' ),
), """
  DO_COMMON ;
  ONWORD( THIS->word, THIS->attribute ) ;
  task->next = REP( task, THIS->rest, task->next ) ;
""" )

T( 'HAS', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WORD', 'word' ),
  A( 'REFERENCE', 'attribute' ),
), """
  DO_COMMON ;
  ONWORD( THIS->word, THIS->attribute ) ;
  task->next = REP( task, THIS->rest, task->next ) ;
""" )
T( 'HASaction', None, 'PARAMsac', (), """
  RETURN( newHAS( task->context->this,
    wordNEW(
      C(STRING, PSTHAT->string->value)->data  ),
    refNEW(
      C(CLASS, PSTHAT->type->value),
      any(PSTHAT->value->value)
    )
  ) ) ;""" )

T( 'IS', None, None, (
  A( 'ANY', 'object_1' ),
  A( 'ANY', 'object_2' ),
), """
  DO_COMMON ;
  task->next = REP( task, ref(THIS->object_1), REP( task, ref(THIS->object_2), task->next ) ) ;
""" )
T( 'ISaction', None, None, (), """
  RETURN( newIS( PSTHAT, PSTHIS ) ) ;
""" )

T( 'GETS', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'CLASS', 'class' ),
  A( 'ANY', 'action' ),
), """
  DO_COMMON ;
  task->next = REC( task, THIS->class, task->context->this, ref(THIS->action), REP( task, THIS->rest, task->next ) ) ;
""" )
T( 'GETSaction', None, 'PARAMcl', (), """
  RETURN( newGETS( task->context->this,
    C(CLASS, PSTHAT->type->specific_value),
    any(newOBJECTIVE( c(SET,PSTHAT->value->specific_value), task->context->closure->view ))
  ) ) ;""" )

T( 'DOES', None, None, (
  A( 'REFERENCE', 'rest' ),
  A( 'WORD', 'word' ),
  A( 'CLASS', 'class' ),
  A( 'ANY', 'action' ),
), """
  DO_COMMON ;
  METHOD( THIS->word, THIS->class, THIS->action ) ;
  task->next = REP( task, THIS->rest, task->next ) ;
""" )
T( 'DOESaction', None, 'PARAMslc', (), """
  RETURN( newDOES( task->context->this, wordNEW( C(STRING,PSTHAT->string->specific_value)->data  ), C(CLASS,PSTHAT->type->specific_value), any(newOBJECTIVE( c(SET,PSTHAT->value->specific_value), task->context->closure->view )) ) ) ;
""" )

T( 'DEFS', None, None, (
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
T( 'DEFSaction', None, 'PARAMsl', (), """RETURN( newDEFS( PSTHIS, wordNEW( C(STRING,PSTHAT->string->specific_value)->data ), any(newOBJECTIVE( c(SET,PSTHAT->value->specific_value), task->context->closure->view )) ) ) ; """ )


	####	general parameters

T( 'PARAM', None, None, (
  A( 'ANY', 'rest' ),
  A( 'WORD', 'word' ),
  A( 'REFERENCE', 'store' ),
  A( 'n_boolean', 'unset' ),
), """
  DO_COMMON ;
  ONWORD( THIS->word, THIS->store ) ;
  task->next = REP( task, ref(THIS->rest), task->next ) ;
  NOMOREWORDS ;
  if ( THIS->unset ) {
    REFERENCE r1 = ref(NONE) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, task->context->this, ref(newNOUN(PTHAT)) ) ;
    task->next = newTASK( ref(THIS->store), c1, r1,
      task->next,
      REP( task, ref(newPARAMset( THIS )), task->exit )
    ) ;
  }
""" )
T( 'PARAMset', None, None, (
  A( 'PARAM', 'param' ),
), """
  THIS->param->unset = FALSE ;
  RETURN( PTHIS ) ;
""" )
T( 'PARAMaction', None, 'PARAMsac', (), """
  RETURN( newPARAM( PSTHIS, wordNEW( C(STRING,PSTHAT->string->specific_value)->data  ), newREFERENCE( C(CLASS,PSTHAT->type->specific_value), any(PSTHAT->value->specific_value), any(PSTHAT->value->specific_value) ), TRUE ) ) ;
""" )


	####	some specific parameters

T( 'PARAMsac', None, None, (
  A( 'PARAM', 'params' ),
  A( 'REFERENCE', 'string' ),
  A( 'REFERENCE', 'value' ),
  A( 'REFERENCE', 'type' ),
), """
  DO_CLASS ;
  task->next = REP( task, ref(THIS->params), task->next ) ;
""",
constructor = """
  REFERENCE string = refNEW( STRING_class, any(newSTRING( "" )) ) ;
  REFERENCE type = refNEW( CLASS_class, any(ANY_class) ) ;
  REFERENCE value = ref(NONE) ;
  return any( newPARAMsac(
    newPARAM(
      any(newPARAM(
        any(newPARAM( any(NONE), WI_value, value ,TRUE )),
      WI_type, type ,TRUE )),
    WI_name, string, TRUE ),
  string, value, type ) ) ;
""" )

T( 'PARAMslc', None, None, (
  A( 'PARAM', 'params' ),
  A( 'REFERENCE', 'string' ),
  A( 'REFERENCE', 'value' ),
  A( 'REFERENCE', 'type' ),
), """
  DO_CLASS ;
  task->next = REP( task, ref(THIS->params), task->next ) ;
""",
constructor = """
  REFERENCE string = refNEW( STRING_class, any(newSTRING( "" )) ) ;
  REFERENCE type = refNEW( CLASS_class, any(ANY_class) ) ;
  REFERENCE value = refNEW( SET_class, any(newLIST( ANY_class, 0, c(REFS,NULL) )) ) ;
  return any( newPARAMslc(
    newPARAM(
      any(newPARAM(
        any(newPARAM( any(NONE), WI_value, value ,TRUE )),
      WI_type, type ,TRUE )),
    WI_name, string, TRUE ),
  string, value, type ) ) ;
""" )

T( 'PARAMsa', None, None, (
  A( 'PARAM', 'params' ),
  A( 'REFERENCE', 'string' ),
  A( 'REFERENCE', 'value' ),
), """
  DO_CLASS ;
  task->next = REP( task, ref(THIS->params), task->next ) ;
""",
constructor = """
  REFERENCE string = refNEW( STRING_class, any(newSTRING( "" )) ) ;
  REFERENCE value = ref(NONE) ;
  return any( newPARAMsa( newPARAM( any(newPARAM( any(NONE), WI_value, value ,TRUE )), WI_name, string ,TRUE ), string, value ) ) ;
""" )

T( 'PARAMsl', None, None, (
  A( 'PARAM', 'params' ),
  A( 'REFERENCE', 'string' ),
  A( 'REFERENCE', 'value' ),
), """
  DO_CLASS ;
  task->next = REP( task, ref(THIS->params), task->next ) ;
""",
constructor = """
  REFERENCE string = refNEW( STRING_class, any(newSTRING( "" )) ) ;
  REFERENCE value = refNEW( SET_class, any(newLIST( ANY_class, 0, c(REFS,NULL) )) ) ;
  return any( newPARAMsl( newPARAM( any(newPARAM( any(NONE), WI_value, value ,TRUE )), WI_name, string ,TRUE ), string, value ) ) ;
""" )

T( 'PARAMcl', None, None, (
  A( 'PARAM', 'params' ),
  A( 'REFERENCE', 'type' ),
  A( 'REFERENCE', 'value' ),
), """
  DO_CLASS ;
  task->next = REP( task, ref(THIS->params), task->next ) ;
""",
constructor = """
  REFERENCE type = refNEW( CLASS_class, any(ANY_class) ) ;
  REFERENCE value = refNEW( SET_class, any(newLIST( ANY_class, 0, c(REFS,NULL) )) ) ;
  return any( newPARAMcl( newPARAM( any(newPARAM( any(NONE), WI_value, value ,TRUE )), WI_type, type ,TRUE ), type, value ) ) ;
""" )


	####	class

T( 'CLASS', None, None, (
  A( 'ID', 'id', 'newID()' ),
  A( 'n_objective', 'instance_objective' ),
  A( 'n_constructor', 'constructor', 'CLASS_class->constructor' ),
  A( 'ANY', 'custom_constructor' ),
), """
//  DO_LIST ;
  DO_CLASS ;
  IFWORD( WI_new,
    if ( THIS->constructor ) RETURN( THIS->constructor() ) ; // remove???
    REFERENCE r1 = ref(NONE ) ;
    task->next = RETA( task, ref(newSIGNCUSTOMCONSTRUCTOR()), THIS_R, r1, task->next ) ;
    CONTEXT c1 = newCONTEXT( task->context->closure, ref(NONE), ref(NONE) ) ;
    task->next = newTASK( ref(THIS->custom_constructor), c1, r1, task->next, task->next ) ;
  ) ;
""" )

T( 'ID' )

T( 'SETCUSTOMCONSTRUCTOR', 'CLASS', None, (), """
  RETURN( newCLASS( newID(), c(n_objective,NULL), c(n_constructor,NULL), any(newOBJECTIVE( c(SET,PSTHAT), task->context->closure->view ) )) ) ;
""" )

T( 'SIGNCUSTOMCONSTRUCTOR', 'CLASS', None, (), """
  RETURN( newSIGNATURE( PSTHIS, PTHAT ) ) ;
""" )

T( 'SIGNATURE', None, None, (
  A( 'CLASS', 'class' ),
  A( 'ANY', 'rest' ),
), """
  DO_CLASS ;
//  DO_COMMON ;
  if ( c( n_integer, PTHAT ) == c( n_integer, THIS->class->id ) ) { RETURN( newREFERENCE( THIS->class, PTHIS, any(THIS) ) ) ; }
  task->next = REP( task, ref(THIS->rest), task->next ) ;
""" )


	####	number

T( 'NUMBER', None, None, (
  A( 'n_float', 'data', '0' ),
), """
  DO_CLASS ;
  IFWORD( WI_ADDADD, THIS->data++ ; RETURN( THIS ) ; ) ;
  IFWORD( WI_SUBSUB, THIS->data-- ; RETURN( THIS ) ; ) ;
  METHOD( WI_EQ,     NUMBER_class, newNUMBERset() ) ;
  METHOD( WI_EXCLAIMEQ,     NUMBER_class, newNUMBERset() ) ;
  METHOD( WI_ADDEQ,  NUMBER_class, newNUMBERaddset() ) ;
  METHOD( WI_SUBEQ,  NUMBER_class, newNUMBERsubset() ) ;
  METHOD( WI_ADD,    NUMBER_class, newNUMBERadd() ) ;
  METHOD( WI_SUB,    NUMBER_class, newNUMBERsub() ) ;
  METHOD( WI_MUL,    NUMBER_class, newNUMBERmul() ) ;
  METHOD( WI_DIV,    NUMBER_class, newNUMBERdiv() ) ;
  METHOD( WI_EQEQ,   NUMBER_class, newNUMBEReq() ) ;
  METHOD( WI_LTEQ,   NUMBER_class, newNUMBERlteq() ) ;
  METHOD( WI_GTEQ,   NUMBER_class, newNUMBERgteq() ) ;
  METHOD( WI_LT,     NUMBER_class, newNUMBERlt() ) ;
  METHOD( WI_GT,     NUMBER_class, newNUMBERgt() ) ;
  METHOD( WI_mod,    NUMBER_class, newNUMBERmod() ) ;
  METHOD( WI_pow,    NUMBER_class, newNUMBERpow() ) ;
  ONWORD( WI_sqrt,   newNUMBER( sqrt( THIS->data ) ) ) ;
""",
debug = D( ' %f', 'c( n_float, C( NUMBER, o )->data )' )
)
T( 'NUMBERliteral', None, None, (
  A( 'NUMBER', 'number' ),
), """
  NUMBER number = newNUMBER( THIS->number->data ) ;
  task->next = REX( task, ref(number), task->next ) ;
""" )

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
  DO_CLASS ;
""" )

T( 'GENERATOR', None, None, (
  A( 'CLASS', 'class' ),
  A( 'SET', 'value' ),
  A( 'CLOSURE', 'closure' ),
), """
  CLASS_RESPONSE( SET_class ) ;
  DO_CLASS ;
  ATTRIB( WI_each, iteratorNEW( task, THIS->class, THIS->value, THIS->closure ) ) ;
""" )
T( 'GENERATORCONSTRUCTOR', None, 'PARAMcl', (), """
  RETURN( newGENERATOR( C(CLASS,PSTHAT->type->specific_value), c(SET,PSTHAT->value->specific_value), task->context->closure ) ) ;
""" )

T( 'METALIST', None, None, (
  A( 'LIST', 'list' ),
), """
  task->next = REC( task, THIS->list->class, THIS_R, ref(newMETAAPPENDLISTaction()), task->next ) ;
""" )
T( 'METAAPPENDLISTaction', 'METALIST', None, (), """
  listAPPEND( PSTHIS->list, ref(PTHAT) ) ;
  RETURN( PSTHIS ) ;
""" )

T( 'LIST', None, None, (
  A( 'CLASS', 'class', 'ANY_class' ),
  A( 'n_integer', 'length', '0' ),
  A( 'REFS', 'data', 'NULL' ),
), """
  CLASS_RESPONSE( SET_class ) ;
  DO_CLASS ;
  ATTRIB( WI_length, newNUMBER( THIS->length ) ) ;
  ATTRIB( WI_each, newLISTITERATOR( THIS, 0, any(NONE) ) ) ;
  METHOD( WI_merge, SET_class, newMERGELISTaction() ) ;
  METHOD( WI_ADD, THIS->class, newAPPENDLISTaction() ) ;
  NOMOREWORDS ;
  task->next = REC( task, THIS->class, THIS_R, ref(newAPPENDLISTaction()), task->next ) ;
""" )
T( 'LISTliteral', None, None, (
  A( 'LIST', 'list' ),
), """
  LIST list = newLIST( THIS->list->class, 0, c(REFS,NULL) ) ;
  listMERGE( list, THIS->list ) ;
  task->next = REX( task, ref(list), task->next ) ;
""" )

T( 'SETCUSTOMLIST', 'CLASS', 'CLASS', (), """
  RETURN( newLIST( PSTHAT, c(n_integer,0), c(REFS,NULL) ) ) ;
""" )
T( 'APPENDLISTaction', 'LIST', None, (), """
  listAPPEND( PSTHIS, ref(PTHAT) ) ;
  RETURN( PSTHIS ) ;
""" )
T( 'MERGELISTaction', 'LIST', None, (), """
  task->result->value = PTHIS ;
	  task->next = newTASK( ref(newEVALUATE( task->context->closure, ref(newMETALIST( PSTHIS )), c(SET,PSTHAT) )), task->context, ref(NONE), task->next, task->exit ) ;
""" )

T( 'LISTITERATOR', None, None, (
  A( 'LIST', 'list' ),
  A( 'n_integer', 'index', '0' ),
  A( 'ANY', 'value' ),
), """
  DO_CLASS ;
  ATTRIB( WI_value, THIS->value ) ;
  IFWORD( WI_next,
    if ( THIS->index < THIS->list->length ) {
      THIS->value = any(THIS->list->data[THIS->index++]->value) ;
    } else {
      THIS->value = any(NONE) ;
    }
    RETURN( THIS->value ) ;
  )
""" )


	####	other objects

T( 'WORD', None, None, (
  A( 'STRING', 'value' ),
), """
  DO_CLASS ;
""",
debug = D( ' \'%s\'', 'c( n_string, C( WORD, o )->value->data )' )
)

T( 'STRING', None, None, (
  A( 'n_string', 'data' ),
), """
  DO_CLASS ;
""",
debug = D( ' \\"%s\\"', 'c( n_string, C( STRING, o )->data )' )
)

T( 'PHRASE', None, None, (
  A( 'LIST', 'value', 'listNEW( ANY_class )' ),
), """
  DO_CLASS ;
""" )

############################################################################################################
############################################################################################################
############################################################################################################

BUILD()


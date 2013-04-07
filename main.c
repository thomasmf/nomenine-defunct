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
#include "parser.h"

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

  NONE = newNONETYPE() ;

  INITIALIZE_core_TYPES() ;
  INITIALIZE_core_WIDS() ;

  IGNORE = newIGNORETYPE() ;
  UNUSED = ref(NONE) ;
  LOOPstop = newLOOPstopTYPE() ;
  CONSOLEOBJECT = newCONSOLE() ;

  ROOT = newCLOSURE( c(CLOSURE,NONE), ref(newCONTEXT( c(CLOSURE,NONE), ref(NONE), ref(NONE) )), ref(newROOTOBJECT()), ref(NONE) ) ;
  ROOT->parent = ROOT ;

  PARAMas = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMas_assort()) ) ;
  PARAMwa = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMwa_assort()) ) ;
  PARAMwc = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMwc_assort()) ) ;
  PARAMws = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMws_assort()) ) ;
  PARAMwf = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMwf_assort()) ) ;
  PARAMwca = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMwca_assort()) ) ;
  PARAMwcs = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMwcs_assort()) ) ;
  PARAMwas = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMwas_assort()) ) ;
  PARAMcs = newTYPE( newTID(), c(n_objective,NULL), any(NONE), any(newPARAMcs_assort()) ) ;

  CATfact = any(newFUNCTION( SET_type, any(newCATconst()) )) ;
  FACTfact = any(newFUNCTION( ANY_type, any(newFACTconst()) )) ;
  ASSORTfact = any(newFUNCTION( TUPLE_type, any(newASSORTconst()) )) ;

  PARAMfact = any(newFUNCTION( TUPLE_type, any(newPARAMconst()) )) ;
  MODULEfact = any(newFUNCTION( STRING_type, any(newMODULEconst()) )) ;

  STATICfact = any(newIS( ref(newFUNCTION( PARAMas, any(newSTATICconst_as()) )), ref(newFUNCTION( SET_type, any(newSTATICconst_s()) )) )) ;

  WORDfact = any(newFUNCTION( STRING_type, any(newWORDconst()) )) ;
  PHRASEfact = any(newFUNCTION( SET_type, any(newPHRASEconst()) )) ;

  FUNCTION_type->constructor = any(newFUNCTION( PARAMcs, any(newFUNCTIONconst()) )) ;
  LIST_type->constructor = any(newFUNCTION( TYPE_type, any(newSETCUSTOMLIST()) )) ;
  GENERATOR_type->constructor = any(newFUNCTION( PARAMcs, any(newGENERATORconst()) )) ;
  STRUCT_type->constructor = any(newFUNCTION( TUPLE_type, any(newSTRUCTconst()) )) ;

  STRINGprimitive_type->id = STRING_type->id ;
  STRING_type->constructor = any(newFUNCTION( STRING_type, any(newSTRINGconst()) )) ;
  STRING_type->comparator = any(newSTRINGcat()) ;

  n_integer parse_index = 0 ;
  PHRASE program = C( PHRASE, PARSE( &parse_index, read_source( (n_string)argv[ 1 ] ) ) ) ;

  REFERENCE r = ref(NONE) ;

  CONTEXT c1 = newCONTEXT( ROOT->parent, ref(NONE), ref(NONE) ) ;
  TASK t0 = newTASK( ref(newOBJECTIVE( c(SET,program->value), ROOT->view )), c1, r, c(TASK,NONE), c(TASK,NONE) ) ;
  TASK task = newTASK( ref(NONE), c1, ref(NONE), t0, t0 ) ;

  while ( TRUE ) {

    task = task->next ;
    if ( !NOTNONE( task ) ) break ;

    ONWID( WI_tron, ( trace_state = TRUE, task->context->this ) ) ;
    ONWID( WI_troff, ( trace_state = FALSE, task->context->this ) ) ;

    task->action->value->objective( task ) ;

    if ( trace_state ) {
      printf( "*\t%-30s%-30s%-30s%-30s\n", DEBUG( task->action->value ), DEBUG( task->context->this->value ), DEBUG( task->context->that->value ), DEBUG( task->result->value ) ) ;
    }

  }

//  LOG( r->value ) ;

  return EX_OK ;
}


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

#define LOG(x...) ( printf( "%04d\t%s\t%s\n", counter(), #x, DEBUG( (x) ) ) )
#define LOU(s,x...) ( printf( "%04d\t%s:%s\t%s\n", counter(), #s, #x, DEBUG( (x) ) ) )
#define OUT(x...) ( printf( "%04d %s\n", counter(), #x ) )
#define DEBUG(x) ( any(x)->debug( any(x) ) )

#define TRUE	1
#define FALSE	0
//#define NULL	0

#define ERROR( _m, _v ) error( (_m), c(n_boolean,(_v)), __FILE__, __LINE__ )
#define TYPE_ERROR( _t, _o ) type_error( (_t), any(_o), __FILE__, __LINE__ )

#define ALLOCATE( t ) ( ( t * )allocate( sizeof( t ) ) )
#define NOTNONE( x ) ( ( any(x) ) != any(NONE) )
#define any( x ) ( (ANY)(x) )
#define ref( x ) refNEW( ANY_type, any( x ) )
#define c( x, y ) ((x)(y))
//#define C( x, y ) ((x)(y))

#define C( _t, _o ) ((_t)( TYPE_ERROR( _t##_type, (_o) ) ))

#define TYPE_RESPONSE(_c1) { if ( c( n_integer, task->context->that->value ) == c( n_integer, _c1->id ) ) { task->result->value = THIS_R->value ; task->result->svalue = THIS_R->svalue ; task->result->type = THIS_R->type ; task->next = task->exit ; } }

#define CONTINUE { return ; }

#define RETURN( _o... ) { RSET( task->result, (_o) ) ; task->next = task->exit ; CONTINUE ; }

#define IFWID( w, p ) { if ( PTHAT == any(w) ) { { p } ; CONTINUE ; } }
#define IFTYPE( c, p... ) { if ( PTHAT->objective == c->instance_objective ) { { p } ; CONTINUE ; } }
#define IFADDR( o1, p... ) { if ( PTHAT == any(o1) ) { { p } ; CONTINUE ; } }

#define ONWID( w, o... ) { if ( PTHAT == any(C(WID,w)) ) { RETURN( o ) ; } }
#define ONTYPE( c, o... ) { if ( PTHAT->objective == c->instance_objective ) RETURN( o ) ; }
#define ONADDR( o1, o2... ) { if ( PTHAT == any(o1) ) RETURN( o2 ) ; }

#define METHOD( w1, c1, n1 ) { ONWID( w1, newAPPLICATOR( THIS_R, ref(newFUNCTION( c1, any(n1) )) ) ) ; }
#define METHOP( w1, f1 ) { ONWID( w1, newAPPLICATOR( THIS_R, ref(f1) ) ) ; }

#define NOMOREWIDS { IFTYPE( WID_type ) ; IFTYPE( TID_type ) ; }

#define RDSET( _r, _v, _sv ) rdset_f( (_r), any(_v), any(_sv) )
#define RSET( _r, _v ) rset_f( (_r), any(_v) )
#define RASET( _r, _v ) raset_f( (_r), any(_v) )
#define RPSET( _r, _v ) rpset_f( (_r), any(_v) )
#define RTSET( _r, _t, _v ) rtset_f( (_r), (_t), any(_v) )

#define PTHIS (task->context->this->value)
#define PTHAT (task->context->that->value)

#define DO_TYPE \
    DO_TYPE_ID_TEST ;												\
    DO_COMMON ;													\

#define DO_NOTSOCOMMON \
    ONWID( WI_DOT, IGNORE ) ;											\
    ONADDR( IGNORE, THIS ) ;											\
    ONWID( WI_delog, printf( "::::\t\t\t%s\n", DEBUG( THIS ) ), PTHIS ) ;					\
    METHOD( WI_em, SEQ_type, newEMaction() ) ;									\
    IFWID( WI_throw, task->next = newTASK( task->context->closure->field, newCONTEXT( task->context->closure, task->context->closure->field, task->context->this ), task->result, task->next, task->exit ) ; ) ; \

#define DO_COMMON \
    DO_NOTSOCOMMON												\
    METHOD( WI_then, SEQ_type, newTHENaction() ) ;								\
    METHOD( WI_else, SEQ_type, newELSEaction() ) ;								\
    ONWID( WI_en, ref(PTHIS) ) ;										\
    METHOD( WI_has, PARAMwa, newHASaction_wa()) ;								\
    METHOD( WI_is, ANY_type, newISaction() ) ;									\
    METHOD( WI_gets, PARAMcs, newGETSaction() ) ;								\
    METHOP( WI_does, newIS( ref(newFUNCTION( PARAMwcs, any(newDOESaction_wcs()) )), ref(newFUNCTION( PARAMwf, any(newDOESaction_wf()) )) ) ) ;					\
    METHOD( WI_noms, PARAMws, newNOMSaction() ) ;								\
    METHOP( WI_inv, newIS( ref(newFUNCTION( PARAMws, any(newINVaction_ws()) )), ref(newFUNCTION( PARAMwas, any(newINVaction_was()) )) ) ) ; \


#define USE_ON( _cont, _obj ) {	\
  if ( (_obj)->objective == OBSERVER_type->instance_objective ) {	\
    task->_cont = newTASK( task->context->closure->field, newCONTEXT( task->context->closure, task->context->closure->field, ref(C(OBSERVER,(_obj))->dep) ), ref(NONE), task->_cont, task->_cont ) ;	\
  }	\
}

#define MOD_ON( _cont, _obj ) { if ( (_obj)->objective == OBSERVER_type->instance_objective ) { task->_cont = newTASK( ref(C(OBSERVER,_obj)->dep), newCONTEXT( task->context->closure, ref(C(OBSERVER,_obj)->dep), ref(WI_modified) ), task->result, task->_cont, task->_cont ) ; } }


inline STRING STRX( n_string fmt, ... ) ;


inline void* allocate( n_integer n ) ;
inline n_integer counter() ;

inline void rdset_f( REFERENCE r, ANY v, ANY sv ) ;
inline void rset_f( REFERENCE r, ANY v ) ;
inline void raset_f( REFERENCE r, ANY v ) ;
inline void rpset_f( REFERENCE r, ANY v ) ;
inline void rtset_f( REFERENCE r, TYPE t, ANY v ) ;


inline REFERENCE refNEW( TYPE c, ANY x ) ;
inline ANY type_error( TYPE c, ANY o, n_string f, n_integer l ) ;
inline void error( n_string m, n_boolean v, n_string f, n_integer l ) ;

inline TASK REC( TASK task, TYPE class, REFERENCE this, REFERENCE action, TASK next ) ;

#define tupleNEW() newTUPLE( ANY_type, 0, c(REFS,NULL) )
inline n_void tupleAPPEND( TUPLE l, REFERENCE e ) ;
#define listNEW( x ) newLIST( (x), 0, c(REFS,NULL) )
inline n_void listAPPEND( LIST l, REFERENCE e ) ;
inline LIST listMERGE( LIST l1, LIST l2 ) ;
inline n_boolean listHASELEMENT( LIST l, REFERENCE e ) ;
inline n_void listREMOVEELEMENT( LIST l, REFERENCE e ) ;


inline OBSERVER obsNEW( OBSERVER o1, REFERENCE o2 ) ;
inline n_void depREEVALUATE( TASK task, DEPENDENCY dep ) ;
inline n_void depPROPAGATE( TASK task, DEPENDENCY dep ) ;
inline n_void depRESET( DEPENDENCY dep ) ;

inline WID widNEW( n_string s ) ;

inline ITERATOR iteratorNEW( TASK task, TYPE class, SEQ l, CLOSURE closure ) ;

CLOSURE ROOT ;
NONETYPE NONE ;
IGNORETYPE IGNORE ;
REFERENCE UNUSED ;
LIST WIDS ;
CONSOLE CONSOLEOBJECT ;
LOOPstopTYPE LOOPstop ;

ANY REFfact ;
ANY CATfact ;
ANY FACTfact ;
ANY ASSORTfact ;
ANY PARAMfact ;
ANY MODULEfact ;
ANY STATICfact ;
ANY WORDfact ;
ANY PHRASEfact ;

TYPE PARAMas ;
TYPE PARAMwa ;
TYPE PARAMwc ;
TYPE PARAMws ;
TYPE PARAMwf ;
TYPE PARAMwca ;
TYPE PARAMwcs ;
TYPE PARAMwas ;
TYPE PARAMcs ;


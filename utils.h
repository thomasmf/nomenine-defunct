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

#define ASSERT( x ) ( assert( x ) )
#define LOG(x...) ( printf( "%04d\t%s\t%s\n", counter(), #x, DEBUG( (x) ) ) )
#define LOU(s,x...) ( printf( "%04d\t%s:%s\t%s\n", counter(), #s, #x, DEBUG( (x) ) ) )
#define OUT(x...) ( printf( "%04d %s\n", counter(), #x ) )
#define DEBUG(x) ( any(x)->debug( any(x) ) )

#define TRUE	1
#define FALSE	0
//#define NULL	0


#define ALLOCATE( t ) ( ( t * )allocate( sizeof( t ) ) )
#define NOTNONE( x ) ( ( any(x) ) != any(NONE) )
#define any( x ) ( (ANY)(x) )
#define ref( x ) refNEW( ANY_class, any( x ) )
#define c( x, y ) ((x)(y))
//#define C( x, y ) ((x)(y))
#define C( x, y ) ((x)(assert_type( x##_class, any(y), __LINE__ )))


#define CLASS_RESPONSE(_c1) { if ( c( n_integer, task->context->that->value ) == c( n_integer, _c1->id ) ) { RETURN( THIS_R ) ; } }

#define CONTINUE { return ; }

#define RETURN( o... ) { task->result->value = any((o)) ; task->next = task->exit ; CONTINUE ; }

#define IFWORD( w, p ) { if ( PTHAT == any(w) ) { { p } ; CONTINUE ; } }
#define IFTYPE( c, p... ) { if ( PTHAT->objective == c->instance_objective ) { { p } ; CONTINUE ; } }
#define IFADDR( o1, p... ) { if ( PTHAT == any(o1) ) { { p } ; CONTINUE ; } }

#define ONWORD( w, o... ) { if ( PTHAT == any(w) ) { RETURN( o ) ; } }
#define ONTYPE( c, o... ) { if ( PTHAT->objective == c->instance_objective ) RETURN( o ) ; }
#define ONADDR( o1, o2... ) { if ( PTHAT == any(o1) ) RETURN( o2 ) ; }

#define ATTRIB( w, o... ) ONWORD( w, o )
#define METHOD( w1, c1, n1 ) { ATTRIB( w1, newAPPLICATOR( THIS_R, c1, any(n1) ) ) ; }

#define NOMOREWORDS { IFTYPE( WORD_class ) ; IFTYPE( ID_class ) ; }

#define STR( s ) ( #s )


#define PTHIS (task->context->this->value)
#define PTHAT (task->context->that->value)

#define DO_EVALUATE \
  IFTYPE( PHRASE_class,												\
    REFERENCE r2 = ref(NONE) ;											\
    task->next = newTASK(											\
      ref(newEVALUATE(												\
        task->context->closure,											\
        ref(newOCONTEXT( any(PTHIS), any(task->context->closure) )),						\
        c(SET,C(PHRASE,PTHAT)->value)										\
      )), task->context, r2,											\
      RETO( task, task->context->this, r2, task->next ),							\
    task->exit ) ;												\
  ) ;														\

#define DO_CLASS \
    DO_CLASS_ID_TEST ;												\
    DO_COMMON ;													\
    if ( c( n_integer, PTHAT ) == c( n_integer, ANY_class->id ) ) { RETURN( THIS_R ) ; }			\

#define DO_CONDITIONS \
    METHOD( WI_then, LIST_class, newTHENaction() ) ;								\
    METHOD( WI_else, LIST_class, newELSEaction() ) ;								\

#define DO_CORE \
    ATTRIB( WI_DOT, IGNORE ) ;											\
    ONADDR( IGNORE, THIS ) ;											\
    ATTRIB( WI_EXCLAIM, newNOUN( any(THIS) ) ) ;								\

#define DO_NOB \
    DO_EVALUATE ;												\
    DO_CORE ;													\

#define DO_DEBUG \
    ATTRIB( WI_delog, printf( "::::\t\t\t%s\n", DEBUG( THIS ) ), PTHIS ) ;					\

#define DO_COMMON \
    DO_NOB ;													\
    DO_CONDITIONS ;												\
    DO_DEBUG ;													\
    METHOD( WI_has, PARAMsac_class, newHASaction() ) ;								\
    METHOD( WI_is, ANY_class, newISaction() ) ;									\
    METHOD( WI_gets, PARAMcl_class, newGETSaction() ) ;								\
    METHOD( WI_does, PARAMslc_class, newDOESaction() ) ;							\
    METHOD( WI_defs, PARAMsl_class, newDEFSaction() ) ;								\
    METHOD( WI_param, PARAMsac_class, newPARAMaction() ) ;							\
    IFWORD( WI_throw, task->next = RETO( task, task->context->closure->field, task->context->this, task->next ) ; ) ;


inline void* allocate( n_integer n ) ;
inline n_integer counter() ;

inline REFERENCE refNEW( CLASS c, ANY x ) ;
inline ANY assert_type( CLASS c, ANY o, n_integer l ) ;

inline TASK REC( TASK task, CLASS class, REFERENCE this, REFERENCE action, TASK next ) ;
inline TASK REP( TASK task, REFERENCE object, TASK next ) ;
inline TASK REX( TASK task, REFERENCE object, TASK next ) ;
inline TASK RETO( TASK task, REFERENCE this, REFERENCE that, TASK next ) ;
inline TASK RETA( TASK task, REFERENCE action, REFERENCE this, REFERENCE that, TASK next ) ;

#define listNEW( x ) newLIST( x, 0, c(REFS,NULL) )
inline n_void listAPPEND( LIST l, REFERENCE e ) ;
inline LIST listMERGE( LIST l1, LIST l2 ) ;

inline WORD wordNEW( n_string s ) ;

inline ITERATOR iteratorNEW( TASK task, CLASS class, SET l, CLOSURE closure ) ;

CLOSURE ROOT ;
NONETYPE NONE ;
IGNORETYPE IGNORE ;
REFERENCE UNUSED ;
LIST WORDS ;

LOOPstopTYPE LOOPstop ;

ANY USERCLASS ;
ANY LISTCLASS ;
ANY FUNCTIONCLASS ;
ANY GENERATORCLASS ;


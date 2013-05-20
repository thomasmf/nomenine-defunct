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

class META :
  NAME = 'unamed'
  HEADER = ''
  DECL = ''
  TYPES = []

def BUILD() :
  result_h = ''
  result_c = META.HEADER

  result_h += ( ''.join( [
    '\nstruct ' + c.name + '_struct ;' +
    '\ntypedef struct ' + c.name + '_struct * ' + c.name + ' ;'
  for c in T.classes ] ) )

  result_h += META.DECL

  result_h += ( ''.join( [
    '\nTYPE ' + c.name + '_type ;'
  for c in T.classes ] ) )

  result_h += ( ''.join( [
    '\nWID WI_' + stringtocid( w ) + ' ;'
  for w in T.wids ] ) )

  result_h += ( ''.join( [
    '\ninline ' + c.name + ' new' + c.name + '( ' +
    ( ', '.join( [
      a.t + ' ' + a.n
    for a in c.attributes ] ) ) + ' ) ;' +
    '\nstruct ' + c.name + '_struct {' +
    '\n  n_void (*objective)( TASK ) ;'
    '\n  n_string (*debug)( ANY ) ;' +
    ( ''.join( [
      '\n  ' + a.t + ' ' + a.n + ' ;'
    for a in c.attributes ] ) ) + '\n} ;'
  for c in T.classes ] ) )

  result_c += ( ''.join( [
    '\n#define THIS c(' + c.name +',task->action->value)' +
    '\n#define THIS_R newREFERENCE( ' + c.name + '_type, task->context->this->value, any(THIS) )' +
    '\n#define DO_TYPE_ID_TEST TYPE_RESPONSE(' + c.name + '_type )'
    '\n#define PSTHIS ' + ( ( 'C(' + c.t1 + ',' ) if c.t1 else 'any(' ) + 'task->context->this->svalue)' +
    '\n#define PSTHAT ' + ( ( 'C(' + c.t2 + ',' ) if c.t2 else 'any(' ) + 'task->context->that->svalue)' +
    '\nn_void ' + c.name + '_objective( TASK task ) {' + c.objective + '}' +
    '\n#undef PSTHAT' +
    '\n#undef PSTHIS' +
    '\n#undef DO_TYPE_ID_TEST' +
    '\n#undef THIS_R' +
    '\n#undef THIS' +
    '\nn_string debug' + c.name + '( ANY o ) {' +
    '\n  char * s ;' +
    '\n  asprintf( &s, "[%04x:%s' + c.debug.f + ']", c( n_integer, o ) >> 4 & 0xfff, "' + c.name + '"' +
    ( ''.join( [
      ', ' + d
    for d in c.debug.d ] ) ) + ' ) ;' +
    '\n  return s ;' +
    '\n}' +
    (
      '\ninline ' + c.name + ' new' + c.name + '( ' +
      ( ', '.join( [
        a.t + ' ' + a.n
      for a in c.attributes ] ) ) + ' ) {' +
      '\n  ' + c.name + ' new_object = ALLOCATE( struct ' + c.name + '_struct ) ;' +
      '\n  new_object->objective = ' + c.name + '_objective ;' +
      '\n  new_object->debug = debug' + c.name + ' ;' +
      ( ''.join( [
         '\n  new_object->' + a.n + ' = ' + a.n + ' ;'
      for a in c.attributes ] ) ) +
      '\n  return new_object ;' +
      '\n}'
    )
  for c in T.classes ] ) + '' )

  result_h += '\nn_void INITIALIZE_' + META.NAME + '_TYPES() ;'
  result_c += ( '\nn_void INITIALIZE_' + META.NAME + '_TYPES() {' + ( ''.join( [
    '\n  ' + c.name + '_type = newTYPE( newTID(), ' + c.name + '_objective, any(NONE), any(NONE) ) ; '
  for c in T.classes ] ) ) + '\n}' )

  result_h += '\nn_void INITIALIZE_' + META.NAME + '_WIDS() ;'
  result_c += ( '\nn_void INITIALIZE_' + META.NAME + '_WIDS() {' +
    '\n  WIDS = listNEW ; ' + ( ''.join( [
    '\n  WI_' + stringtocid( w ) + ' = widNEW( "' + w + '" ) ; '
  for w in T.wids ] ) ) + '\n}' )

  result_h += '\n\n'
  result_c += '\n\n'

  open( META.NAME + '.h', 'w' ).write( result_h ) ;
  open( META.NAME + '.c', 'w' ).write( result_c ) ;

class D:
  def __init__( self, f = '', *d ) :
    self.f = f
    self.d = d

class A:
  def __init__( self, t, n ) :
    self.t = t
    self.n = n

class T:
  classes = []
  wids = []
  def __init__( self, name, t1 = None, t2 = None, attributes = (), objective = "", debug = D() ) :
    self.name = name
    self.t1 = t1
    self.t2 = t2
    self.attributes = attributes
    self.objective = objective
    self.debug = debug
    T.classes.append( self )

def stringtocid( s ) :
  for a, b in {
    '.':'DOT', '!':'EXCLAIM',':':'COLON',
    '+':'ADD', '-':'SUB', '*':'MUL', '/':'DIV',
    '<':'LT', '=':'EQ', '>':'GT', '%':'PERC'
  }.iteritems() :
    s = s.replace( a, b )
  return s

def W( *wids ) :
  T.wids = wids

class X:
  def __init__( self, n, c ) :
    self.n = n
    self.c = c
  

def P( name, *parameters ) :

  T( 'PARAM' + name + '_assort', None, None, (), """
    REFERENCE tuple = refNEW( TUPLE_type, any(NONE) ) ;
    REFERENCE tuple_ref = ref(tuple) ;
    task->next = newTASK( ref(newPARAM%(name)s_0( tuple )), task->context, task->result, task->next, task->exit ) ;
    CONTEXT c0 = newCONTEXT( task->context->closure, tuple_ref, ref(newNOUN( task->context->that )) ) ;
    task->next = newTASK( tuple_ref, c0, ref(NONE), task->next, task->next ) ;
  """ % { 'name':name } )

  T( 'PARAM' + name + '_0', None, None, (
    A( 'REFERENCE', 'tuple' ),
  ), """
//    OUT( assort 0 ) ;
//    %(dbg)s
    if ( NOTNONE( THIS->tuple->value ) ) {
      if ( C(TUPLE,THIS->tuple->value)->list->length == %(len)s ) {
//        OUT( assort 0.1 ) ;
        %(decl)s
        task->next = newTASK( ref(newPARAM%(name)s_1( %(attr)s )), task->context, task->result, task->next, task->exit ) ;
        %(check)s
      }
    }
  """ % { 'name':name, 'len':len(parameters),
    'dbg': ( ''.join( [ 'LOG( C(TUPLE,THIS->tuple->value)->list->data[%s]->value ) ;' % str( i ) for i in range( len(parameters) ) ] ) ),
    'attr': ( ', '.join( [ p.n + '_ref' for p in parameters ] ) ),
    'decl': ( ''.join( [ """
        REFERENCE %(name)s_ref = refNEW( %(cls)s_type, any(NONE) ) ;
        REFERENCE %(name)s_ref_ref = ref(%(name)s_ref) ;
      """ % { 'name':p.n, 'cls':p.c } for p in parameters ] ) ),
    'check': ( ''.join( [ """
//        LOG( %(name)s_ref_ref ) ;
        CONTEXT c%(name)s = newCONTEXT( task->context->closure, %(name)s_ref_ref, ref(newNOUN( C(TUPLE,THIS->tuple->value)->list->data[%(i)s] )) ) ;
        task->next = newTASK( %(name)s_ref_ref, c%(name)s, ref(NONE), task->next, task->next ) ;
    """ % { 'i':i, 'name':parameters[i].n } for i in range( len(parameters) ) ] ) )
  } )

  T( 'PARAM' + name + '_1', None, None, [
    A( 'REFERENCE', p.n + '_ref' ) for p in parameters
  ], """
//    OUT( assort 1 ) ;
//    %(dbg)s
    if ( %(test)s ) {
//      OUT( assort 1.1 ) ;
      RETURN( newPARAM%(name)s_struct( %(pass)s ) ) ;
    }
  """ % { 'name':name,
    'dbg': ( ''.join( [ 'LOG( THIS->%s_ref->value ) ;' % p.n for p in parameters ] ) ),
    'test': ( ' && '.join( [ 'NOTNONE( THIS->%s_ref->value )' % p.n for p in parameters ] ) ),
    'pass': ( ', '.join( [ 'THIS->%s_ref' % p.n for p in parameters ] ) )
  } )

  T( 'PARAM' + name + '_struct', None, None, [
    A( 'REFERENCE', p.n + '_ref' ) for p in parameters
  ], """
    DO_TYPE ;
    %(attr)s
  """ % { 'attr': ( ''.join( [ """
    ONWID( WI_%(p)s, THIS->%(p)s_ref->value ) ;
  """ % { 'p':p.n } for p in parameters ] ) ) } )









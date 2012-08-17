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
  TYPES = ''
  CLASSES = []

def BUILD() :
  result_h = ''
  result_c = META.HEADER

  result_h += ( ''.join( [
    '\nstruct ' + c.name + '_struct ;' +
    '\ntypedef struct ' + c.name + '_struct * ' + c.name + ' ;'
  for c in T.classes ] ) )

  result_h += META.TYPES

  result_h += ( ''.join( [
    '\nCLASS ' + c.name + '_class ;'
  for c in T.classes ] ) )

  result_h += ( ''.join( [
    '\nWORD WI_' + stringtocid( w ) + ' ;'
  for w in T.words ] ) )

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
    '\n#define THIS_R newREFERENCE( ' + c.name + '_class, task->context->this->value, any(THIS) )' +
    '\n#define DO_CLASS_ID_TEST CLASS_RESPONSE(' + c.name + '_class )'
    '\n#define PSTHIS ' + ( ( 'C(' + c.t1 + ',' ) if c.t1 else 'any(' ) + 'task->context->this->specific_value)' +
    '\n#define PSTHAT ' + ( ( 'C(' + c.t2 + ',' ) if c.t2 else 'any(' ) + 'task->context->that->specific_value)' +
    '\nn_void ' + c.name + '_objective( TASK task ) {' + c.objective + '}' +
    '\n#undef PSTHAT' +
    '\n#undef PSTHIS' +
    '\n#undef DO_CLASS_ID_TEST' +
    '\n#undef THIS_R' +
    '\n#undef THIS' +
    '\nANY ' + c.name + '_constructor( n_void ) {' +
    ( (
      '\n  return any(new' + c.name + '( ' +
      ( ', '.join( [
        'c(' + a.t + ',' + a.v + ')'
      for a in c.attributes ] ) ) + ' ) ) ;'
    ) if ( not c.constructor ) else ( c.constructor ) ) +
    '\n' + '}' +
    '\nn_string debug' + c.name + '( ANY o ) {' +
    '\n  char * s ;' +
    '\n  asprintf( &s, "[%03x:%s' + c.debug.f + ']", c( n_integer, o ) >> 4 & 0xfff, "' + c.name + '"' +
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

  result_h += '\nn_void INITIALIZE_' + META.NAME + '_CLASSES() ;'
  result_c += ( '\nn_void INITIALIZE_' + META.NAME + '_CLASSES() {' + ( ''.join( [
    '\n  ' + c.name + '_class = newCLASS( newID(), ' + c.name + '_objective, ' + c.name + '_constructor, any(NONE) ) ; '
  for c in T.classes ] ) ) + '\n}' )

  result_h += '\nn_void INITIALIZE_' + META.NAME + '_WORDS() ;'
  result_c += ( '\nn_void INITIALIZE_' + META.NAME + '_WORDS() {' +
    '\n  WORDS = listNEW( WORD_class ) ; ' + ( ''.join( [
    '\n  WI_' + stringtocid( w ) + ' = wordNEW( "' + w + '" ) ; '
  for w in T.words ] ) ) + '\n}' )

  result_h += '\n\n'
  result_c += '\n\n'

  open( META.NAME + '.h', 'w' ).write( result_h ) ;
  open( META.NAME + '.c', 'w' ).write( result_c ) ;

class D:
  def __init__( self, f = '', *d ) :
    self.f = f
    self.d = d

class A:
  def __init__( self, t, n, v = 'NONE' ) :
    self.t = t
    self.n = n
    self.v = v

class T:
  classes = []
  words = []
  def __init__( self, name, t1 = None, t2 = None, attributes = (), objective = "", debug = D(), constructor = None ) :
    self.name = name
    self.t1 = t1
    self.t2 = t2
    self.attributes = attributes
    self.objective = objective
    self.debug = debug
    self.constructor = constructor
    T.classes.append( self )

def stringtocid( s ) :
  for a, b in {
    '.':'DOT', '!':'EXCLAIM',':':'COLON',
    '+':'ADD', '-':'SUB', '*':'MUL', '/':'DIV',
    '<':'LT', '=':'EQ', '>':'GT', '%':'PERC'
  }.iteritems() :
    s = s.replace( a, b )
  return s

def W( *words ) :
  T.words = words



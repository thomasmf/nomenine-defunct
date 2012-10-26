#! /usr/bin/node

// Copyright Thomas M. Farrelly, 2012

function newNumber( state ) {
  result = function( that ) {
    if ( that.type == 'number' ) {
      return newNumber( arguments.callee.state + that.state )
    } else if ( that.type = 'word' ) {
      if ( that.state == 'output' ) {
        console.log( arguments.callee.state )
        return arguments.callee
      }
    }
    return none ;
  }
  result.type = 'number' ;
  result.state = state ;
  return result ;
}

function newWord( state ) {
  result = none ;
  result.type = 'word' ;
  result.state = state ;
  return result ;
}

start_context = function( that ) {
  return that ;
}

none = function( that ) {
  return none ;
}

// ( 10 5 output 100 output )
start_context( newNumber( 10 ) )( newNumber( 5 ) )( newWord( 'output' ) )( newNumber( 100 ) )( newWord( 'output' ) )



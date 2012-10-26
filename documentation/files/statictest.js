#! /usr/bin/node

// Copyright Thomas M. Farrelly, 2012

function scope( props ) {
  this.props = props
}

scope.prototype = {
  'set' : function( n, v ) {
    this.props[ n ].v = v
    this.update( n )
  },
  'get' : function( n ) {
    return this.props[ n ].v
  },
  'update' : function( n ) {
    if ( this.props[ n ].v != this.props[ n ].c ) {
      this.props[ n ].c = this.props[ n ].v
      for ( i in this.props[ n ].l ) {
        this.compute( this.props[ this.props[ n ].l[ i ] ].n )
      }
    }
  },
  'compute' : function( n ) {
    this.props[ n ].v = this.props[ n ].d.apply( this, [] )
    this.update( n )
  },
  'log' : function() {
    for ( i in this.props ) {
      console.log( this.props[ i ].n, this.props[ i ].v )
    }
  }
}

function prop( n, d, l, v ) {
  this.n = n
  this.d = d
  this.v = v || 0
  this.c = v || 0
  this.l = l || []
}

var test1 = new scope( {
  'a' : new prop( 'a', function() { return this.get( 'b' ) + 1 }, [ 'b' ] ),
  'b' : new prop( 'b', function() { return this.get( 'a' ) - 1 }, [ 'a' ] ),
} )


test1.set( 'a', 4 )
test1.log()
test1.set( 'b', 8 )
test1.log()


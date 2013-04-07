
import os

for fn in os.listdir( 'test' ) :
  print 'Test: test/' + fn
  os.system( './nominine test/' + fn )


class Attribute(object):

  def __init__( self, parent, name, **options ):
    self.name = name
    self.options = options
    self.parent = parent

  def key( self ):
    return self.options.get('key', self.name)

  def value_for( self, item, args = {} ):
    if hasattr( self.parent, self.name):
      return getattr( self.parent, self.name )( item, args )
    elif hasattr( item, self.name ):
      val = getattr( item, self.name )
      if callable( val ):
        val = val()
      return val 
    else:
      raise Exception( "Neither %s nor %s responds to %s" % ( self.parent, item, self.name ) )
      

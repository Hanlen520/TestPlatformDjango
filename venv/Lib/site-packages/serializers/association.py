from serializers.attribute import Attribute
from itertools import starmap

class Association(Attribute):
  def __init__( self, parent, name, **options ):
    super( Association, self ).__init__( parent, name, **options )
    self.serializer = options[ 'serializer' ]

  #private

  def _dict_for( self, item, args ):
    return self.serializer( item, args ).to_dict()

class HasOneAssociation(Association):

  def value_for( self, item, args ):
    # get the object to serialize      
    assoc_item = super( Association, self ).value_for( item, args )

    if (isinstance( assoc_item, list )):
      raise Exception("has_one associations must be applied to a single object, not a list")
    # serialize the object and get its to_dict
    return self._dict_for( assoc_item, args )

class HasManyAssociation(Association):

  def value_for( self, items, args ):
    # get the objects to serialize      
    assoc_items = super( Association, self ).value_for( items, args )

    if not ( isinstance( assoc_items, list ) ):
      raise Exception("has_many associations must be applied to a list")
    
    # serialize the objects and get their to_dict
    return [ self._dict_for( item, args ) for item in assoc_items ]

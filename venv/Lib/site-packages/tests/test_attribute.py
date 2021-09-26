from serializers.serializer import Serializer
import tests
from tests import BaseModel, OtherModel, BaseSerializer, OtherSerializer

from nose.tools import assert_true, assert_equals
import json

class TestAttribute:
  def setup( self ):
    self.base = BaseModel() 
    self.other = OtherModel()

  def test_attribute_to_dict( self ):
    obj_dict = BaseSerializer( self.base ).to_dict()

    assert_true( isinstance( obj_dict, dict ) )

    assert_equals( obj_dict['string_var'], "string" )
    assert_equals( obj_dict['int_var'], 6 )
    assert_equals( obj_dict['arr_var'], [1, 2, "string"] )
    assert_equals( obj_dict['dict_var'], { 'key' : 'value' } )
    assert_equals( obj_dict['serialized_name'], "poops" )
    assert_equals( obj_dict['func_var'], "funk" )


  def test_attribute_to_json( self ):
    obj_json = BaseSerializer( self.base ).to_json()

    expeted_json = json.dumps( {"arr_var": [1, 2, "string"], "func_var": "funk", "dict_var": {"key": "value"}, "string_var": "string", "int_var": 6, "serialized_name": "poops"}, sort_keys=True)
    assert_equals( expeted_json, obj_json )

  def test_attributes_to_dict( self ):
    obj_dict = OtherSerializer( self.other ).to_dict()

    assert_true( isinstance( obj_dict, dict ) )

    assert_equals( obj_dict['attr'], "string" )
    assert_equals( obj_dict['func'], "lol" )
    assert_equals( obj_dict['here'], "poops" )
    assert_equals( obj_dict['lol'], 6 )
    assert_equals( obj_dict['something'], [1, 2, "string"] )
    assert_equals( obj_dict['wonderful'], {"key": "value"} )

  def test_attributes_to_json( self ):
    obj_json = OtherSerializer( self.other ).to_json()

    expeted_json = json.dumps( {"attr": "string", "func": "lol", "here": "poops", "lol": 6, "something": [1, 2, "string"], "wonderful": {"key": "value"}}, sort_keys=True)
    assert_equals( expeted_json, obj_json )


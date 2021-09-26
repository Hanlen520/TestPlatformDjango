from serializers.serializer import Serializer
import tests
from tests import BaseModel, OtherModel, ComplexModel, BaseSerializer, OtherSerializer, ComplexSerializer, HyperComplexSerializer

from nose.tools import assert_true, assert_equals, raises
import json

class TestAssociation:
  def setup(self):
    self.complex = ComplexModel()

  @raises( Exception )
  def test_has_one_raises_without_serializer_option( self ):
    assert_raises(  Exception,
                    ComplexSerializer.has_one,
                    'thing' )

  @raises( Exception)
  def test_has_many_raises_whithout_resializer_option( self ):
    assert_raises(  Exception,
                    ComplexSerializer.has_many,
                    'things' )

  def test_has_one_serializes_submodels( self ):
    serializer = ComplexSerializer( self.complex )

    obj_dict = serializer.to_dict()

    base_dict = {"arr_var": [1, 2, "string"], "func_var": "funk", "dict_var": {"key": "value"}, "string_var": "string", "int_var": 6, "serialized_name": "poops"}
    assert_equals( obj_dict['base'], base_dict )

    other_dict = {"attr": "string", "func": "lol", "here": "poops", "lol": 6, "something": [1, 2, "string"], "wonderful": {"key": "value"}}

    assert_equals( obj_dict['others'], [other_dict, other_dict] )

  def test_associations_can_beinvoked_from_serializer_methods( self ):
    serializer = HyperComplexSerializer( self.complex )

    obj_dict = serializer.to_dict()

    base_dict = {"arr_var": [1, 2, "string"], "func_var": "funk", "dict_var": {"key": "value"}, "string_var": "string", "int_var": 6, "serialized_name": "poops"}
    assert_equals( obj_dict['custom_base'], base_dict )

    other_dict = {"attr": "string", "func": "lol", "here": "poops", "lol": 6, "something": [1, 2, "string"], "wonderful": {"key": "value"}}

    assert_equals( obj_dict['magic'], [other_dict, other_dict] )
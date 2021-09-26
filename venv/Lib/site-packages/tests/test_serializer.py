from serializers.serializer import Serializer
import tests
from tests import OtherModel, MethodizedSerializer

from nose.tools import assert_true, assert_equals
import json

class TestSerializer:
  def test_serializer_can_define_methods( self ):
    result_dict = MethodizedSerializer( OtherModel() ).to_dict()
    assert_equals( "poops", result_dict['custom_field'] )

  def test_serializer_can_take_optional_args( self ):
    result_dict = MethodizedSerializer( OtherModel(), { 'lol': "thing" } ).to_dict()
    assert_equals( "object.here:poops, args['lol']:thing", result_dict['custom_field_with_args'] )

  def test_serializer_methods_can_be_keyed( self ):
    result_dict = MethodizedSerializer( OtherModel(), { 'lol': "thing" } ).to_dict()
    assert_equals( "lol", result_dict['kek'] )

  def test_serializer_methods_shadow_object_methods( self ):
    result_dict = MethodizedSerializer( OtherModel(), { 'lol': "thing" } ).to_dict()
    assert_equals( 'overridden func: lol', result_dict['func'] )

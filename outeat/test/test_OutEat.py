
from nose.tools import assert_true

from outeat.outeat import OutEat

class TestOutEat:
    def test_register(self):
        result = OutEat().register("Charles")
        assert_true(result)

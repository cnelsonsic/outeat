
from nose.tools import assert_true, assert_equal

from outeat.outeat import OutEat

class TestOutEat:
    def setup(cls):
        cls.outeat = OutEat(dbpath="sqlite://", dbecho=False)

    def test_register(self):
        result = self.outeat.register("Charles")
        assert_true(result)
        assert_equal(result[0]['who'], 'Charles')
        assert_equal(result[0]['when'], ['any'])
        assert_equal(result[0]['where'], ['any'])

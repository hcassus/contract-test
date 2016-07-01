from unittest.case import TestCase

from ddt import ddt, unpack, data
from unittest.mock import create_autospec
from mockextras import when

from .contract_constants import *
from .production_code import *




@ddt
class HeightEntityContractTests(TestCase):

    def setUp(self):
        self.height_entity = HeightEntity()

    @data(
        (PLAYER_170_75, ONE_POINT_SEVEN_METERS),
        (PLAYER_170_57, ONE_POINT_SEVEN_METERS),
        (PLAYER_170_76, ONE_POINT_SEVEN_METERS),
        (PLAYER_170_72, ONE_POINT_SEVEN_METERS),
        (PLAYER_174_7871, ONE_POINT_SEVENTY_FOUR),
        (PLAYER_160_75, ONE_POINT_SIX_METERS),
        (PLAYER_170_607,ONE_POINT_SEVEN_METERS),
        (PLAYER_224_130, TWO_POINT_TWENTY_FOUR)
    )
    @unpack
    def test_returns_height(self, player, expected_height_in_meters):
        self.assertEqual(expected_height_in_meters, self.height_entity.get_height_in_meters(player))


@ddt
class WeightEntityContractTests(TestCase):

    def setUp(self):
        self.weight_entity = WeightEntity()

    @data(
        (PLAYER_170_57, FIFTY_SEVEN_KILOS),
        (PLAYER_170_75, SEVENTY_FIVE_KILOS),
        (PLAYER_170_76, SEVENTY_SIX_KILOS),
        (PLAYER_170_72, SEVENTY_TWO_KILOS),
        (PLAYER_174_7871, SEVENTY_EIGHT_POINT_SEVENTY_ONE_KILOS),
        (PLAYER_170_131, ONE_HUNDRED_THIRTY_ONE),
        (PLAYER_170_607, SIXTY_POINT_SEVEN_KILOS),
        (PLAYER_224_130, ONE_HUNDRED_THIRTY_KILOS)
    )
    @unpack
    def test_returns_weight(self, player, expected_weight):
        self.assertEqual(expected_weight, self.weight_entity.get_weight(player))


@ddt
class BmiEntityContractTests(TestCase):

    def setUp(self):
        self.height_entity = create_autospec(HeightEntity)
        self.weight_entity = create_autospec(WeightEntity)
        self.bmi_entity = BmiEntity(self.height_entity, self.weight_entity)

    @unpack
    @data(
        (PLAYER_170_57, ONE_POINT_SEVEN_METERS, FIFTY_SEVEN_KILOS, BMI_NINETEEN_POINT_SEVENTY_TWO),
        (PLAYER_170_76, ONE_POINT_SEVEN_METERS, SEVENTY_SIX_KILOS, BMI_TWENTY_SIX_POINT_THREE),
        (PLAYER_170_72, ONE_POINT_SEVEN_METERS, SEVENTY_TWO_KILOS, BMI_TWENTY_FOUR_POINT_NINETY_ONE),
        (PLAYER_174_7871, ONE_POINT_SEVENTY_FOUR, SEVENTY_EIGHT_POINT_SEVENTY_ONE_KILOS, BMI_TWENTY_SIX),
        (PLAYER_170_607, ONE_POINT_SEVEN_METERS, SIXTY_POINT_SEVEN_KILOS, BMI_TWENTY_ONE),
        (PLAYER_224_130, TWO_POINT_TWENTY_FOUR, ONE_HUNDRED_THIRTY_KILOS, BMI_TWENTY_FIVE_POINT_NINETY_ONE)
    )
    def test_returns_bmi(self, player, height, weight, expected_bmi):
        when(self.height_entity.get_height_in_meters).called_with(player).then(height)
        when(self.weight_entity.get_weight).called_with(player).then(weight)

        self.assertEqual(expected_bmi, self.bmi_entity.calculate_bmi(player))

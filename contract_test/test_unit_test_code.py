from unittest.case import TestCase

from mock.mock import create_autospec
from mockextras import when

from .contract_constants import *
from .production_code import *

_multiprocess_can_split_ = True


class WeightUnitTests(TestCase):

    def setUp(self):
        self.weight_entity = WeightEntity()

    def test_returns_weight(self):
        player = {'weight_kg': 80}
        self.assertEqual(80, self.weight_entity.get_weight(player))


class HeightUnitTests(TestCase):

    def setUp(self):
        self.height_entity = HeightEntity()

    def test_returns_height(self):
        player = {'height_cm': 170}
        self.assertEqual(1.70, self.height_entity.get_height_in_meters(player))


class BmiUnitTests(TestCase):

    def setUp(self):
        self.height_entity = create_autospec(HeightEntity)
        self.weight_entity = create_autospec(WeightEntity)
        self.bmi_entity = BmiEntity(self.height_entity, self.weight_entity)

    def test_calculates_bmi(self):
        player = PLAYER_170_75
        when(self.height_entity.get_height_in_meters).called_with(player).then(ONE_POINT_SEVEN_METERS)
        when(self.weight_entity.get_weight).called_with(player).then(SEVENTY_FIVE_KILOS)

        self.assertEqual(25.95, self.bmi_entity.calculate_bmi(player))


class SelectPlayerUnitTests(TestCase):

    def setUp(self):
        self.height_entity = create_autospec(HeightEntity)
        self.weight_entity = create_autospec(WeightEntity)
        self.bmi_entity = create_autospec(BmiEntity)
        self.select_player = SelectPlayerUsecase(self.height_entity, self.weight_entity, self.bmi_entity)

    def test_player_too_short(self):
        player = PLAYER_160_75
        when(self.height_entity.get_height_in_meters).called_with(player).then(ONE_POINT_SIX_METERS)
        self.assertEqual("Player is too short (1.6)", self.select_player.select_player(player))

    def test_player_too_heavy(self):
        player = PLAYER_170_131
        when(self.height_entity.get_height_in_meters).called_with(player).then(ONE_POINT_SEVEN_METERS)
        when(self.weight_entity.get_weight).called_with(player).then(ONE_HUNDRED_THIRTY_ONE)
        when(self.bmi_entity.calculate_bmi).called_with(player).then(BMI_FORTY_FIVE_POINT_THIRTY_THREE)
        self.assertEqual("Player is too heavy (131)", self.select_player.select_player(player))

    def test_player_too_heavy_limit(self):
        player = PLAYER_170_130
        when(self.height_entity.get_height_in_meters).called_with(player).then(TWO_POINT_TWENTY_FOUR)
        when(self.weight_entity.get_weight).called_with(player).then(ONE_HUNDRED_THIRTY_KILOS)
        when(self.bmi_entity.calculate_bmi).called_with(player).then(BMI_TWENTY_FIVE_POINT_NINETY_ONE)
        self.assertEqual("Player was successfully selected", self.select_player.select_player(player))

    def test_low_bmi(self):
        player = PLAYER_170_57
        when(self.height_entity.get_height_in_meters).called_with(player).then(ONE_POINT_SEVEN_METERS)
        when(self.weight_entity.get_weight).called_with(player).then(FIFTY_SEVEN_KILOS)
        when(self.bmi_entity.calculate_bmi).called_with(player).then(BMI_NINETEEN_POINT_SEVENTY_TWO)
        self.assertEqual("Player's BMI is too low (19.72)", self.select_player.select_player(player))

    def test_low_limit_bmi(self):
        player = PLAYER_170_607
        when(self.height_entity.get_height_in_meters).called_with(player).then(ONE_POINT_SEVEN_METERS)
        when(self.weight_entity.get_weight).called_with(player).then(SIXTY_POINT_SEVEN_KILOS)
        when(self.bmi_entity.calculate_bmi).called_with(player).then(BMI_TWENTY_ONE)
        self.assertEqual("Player was successfully selected", self.select_player.select_player(player))

    def test_high_bmi(self):
        player = PLAYER_170_76
        when(self.height_entity.get_height_in_meters).called_with(player).then(ONE_POINT_SEVEN_METERS)
        when(self.weight_entity.get_weight).called_with(player).then(SEVENTY_SIX_KILOS)
        when(self.bmi_entity.calculate_bmi).called_with(player).then(BMI_TWENTY_SIX_POINT_THREE)
        self.assertEqual("Player's BMI is too high (26.3)", self.select_player.select_player(player))

    def test_max_limit_bmi(self):
        player = PLAYER_170_76
        when(self.height_entity.get_height_in_meters).called_with(player).then(ONE_POINT_SEVENTY_FOUR)
        when(self.weight_entity.get_weight).called_with(player).then(SEVENTY_EIGHT_POINT_SEVENTY_ONE_KILOS)
        when(self.bmi_entity.calculate_bmi).called_with(player).then(BMI_TWENTY_SIX)
        self.assertEqual("Player was successfully selected", self.select_player.select_player(player))

    def test_selected_player(self):
        player = PLAYER_170_72
        when(self.height_entity.get_height_in_meters).called_with(player).then(ONE_POINT_SEVEN_METERS)
        when(self.weight_entity.get_weight).called_with(player).then(SEVENTY_TWO_KILOS)
        when(self.bmi_entity.calculate_bmi).called_with(player).then(BMI_TWENTY_FOUR_POINT_NINETY_ONE)
        self.assertEqual("Player was successfully selected", self.select_player.select_player(player))

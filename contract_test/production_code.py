"""
Players must be taller than 1.70m
Players must weigh less than 130 Kg
Players' BMI must be between 21 and 26
"""

class HeightEntity(object):

    def get_height_in_meters(self, player):
        return float(player['height_cm']) / 100


class WeightEntity(object):

    def get_weight(self, player):
        return player['weight_kg']


class BmiEntity(object):

    def __init__(self, height_entity, weight_entity):
        self.height_entity = height_entity
        self.weight_entity = weight_entity


    def calculate_bmi(self, player):
        player_height = self.height_entity.get_height_in_meters(player)
        player_weight = self.weight_entity.get_weight(player)
        return round(player_weight / (player_height ** 2), 2)


class SelectPlayerUsecase(object):

    def __init__(self, height_entity, weight_entity, bmi_entity):
        self.height_entity = height_entity
        self.weight_entity = weight_entity
        self.bmi_entity = bmi_entity

    def select_player(self, player):
        player_height = self.height_entity.get_height_in_meters(player)
        player_weight = self.weight_entity.get_weight(player)
        bmi = self.bmi_entity.calculate_bmi(player)

        if player_height < 1.7:
            message = "Player is too short ({0})".format(str(player_height))
        elif player_weight > 130:
            message = "Player is too heavy ({0})".format(str(player_weight))
        elif bmi < 21:
            message = "Player's BMI is too low ({0})".format(str(bmi))
        elif bmi > 26:
            message = "Player's BMI is too high ({0})".format(str(bmi))
        else:
            message = "Player was successfully selected"

        return message
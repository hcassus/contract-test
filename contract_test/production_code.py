"""
Jogadores devem ter mais de 1.70m
Jogadores devem pesar menos de 130 Kg
Jogadores devem ter um IMC entre 21 e 26
"""

jogador_exemplo = {'nome': 'nome', 'altura_cm': 0, 'peso_kg': 0}


class AlturaEntity(object):

    def obter_altura_em_metro(self, jogador):
        return float(jogador['altura_cm']) / 100


class PesoEntity(object):

    def obter_peso_jogador(self, jogador):
        return jogador['peso_kg']


class ImcEntity(object):

    def __init__(self, altura_entity, peso_entity):
        self.altura_entity = altura_entity
        self.peso_entity = peso_entity


    def calcular_imc(self, jogador):
        altura_jogador = self.altura_entity.obter_altura_em_metro(jogador)
        peso_jogador = self.peso_entity.obter_peso_jogador(jogador)
        return round(peso_jogador / (altura_jogador ** 2), 2)


class SelecaoJogadorUsecase(object):

    def __init__(self, altura_entity, peso_entity, imc_entity):
        self.altura_entity = altura_entity
        self.peso_entity = peso_entity
        self.imc_entity = imc_entity

    def selecionar_jogador(self, jogador):
        altura_jogador = self.altura_entity.obter_altura_em_metro(jogador)
        peso_jogador = self.peso_entity.obter_peso_jogador(jogador)
        imc = self.imc_entity.calcular_imc(jogador)

        if altura_jogador < 1.7:
            mensagem = "Jogador muito baixo (" + str(altura_jogador) + ")"
        elif peso_jogador > 130:
            mensagem = "Jogador muito pesado (" + str(peso_jogador) + ")"
        elif imc < 21:
            mensagem = "Jogador com IMC muito baixo (" + str(imc) + ")"
        elif imc > 26:
            mensagem = "Jogador com IMC muito alto (" + str(imc) + ")"
        else:
            mensagem = "Jogador selecionado"

        return mensagem
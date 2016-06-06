from unittest.case import TestCase

from mock.mock import create_autospec
from mockextras import when

from contract_constants import *
from production_code import PesoEntity, AlturaEntity, ImcEntity, SelecaoJogadorUsecase




class PesoUnitTests(TestCase):

    def setUp(self):
        self.peso_entity = PesoEntity()

    def test_retorna_peso(self):
        self.jogador = {'peso_kg': 80}
        self.assertEqual(80, self.peso_entity.obter_peso_jogador(self.jogador))


class AlturaUnitTests(TestCase):

    def setUp(self):
        self.jogador = {'altura_cm': 170}
        self.altura_entity = AlturaEntity()

    def test_retorna_altura(self):
        self.assertEqual(1.70, self.altura_entity.obter_altura_em_metro(self.jogador))


class ImcUnitTests(TestCase):

    def setUp(self):
        self.altura_entity = create_autospec(AlturaEntity)
        self.peso_entity = create_autospec(PesoEntity)
        self.imc_entity = ImcEntity(self.altura_entity, self.peso_entity)

    def test_calcula_imc(self):
        jogador = JOGADOR_170_75
        when(self.altura_entity.obter_altura_em_metro).called_with(jogador).then(UM_METRO_E_SETENTA)
        when(self.peso_entity.obter_peso_jogador).called_with(jogador).then(SETENTA_E_CINCO_QUILOS)

        self.assertEqual(25.95, self.imc_entity.calcular_imc(jogador))


class SelecionaJogadorUnitTests(TestCase):

    def setUp(self):
        self.altura_entity = create_autospec(AlturaEntity)
        self.peso_entity = create_autospec(PesoEntity)
        self.imc_entity = create_autospec(ImcEntity)
        self.selecionar_jogador = SelecaoJogadorUsecase(self.altura_entity, self.peso_entity, self.imc_entity)

    def test_altura_muito_baixa(self):
        jogador = JOGADOR_160_75
        when(self.altura_entity.obter_altura_em_metro).called_with(jogador).then(UM_METRO_E_SESSENTA)
        self.assertEqual("Jogador muito baixo (1.6)", self.selecionar_jogador.selecionar_jogador(jogador))

    def test_peso_muito_alto(self):
        jogador = JOGADOR_170_140
        when(self.altura_entity.obter_altura_em_metro).called_with(jogador).then(UM_METRO_E_SETENTA)
        when(self.peso_entity.obter_peso_jogador).called_with(jogador).then(CENTO_E_QUARENTA_QUILOS)
        self.assertEqual("Jogador muito pesado (140)", self.selecionar_jogador.selecionar_jogador(jogador))

    def test_imc_muito_baixo(self):
        jogador = JOGADOR_170_57
        when(self.altura_entity.obter_altura_em_metro).called_with(jogador).then(UM_METRO_E_SETENTA)
        when(self.peso_entity.obter_peso_jogador).called_with(jogador).then(CINQUENTA_E_SETE_QUILOS)
        when(self.imc_entity.calcular_imc).called_with(jogador).then(IMC_DEZENOVE_PONTO_SETENTA_E_DOIS)
        self.assertEqual("Jogador com IMC muito baixo (19.72)", self.selecionar_jogador.selecionar_jogador(jogador))

    def test_imc_muito_alto(self):
        jogador = JOGADOR_170_76
        when(self.altura_entity.obter_altura_em_metro).called_with(jogador).then(UM_METRO_E_SETENTA)
        when(self.peso_entity.obter_peso_jogador).called_with(jogador).then(SETENTA_E_SEIS_QUILOS)
        when(self.imc_entity.calcular_imc).called_with(jogador).then(IMC_VINTE_E_SEIS_PONTO_TRES)
        self.assertEqual("Jogador com IMC muito alto (26.3)", self.selecionar_jogador.selecionar_jogador(jogador))

    def test_jogador_selecionado(self):
        jogador = JOGADOR_170_72
        when(self.altura_entity.obter_altura_em_metro).called_with(jogador).then(UM_METRO_E_SETENTA)
        when(self.peso_entity.obter_peso_jogador).called_with(jogador).then(SETENTA_E_DOIS_QUILOS)
        when(self.imc_entity.calcular_imc).called_with(jogador).then(IMC_VINTE_E_QUATRO_PONTO_NOVENTA_E_UM)
        self.assertEqual("Jogador selecionado", self.selecionar_jogador.selecionar_jogador(jogador))

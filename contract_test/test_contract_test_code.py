from unittest.case import TestCase

from ddt import ddt, unpack, data
from mock.mock import create_autospec
from mockextras import when

from contract_constants import *
from production_code import AlturaEntity, PesoEntity, ImcEntity




@ddt
class AlturaEntityContractTests(TestCase):

    def setUp(self):
        self.altura_entity = AlturaEntity()

    @data(
        (JOGADOR_170_75, UM_METRO_E_SETENTA),
        (JOGADOR_170_57, UM_METRO_E_SETENTA),
        (JOGADOR_170_76, UM_METRO_E_SETENTA),
        (JOGADOR_170_72, UM_METRO_E_SETENTA),
        (JOGADOR_160_75, UM_METRO_E_SESSENTA)
    )
    @unpack
    def test_retorna_altura(self, jogador, altura_esperada_metros):
        self.assertEqual(altura_esperada_metros, self.altura_entity.obter_altura_em_metro(jogador))


@ddt
class PesoEntityContractTests(TestCase):

    def setUp(self):
        self.peso_entity = PesoEntity()

    @data(
        (JOGADOR_170_57, CINQUENTA_E_SETE_QUILOS),
        (JOGADOR_170_75, SETENTA_E_CINCO_QUILOS),
        (JOGADOR_170_76, SETENTA_E_SEIS_QUILOS),
        (JOGADOR_170_72, SETENTA_E_DOIS_QUILOS),
        (JOGADOR_170_140, CENTO_E_QUARENTA_QUILOS)
    )
    @unpack
    def test_retorna_peso(self, jogador, peso_retornado):
        self.assertEqual(peso_retornado, self.peso_entity.obter_peso_jogador(jogador))


@ddt
class ImcEntityContractTests(TestCase):

    def setUp(self):
        self.altura_entity = create_autospec(AlturaEntity)
        self.peso_entity = create_autospec(PesoEntity)
        self.imc_entity = ImcEntity(self.altura_entity, self.peso_entity)

    @unpack
    @data(
        (JOGADOR_170_57, UM_METRO_E_SETENTA, CINQUENTA_E_SETE_QUILOS, IMC_DEZENOVE_PONTO_SETENTA_E_DOIS),
        (JOGADOR_170_76, UM_METRO_E_SETENTA, SETENTA_E_SEIS_QUILOS, IMC_VINTE_E_SEIS_PONTO_TRES),
        (JOGADOR_170_72, UM_METRO_E_SETENTA, SETENTA_E_DOIS_QUILOS, IMC_VINTE_E_QUATRO_PONTO_NOVENTA_E_UM)
    )
    def test_retorna_imc(self, jogador, altura, peso, imc_esperado):
        when(self.altura_entity.obter_altura_em_metro).called_with(jogador).then(altura)
        when(self.peso_entity.obter_peso_jogador).called_with(jogador).then(peso)

        self.assertEqual(imc_esperado, self.imc_entity.calcular_imc(jogador))

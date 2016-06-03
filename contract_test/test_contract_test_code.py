from unittest.case import TestCase

from ddt import ddt, unpack, data
from mock.mock import create_autospec
from mockextras import when

from contract_constants import *
from production_code import AlturaEntity, PesoEntity, ImcEntity


@ddt
class AlturaEntityContractTests(TestCase):

    def setUp(self):
        self.jogador = {'altura_cm': 0}
        self.altura_entity = AlturaEntity()

    @data(
        (170, UM_METRO_E_SETENTA),
        (160, UM_METRO_E_SESSENTA)
    )
    @unpack
    def test_retorna_altura(self, altura_cm, altura_esperada_metros):
        self.jogador['altura_cm'] = altura_cm
        self.assertEqual(altura_esperada_metros, self.altura_entity.obter_altura_em_metro(self.jogador))


@ddt
class PesoEntityContractTests(TestCase):

    def setUp(self):
        self.jogador = {'peso_kg': 0}
        self.peso_entity = PesoEntity()

    @data(
        (57, CINQUENTA_E_SETE_QUILOS),
        (75, SETENTA_E_CINCO_QUILOS),
        (140, CENTO_E_QUARENTA_QUILOS)
    )
    @unpack
    def test_retorna_peso(self, peso_jogador, peso_retornado):
        self.jogador['peso_kg'] = peso_jogador
        self.assertEqual(peso_retornado, self.peso_entity.obter_peso_jogador(self.jogador))


@ddt
class ImcEntityContractTests(TestCase):

    def setUp(self):
        self.jogador = {}
        self.altura_entity = create_autospec(AlturaEntity)
        self.peso_entity = create_autospec(PesoEntity)
        self.imc_entity = ImcEntity(self.altura_entity, self.peso_entity)

    @unpack
    @data(
        (UM_METRO_E_SETENTA, CINQUENTA_E_SETE_QUILOS, IMC_DEZENOVE_PONTO_SETENTA_E_DOIS),
        (UM_METRO_E_SETENTA, SETENTA_E_SEIS_QUILOS, IMC_VINTE_E_SEIS_PONTO_TRES),
        (UM_METRO_E_SETENTA, SETENTA_E_DOIS_QUILOS, IMC_VINTE_E_QUATRO_PONTO_NOVENTA_E_UM)
    )
    def test_retorna_imc(self, altura, peso, imc_esperado):
        when(self.altura_entity.obter_altura_em_metro).called_with(self.jogador).then(altura)
        when(self.peso_entity.obter_peso_jogador).called_with(self.jogador).then(peso)

        self.assertEqual(imc_esperado, self.imc_entity.calcular_imc(self.jogador))

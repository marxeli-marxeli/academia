from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from .models import Modalidade, Turma


class ModalidadeTests(TestCase):
    def test_nome_deve_ser_unico(self):
        Modalidade.objects.create(nome="Pilates", descricao="Aulas de pilates")

        with self.assertRaises(IntegrityError):
            Modalidade.objects.create(nome="Pilates", descricao="Outra descrição")

    def test_nao_pode_excluir_modalidade_com_turmas(self):
        modalidade = Modalidade.objects.create(
            nome="Pilates",
            descricao="Aulas de pilates",
        )
        Turma.objects.create(
            modalidade=modalidade,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="07:30",
            instrutor="Ana",
            vagas=10,
        )

        with self.assertRaises(ProtectedError):
            modalidade.delete()


class TurmaTests(TestCase):
    def setUp(self):
        self.modalidade = Modalidade.objects.create(
            nome="Natação",
            descricao="Aulas de natação",
        )

    def test_rejeita_dia_da_semana_fora_da_lista(self):
        with self.assertRaises(IntegrityError):
            Turma.objects.create(
                modalidade=self.modalidade,
                dia_semana=7,
                horario="07:30",
                instrutor="Ana",
                vagas=10,
            )

    def test_vagas_nao_podem_ser_negativas(self):
        with self.assertRaises(IntegrityError):
            Turma.objects.create(
                modalidade=self.modalidade,
                dia_semana=Turma.DiaSemana.SEGUNDA,
                horario="07:30",
                instrutor="Ana",
                vagas=-1,
            )

    def test_turmas_sao_ordenadas_por_dia_e_horario(self):
        turma_mais_tarde = Turma.objects.create(
            modalidade=self.modalidade,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="18:00",
            instrutor="Ana",
            vagas=10,
        )
        turma_mais_cedo = Turma.objects.create(
            modalidade=self.modalidade,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="07:30",
            instrutor="Bruno",
            vagas=10,
        )

        self.assertEqual(
            list(Turma.objects.all()),
            [turma_mais_cedo, turma_mais_tarde],
        )

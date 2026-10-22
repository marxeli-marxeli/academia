from django.db import models
from django.db.models import Q


class Modalidade(models.Model):
    nome = models.CharField("nome", max_length=100, unique=True)
    descricao = models.TextField("descrição")
    ativa = models.BooleanField("ativa", default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "modalidade"
        verbose_name_plural = "modalidades"

    def __str__(self):
        return self.nome


class Turma(models.Model):
    class DiaSemana(models.IntegerChoices):
        SEGUNDA = 1, "Segunda-feira"
        TERCA = 2, "Terça-feira"
        QUARTA = 3, "Quarta-feira"
        QUINTA = 4, "Quinta-feira"
        SEXTA = 5, "Sexta-feira"
        SABADO = 6, "Sábado"

    modalidade = models.ForeignKey(
        Modalidade,
        on_delete=models.PROTECT,
        related_name="turmas",
        verbose_name="modalidade",
    )
    dia_semana = models.PositiveSmallIntegerField(
        "dia da semana",
        choices=DiaSemana.choices,
    )
    horario = models.TimeField("horário")
    instrutor = models.CharField("instrutor", max_length=120)
    vagas = models.PositiveIntegerField("vagas")

    class Meta:
        ordering = ["dia_semana", "horario"]
        verbose_name = "turma"
        verbose_name_plural = "turmas"
        constraints = [
            models.CheckConstraint(
                condition=Q(dia_semana__range=(1, 6)),
                name="turma_dia_semana_valido",
            ),
            models.CheckConstraint(
                condition=Q(vagas__gte=0),
                name="turma_vagas_nao_negativas",
            ),
        ]

    def __str__(self):
        return f"{self.modalidade} - {self.get_dia_semana_display()} {self.horario:%H:%M}"

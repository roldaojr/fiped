from django.shortcuts import render
from .models import Horario


def programacao(request):
    horarios = Horario.objects.exclude(atividade__tipo='Minicurso')\
                      .order_by('data', 'hora_inicial', 'hora_final')
    return render(request, 'eventos/programacao.html', {'horarios': horarios})

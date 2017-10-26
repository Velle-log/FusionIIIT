# from django.shortcuts import render

from django.shortcuts import render


def homepage(request):
    context = {}

    return render(request, "ais/ais.html", context)


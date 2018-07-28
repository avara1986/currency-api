from django.shortcuts import render


def graphs(request):
    return render(request, 'backoffice/index.html', {})

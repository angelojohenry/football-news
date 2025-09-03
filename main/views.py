from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2406428825',
        'name': 'Angelo Johenry Apituley',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)

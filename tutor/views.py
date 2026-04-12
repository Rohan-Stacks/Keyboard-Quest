from django.shortcuts import render
from django.http import Http404

def home(request):
    return render(request, "tutor/home.html")


def level_select(request):
    completed_levels = 0  # temporary placeholder until the game tracks progress

    levels = []
    for number in range(1, 11):
        if number <= completed_levels:
            status = "completed"
        elif number == completed_levels + 1:
            status = "current"
        else:
            status = "locked"

        levels.append({
            "number": number,
            "status": status,
        })

    return render(request, "tutor/levels.html", {"levels": levels})


def level_placeholder(request, level):
    if 1 <= level <= 10:
        return render(request, "tutor/level_placeholder.html", {"level": level})
    raise Http404("Level does not exist")
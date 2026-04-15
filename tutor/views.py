from django.shortcuts import render
from django.http import Http404

# I kept the home page simple while I build the game pages underneath it.
def home(request):
    return render(request, "tutor/home.html")

def about(request):
    return render(request, "tutor/about.html")

def level_select(request):
    completed_levels = 0  # I am leaving progress at zero for now because the game is not finished yet.

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

def level_page(request, level):
    if 1 <= level <= 10:
        # This is the reusable page for every level.
        return render(request, "tutor/level_page.html", {"level": level})
    raise Http404("Level does not exist")
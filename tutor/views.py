from django.shortcuts import render
from django.http import Http404

def home(request):
    return render(request, "tutor/home.html")

def about(request):
    return render(request, "tutor/about.html")

def level_select(request):
    completed_levels = 0

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
        return render(request, f"tutor/levels/level{level}.html", {"level": level})
    else:
        raise Http404

def level_complete(request, level):
    if 1 <= level <= 10:
        return render(request, "tutor/level_complete.html", {"level": level})
    else:
        raise Http404
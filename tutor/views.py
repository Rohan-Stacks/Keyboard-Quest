from django.shortcuts import render

def home(request):
    return render(request, "tutor/home.html")

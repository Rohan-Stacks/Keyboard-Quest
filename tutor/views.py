from functools import wraps

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from . import vocabulary

ADMIN_PASSWORD = "Admin123"
ADMIN_SESSION_KEY = "keyboard_quest_admin"


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get(ADMIN_SESSION_KEY):
            return redirect("admin_login")
        return view_func(request, *args, **kwargs)

    return wrapper


def home(request):
    return render(request, "tutor/home.html")


def about(request):
    return render(request, "tutor/about.html")


def settings(request):
    return render(request, "tutor/settings.html")


def admin_login(request):
    if request.session.get(ADMIN_SESSION_KEY):
        return redirect("admin_vocab")

    error = None

    if request.method == "POST":
        password = request.POST.get("password", "")

        if password == ADMIN_PASSWORD:
            request.session[ADMIN_SESSION_KEY] = True
            return redirect("admin_vocab")

        error = "Wrong password. Try again."

    return render(request, "tutor/admin_login.html", {"error": error})


def admin_logout(request):
    request.session.pop(ADMIN_SESSION_KEY, None)
    return redirect("home")


@admin_required
def admin_vocab(request):
    topics = vocabulary.TOPICS

    if request.method == "POST":
        saved_count = 0
        all_errors = []

        for topic in topics:
            field_name = f"vocab_{topic['slug']}"
            raw_text = request.POST.get(field_name, "")
            words = vocabulary.parse_word_input(raw_text)

            if not words:
                continue

            ok, errors = vocabulary.save_vocabulary(topic["slug"], words)
            if ok:
                saved_count += 1
            else:
                for err in errors:
                    all_errors.append(f"{topic['name']}: {err}")

        if all_errors:
            for err in all_errors:
                messages.error(request, err)

        if saved_count > 0:
            messages.success(request, "Saved.")

        if saved_count == 0 and not all_errors:
            messages.warning(request, "Nothing to save.")

    topic_rows = []
    for topic in topics:
        words = vocabulary.load_vocabulary(topic["slug"])
        topic_rows.append(
            {
                "slug": topic["slug"],
                "name": topic["name"],
                "words_text": vocabulary.words_to_textarea(words),
            }
        )

    return render(
        request,
        "tutor/admin_vocab.html",
        {
            "topic_rows": topic_rows,
            "max_words": vocabulary.MAX_WORDS_PER_TOPIC,
        },
    )


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

        levels.append(
            {
                "number": number,
                "status": status,
            }
        )

    return render(request, "tutor/levels.html", {"levels": levels})


def level_page(request, level):
    if 1 <= level <= 10:
        prompt_text = vocabulary.get_level_prompt(level)
        return render(
            request,
            f"tutor/levels/level{level}.html",
            {
                "level": level,
                "prompt_text": prompt_text,
            },
        )
    else:
        raise Http404


def level_complete(request, level):
    if 1 <= level <= 10:
        return render(request, "tutor/level_complete.html", {"level": level})
    else:
        raise Http404

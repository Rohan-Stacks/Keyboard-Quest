import json
import re
from pathlib import Path

from django.conf import settings

# I keep topic names here so the admin page and game can use the same list.
MAX_WORDS_PER_TOPIC = 10

TOPICS = [
    {"slug": "programming_fundamentals", "name": "Programming Fundamentals"},
    {"slug": "object_oriented_programming", "name": "Object-Oriented Programming"},
    {"slug": "programming_mechatronics", "name": "Programming Mechatronics"},
    {"slug": "secure_software_architecture", "name": "Secure Software Architecture"},
    {"slug": "programming_for_the_web", "name": "Programming for the Web"},
    {"slug": "software_automation", "name": "Software Automation"},
]

# Level 2 uses combined vocabulary topics. Level 3 uses combined vocabulary topics. Level 4-10 use NESA exemplars.
LEVEL_VOCAB_2 = [
    "programming_fundamentals",
    "object_oriented_programming",
    "programming_mechatronics",
]

LEVEL_VOCAB_3 = [
    "secure_software_architecture",
    "programming_for_the_web",
    "software_automation",
]

LEVEL_NESA_TERMS = {
    4: "Identify",
    5: "Define",
    6: "Describe",
    7: "Explain",
    8: "Analyse",
    9: "Justify",
    10: "Evaluate",
}

NESA_KEY_TERMS = [
    "Identify",
    "Define",
    "Describe",
    "Explain",
    "Analyse",
    "Justify",
    "Evaluate",
]

# I only allow plain characters so bad input can't break the json files.
VALID_WORD = re.compile(r"^[A-Za-z0-9_\-./() ]+$")

# Home row drills and half key combos for level 1.
HOME_ROW_CHUNK = (
    "asdf jkl; asdf jkl; fjdk slaf asdf jkl; asdf jkl; fjdk slaf a s d f j k l ; aa ss dd ff jj kk ll ;; fd jk sk dl af jf kd ls fa jk da sf kl ja fd ks lj af ds jk fr de sw ed rf tg yh uj ik ol as df jk la sa df jk ll ff jj kk dd ss aa "
)


def vocab_dir():
    folder = Path(settings.BASE_DIR) / "data" / "vocabulary"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def nesa_file_path():
    return Path(settings.BASE_DIR) / "data" / "nesa" / "nesa_exemplars.json"


def file_path(slug):
    return vocab_dir() / f"{slug}.json"


def load_nesa_data():
    path = nesa_file_path()
    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(data, dict):
        return {}

    return data


def load_nesa_exemplar(term):
    data = load_nesa_data()
    entry = data.get(term)

    if isinstance(entry, str):
        return entry.strip()

    if isinstance(entry, dict):
        return str(entry.get("exemplar", "")).strip()

    return ""


def load_nesa_definition(term):
    data = load_nesa_data()
    entry = data.get(term)

    if isinstance(entry, dict):
        return str(entry.get("definition", "")).strip()

    return ""


def parse_word_input(text):
    words = []
    for line in text.splitlines():
        word = line.strip()
        if word:
            words.append(word)
    return words[:MAX_WORDS_PER_TOPIC]


def validate_words(words):
    errors = []
    clean = []
    seen = set()

    for word in words:
        if len(word) > 60:
            errors.append(f"'{word}' is too long.")
            continue
        if not VALID_WORD.match(word):
            errors.append(f"'{word}' has invalid characters.")
            continue
        key = word.lower()
        if key in seen:
            continue
        seen.add(key)
        clean.append(word)

    if len(clean) > MAX_WORDS_PER_TOPIC:
        errors.append(f"Only {MAX_WORDS_PER_TOPIC} words allowed per topic.")

    return clean, errors


def load_vocabulary(slug):
    path = file_path(slug)
    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return [str(item).strip() for item in data if str(item).strip()][:MAX_WORDS_PER_TOPIC]


def save_vocabulary(slug, words):
    clean, errors = validate_words(words)
    if errors:
        return False, errors

    path = file_path(slug)
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(clean, handle, indent=2)
    except OSError as exc:
        return False, [str(exc)]

    return True, []


def words_to_textarea(words):
    return "\n".join(words)


def get_level_prompt(level, fallback="Type the words below."):
    if level == 1:
        return HOME_ROW_CHUNK

    nesa_term = LEVEL_NESA_TERMS.get(level)
    if nesa_term:
        exemplar = load_nesa_exemplar(nesa_term)
        if exemplar:
            return exemplar
        return (
            f"NESA key term: {nesa_term}. "
            f"The exemplar paragraph for this term will added after finding data file"
        )

    if level == 2:
        all_words = []
        for slug in LEVEL_VOCAB_2:
            words = load_vocabulary(slug)
            all_words.extend(words)
        if not all_words:
            return fallback
        return " ".join(all_words) + "."

    if level == 3:
        all_words = []
        for slug in LEVEL_VOCAB_3:
            words = load_vocabulary(slug)
            all_words.extend(words)
        if not all_words:
            return fallback
        return " ".join(all_words) + "."

    return fallback

// I put all my pass requirements here so I only change them in one spot.
var DIFFICULTY_RULES = {
    easy: { accuracy: 80, wpm: 20 },
    medium: { accuracy: 90, wpm: 40 },
    hard: { accuracy: 95, wpm: 65 }
};

function getDifficulty() {
    var saved = localStorage.getItem("difficulty");
    if (saved === "easy" || saved === "medium" || saved === "hard") {
        return saved;
    }
    return "medium";
}

function setDifficulty(mode) {
    localStorage.setItem("difficulty", mode);
}

function getPassRules() {
    return DIFFICULTY_RULES[getDifficulty()];
}

function didPass(accuracy, wpm) {
    var rules = getPassRules();
    return accuracy >= rules.accuracy && wpm >= rules.wpm;
}

function getPassedStorageKey() {
    return "levels_passed_" + getDifficulty();
}

function getPassedLevels() {
    migrateOldProgress();
    var raw = localStorage.getItem(getPassedStorageKey());
    if (!raw) return [];
    try {
        return JSON.parse(raw);
    } catch (e) {
        return [];
    }
}

function savePassedLevel(levelNum) {
    var beaten = getPassedLevels();
    if (beaten.indexOf(levelNum) === -1) {
        beaten.push(levelNum);
        localStorage.setItem(getPassedStorageKey(), JSON.stringify(beaten));
    }
}

function getResultKey(levelNum) {
    return "level_result_" + getDifficulty() + "_" + levelNum;
}

function nextOpenLevel() {
    var passed = getPassedLevels();
    if (passed.length === 0) return 1;
    return Math.max.apply(null, passed) + 1;
}

function formatPassRules() {
    var rules = getPassRules();
    return rules.accuracy + "% accuracy and " + rules.wpm + " WPM";
}

function formatAllPassRulesHtml() {
    var modes = ["easy", "medium", "hard"];
    var labels = { easy: "Easy", medium: "Medium", hard: "Hard" };
    var current = getDifficulty();
    var parts = [];

    for (var i = 0; i < modes.length; i++) {
        var mode = modes[i];
        var rules = DIFFICULTY_RULES[mode];
        var cls = mode === current ? "difficulty-summary active" : "difficulty-summary";

        parts.push(
            '<span class="' + cls + '">' +
            labels[mode] + ": " + rules.accuracy + "% accuracy and " + rules.wpm + " WPM" +
            "</span>"
        );
    }

    return parts.join("");
}

// I move old progress into medium once so I don't lose anything from before difficulties existed.
function migrateOldProgress() {
    var oldRaw = localStorage.getItem("levels_passed");
    if (!oldRaw) return;

    if (!localStorage.getItem("levels_passed_medium")) {
        localStorage.setItem("levels_passed_medium", oldRaw);
    }

    localStorage.removeItem("levels_passed");
}

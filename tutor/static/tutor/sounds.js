//here are the sounds for the button clicks and the level finish

var clickSound = null;
var finishSound = null;
var soundsReady = false;

var SFX_KEY = "sfx_on";

function sfxOn() {
    try {
        return localStorage.getItem(SFX_KEY) !== "false";
    } catch (e) {
        return true;
    }
}

function applySfxSetting() {
    var on = sfxOn();

    if (clickSound) {
        clickSound.muted = !on;
    }
    if (finishSound) {
        finishSound.muted = !on;
    }
}

function setSfxOn(on) {
    try {
        localStorage.setItem(SFX_KEY, on ? "true" : "false");
    } catch (e) {
        return;
    }

    applySfxSetting();
}

function initSounds(clickPath, finishPath) {
    if (soundsReady) {
        applySfxSetting();
        return;
    }

    clickSound = new Audio(clickPath);
    finishSound = new Audio(finishPath);
    clickSound.volume = 0.45;
    finishSound.volume = 0.55;
    soundsReady = true;

    applySfxSetting();

    // I use mousedown so the sound still plays before a link changes the page.
    document.addEventListener("mousedown", function (e) {
        if (e.target.closest(".toggle, #sfx-toggle")) {
            return;
        }

        var target = e.target.closest("a, button");
        if (!target || target.disabled) {
            return;
        }

        playClick();
    });
}

function playClick() {
    applySfxSetting();
    if (!clickSound || !sfxOn()) {
        return;
    }

    clickSound.currentTime = 0;
    clickSound.play();
}

function playFinish() {
    applySfxSetting();
    if (!finishSound || !sfxOn()) {
        return;
    }

    finishSound.currentTime = 0;
    finishSound.play();
}

inlets = 1;
outlets = 1;

var dictModes = new Dict("modes");

function romanToDegree(symbol) {
    const clean = symbol.replace("°", "").replace("♭", "").toLowerCase();
    const map = {
        i: 1, ii: 2, iii: 3, iv: 4, v: 5, vi: 6, vii: 7
    };
    const accidental = symbol.indexOf("♭") !== -1 ? -1 : 0;
    return (map[clean] || 1) + accidental;
}

function isUppercase(s) {
    return s === s.toUpperCase();
}

function hasDiminished(s) {
    return s.indexOf("°") !== -1 ? -1 : 0;
}

function flatten(arr) {
    var result = [];
    for (var i = 0; i < arr.length; i++) {
        var sub = arr[i];
        for (var j = 0; j < sub.length; j++) {
            result.push(sub[j]);
        }
    }
    return result;
}

function chords() {
    var args = arrayfromargs(messagename, arguments);
    if (args.length < 4) {
        post("Usage: mode root chord ...\n");
        return;
    }

    var symbol = args[1] + "";
    var rootMidi = parseInt(args[2]);
    var modeName = args[3];

    var scale = dictModes.get(modeName);
    if (!scale || scale.length !== 7) {
        post("Mode not found or invalid: " + modeName + "\n");
        return;
    }

    var degree = romanToDegree(symbol);
    var index = ((degree - 1) % 7 + 7) % 7;

    var rootOffset = scale[index];
    var rootNote = rootMidi + rootOffset;

    var third, fifth;

    if (hasDiminished(symbol)) {
        third = 3;
        fifth = 6;
    } else if (isUppercase(symbol)) {
        third = 4;
        fifth = 7;
    } else {
        third = 3;
        fifth = 7;
    }

    outlet(0, [rootNote, rootNote + third, rootNote + fifth]);
}
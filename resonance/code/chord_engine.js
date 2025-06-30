const path = require("path");
const fs = require("fs");
const Max = require("max-api");

const modesPath = path.join(__dirname, "../data/modes.json");
const chordsPath = path.join(__dirname, "../data/modal_chords.json");

const MODE = "Ionian";
const ROOT_NOTE = 60;

let modes = {};
let modalChords = {};

try {
    modes = JSON.parse(fs.readFileSync(modesPath));
    modalChords = JSON.parse(fs.readFileSync(chordsPath));
    console.log(`modes ${JSON.stringify(modes)}`)
    Max.post("Loaded modes and modal chords from data folder.");
} catch (e) {
    Max.post("Error loading JSON files: " + e);
}

function romanToDegree(symbol) {
    const map = {
        "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7,
        "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
        "♭II": 2, "♭III": 3, "♭V": 5, "♭VI": 6, "♭VII": 7,
        "ii°": 2, "i°": 1
    };
    return map[symbol] || 1;
}

function generateChord(rootMidi, degree, mode) {
    const scale = modes[mode];
    console.log(`scale ${scale}`)
    if (!scale) return [];
    const deg = (degree - 1) % 7;
    const root = rootMidi + scale[deg];
    const third = rootMidi + scale[(deg + 2) % 7];
    const fifth = rootMidi + scale[(deg + 4) % 7];
    return [root, third, fifth];
}

function circleMapForChord(chord) {
    const circleMap = {
        "I": ["IV", "V", "vi"],
        "ii": ["V", "IV"],
        "iii": ["vi", "IV"],
        "IV": ["I", "ii"],
        "V": ["I", "vi"],
        "vi": ["ii", "IV"],
        "vii°": ["I"],
        "i": ["iv", "v", "♭VII"],
        "iv": ["i", "♭VII", "♭VI"],
        "v": ["i", "♭VI"],
        "♭VII": ["i", "iv"],
        "♭II": ["i", "v"],
        "ii°": ["v"],
        "i°": ["♭III"]
    };
    return circleMap[chord] || [];
}

function nextChord(mode, currentChord, valence, arousal, dominance) {
    console.log(`mode ${mode}`)
    const pool = modalChords[mode] || [];
    const movement = circleMapForChord(currentChord);

    let candidates = movement.filter(ch => pool.includes(ch));
    console.log(`candidates ${candidates}`)

    if (valence < 0.4) {
        candidates = candidates.filter(ch => ch.toLowerCase() === ch || ch.indexOf("°") !== -1);
    } else if (valence > 0.6) {
        candidates = candidates.filter(ch => ch.toUpperCase() === ch && ch.indexOf("°") === -1);
    }

    if (candidates.length === 0) candidates = pool.slice();

    console.log(`candidates filtered ${candidates}`)

    const index = Math.floor(Math.random() * Math.max(1, candidates.length * (0.5 + arousal)));
    return candidates[index % candidates.length];
}

Max.addHandler("nextChord", (mode, root, current, val, aro, dom) => {
    const next = nextChord(mode, current, val, aro, dom);
    console.log(`next chord ${next}`)
    console.log(`root ${root}`)
    const midi = generateChord(root, romanToDegree(next), mode);
    console.log(`midi ${midi}`)
    Max.outlet(midi);
});

Max.addHandler("getMode", () => {
    Max.outlet(MODE);
})
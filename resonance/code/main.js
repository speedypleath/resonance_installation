"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// src/main.ts
var import_max_api = __toESM(require("max-api"));
var import_path = __toESM(require("path"));
var import_fs = __toESM(require("fs"));
var loadJson = (file) => JSON.parse(import_fs.default.readFileSync(file, "utf-8"));
var modesPath = import_path.default.join(__dirname, "../data/modes.json");
var chordsPath = import_path.default.join(__dirname, "../data/modal_chords.json");
var modes = loadJson(modesPath);
var modalChords = loadJson(chordsPath);
import_max_api.default.post("Loaded modes and modal chords from JSON.");
var state = {
  mode: "Ionian",
  root: 60,
  valence: 0.5,
  arousal: 0.5,
  dominance: 0.5,
  set(key, value) {
    if (key in this) {
      this[key] = value;
      console.log(`state.${key} set to`, value);
    } else {
      console.warn(`Invalid key: ${key}`);
    }
  }
};
var romanToDegree = (symbol) => {
  const map = {
    i: 1,
    ii: 2,
    iii: 3,
    iv: 4,
    v: 5,
    vi: 6,
    vii: 7,
    I: 1,
    II: 2,
    III: 3,
    IV: 4,
    V: 5,
    VI: 6,
    VII: 7,
    "\u266DII": 2,
    "\u266DIII": 3,
    "\u266DV": 5,
    "\u266DVI": 6,
    "\u266DVII": 7,
    "ii\xB0": 2,
    "i\xB0": 1
  };
  return map[symbol] || 1;
};
var generateChord = (rootMidi, degree, mode) => {
  const scale = modes[mode];
  if (!scale) return [];
  const deg = (degree - 1) % 7;
  return [
    rootMidi + scale[deg],
    rootMidi + scale[(deg + 2) % 7],
    rootMidi + scale[(deg + 4) % 7]
  ];
};
var circleMapForChord = (chord) => {
  const map = {
    I: ["IV", "V", "vi"],
    ii: ["V", "IV"],
    iii: ["vi", "IV"],
    IV: ["I", "ii"],
    V: ["I", "vi"],
    vi: ["ii", "IV"],
    "vii\xB0": ["I"],
    i: ["iv", "v", "\u266DVII"],
    iv: ["i", "\u266DVII", "\u266DVI"],
    v: ["i", "\u266DVI"],
    "\u266DVII": ["i", "iv"],
    "\u266DII": ["i", "v"],
    "ii\xB0": ["v"],
    "i\xB0": ["\u266DIII"]
  };
  return map[chord] || [];
};
var makeNextChord = () => {
  console.log(`Mode: ${state.mode}`);
  let currentChord = modalChords[state.mode]?.[0] || "I";
  return () => {
    const pool = modalChords[state.mode] || [];
    let candidates = circleMapForChord(currentChord).filter(
      (ch) => pool.includes(ch)
    );
    if (state.valence < 0.4) {
      candidates = candidates.filter(
        (ch) => ch.toLowerCase() === ch || ch.includes("\xB0")
      );
    } else if (state.valence > 0.6) {
      candidates = candidates.filter(
        (ch) => ch.toUpperCase() === ch && !ch.includes("\xB0")
      );
    }
    if (candidates.length === 0) candidates = pool.slice();
    const index = Math.floor(
      Math.random() * Math.max(1, candidates.length * (0.5 + state.arousal))
    );
    currentChord = candidates[index % candidates.length];
    const midi = generateChord(
      state.root,
      romanToDegree(currentChord),
      state.mode
    );
    return { chord: currentChord, midi };
  };
};
var nextChord = makeNextChord();
import_max_api.default.addHandler("nextChord", () => {
  const { chord, midi } = nextChord();
  import_max_api.default.outlet([chord, ...midi]);
});
import_max_api.default.addHandler("getMode", () => {
  return state.mode;
});
import_max_api.default.addHandler("setMode", (mode) => {
  state.set("mode", mode);
});

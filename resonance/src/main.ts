import MaxAPI from "max-api";
import path from "path";
import fs from "fs";

// Type declarations
interface ModeMap {
  [key: string]: number[];
}
interface ChordMap {
  [key: string]: string[];
}

// Load external data
const loadJson = (file: string): any =>
  JSON.parse(fs.readFileSync(file, "utf-8"));

const modesPath = path.join(__dirname, "../data/modes.json");
const chordsPath = path.join(__dirname, "../data/modal_chords.json");

const modes: ModeMap = loadJson(modesPath);
const modalChords: ChordMap = loadJson(chordsPath);

MaxAPI.post("Loaded modes and modal chords from JSON.");

interface State {
  mode: string;
  root: number;
  valence: number;
  arousal: number;
  dominance: number;
  set: (key: keyof Omit<State, 'set'>, value: any) => void;
}

const state: State = {
  mode: "Ionian",
  root: 60,
  valence: 0.5,
  arousal: 0.5,
  dominance: 0.5,
  set(key, value) {
    if (key in this) {
      (this as any)[key] = value;
      console.log(`${key} set to`, value);
    } else {
      console.warn(`Invalid key: ${key}`);
    }
  }
};

const romanToDegree = (symbol: string): number => {
  const map: Record<string, number> = {
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
    "♭II": 2,
    "♭III": 3,
    "♭V": 5,
    "♭VI": 6,
    "♭VII": 7,
    "ii°": 2,
    "i°": 1,
  };
  return map[symbol] || 1;
};

// Generate a triad from mode and degree
const generateChord = (
  rootMidi: number,
  degree: number,
  mode: string
): number[] => {
  const scale = modes[mode];
  if (!scale) return [];
  const deg = (degree - 1) % 7;
  return [
    rootMidi + scale[deg],
    rootMidi + scale[(deg + 2) % 7],
    rootMidi + scale[(deg + 4) % 7],
  ];
};

// Movement map
const circleMapForChord = (chord: string): string[] => {
  const map: Record<string, string[]> = {
    I: ["IV", "V", "vi"],
    ii: ["V", "IV"],
    iii: ["vi", "IV"],
    IV: ["I", "ii"],
    V: ["I", "vi"],
    vi: ["ii", "IV"],
    "vii°": ["I"],
    i: ["iv", "v", "♭VII"],
    iv: ["i", "♭VII", "♭VI"],
    v: ["i", "♭VI"],
    "♭VII": ["i", "iv"],
    "♭II": ["i", "v"],
    "ii°": ["v"],
    "i°": ["♭III"],
  };
  return map[chord] || [];
};

const makeNextChord = () => {
    console.log(`Mode: ${state.mode}`)
  let currentChord = modalChords[state.mode]?.[0] || "I"; // start on tonic

  return (): { chord: string; midi: number[] } => {
    const pool = modalChords[state.mode] || [];
    let candidates = circleMapForChord(currentChord).filter((ch) =>
      pool.includes(ch)
    );

    if (state.valence < 0.4) {
      candidates = candidates.filter(
        (ch) => ch.toLowerCase() === ch || ch.includes("°")
      );
    } else if (state.valence > 0.6) {
      candidates = candidates.filter(
        (ch) => ch.toUpperCase() === ch && !ch.includes("°")
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

const nextChord = makeNextChord();

// Max message handler
MaxAPI.addHandler("nextChord", () => {
  const { chord, midi } = nextChord();
  MaxAPI.outlet([chord, ...midi]);
});

MaxAPI.addHandler("getMode", () => {
  return state.mode;
});

MaxAPI.addHandler("setMode", (mode: string) => {
  state.set('mode', mode);
});

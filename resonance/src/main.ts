import MaxAPI from "max-api";
import { Note, Midi, Scale, Chord } from "tonal";

interface State {
  mode: string;
  root: number;
  valence: number;
  arousal: number;
  dominance: number;
  set: (key: keyof Omit<State, "set">, value: any) => void;
}

type ModeConfig = {
  tonic: string;
  mode: string;
};

const state: State = {
  mode: "ionian",
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
  },
};

// Characteristic note by relative index in scale
const CHARACTERISTIC_NOTE_INDEX: Record<string, number> = {
  ionian: 6,       // 7th degree
  dorian: 5,       // ♮6
  phrygian: 1,     // ♭2
  lydian: 3,       // ♯4
  mixolydian: 6,   // ♭7
  aeolian: 5,      // ♭6
  locrian: 1       // ♭2
};

const romanNumerals = ["I", "II", "III", "IV", "V", "VI", "VII"];

const rotate = (arr: any[], n: number) => arr.slice(n).concat(arr.slice(0, n));

const semitoneDistance = (a: string, b: string): number =>
  Math.abs(Note.midi(a)! - Note.midi(b)!);

const hasDiatonicTritone = (chord: string[]): boolean => {
  for (let i = 0; i < chord.length; i++) {
    for (let j = i + 1; j < chord.length; j++) {
      if (semitoneDistance(chord[i], chord[j]) === 6) return true;
    }
  }
  return false;
};

const buildTriads = (scale: string[]): string[][] => {
  return scale.map((_, i) => {
    const rotated = rotate(scale, i);
    return [rotated[0], rotated[2 % 7], rotated[4 % 7]];
  });
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
  const scale = Scale.get(
    `${Midi.midiToNoteName(rootMidi)} ${mode.toLowerCase()}`
  ).notes.map((note) => Midi.toMidi(note)!);

  console.log(`Notes: ${scale}`)
  
  if (!scale) return [];
  const deg = (degree - 1) % 7;
  return [
    scale[deg],
    scale[(deg + 2) % 7],
    scale[(deg + 4) % 7],
  ].sort((a, b) => a - b);
};

const getRoman = (i: number, chord: string[]): string => {
  const detected = Chord.detect(chord)[0] || "";
  const isMinor = detected.toLowerCase().includes("m") && !detected.includes("maj");
  const isDim = detected.includes("dim") || detected.includes("°");
  const numeral = romanNumerals[i % 7];

  if (isDim) return numeral + "°";
  return isMinor ? numeral.toLowerCase() : numeral;
};

const makeNextChord = () => {
  let currentChord: string = romanNumerals[0];
  
  return (): { chord: string; midi: number[] } => {
    const scale = Scale.get(`${Midi.midiToNoteName(state.root)} ${state.mode}`).notes;
    console.log(`Scale: ${Midi.midiToNoteName(state.root)} ${state.mode},  ${scale}`)
    const triads = buildTriads(scale);
    const characteristicNote = scale[CHARACTERISTIC_NOTE_INDEX[state.mode] ?? 0];

    const pool: { name: string; notes: string[] }[] = triads
      .map((chord, i) => {
        if (hasDiatonicTritone(chord)) return null;
        const name = getRoman(i, chord);
        return { name, notes: chord };
      })
      .filter(Boolean) as { name: string; notes: string[] }[];

    if (pool.length === 0) {
      console.warn("No valid chords found for current mode/tonic");
      return { chord: "N/A", midi: [] };
    }

    // initialize on first call
    if (!currentChord) {
      currentChord = pool[0].name;
    }

    let candidates = pool.map((p) => p.name);

    if (state.valence < 0.4) {
      candidates = candidates.filter(
        (ch) => ch.toLowerCase() === ch || ch.includes("°")
      );
    } else if (state.valence > 0.6) {
      candidates = candidates.filter(
        (ch) => ch.toUpperCase() === ch && !ch.includes("°")
      );
    }

    if (candidates.length === 0) {
      candidates = pool.map((p) => p.name);
    }

    const weighted = candidates.flatMap((ch) => {
      const chordObj = pool.find((p) => p.name === ch);
      if (!chordObj) return [];
      const weight = chordObj.notes.includes(characteristicNote) ? 3 : 1;
      return Array(weight).fill(ch);
    });

    if (weighted.length === 0) {
      currentChord = pool[0].name;
    } else {
      const index = Math.floor(
        Math.random() * Math.max(1, weighted.length * (0.5 + state.arousal))
      );
      currentChord = weighted[index % weighted.length];
    }

    const degree = romanToDegree(currentChord);
    const midi = generateChord(state.root, degree, state.mode);

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
  state.set("mode", mode.toLowerCase());
  console.log(`Mode: ${state.mode}`);
});

MaxAPI.addHandler("setRoot", (root: number) => {
  state.set("root", root);
});
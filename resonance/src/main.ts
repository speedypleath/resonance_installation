import MaxAPI from "max-api";
import { Note, Midi, Scale, Chord, RhythmPattern } from "tonal";

interface State {
  mode: string;
  root: number;
  valence: number;
  arousal: number;
  dominance: number;
  set: (key: keyof Omit<State, "set">, value: any) => void;
}

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

const durationOptions = ["16n", "8n", "4n", "2n", "1n"];
const durationToTicks: Record<string, number> = {
  "16n": 120,
  "8n": 240,
  "4n": 480,
  "2n": 960,
  "1n": 1920,
};
const durationWeights = [0.03, 0.1, 0.4, 0.2, 0.07];

// Characteristic note by relative index in scale
const CHARACTERISTIC_NOTE_INDEX: Record<string, number> = {
  ionian: 6, // 7th degree
  dorian: 5, // ♮6
  phrygian: 1, // ♭2
  lydian: 3, // ♯4
  mixolydian: 6, // ♭7
  aeolian: 5, // ♭6
  locrian: 1, // ♭2
};

const romanNumerals = ["I", "II", "III", "IV", "V", "VI", "VII"];

let modes: { [key: string]: any } = {};

const main = async () => { modes = await MaxAPI.getDict("modes"); console.log(modes) };
main();

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

  console.log(`Notes: ${scale}`);

  if (!scale) return [];
  const deg = (degree - 1) % 7;
  return [scale[deg], scale[(deg + 2) % 7], scale[(deg + 4) % 7]].sort(
    (a, b) => a - b
  );
};

const getRoman = (i: number, chord: string[]): string => {
  const detected = Chord.detect(chord)[0] || "";
  const isMinor =
    detected.toLowerCase().includes("m") && !detected.includes("maj");
  const isDim = detected.includes("dim") || detected.includes("°");
  const numeral = romanNumerals[i % 7];

  if (isDim) return numeral + "°";
  return isMinor ? numeral.toLowerCase() : numeral;
};

const makeNextChord = () => {
  let currentChord: string = romanNumerals[0];

  return (): { chord: string; midi: number[] } => {
    const scale = Scale.get(
      `${Midi.midiToNoteName(state.root)} ${state.mode}`
    ).notes;
    console.log(
      `Scale: ${Midi.midiToNoteName(state.root)} ${state.mode},  ${scale}`
    );
    const triads = buildTriads(scale);
    const characteristicNote =
      scale[CHARACTERISTIC_NOTE_INDEX[state.mode] ?? 0];

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

// Melody generation
const getTraits = ([val, ar, dom]: [number, number, number]) => ({
  maxStepJump: 2 + Math.floor(ar * 4),
  stepBias: 0.6 + dom * 0.4,
  restChance: 0.1 + (1 - ar) * 0.3,
  ornamentChance: 0.15 + (1 - val) * 0.3,
  velocityBase: 50 + val * 40 + ar * 20,
});

const chooseWeighted = <T>(items: T[], weights: number[]): T => {
  const sum = weights.reduce((a, b) => a + b, 0);
  let r = Math.random() * sum;
  for (let i = 0; i < items.length; i++) {
    if (r < weights[i]) return items[i];
    r -= weights[i];
  }
  return items[items.length - 1];
};

const parseTimeString = (time: string): number => {
  const [bars = 0, beats = 0, sixteenths = 0] = time.split(".").map(Number);
  return (bars * 4 + beats + sixteenths / 4) * 480;
};

export const generateMelody = (
  length: string
): Array<[number | "rest", number, string]> => {
  const { maxStepJump, stepBias, restChance, ornamentChance, velocityBase } =
    getTraits([state.valence, state.arousal, state.dominance]);

  const result: Array<[number | "rest", number, string]> = [];

  let currentDegree = 1;
  let totalTicks = 0;
  const maxTicks = parseTimeString(length);
  const modeValues = modes[`${state.mode[0].toUpperCase()}${state.mode.slice(1).toLowerCase()}`]

  while (totalTicks < maxTicks) {
    const insertRest = result.length > 0 && Math.random() < restChance;
    if (insertRest) {
      const duration = chooseWeighted(durationOptions, [0.35, 0.5, 0.05, 0.0, 0.0]);
      const ticks = durationToTicks[duration];
      result.push(["rest", 0, duration]);
      totalTicks += ticks;
      continue;
    }

    let duration = chooseWeighted(durationOptions, durationWeights);
    let ticks = durationToTicks[duration];
    if (totalTicks + ticks > maxTicks) {
      const remainingTicks = maxTicks - totalTicks;
      const remainingDuration = durationOptions.find(
        (d) => durationToTicks[d] <= remainingTicks
      );
      if (remainingDuration) {
        duration = remainingDuration;
        ticks = durationToTicks[remainingDuration];
      }
    }

    const velocity = Math.max(
      20,
      Math.min(127, Math.round(velocityBase + (Math.random() - 0.5) * 20))
    );

    const insertOrnament =
      result.length > 0 && Math.random() < ornamentChance && ticks >= 240;

    const jumpOneScale = Math.random() > 0.2 * state.valence ? 12 : 0;
    const realValue = modeValues[currentDegree - 1] + jumpOneScale;

    if (insertOrnament) {
      const shortDur = "16n";
      const shortTicks = durationToTicks[shortDur];

      const auxOffset = Math.random() < 0.5 ? -1 : 1;
      const auxDegree = Math.max(1, Math.min(currentDegree + auxOffset, 7));

      result.push([modeValues[auxDegree - 1], velocity - 10, shortDur]);
      result.push([modeValues[currentDegree - 1], velocity, shortDur]);

      totalTicks += shortTicks * 2;
    } else {
      result.push([realValue, velocity, duration]);
      totalTicks += ticks;
    }

    // Step movement
    const intervalOptions = [];
    for (let offset = -maxStepJump; offset <= maxStepJump; offset++) {
      if (offset === 0) continue;
      const nextDeg = currentDegree + offset;
      if (nextDeg < 1 || nextDeg > 7) continue;
      const weight =
        Math.exp(-Math.abs(offset)) *
        (Math.abs(offset) === 1 ? stepBias : 1 - stepBias);
      intervalOptions.push({ offset, weight });
    }

    const totalWeight = intervalOptions.reduce((s, o) => s + o.weight, 0);
    let acc = 0;
    const r = Math.random() * totalWeight;
    for (const opt of intervalOptions) {
      acc += opt.weight;
      if (r <= acc) {
        currentDegree = currentDegree + opt.offset;
        break;
      }
    }
  }

  return result;
};

// Max message handler
MaxAPI.addHandler("nextChord", () => {
  const { chord, midi } = nextChord();
  MaxAPI.outlet(["chord", chord, ...midi]);
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

MaxAPI.addHandler("generateEuclidean", (beats: number, steps: number) => {
  return RhythmPattern.euclid(steps, beats);
});

MaxAPI.addHandler("computeProbability", (...args) => {
  MaxAPI.outlet(["probs", ...RhythmPattern.probability(args)]);
});

MaxAPI.addHandler("generateMelody", (length: string) => {
  const sequence = generateMelody(length)
  MaxAPI.outlet(["melody", {
    array: sequence,
    length: sequence.length
  }]);
});
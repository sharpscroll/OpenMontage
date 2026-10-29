import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  staticFile,
  useCurrentFrame,
} from 'remotion';

const FPS = 24;
const ink = '#1b2e38';
const paper = '#faf9f4';
const gold = '#ffe35a';
const faultColor = '#d7584d';

type WordTiming = [string, number, number];

const WORD_TIMINGS: WordTiming[] = [
  ["This", 0.0, 0.48], ["wire", 0.48, 0.9], ["doesn't", 0.9, 1.32], ["help", 1.32, 1.54], ["the", 1.54, 1.72], ["motor", 1.72, 2.04], ["turn.", 2.04, 2.42],
  ["So", 2.66, 3.0], ["why", 3.0, 3.4], ["does", 3.4, 3.52], ["your", 3.52, 3.64], ["washing", 3.64, 3.92], ["machine", 3.92, 4.24], ["need", 4.24, 4.5], ["it?", 4.5, 4.84],
  ["Live", 5.66, 5.84], ["and", 5.84, 6.16], ["neutral", 6.16, 6.56], ["form", 6.56, 6.98], ["the", 6.98, 7.2], ["circuit", 7.2, 7.44],
  ["that", 7.44, 7.68], ["runs", 7.68, 7.9], ["the", 7.9, 8.12], ["motor.", 8.12, 8.36],
  ["The", 8.94, 9.04], ["earth", 9.04, 9.28], ["wire", 9.28, 9.62], ["connects", 9.62, 9.92], ["to", 9.92, 10.2], ["the", 10.2, 10.28], ["metal", 10.28, 10.5], ["case", 10.5, 10.82], ["instead.", 10.82, 11.3],
  ["Insulation", 12.18, 12.6], ["keeps", 12.6, 13.0], ["that", 13.0, 13.24], ["case", 13.24, 13.5], ["separate", 13.5, 13.86], ["from", 13.86, 14.16], ["the", 14.16, 14.3], ["working", 14.3, 14.6], ["circuit.", 14.6, 15.02],
  ["That's", 15.5, 15.78], ["why", 15.78, 15.92], ["earth", 15.92, 16.18], ["doesn't", 16.18, 16.58], ["normally", 16.58, 17.0], ["carry", 17.0, 17.3], ["the", 17.3, 17.5], ["motor's", 17.5, 17.84], ["current.", 17.84, 18.08],
  ["But", 18.8, 19.02], ["if", 19.02, 19.1], ["a", 19.1, 19.26], ["live", 19.26, 19.5], ["wire", 19.5, 19.96], ["touches", 19.96, 20.26], ["the", 20.26, 20.5], ["case,", 20.5, 20.78],
  ["that", 21.14, 21.38], ["metal", 21.38, 21.68], ["can", 21.68, 21.9], ["become", 21.9, 22.16], ["a", 22.16, 22.28], ["shock", 22.28, 22.6], ["hazard.", 22.6, 22.98],
  ["In", 23.56, 23.72], ["this", 23.72, 23.88], ["grounded", 23.88, 24.34], ["system,", 24.34, 24.88],
  ["earth", 25.24, 25.36], ["provides", 25.36, 25.74], ["a", 25.74, 25.94], ["path", 25.94, 26.18], ["back", 26.18, 26.6], ["to", 26.6, 26.82], ["the", 26.82, 26.92], ["supply,", 26.92, 27.38],
  ["helping", 27.38, 27.96], ["the", 27.96, 28.16], ["breaker", 28.16, 28.4],
  ["cut", 28.4, 28.76], ["the", 28.76, 28.94], ["power.", 28.94, 29.3],
  ["Neutral", 30.0, 30.28], ["runs", 30.28, 30.78], ["the", 30.78, 30.98], ["machine.", 30.98, 31.3],
  ["Earth", 31.96, 32.0], ["provides", 32.0, 32.52], ["the", 32.52, 32.72], ["protective", 32.72, 33.06], ["path.", 33.06, 33.5],
  ["If", 34.42, 34.5], ["you", 34.5, 34.64], ["enjoy", 34.64, 34.92], ["discovering", 34.92, 35.38], ["how", 35.38, 35.66], ["everyday", 35.66, 36.02], ["things", 36.02, 36.42], ["work,", 36.42, 36.84],
  ["subscribe", 37.24, 37.6], ["to", 37.6, 37.88], ["Cause", 37.88, 38.22], ["&", 38.22, 38.5], ["Motion.", 38.5, 38.86],
  ["And", 38.86, 39.36], ["tell", 39.36, 39.52], ["us", 39.52, 39.66], ["in", 39.66, 39.76], ["the", 39.76, 39.86], ["comments", 39.86, 40.14],
  ["what", 40.14, 40.42], ["you’d", 40.42, 40.62], ["like", 40.62, 40.7], ["us", 40.7, 40.88], ["to", 40.88, 41.02], ["explain", 41.02, 41.34], ["next.", 41.34, 41.68]
];

interface PhraseCard {
  start: number;
  end: number;
  words: WordTiming[];
}

const PHRASE_CARDS: PhraseCard[] = [
  { start: 0.0, end: 2.55, words: WORD_TIMINGS.slice(0, 7) },
  { start: 2.66, end: 5.4, words: WORD_TIMINGS.slice(7, 15) },
  { start: 5.66, end: 7.4, words: WORD_TIMINGS.slice(15, 21) },
  { start: 7.44, end: 8.8, words: WORD_TIMINGS.slice(21, 25) },
  { start: 8.94, end: 11.8, words: WORD_TIMINGS.slice(25, 34) },
  { start: 12.18, end: 15.2, words: WORD_TIMINGS.slice(34, 43) },
  { start: 15.5, end: 18.4, words: WORD_TIMINGS.slice(43, 51) },
  { start: 18.8, end: 20.9, words: WORD_TIMINGS.slice(51, 59) },
  { start: 21.14, end: 23.2, words: WORD_TIMINGS.slice(59, 66) },
  { start: 23.56, end: 25.0, words: WORD_TIMINGS.slice(66, 70) },
  { start: 25.24, end: 27.3, words: WORD_TIMINGS.slice(70, 78) },
  { start: 27.38, end: 29.5, words: WORD_TIMINGS.slice(78, 84) },
  { start: 30.0, end: 31.6, words: WORD_TIMINGS.slice(84, 88) },
  { start: 31.96, end: 33.8, words: WORD_TIMINGS.slice(88, 93) },
  { start: 34.42, end: 37.0, words: WORD_TIMINGS.slice(93, 101) },
  { start: 37.24, end: 38.8, words: WORD_TIMINGS.slice(101, 106) },
  { start: 38.86, end: 41.8, words: WORD_TIMINGS.slice(106, 120) },
];

const Header: React.FC<{ lead: string; highlight: string; highlightColor?: string; textColor?: string }> = ({
  lead,
  highlight,
  highlightColor = gold,
  textColor = ink,
}) => (
  <div
    style={{
      position: 'absolute',
      left: 70,
      right: 70,
      top: 100,
      fontFamily: '"Segoe Print", "Ink Free", "Comic Sans MS", cursive, sans-serif',
      fontWeight: 800,
      fontSize: 64,
      lineHeight: 1.18,
      color: textColor,
      zIndex: 30,
      letterSpacing: -1,
    }}
  >
    {lead}{' '}
    <span
      style={{
        background: highlightColor,
        color: highlightColor === faultColor ? '#ffffff' : ink,
        padding: '3px 14px',
        borderRadius: 8,
        display: 'inline-block',
      }}
    >
      {highlight}
    </span>
  </div>
);

const Watermark: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      right: 50,
      top: 40,
      fontFamily: 'Arial, sans-serif',
      fontWeight: 800,
      fontSize: 22,
      letterSpacing: 2,
      color: '#7b8a92',
      zIndex: 30,
      textTransform: 'uppercase',
    }}
  >
    Cause &amp; Motion · Q61
  </div>
);

const WordCaptions: React.FC<{ time: number }> = ({ time }) => {
  const activePhrase = PHRASE_CARDS.find((p) => time >= p.start && time <= p.end);
  if (!activePhrase) return null;

  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        right: 60,
        bottom: 180,
        minHeight: 130,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexWrap: 'wrap',
        gap: '4px 12px',
        textAlign: 'center',
        fontFamily: 'Arial, Helvetica, sans-serif',
        fontWeight: 800,
        fontSize: 48,
        lineHeight: 1.25,
        color: ink,
        background: '#fffdf4fa',
        borderRadius: 24,
        padding: '16px 28px',
        boxShadow: '0 10px 30px rgba(27, 46, 56, 0.22)',
        border: '3px solid rgba(27, 46, 56, 0.08)',
        zIndex: 50,
      }}
    >
      {activePhrase.words.map(([w, start, end], idx) => {
        const isSpoken = time >= start && time < end;
        return (
          <span
            key={`${activePhrase.start}-${idx}`}
            style={{
              background: isSpoken ? gold : 'transparent',
              borderRadius: 6,
              padding: '2px 8px',
              transition: 'background 0.05s ease-out',
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  );
};

export const Q61Short: React.FC = () => {
  const frame = useCurrentFrame();
  const time = frame / FPS;

  return (
    <AbsoluteFill style={{ background: paper, overflow: 'hidden' }}>
      {/* Background audio track */}
      <Audio src={staticFile('q61/owner-v04.wav')} />

      {/* Top watermark */}
      <Watermark />

      {/* SCENE 1 (0.00 - 5.65s): Brand-New Washer Cutaway Artwork */}
      {time < 5.66 && (
        <AbsoluteFill>
          <Img
            src={staticFile('q61_new/scene1_washer_cutaway.png')}
            style={{
              position: 'absolute',
              width: 1080,
              height: 1920,
              left: 0,
              top: 0,
              objectFit: 'cover',
            }}
          />
          <Header lead="Why this" highlight="wire?" />
        </AbsoluteFill>
      )}

      {/* SCENE 2 (5.66 - 8.93s): Brand-New Circuit Normal Schematic */}
      {time >= 5.66 && time < 8.94 && (
        <AbsoluteFill>
          <Img
            src={staticFile('q61_new/scene2_circuit_normal.png')}
            style={{
              position: 'absolute',
              width: 1080,
              height: 1920,
              left: 0,
              top: 0,
              objectFit: 'cover',
            }}
          />
          <Header lead="Live &amp; Neutral" highlight="run the motor" />
        </AbsoluteFill>
      )}

      {/* SCENE 3 (8.94 - 12.17s): Brand-New Chassis Stud Macro Detail */}
      {time >= 8.94 && time < 12.18 && (
        <AbsoluteFill>
          <Img
            src={staticFile('q61_new/scene3_chassis_stud.png')}
            style={{
              position: 'absolute',
              width: 1080,
              height: 1920,
              left: 0,
              top: 0,
              objectFit: 'cover',
            }}
          />
          <Header lead="Earth connects to" highlight="metal case" />
        </AbsoluteFill>
      )}

      {/* SCENE 4 (12.18 - 18.79s): Brand-New Insulation Barrier Cross-Section */}
      {time >= 12.18 && time < 18.8 && (
        <AbsoluteFill>
          <Img
            src={staticFile('q61_new/scene4_insulation_barrier.png')}
            style={{
              position: 'absolute',
              width: 1080,
              height: 1920,
              left: 0,
              top: 0,
              objectFit: 'cover',
            }}
          />
          <Header lead="Normally" highlight="kept apart" />
        </AbsoluteFill>
      )}

      {/* SCENE 5 (18.80 - 27.37s): Brand-New Fault Surge Scenario */}
      {time >= 18.8 && time < 27.38 && (
        <AbsoluteFill>
          <Img
            src={staticFile('q61_new/scene5_fault_surge.png')}
            style={{
              position: 'absolute',
              width: 1080,
              height: 1920,
              left: 0,
              top: 0,
              objectFit: 'cover',
            }}
          />
          <Header lead="If wire" highlight="touches case" highlightColor={faultColor} />
        </AbsoluteFill>
      )}

      {/* SCENE 6 (27.38 - 29.99s): Brand-New Breaker Trip Action */}
      {time >= 27.38 && time < 30.0 && (
        <AbsoluteFill>
          <Img
            src={staticFile('q61_new/scene6_breaker_trip.png')}
            style={{
              position: 'absolute',
              width: 1080,
              height: 1920,
              left: 0,
              top: 0,
              objectFit: 'cover',
            }}
          />
          <Header lead="Breaker" highlight="cuts power!" />
        </AbsoluteFill>
      )}

      {/* SCENE 7 (30.00 - 42.25s): Brand-New Payoff Summary Cards & Branding */}
      {time >= 30.0 && (
        <AbsoluteFill>
          <Img
            src={staticFile('q61_new/scene7_payoff_summary.png')}
            style={{
              position: 'absolute',
              width: 1080,
              height: 1920,
              left: 0,
              top: 0,
              objectFit: 'cover',
            }}
          />
          <Header lead="Two different" highlight="jobs" />
        </AbsoluteFill>
      )}

      {/* Floating Active Word-Highlighted Captions */}
      <WordCaptions time={time} />
    </AbsoluteFill>
  );
};

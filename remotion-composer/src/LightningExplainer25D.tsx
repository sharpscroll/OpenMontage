import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export const LightningExplainer25D: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // -------------------------------------------------------------
  // Camera Pan & Zoom Grammar (4 Scenes across 20 seconds)
  // -------------------------------------------------------------
  let scale = 1.0;
  let tx = 0;
  let ty = 0;

  if (t < 4.2) {
    // Scene 1 (0-4.2s): Establishing Wide Shot
    scale = interpolate(t, [0, 4.2], [1.0, 1.05], { extrapolateRight: 'clamp' });
    tx = 0;
    ty = 0;
  } else if (t < 8.0) {
    // Scene 2 (4.2-8.0s): Macro Zoom onto Copper Air Terminal (peak_x: 1800, peak_y: 480)
    scale = interpolate(t, [4.2, 5.0, 8.0], [1.05, 1.75, 1.82], { extrapolateRight: 'clamp' });
    tx = interpolate(t, [4.2, 5.0], [0, -120], { extrapolateRight: 'clamp' });
    ty = interpolate(t, [4.2, 5.0], [0, 260], { extrapolateRight: 'clamp' });
  } else if (t < 13.5) {
    // Scene 3 (8.0-13.5s): Tilt Down following exterior Down-Conductor
    scale = interpolate(t, [8.0, 9.0], [1.82, 1.45], { extrapolateRight: 'clamp' });
    tx = interpolate(t, [8.0, 13.5], [-120, 320], { extrapolateRight: 'clamp' });
    ty = interpolate(t, [8.0, 13.5], [260, -120], { extrapolateRight: 'clamp' });
  } else {
    // Scene 4 (13.5-20.0s): Sub-surface Macro Zoom onto Earth Pit (ground_x: 960, ground_y: 1800)
    scale = interpolate(t, [13.5, 14.5, 20.0], [1.45, 1.7, 1.75], { extrapolateRight: 'clamp' });
    tx = interpolate(t, [13.5, 14.5], [320, 440], { extrapolateRight: 'clamp' });
    ty = interpolate(t, [13.5, 14.5], [-120, -320], { extrapolateRight: 'clamp' });
  }

  // -------------------------------------------------------------
  // HUD Callouts & Subtitles
  // -------------------------------------------------------------
  let badgeTitle = 'THUNDERCLOUD CHARGE ACCUMULATION';
  let badgeSub = 'Negative stepped leader forms in cumulonimbus cloud';
  let badgeColor = '#eb5757';
  let caption = 'A SINGLE LIGHTNING BOLT DELIVERS 300 MILLION VOLTS';

  if (t >= 4.2 && t < 8.0) {
    badgeTitle = 'DIRECT STRIKE INTERCEPTED AT AIR TERMINAL';
    badgeSub = 'Pointed copper Franklin rod provides preferential ionization path';
    badgeColor = '#ffe259';
    caption = 'WITHOUT PROTECTION, IT DESTROYS STRUCTURES AND CAUSES FIRES';
  } else if (t >= 8.0 && t < 13.5) {
    badgeTitle = 'BARE COPPER DOWN-CONDUCTOR // LOW IMPEDANCE';
    badgeSub = '30,000 Amperes routed along exterior, completely bypassing interior';
    badgeColor = '#ffaa33';
    caption = 'A COPPER ROD INTERCEPTS AND CHANNELS THE SURGE SAFELY DOWN';
  } else if (t >= 13.5) {
    badgeTitle = 'EQUIPOTENTIAL GROUND DISSIPATION // ZERO DAMAGE';
    badgeSub = 'Current harmlessly discharged into bentonite bed and deep 0V earth';
    badgeColor = '#2ecc71';
    caption = 'SAFELY DISSIPATING THE ENORMOUS SURGE DEEP INTO THE EARTH';
  }

  // Lightning bolt visual trigger at t = 4.4s to 5.2s
  const showLightning = t >= 4.4 && t <= 5.1;
  const lightningFlash = t >= 4.4 && t <= 4.7 ? (t < 4.5 ? 0.6 : 0.25) : 0;

  // Ground dissipation rings expansion at t >= 13.5s
  const groundWaves = [0, 1, 2, 3].map((i) => {
    if (t < 13.5) return null;
    const waveProgress = ((t - 13.5) * 1.5 + i * 0.25) % 1.0;
    const radius = waveProgress * 180 + 20;
    const opacity = Math.max(0, 1.0 - waveProgress);
    return { radius, opacity };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0b121c', overflow: 'hidden' }}>
      <Audio src={staticFile('lightning-audio.wav')} />

      {/* Camera Viewport Container */}
      <div
        style={{
          width: '100%',
          height: '100%',
          position: 'absolute',
          transform: `scale(${scale}) translate(${tx}px, ${ty}px)`,
          transformOrigin: 'center center',
          transition: 'transform 0.05s linear',
        }}
      >
        {/* 4K Master Illustration Plate */}
        <Img
          src={staticFile('lightning-master-plate.png')}
          style={{ width: '100%', height: '100%', objectFit: 'contain' }}
        />

        {/* Dynamic SVG EffectCraft Overlay */}
        <svg
          style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
          viewBox="0 0 3840 2160"
        >
          {/* Lightning Discharge Arc */}
          {showLightning && (
            <g>
              <polyline
                points="1740,60 1780,180 1720,240 1800,320 1760,400 1800,480"
                fill="none"
                stroke="rgba(100, 220, 255, 0.9)"
                strokeWidth="24"
                strokeLinecap="round"
              />
              <polyline
                points="1740,60 1780,180 1720,240 1800,320 1760,400 1800,480"
                fill="none"
                stroke="#ffffff"
                strokeWidth="10"
                strokeLinecap="round"
              />
              {/* Terminal Bloom Flash */}
              <circle cx="1800" cy="480" r="90" fill="rgba(255, 255, 255, 0.85)" />
              <circle cx="1800" cy="480" r="160" fill="rgba(100, 220, 255, 0.45)" />
            </g>
          )}

          {/* Surge Current Pulses down conductor (t: 5.0s to 14.0s) */}
          {t >= 5.0 && t <= 14.0 && (
            <g>
              {[0, 0.2, 0.4, 0.6, 0.8].map((offset, idx) => {
                const prog = ((t - 5.0) * 1.8 + offset) % 1.0;
                let px = 1800;
                let py = 480;

                // Path segments on master plate:
                // 1. Peak (1800, 480) -> Roof Eaves (960, 780)
                // 2. Eaves (960, 780) -> Ground (960, 1580)
                // 3. Ground (960, 1580) -> Pit (960, 1940)
                if (prog < 0.35) {
                  const u = prog / 0.35;
                  px = (1 - u) * 1800 + u * 960;
                  py = (1 - u) * 480 + u * 780;
                } else if (prog < 0.8) {
                  const u = (prog - 0.35) / 0.45;
                  px = 960;
                  py = (1 - u) * 780 + u * 1580;
                } else {
                  const u = (prog - 0.8) / 0.2;
                  px = 960;
                  py = (1 - u) * 1580 + u * 1940;
                }

                return (
                  <circle
                    key={idx}
                    cx={px}
                    cy={py}
                    r="16"
                    fill="#ffe259"
                    filter="drop-shadow(0 0 12px rgba(255,226,89,0.9))"
                  />
                );
              })}
            </g>
          )}

          {/* Sub-surface Radial Ground Dissipation Waves */}
          {t >= 13.5 &&
            groundWaves.map((wave, idx) => {
              if (!wave) return null;
              return (
                <ellipse
                  key={idx}
                  cx="960"
                  cy="1940"
                  rx={wave.radius * 2.2}
                  ry={wave.radius * 1.1}
                  fill="none"
                  stroke={`rgba(46, 204, 113, ${wave.opacity * 0.8})`}
                  strokeWidth="8"
                />
              );
            })}
        </svg>

        {/* Full-screen flash on strike */}
        {lightningFlash > 0 && (
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: `rgba(255, 255, 255, ${lightningFlash})`,
              pointerEvents: 'none',
            }}
          />
        )}
      </div>

      {/* Top Header Banner */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 80,
          backgroundColor: 'rgba(15, 24, 38, 0.95)',
          borderBottom: '2px solid rgba(45, 75, 110, 0.8)',
          display: 'flex',
          alignItems: 'center',
          paddingLeft: 60,
          zIndex: 50,
        }}
      >
        <span
          style={{
            fontFamily: '"Arial Black", Arial, sans-serif',
            fontSize: 28,
            color: '#f5f8fc',
            letterSpacing: 0.5,
          }}
        >
          HOW A LIGHTNING CONDUCTOR WORKS
        </span>
        <span
          style={{
            marginLeft: 30,
            background: '#ffe259',
            color: '#111111',
            padding: '4px 14px',
            borderRadius: 6,
            fontFamily: '"Arial Black", Arial, sans-serif',
            fontSize: 14,
            fontWeight: 900,
            textTransform: 'uppercase',
          }}
        >
          CAUSE & MOTION // TECHNICAL EXPLAINER
        </span>
      </div>

      {/* Technical HUD Callout Badge */}
      <div
        style={{
          position: 'absolute',
          top: 110,
          left: 60,
          backgroundColor: 'rgba(15, 24, 38, 0.92)',
          border: '2px solid rgba(40, 65, 95, 0.9)',
          borderLeft: `8px solid ${badgeColor}`,
          padding: '14px 24px',
          borderRadius: 8,
          maxWidth: 750,
          zIndex: 50,
          boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
        }}
      >
        <div
          style={{
            fontFamily: '"Arial Black", Arial, sans-serif',
            fontSize: 20,
            color: badgeColor,
            marginBottom: 4,
          }}
        >
          {badgeTitle}
        </div>
        <div
          style={{
            fontFamily: 'Arial, sans-serif',
            fontSize: 16,
            color: '#8ca0b9',
            lineHeight: 1.3,
          }}
        >
          {badgeSub}
        </div>
      </div>

      {/* Bottom Narration Captions (Zenthral High-Contrast Style) */}
      <div
        style={{
          position: 'absolute',
          bottom: 45,
          left: 60,
          right: 60,
          textAlign: 'center',
          zIndex: 50,
        }}
      >
        <span
          style={{
            fontFamily: '"Arial Black", Arial, sans-serif',
            fontSize: 28,
            color: '#ffe259',
            textTransform: 'uppercase',
            backgroundColor: 'rgba(8, 14, 22, 0.92)',
            padding: '10px 24px',
            borderRadius: 8,
            border: '2px solid rgba(35, 55, 80, 0.9)',
            boxShadow: '0 6px 18px rgba(0,0,0,0.6)',
            letterSpacing: 0.5,
          }}
        >
          {caption}
        </span>
      </div>
    </AbsoluteFill>
  );
};

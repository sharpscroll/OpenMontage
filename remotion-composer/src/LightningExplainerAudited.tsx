import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, staticFile, Audio } from 'remotion';

export const LightningExplainerAudited: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps; // Current playback time in seconds (0 to 20s)

  // -------------------------------------------------------------
  // Camera Pan & Zoom Grammar (Cause & Motion Standards)
  // Designed so all technical labels remain in safe viewing area
  // -------------------------------------------------------------
  let scale = 1.0;
  let tx = 0;
  let ty = 0;
  let badgeText = 'CHARGE ACCUMULATION';
  let badgeBg = '#ffe259';
  let badgeColor = '#18313b';

  if (t < 4.5) {
    // Phase 1 (0-4.5s): Wide Overview - Establishing Cloud & Structure
    scale = interpolate(t, [0, 4.5], [1.0, 1.03], { extrapolateRight: 'clamp' });
    tx = 0;
    ty = 0;
    badgeText = 'CHARGE ACCUMULATION';
    badgeBg = '#ffe259';
    badgeColor = '#18313b';
  } else if (t < 8.5) {
    // Phase 2 (4.5-8.5s): Focused View on Air Terminal Intercept
    scale = interpolate(t, [4.5, 5.3, 8.5], [1.03, 1.30, 1.34], { extrapolateRight: 'clamp' });
    tx = interpolate(t, [4.5, 5.3], [0, -120], { extrapolateRight: 'clamp' });
    ty = interpolate(t, [4.5, 5.3], [0, 60], { extrapolateRight: 'clamp' });
    badgeText = 'STRIKE INTERCEPTED';
    badgeBg = '#bf5844';
    badgeColor = '#ffffff';
  } else if (t < 14.0) {
    // Phase 3 (8.5-14.0s): Follow Down-Conductor & Isolated Domestic Service
    scale = interpolate(t, [8.5, 9.2], [1.34, 1.18], { extrapolateRight: 'clamp' });
    tx = interpolate(t, [8.5, 14.0], [-120, 40], { extrapolateRight: 'clamp' });
    ty = interpolate(t, [8.5, 14.0], [60, -30], { extrapolateRight: 'clamp' });
    badgeText = 'SURGE DIVERTED';
    badgeBg = '#bf5844';
    badgeColor = '#ffffff';
  } else {
    // Phase 4 (14.0-20.0s): Earth Electrode Ground Dissipation
    scale = interpolate(t, [14.0, 14.8, 20.0], [1.18, 1.20, 1.22], { extrapolateRight: 'clamp' });
    tx = interpolate(t, [14.0, 14.8], [40, 50], { extrapolateRight: 'clamp' });
    ty = interpolate(t, [14.0, 14.8], [-30, -25], { extrapolateRight: 'clamp' });
    badgeText = 'GROUND DISSIPATION';
    badgeBg = '#53845b';
    badgeColor = '#ffffff';
  }

  // -------------------------------------------------------------
  // Subtitle Synchronization
  // -------------------------------------------------------------
  let captionText = 'A SINGLE LIGHTNING BOLT DELIVERS 300 MILLION VOLTS.';
  if (t >= 4.5 && t < 8.5) {
    captionText = 'WITHOUT PROTECTION, IT DESTROYS STRUCTURES AND CAUSES FIRES.';
  } else if (t >= 8.5 && t < 14.0) {
    captionText = 'A POINTED COPPER ROD INTERCEPTS AND CHANNELS THE SURGE SAFELY.';
  } else if (t >= 14.0) {
    captionText = 'SAFELY DISSIPATING THE ENORMOUS CHARGE DEEP INTO THE EARTH.';
  }

  // -------------------------------------------------------------
  // Lightning Arc Physics & Visual Timing
  // Pre-leader: t = 4.1s - 4.49s
  // Main return strike: t = 4.5s - 5.6s
  // -------------------------------------------------------------
  const showPreLeader = t >= 4.1 && t < 4.5;
  const showMainStrike = t >= 4.5 && t <= 5.6;

  // Flash decay factor
  const flashOpacity = showMainStrike
    ? interpolate(t, [4.5, 4.55, 4.75, 5.1, 5.6], [0, 0.45, 0.35, 0.15, 0], { extrapolateRight: 'clamp' })
    : 0;

  // -------------------------------------------------------------
  // Motion Invariant: An open gap NEVER receives current dots!
  // Current dots ONLY move along conductor AFTER t = 4.5s
  // -------------------------------------------------------------
  const showCurrentFlow = t >= 4.6 && t <= 14.0;
  const numDots = 14;

  // Conductor path geometry:
  // Segment 1: Roof run from (1140, 298) to (650, 470), length ~519px
  // Segment 2: Vertical drop from (650, 470) to (650, 915), length 445px
  // Total length = 964px
  const seg1Len = 519.3;
  const seg2Len = 445.0;
  const totalLen = seg1Len + seg2Len;

  const currentDots = [];
  if (showCurrentFlow) {
    const elapsed = t - 4.6;
    const baseProgress = (elapsed * 0.8) % 1.0;

    for (let i = 0; i < numDots; i++) {
      const p = (baseProgress + i / numDots) % 1.0;
      const d = p * totalLen;
      let x = 1140;
      let y = 298;

      if (d <= seg1Len) {
        const u = d / seg1Len;
        x = 1140 + u * (650 - 1140);
        y = 298 + u * (470 - 298);
      } else {
        const u = (d - seg1Len) / seg2Len;
        x = 650;
        y = 470 + u * (915 - 470);
      }
      currentDots.push({ x, y, id: i });
    }
  }

  // Sub-surface dissipation expansion waves (t >= 5.0s)
  const showDissipation = t >= 5.0;
  const dissipationWaves = [0, 1, 2, 3].map((idx) => {
    if (!showDissipation) return { r: 0, opacity: 0 };
    const phaseOffset = idx * 0.35;
    const waveT = (t - 5.0 + phaseOffset) % 1.4;
    const r = interpolate(waveT, [0, 1.4], [10, 130]);
    const opacity = interpolate(waveT, [0, 0.4, 1.4], [0.8, 0.6, 0]);
    return { r, opacity };
  });

  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        position: 'relative',
        backgroundColor: '#fbfaf6',
        overflow: 'hidden',
        fontFamily: 'Arial, sans-serif'
      }}
    >
      {/* Synchronized 44.1 kHz Sound Design (Thunder + Surge + Narration) */}
      <Audio src={staticFile('lightning-audio.wav')} />

      {/* Camera Stage (Transforms Master Plate and Motion Layers Together) */}
      <div
        style={{
          width: 1920,
          height: 1080,
          position: 'absolute',
          top: 0,
          left: 0,
          transformOrigin: '960px 540px',
          transform: `scale(${scale}) translate(${tx}px, ${ty}px)`
        }}
      >
        {/* Audited Vector Schematic Master Plate */}
        <img
          src={staticFile('lightning-schematic-plate.svg')}
          alt="Lightning Master Schematic Plate"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: 1920,
            height: 1080
          }}
        />

        {/* Dynamic Motion Layer: Lightning Arcs, Current Packets, and Dissipation */}
        <svg
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: 1920,
            height: 1080,
            pointerEvents: 'none'
          }}
        >
          {/* Pre-leader Ionized Stepped Sparks (t = 4.1s - 4.49s) */}
          {showPreLeader && (
            <g stroke="#ffe259" strokeWidth="3" fill="none" opacity="0.75" strokeLinecap="round">
              <path d="M 480 280 L 600 290 L 710 270 L 800 240 L 920 220" strokeDasharray="10 14" />
              <path d="M 1140 132 L 1120 180 L 1050 200" strokeDasharray="8 12" />
            </g>
          )}

          {/* Main Return Lightning Strike Arc (t = 4.5s - 5.6s) */}
          {showMainStrike && (
            <g>
              {/* Outer Radiant Glow */}
              <path
                d="M 480 280 L 590 260 L 720 280 L 850 220 L 970 250 L 1070 170 L 1140 132"
                stroke="#ffe259"
                strokeWidth="24"
                fill="none"
                opacity="0.35"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {/* Secondary Branch Forks */}
              <path
                d="M 720 280 L 760 340 L 800 370"
                stroke="#ffe259"
                strokeWidth="6"
                fill="none"
                strokeLinecap="round"
                opacity="0.8"
              />
              <path
                d="M 970 250 L 1010 300 L 1040 320"
                stroke="#ffe259"
                strokeWidth="5"
                fill="none"
                strokeLinecap="round"
                opacity="0.7"
              />
              {/* Core High-Energy Strike Channel */}
              <path
                d="M 480 280 L 590 260 L 720 280 L 850 220 L 970 250 L 1070 170 L 1140 132"
                stroke="#ffe259"
                strokeWidth="10"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {/* White-Hot Core Filament */}
              <path
                d="M 480 280 L 590 260 L 720 280 L 850 220 L 970 250 L 1070 170 L 1140 132"
                stroke="#ffffff"
                strokeWidth="4"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {/* Intercept Flash Bloom at Rod Tip */}
              <circle cx="1140" cy="132" r="32" fill="#ffe259" opacity="0.6" />
              <circle cx="1140" cy="132" r="14" fill="#ffffff" />
            </g>
          )}

          {/* Moving Current Surge Packets Along Conductor (#ffe259) */}
          {showCurrentFlow &&
            currentDots.map((dot) => (
              <g key={dot.id}>
                {/* Glow ring */}
                <circle cx={dot.x} cy={dot.y} r={11} fill="#ffe259" opacity={0.4} />
                {/* Core current charge particle */}
                <circle cx={dot.x} cy={dot.y} r={6.5} fill="#ffe259" stroke="#18313b" strokeWidth={2} />
              </g>
            ))}

          {/* Sub-Surface Ground Radial Dissipation Waves */}
          {showDissipation && (
            <g transform="translate(650, 915)">
              {dissipationWaves.map((wave, idx) => (
                <circle
                  key={idx}
                  cx="0"
                  cy="0"
                  r={wave.r}
                  fill="none"
                  stroke="#53845b"
                  strokeWidth="3.5"
                  opacity={wave.opacity}
                />
              ))}
            </g>
          )}
        </svg>

        {/* Ambient Lightning Flash Overlay across Scene */}
        {showMainStrike && (
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: 1920,
              height: 1080,
              backgroundColor: '#ffffff',
              opacity: flashOpacity,
              pointerEvents: 'none'
            }}
          />
        )}
      </div>

      {/* ========================================================= */}
      {/* SCREEN-SPACE FIXED HUD & Q61 AUDITED TYPOGRAPHY            */}
      {/* Kept independent of camera transforms for pristine layout  */}
      {/* ========================================================= */}

      {/* Top HUD Clean Fade Vignette (Guarantees zero bleed into headline) */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1920,
          height: 120,
          background: 'linear-gradient(to bottom, #fbfaf6 75%, rgba(251, 250, 246, 0) 100%)',
          zIndex: 90,
          pointerEvents: 'none'
        }}
      />

      {/* Top Headline & Dynamic Status Badge */}
      <div
        style={{
          position: 'absolute',
          top: 36,
          left: 80,
          display: 'flex',
          alignItems: 'center',
          gap: 16,
          zIndex: 100
        }}
      >
        <span
          style={{
            fontFamily: 'Arial, sans-serif',
            fontSize: 34,
            fontWeight: 900,
            color: '#18313b',
            letterSpacing: '0.04em'
          }}
        >
          HOW A LIGHTNING CONDUCTOR WORKS
        </span>
        <span
          style={{
            fontFamily: 'Arial, sans-serif',
            fontSize: 20,
            fontWeight: 900,
            color: badgeColor,
            backgroundColor: badgeBg,
            padding: '6px 14px',
            borderRadius: 6,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            boxShadow: '0 2px 8px rgba(24, 49, 59, 0.1)'
          }}
        >
          {badgeText}
        </span>
      </div>

      {/* Bottom Subtitle Safe Vignette */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          width: 1920,
          height: 100,
          background: 'linear-gradient(to top, #fbfaf6 65%, rgba(251, 250, 246, 0) 100%)',
          zIndex: 90,
          pointerEvents: 'none'
        }}
      />

      {/* Bottom Subtitle Bar (Clean White Pill with Ink Border) */}
      <div
        style={{
          position: 'absolute',
          bottom: 24,
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 100,
          backgroundColor: '#ffffff',
          border: '2.5px solid #18313b',
          borderRadius: 8,
          padding: '10px 28px',
          boxShadow: '0 4px 16px rgba(24, 49, 59, 0.10)'
        }}
      >
        <span
          style={{
            fontFamily: 'Arial, sans-serif',
            fontSize: 22,
            fontWeight: 800,
            color: '#18313b',
            letterSpacing: '0.03em',
            textTransform: 'uppercase'
          }}
        >
          {captionText}
        </span>
      </div>
    </div>
  );
};

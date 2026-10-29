import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';

export const LightningConductor: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0b121c' }}>
      <OffthreadVideo
        src={staticFile('lightning-conductor.mp4')}
        style={{ width: '100%', height: '100%', objectFit: 'contain' }}
      />
    </AbsoluteFill>
  );
};

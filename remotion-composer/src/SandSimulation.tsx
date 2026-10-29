import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';

export const SandSimulation: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#EFE8D8' }}>
      <OffthreadVideo
        src={staticFile('sand-electricity.mp4')}
        style={{ width: '100%', height: '100%', objectFit: 'contain' }}
      />
    </AbsoluteFill>
  );
};

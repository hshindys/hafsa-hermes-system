import React from "react";
import { CinematicRenderer } from "./CinematicRenderer";
import { calculateCinematicMetadata } from "./CinematicRenderer";

export const wc2026Teaser: React.FC = () => {
  const scenes = [
    {
      id: "s1",
      startSeconds: 0,
      durationSeconds: 5.5,
      kind: "video",
      src: `file:///home/hatem/OpenMontage/projects/wc2026-teaser/assets/images/egyptian-crowd.jpg`,
      tone: "void",
      fadeInFrames: 12,
      fadeOutFrames: 18,
    },
    {
      id: "t1",
      startSeconds: 0.3,
      durationSeconds: 4.2,
      kind: "title",
      text: "EGYPT\n2026",
      accent: "#C8102E",
      intensity: 0.9,
      titleFontSize: 96,
      titleWidth: 1400,
      signalLineCount: 14,
      variant: "overlay",
    },
    {
      id: "s2",
      startSeconds: 5.5,
      durationSeconds: 5.5,
      kind: "video",
      src: `file:///home/hatem/OpenMontage/projects/wc2026-teaser/assets/images/stadium-fans.jpg`,
      tone: "steel",
      fadeInFrames: 10,
      fadeOutFrames: 18,
    },
    {
      id: "t2",
      startSeconds: 5.8,
      durationSeconds: 4,
      kind: "title",
      text: "ROAD TO WORLD CUP",
      accent: "#D4AF37",
      intensity: 0.9,
      titleFontSize: 90,
      titleWidth: 1400,
      signalLineCount: 14,
      variant: "overlay",
    },
    {
      id: "s3",
      startSeconds: 11,
      durationSeconds: 5.5,
      kind: "video",
      src: `file:///home/hatem/OpenMontage/projects/wc2026-teaser/assets/images/fans-celebration.jpg`,
      tone: "neutral",
      fadeInFrames: 12,
      fadeOutFrames: 18,
    },
    {
      id: "t3",
      startSeconds: 11.3,
      durationSeconds: 3.8,
      kind: "title",
      text: "WE\nQUALIFY",
      accent: "#C8102E",
      intensity: 0.9,
      titleFontSize: 94,
      titleWidth: 1400,
      signalLineCount: 14,
      variant: "overlay",
    },
    {
      id: "s4",
      startSeconds: 16.5,
      durationSeconds: 5,
      kind: "video",
      src: `file:///home/hatem/OpenMontage/projects/wc2026-teaser/assets/images/egyptian-crowd.jpg`,
      tone: "cold",
      fadeInFrames: 10,
      fadeOutFrames: 20,
    },
    {
      id: "t4",
      startSeconds: 17,
      durationSeconds: 3.5,
      kind: "title",
      text: "#مصر\n2026",
      accent: "#D4AF37",
      intensity: 1,
      titleFontSize: 100,
      titleWidth: 1400,
      signalLineCount: 14,
      variant: "overlay",
    },
  ];

  return (
    <CinematicRenderer
      scenes={scenes}
      titleFontSize={88}
      titleWidth={1400}
      signalLineCount={12}
      soundtrack={undefined}
      music={undefined}
      captions={undefined}
    />
  );
};

export const wc2026Meta = calculateCinematicMetadata;

import React from "react";

const MODEL_INFO: Record<string, { size: string; speed: string; lang: string; quality: string; note: string }> = {
  "all-MiniLM-L6-v2": {
    size: "~80MB",
    speed: "Gyors",
    lang: "EN",
    quality: "Közepes",
    note: "Alapértelmezett, kis méret"
  },
  "paraphrase-multilingual-MiniLM-L12-v2": {
    size: "~120MB",
    speed: "Gyors",
    lang: "Multilingual",
    quality: "Jó",
    note: "Jelenlegi default"
  },
  "paraphrase-multilingual-mpnet-base-v2": {
    size: "~1GB",
    speed: "Lassabb",
    lang: "Multilingual",
    quality: "Nagyon jó",
    note: "Nagyobb memória igény"
  },
  "intfloat/multilingual-e5-large": {
    size: "~2.2GB",
    speed: "Lassú",
    lang: "Multilingual",
    quality: "Legjobb",
    note: "Nagy, pontos, lassú"
  }
};

export const ModelInfo: React.FC<{ model: string }> = ({ model }) => {
  const info = MODEL_INFO[model];
  if (!info) return null;
  return (
    <div style={{ marginTop: 8 }}>
      <div><b>Méret:</b> {info.size}</div>
      <div><b>Sebesség:</b> {info.speed}</div>
      <div><b>Nyelv:</b> {info.lang}</div>
      <div><b>Pontosság:</b> {info.quality}</div>
      <div><b>Megjegyzés:</b> {info.note}</div>
    </div>
  );
};

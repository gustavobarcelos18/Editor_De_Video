/* GERADO por `pnpm gen` a partir de schema.json. Não edite. */

/**
 * This interface was referenced by `CronistaContracts`'s JSON-Schema
 * via the `definition` "MarkerKind".
 */
export type MarkerKind =
  "momento" | "morte_falha" | "engracado" | "conquista" | "novo_dia" | "construcao" | "foto_progresso" | "cinematica";
export type AudioStreams = number;
export type BitDepth = number;
export type DurationS = number | null;
export type Fps = string | null;
export type Height = number | null;
export type Interrupted = boolean;
export type Path = string;
export type PixFmt = string | null;
export type VideoCodec = string | null;
export type Width = number | null;
export type Files = string[];
export type Warnings = string[];

export interface CronistaContracts {
  [k: string]: unknown;
}
/**
 * Resultado do `ffprobe` de um arquivo de gravação.
 *
 * This interface was referenced by `CronistaContracts`'s JSON-Schema
 * via the `definition` "MediaProbe".
 */
export interface MediaProbe {
  audio_streams?: AudioStreams;
  bit_depth?: BitDepth;
  duration_s?: DurationS;
  fps?: Fps;
  height?: Height;
  interrupted?: Interrupted;
  path: Path;
  pix_fmt?: PixFmt;
  video_codec?: VideoCodec;
  width?: Width;
}
/**
 * Saída de uma etapa do pipeline, persistida como `result.json` no cache.
 *
 * This interface was referenced by `CronistaContracts`'s JSON-Schema
 * via the `definition` "StageResult".
 */
export interface StageResult {
  data?: Data;
  files?: Files;
  warnings?: Warnings;
}
export interface Data {
  [k: string]: unknown;
}

import { invoke } from "@tauri-apps/api/core";
import type { AppConfig, BatchResizeResponse } from "../types/tool";

export async function loadConfig(): Promise<AppConfig> {
  return invoke<AppConfig>("load_config");
}

export async function saveConfig(config: AppConfig): Promise<void> {
  return invoke("save_config", { config });
}

export async function batchResizeImages(
  inputDir: string,
  outputDir: string,
  maxSize: number,
  workers: number,
): Promise<BatchResizeResponse> {
  return invoke<BatchResizeResponse>("batch_resize_images_command", {
    inputDir,
    outputDir,
    maxSize,
    workers,
  });
}

export function formatResultLine(result: {
  filename: string;
  source_size: [number, number];
  output_size: [number, number];
  skipped: boolean;
}): string {
  if (result.skipped) {
    return `${result.filename}: ${result.source_size[0]}x${result.source_size[1]} (无需缩放)`;
  }
  return `${result.filename}: ${result.source_size[0]}x${result.source_size[1]} -> ${result.output_size[0]}x${result.output_size[1]}`;
}

import type { ComponentType } from "react";

export interface ToolProps {
  onStatus: (message: string) => void;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  component: ComponentType<ToolProps>;
}

export type AppView = "tools" | "settings" | "tool";

export interface AppConfig {
  thread_count: number;
  export_dir: string;
  tauri: Record<string, unknown>;
}

export interface ResizeResult {
  filename: string;
  source_size: [number, number];
  output_size: [number, number];
  skipped: boolean;
}

export interface ResizeError {
  filename: string;
  message: string;
}

export interface BatchResizeResponse {
  results: ResizeResult[];
  errors: ResizeError[];
}

export interface ResizeProgressPayload {
  current: number;
  total: number;
  filename: string;
}

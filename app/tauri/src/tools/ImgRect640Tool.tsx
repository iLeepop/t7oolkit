import { useEffect, useRef, useState } from "react";
import { listen } from "@tauri-apps/api/event";
import { open } from "@tauri-apps/plugin-dialog";
import { batchResizeImages, formatResultLine, loadConfig } from "../api/config";
import type { ResizeProgressPayload, ToolProps } from "../types/tool";
import "../components/SettingsPanel.css";
import "./tools.css";

export function ImgRect640Tool({ onStatus }: ToolProps) {
  const [inputDir, setInputDir] = useState("");
  const [outputDir, setOutputDir] = useState("");
  const [maxSize, setMaxSize] = useState("640");
  const [summary, setSummary] = useState("请选择输入文件夹后开始处理。");
  const [progress, setProgress] = useState(0);
  const [logLines, setLogLines] = useState<string[]>([]);
  const [running, setRunning] = useState(false);
  const logRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    loadConfig().then((config) => {
      setOutputDir(config.export_dir);
    });
  }, []);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [logLines]);

  async function browseDirectory(
    title: string,
    setter: (value: string) => void,
    initial?: string,
  ) {
    const selected = await open({
      directory: true,
      multiple: false,
      title,
      defaultPath: initial || undefined,
    });
    if (typeof selected === "string") {
      setter(selected);
    }
  }

  async function run() {
    if (running) {
      return;
    }

    const input = inputDir.trim();
    const output = outputDir.trim();
    if (!input) {
      setSummary("请先选择输入文件夹。");
      return;
    }
    if (!output) {
      setSummary("请先选择输出文件夹。");
      return;
    }

    const parsedSize = Number.parseInt(maxSize, 10);
    if (Number.isNaN(parsedSize) || parsedSize <= 0) {
      setSummary("最大边长必须是大于 0 的整数。");
      return;
    }

    const config = await loadConfig();
    setRunning(true);
    setProgress(0);
    setLogLines([]);
    setSummary("正在准备处理…");
    onStatus("正在准备处理…");

    const unlisten = await listen<ResizeProgressPayload>("resize-progress", (event) => {
      const { current, total } = event.payload;
      setProgress(total > 0 ? Math.round((current / total) * 100) : 0);
      setSummary(`正在处理 ${current}/${total}：${event.payload.filename}`);
      onStatus(`正在处理 ${current}/${total} 个图片…`);
    });

    try {
      const response = await batchResizeImages(
        input,
        output,
        parsedSize,
        config.thread_count,
      );

      if (response.results.length === 0 && response.errors.length === 0) {
        setSummary("输入文件夹中没有可处理的图片。");
        onStatus("输入文件夹中没有可处理的图片。");
        return;
      }

      const lines = [
        ...response.results.map(formatResultLine),
        ...response.errors.map((item) => `${item.filename}: 失败 - ${item.message}`),
      ];
      setLogLines(lines);

      const message = `处理完成：成功 ${response.results.length} 个，失败 ${response.errors.length} 个`;
      setSummary(message);
      setProgress(100);
      onStatus(message);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      setSummary(`处理失败：${message}`);
      onStatus(`处理失败：${message}`);
    } finally {
      await unlisten();
      setRunning(false);
    }
  }

  return (
    <div className="tool-form tool-form-wide">
      <div className="settings-form img-tool-form">
        <label className="field-label">输入文件夹</label>
        <div className="field-row">
          <input
            className="field-input"
            type="text"
            value={inputDir}
            onChange={(event) => setInputDir(event.target.value)}
          />
          <button
            type="button"
            className="secondary-button"
            onClick={() => browseDirectory("选择输入文件夹", setInputDir)}
          >
            浏览…
          </button>
        </div>

        <label className="field-label">输出文件夹</label>
        <div className="field-row">
          <input
            className="field-input"
            type="text"
            value={outputDir}
            onChange={(event) => setOutputDir(event.target.value)}
          />
          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              browseDirectory("选择输出文件夹", setOutputDir, outputDir)
            }
          >
            浏览…
          </button>
        </div>

        <label className="field-label" htmlFor="max-size">
          最大边长
        </label>
        <input
          id="max-size"
          className="field-input field-input-narrow"
          type="number"
          min={1}
          max={8192}
          value={maxSize}
          onChange={(event) => setMaxSize(event.target.value)}
        />
      </div>

      <button
        type="button"
        className="accent-button"
        disabled={running}
        onClick={run}
      >
        开始处理
      </button>

      <p className="muted-text">{summary}</p>
      <progress className="progress-bar" value={progress} max={100} />
      <textarea
        ref={logRef}
        className="tool-log"
        readOnly
        value={logLines.join("\n")}
      />
    </div>
  );
}

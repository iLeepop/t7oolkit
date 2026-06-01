import { useEffect, useState } from "react";
import { open } from "@tauri-apps/plugin-dialog";
import { loadConfig, saveConfig } from "../api/config";
import type { AppConfig } from "../types/tool";
import "./SettingsPanel.css";

export function SettingsPanel() {
  const [threadCount, setThreadCount] = useState("4");
  const [exportDir, setExportDir] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadConfig().then((config) => {
      setThreadCount(String(config.thread_count));
      setExportDir(config.export_dir);
    });
  }, []);

  async function browseExportDir() {
    const selected = await open({
      directory: true,
      multiple: false,
      title: "选择默认导出位置",
      defaultPath: exportDir || undefined,
    });
    if (typeof selected === "string") {
      setExportDir(selected);
    }
  }

  async function handleSave() {
    const parsed = Number.parseInt(threadCount, 10);
    if (Number.isNaN(parsed)) {
      setMessage("线程数量必须是整数。");
      return;
    }
    if (parsed < 1 || parsed > 32) {
      setMessage("线程数量需在 1 到 32 之间。");
      return;
    }

    const current = await loadConfig();
    const config: AppConfig = {
      ...current,
      thread_count: parsed,
      export_dir: exportDir.trim(),
    };

    await saveConfig(config);
    setMessage("配置已保存。");
  }

  return (
    <section className="settings-panel">
      <h2 className="section-title">基础配置</h2>
      <p className="muted-text">通用线程数量与默认导出位置将应用于各工具。</p>

      <div className="settings-form">
        <label className="field-label" htmlFor="thread-count">
          线程数量
        </label>
        <input
          id="thread-count"
          className="field-input field-input-narrow"
          type="number"
          min={1}
          max={32}
          value={threadCount}
          onChange={(event) => setThreadCount(event.target.value)}
        />

        <label className="field-label" htmlFor="export-dir">
          默认导出位置
        </label>
        <div className="field-row">
          <input
            id="export-dir"
            className="field-input"
            type="text"
            value={exportDir}
            onChange={(event) => setExportDir(event.target.value)}
          />
          <button type="button" className="secondary-button" onClick={browseExportDir}>
            浏览…
          </button>
        </div>
      </div>

      <div className="settings-actions">
        <button type="button" className="accent-button" onClick={handleSave}>
          保存
        </button>
        {message ? <p className="muted-text settings-message">{message}</p> : null}
      </div>
    </section>
  );
}

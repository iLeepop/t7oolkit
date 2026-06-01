import { useState } from "react";
import type { ToolProps } from "../types/tool";
import "../components/SettingsPanel.css";

export function DemoTextTool({ onStatus }: ToolProps) {
  const [input, setInput] = useState("Hello, t7oolkit!");
  const [result, setResult] = useState("");

  function run() {
    onStatus("处理中…");
    const text = input.trim();
    setResult(`字符数：${text.length} · 大写：${text.toUpperCase()}`);
    onStatus("处理完成");
  }

  return (
    <div className="tool-form">
      <label className="field-label" htmlFor="demo-text-input">
        输入文本
      </label>
      <input
        id="demo-text-input"
        className="field-input"
        type="text"
        value={input}
        onChange={(event) => setInput(event.target.value)}
      />
      {result ? <p className="muted-text tool-result">{result}</p> : null}
      <button type="button" className="accent-button" onClick={run}>
        运行
      </button>
    </div>
  );
}

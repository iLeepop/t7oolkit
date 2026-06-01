import { listTools } from "../registry/tools";
import type { Tool } from "../types/tool";
import "./ToolsGrid.css";

interface ToolsGridProps {
  onToolSelect: (tool: Tool) => void;
}

export function ToolsGrid({ onToolSelect }: ToolsGridProps) {
  const tools = listTools();

  return (
    <section className="tools-grid-view">
      <h2 className="section-title">工具栏</h2>
      {tools.length === 0 ? (
        <p className="muted-text">暂无已注册工具。</p>
      ) : (
        <div className="tools-grid">
          {tools.map((tool) => (
            <button
              key={tool.id}
              type="button"
              className="tool-card"
              onClick={() => onToolSelect(tool)}
            >
              <h3 className="tool-card-title">{tool.name}</h3>
              <p className="tool-card-desc">{tool.description}</p>
            </button>
          ))}
        </div>
      )}
    </section>
  );
}

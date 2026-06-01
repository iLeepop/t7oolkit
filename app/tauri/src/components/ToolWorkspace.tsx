import type { Tool } from "../types/tool";
import "./ToolWorkspace.css";

interface ToolWorkspaceProps {
  tool: Tool | null;
  onBack: () => void;
  onStatus: (message: string) => void;
}

export function ToolWorkspace({ tool, onBack, onStatus }: ToolWorkspaceProps) {
  if (!tool) {
    return null;
  }

  const ToolComponent = tool.component;

  return (
    <section className="tool-workspace">
      <div className="tool-workspace-header">
        <button type="button" className="back-button" onClick={onBack}>
          ← 返回
        </button>
        <h2 className="tool-workspace-title">{tool.name}</h2>
      </div>
      <div className="tool-workspace-body">
        <ToolComponent onStatus={onStatus} />
      </div>
    </section>
  );
}

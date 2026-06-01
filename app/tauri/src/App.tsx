import { useCallback, useState } from "react";
import { HeaderBar } from "./components/HeaderBar";
import { SettingsPanel } from "./components/SettingsPanel";
import { SidebarNav, NAV_SETTINGS, NAV_TOOLS } from "./components/SidebarNav";
import { StatusFooter } from "./components/StatusFooter";
import { ToolWorkspace } from "./components/ToolWorkspace";
import { ToolsGrid } from "./components/ToolsGrid";
import type { AppView, Tool } from "./types/tool";
import "./App.css";

function App() {
  const [sidebarActive, setSidebarActive] = useState<string>(NAV_TOOLS);
  const [view, setView] = useState<AppView>("tools");
  const [activeTool, setActiveTool] = useState<Tool | null>(null);
  const [footerMessage, setFooterMessage] = useState("就绪");

  const showToolsGrid = useCallback(() => {
    setView("tools");
    setActiveTool(null);
    setSidebarActive(NAV_TOOLS);
    setFooterMessage("就绪");
  }, []);

  const showSettings = useCallback(() => {
    setView("settings");
    setActiveTool(null);
    setSidebarActive(NAV_SETTINGS);
    setFooterMessage("基础配置");
  }, []);

  const openTool = useCallback((tool: Tool) => {
    setView("tool");
    setActiveTool(tool);
    setSidebarActive(NAV_TOOLS);
    setFooterMessage(`「${tool.name}」`);
  }, []);

  const handleNavigate = useCallback(
    (navId: string) => {
      if (navId === NAV_TOOLS) {
        showToolsGrid();
        return;
      }
      if (navId === NAV_SETTINGS) {
        showSettings();
      }
    },
    [showSettings, showToolsGrid],
  );

  const handleToolStatus = useCallback(
    (message: string) => {
      if (activeTool) {
        setFooterMessage(`「${activeTool.name}」· ${message}`);
      } else {
        setFooterMessage(message);
      }
    },
    [activeTool],
  );

  const handleBack = useCallback(() => {
    if (sidebarActive === NAV_TOOLS) {
      showToolsGrid();
    } else {
      setFooterMessage("就绪");
    }
  }, [showToolsGrid, sidebarActive]);

  return (
    <div className="app-shell">
      <HeaderBar />
      <div className="app-body">
        <SidebarNav active={sidebarActive} onNavigate={handleNavigate} />
        <main className="app-main">
          {view === "tools" ? <ToolsGrid onToolSelect={openTool} /> : null}
          {view === "settings" ? <SettingsPanel /> : null}
          {view === "tool" ? (
            <ToolWorkspace
              tool={activeTool}
              onBack={handleBack}
              onStatus={handleToolStatus}
            />
          ) : null}
        </main>
      </div>
      <StatusFooter message={footerMessage} />
    </div>
  );
}

export default App;

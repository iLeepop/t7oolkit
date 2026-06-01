import "./SidebarNav.css";

export const NAV_TOOLS = "tools";
export const NAV_SETTINGS = "settings";

interface SidebarNavProps {
  active: string;
  onNavigate: (navId: string) => void;
}

export function SidebarNav({ active, onNavigate }: SidebarNavProps) {
  const items = [
    { id: NAV_TOOLS, label: "工具栏" },
    { id: NAV_SETTINGS, label: "基础配置" },
  ];

  return (
    <nav className="sidebar-nav">
      {items.map((item) => (
        <button
          key={item.id}
          type="button"
          className={`sidebar-button ${active === item.id ? "sidebar-button-active" : ""}`}
          onClick={() => onNavigate(item.id)}
        >
          {item.label}
        </button>
      ))}
    </nav>
  );
}

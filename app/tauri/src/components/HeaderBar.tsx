import { APP_VERSION } from "../theme/colors";
import "./HeaderBar.css";

export function HeaderBar() {
  return (
    <header className="header-bar">
      <div>
        <h1 className="header-title">t7oolkit</h1>
        <p className="header-subtitle">v{APP_VERSION}</p>
      </div>
    </header>
  );
}

import "./StatusFooter.css";

interface StatusFooterProps {
  message: string;
}

export function StatusFooter({ message }: StatusFooterProps) {
  return (
    <footer className="status-footer">
      <span className="status-text">{message}</span>
    </footer>
  );
}

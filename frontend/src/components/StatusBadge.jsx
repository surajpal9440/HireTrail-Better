import { getBadgeClass, STATUS_LABELS } from "../utils/formatters";

export default function StatusBadge({ status }) {
  return (
    <span className={getBadgeClass(status)} id={`status-badge-${status}`}>
      {STATUS_LABELS[status] || status}
    </span>
  );
}

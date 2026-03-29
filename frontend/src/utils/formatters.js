export const STATUS_LABELS = {
  applied: "Applied",
  interviewing: "Interviewing",
  offer: "Offer",
  rejected: "Rejected",
  withdrawn: "Withdrawn",
};

export const ALL_STATUSES = Object.keys(STATUS_LABELS);

export function formatDate(dateStr) {
  if (!dateStr) return "—";
  return new Date(dateStr + "T00:00:00").toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function daysSince(dateStr) {
  if (!dateStr) return null;
  const diff = Date.now() - new Date(dateStr + "T00:00:00").getTime();
  return Math.floor(diff / (1000 * 60 * 60 * 24));
}

export function getBadgeClass(status) {
  return `badge badge-${status}`;
}

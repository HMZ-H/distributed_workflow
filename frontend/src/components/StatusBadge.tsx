const statusStyles: Record<string, string> = {
  draft: 'bg-text-muted/20 text-text-secondary',
  active: 'bg-success/20 text-success',
  paused: 'bg-warning/20 text-warning',
  completed: 'bg-info/20 text-info',
  failed: 'bg-error/20 text-error',
  running: 'bg-success/20 text-success',
  pending: 'bg-warning/20 text-warning',
};

export default function StatusBadge({ status }: { status: string }) {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${
        statusStyles[status] ?? statusStyles.draft
      }`}
    >
      {status}
    </span>
  );
}

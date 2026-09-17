import { Workflow } from 'lucide-react';

export default function Monitoring() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-text-primary mb-6">Monitoring</h1>

      <div className="bg-bg-secondary border border-border rounded-xl p-12 text-center">
        <Workflow size={48} className="text-text-muted mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-text-primary mb-2">Monitoring Dashboard</h3>
        <p className="text-sm text-text-secondary max-w-md mx-auto">
          System metrics, logs, and health checks will be displayed here.
          This feature is coming in a future phase.
        </p>
      </div>
    </div>
  );
}

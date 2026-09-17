import { Activity } from 'lucide-react';

export default function Executions() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-text-primary mb-6">Executions</h1>

      <div className="bg-bg-secondary border border-border rounded-xl p-12 text-center">
        <Activity size={48} className="text-text-muted mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-text-primary mb-2">No executions yet</h3>
        <p className="text-sm text-text-secondary max-w-md mx-auto">
          Workflow executions will appear here once you run a workflow.
          This feature is coming in a future phase.
        </p>
      </div>
    </div>
  );
}

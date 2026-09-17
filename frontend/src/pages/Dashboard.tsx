import { useEffect, useState } from 'react';
import { GitBranch, Activity, CheckCircle, AlertTriangle } from 'lucide-react';
import { workflowApi, type Workflow } from '../api/workflows';
import StatusBadge from '../components/StatusBadge';

interface StatCard {
  label: string;
  value: number;
  icon: React.ElementType;
  color: string;
}

export default function Dashboard() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    workflowApi
      .list()
      .then(({ data }) => setWorkflows(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const stats: StatCard[] = [
    {
      label: 'Total Workflows',
      value: workflows.length,
      icon: GitBranch,
      color: 'text-info',
    },
    {
      label: 'Active',
      value: workflows.filter((w) => w.status === 'active').length,
      icon: Activity,
      color: 'text-success',
    },
    {
      label: 'Completed',
      value: workflows.filter((w) => w.status === 'completed').length,
      icon: CheckCircle,
      color: 'text-info',
    },
    {
      label: 'Failed',
      value: workflows.filter((w) => w.status === 'failed').length,
      icon: AlertTriangle,
      color: 'text-error',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-text-primary mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map(({ label, value, icon: Icon, color }) => (
          <div
            key={label}
            className="bg-bg-secondary border border-border rounded-xl p-5"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-text-secondary">{label}</span>
              <Icon size={18} className={color} />
            </div>
            <p className="text-3xl font-bold text-text-primary tabular-nums">{value}</p>
          </div>
        ))}
      </div>

      <div className="bg-bg-secondary border border-border rounded-xl">
        <div className="px-5 py-4 border-b border-border">
          <h2 className="text-base font-semibold text-text-primary">Recent Workflows</h2>
        </div>
        {workflows.length === 0 ? (
          <div className="p-8 text-center text-text-muted text-sm">
            No workflows yet. Create your first one.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-text-secondary text-left border-b border-border">
                  <th className="px-5 py-3 font-medium">Name</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Created</th>
                  <th className="px-5 py-3 font-medium">Updated</th>
                </tr>
              </thead>
              <tbody>
                {workflows.slice(0, 5).map((w) => (
                  <tr
                    key={w.id}
                    className="border-b border-border last:border-0 hover:bg-bg-hover transition-colors"
                  >
                    <td className="px-5 py-3 text-text-primary font-medium">{w.name}</td>
                    <td className="px-5 py-3">
                      <StatusBadge status={w.status} />
                    </td>
                    <td className="px-5 py-3 text-text-secondary">
                      {new Date(w.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-5 py-3 text-text-secondary">
                      {new Date(w.updated_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

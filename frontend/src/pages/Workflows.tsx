import { useEffect, useState } from 'react';
import { Plus, Pencil, Trash2, Search } from 'lucide-react';
import { workflowApi, type Workflow, type WorkflowCreate } from '../api/workflows';
import StatusBadge from '../components/StatusBadge';

export default function Workflows() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showCreate, setShowCreate] = useState(false);
  const [editId, setEditId] = useState<string | null>(null);
  const [form, setForm] = useState<WorkflowCreate>({ name: '', description: '' });

  const load = () => {
    workflowApi
      .list()
      .then(({ data }) => setWorkflows(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const filtered = workflows.filter((w) =>
    w.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await workflowApi.create(form);
    setForm({ name: '', description: '' });
    setShowCreate(false);
    load();
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editId) return;
    await workflowApi.update(editId, form);
    setForm({ name: '', description: '' });
    setEditId(null);
    load();
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this workflow?')) return;
    await workflowApi.delete(id);
    load();
  };

  const startEdit = (w: Workflow) => {
    setEditId(w.id);
    setForm({ name: w.name, description: w.description ?? '' });
    setShowCreate(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-text-primary">Workflows</h1>
        <button
          onClick={() => {
            setShowCreate(true);
            setEditId(null);
            setForm({ name: '', description: '' });
          }}
          className="flex items-center gap-2 px-4 py-2.5 bg-accent hover:bg-accent-hover text-white rounded-lg text-sm font-medium transition-colors cursor-pointer"
        >
          <Plus size={16} />
          New Workflow
        </button>
      </div>

      {(showCreate || editId) && (
        <div className="bg-bg-secondary border border-border rounded-xl p-5 mb-6">
          <h3 className="text-base font-semibold text-text-primary mb-4">
            {editId ? 'Edit Workflow' : 'Create Workflow'}
          </h3>
          <form
            onSubmit={editId ? handleUpdate : handleCreate}
            className="flex flex-col gap-4"
          >
            <div>
              <label className="block text-sm text-text-secondary mb-1.5">Name</label>
              <input
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                className="w-full px-3 py-2.5 bg-bg-tertiary border border-border rounded-lg text-text-primary text-sm outline-none focus:border-accent transition-colors"
                placeholder="My Workflow"
              />
            </div>
            <div>
              <label className="block text-sm text-text-secondary mb-1.5">Description</label>
              <textarea
                value={form.description ?? ''}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                rows={3}
                className="w-full px-3 py-2.5 bg-bg-tertiary border border-border rounded-lg text-text-primary text-sm outline-none focus:border-accent transition-colors resize-none"
                placeholder="Optional description..."
              />
            </div>
            <div className="flex gap-3">
              <button
                type="submit"
                className="px-4 py-2.5 bg-accent hover:bg-accent-hover text-white rounded-lg text-sm font-medium transition-colors cursor-pointer"
              >
                {editId ? 'Save Changes' : 'Create'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowCreate(false);
                  setEditId(null);
                }}
                className="px-4 py-2.5 bg-bg-tertiary hover:bg-bg-hover text-text-secondary rounded-lg text-sm transition-colors cursor-pointer"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="bg-bg-secondary border border-border rounded-xl">
        <div className="px-5 py-4 border-b border-border flex items-center gap-3">
          <div className="relative flex-1 max-w-xs">
            <Search
              size={16}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted"
            />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search workflows..."
              className="w-full pl-9 pr-3 py-2 bg-bg-tertiary border border-border rounded-lg text-text-primary text-sm outline-none focus:border-accent transition-colors"
            />
          </div>
          <span className="text-sm text-text-muted">{filtered.length} workflows</span>
        </div>

        {filtered.length === 0 ? (
          <div className="p-8 text-center text-text-muted text-sm">
            {workflows.length === 0
              ? 'No workflows yet. Create your first one.'
              : 'No workflows match your search.'}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-text-secondary text-left border-b border-border">
                  <th className="px-5 py-3 font-medium">Name</th>
                  <th className="px-5 py-3 font-medium">Description</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Created</th>
                  <th className="px-5 py-3 font-medium w-24">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((w) => (
                  <tr
                    key={w.id}
                    className="border-b border-border last:border-0 hover:bg-bg-hover transition-colors"
                  >
                    <td className="px-5 py-3 text-text-primary font-medium">{w.name}</td>
                    <td className="px-5 py-3 text-text-secondary max-w-xs truncate">
                      {w.description || '—'}
                    </td>
                    <td className="px-5 py-3">
                      <StatusBadge status={w.status} />
                    </td>
                    <td className="px-5 py-3 text-text-secondary">
                      {new Date(w.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-5 py-3">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => startEdit(w)}
                          className="p-1.5 text-text-muted hover:text-text-primary hover:bg-bg-tertiary rounded-md transition-colors cursor-pointer"
                        >
                          <Pencil size={14} />
                        </button>
                        <button
                          onClick={() => handleDelete(w.id)}
                          className="p-1.5 text-text-muted hover:text-error hover:bg-error/10 rounded-md transition-colors cursor-pointer"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
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

import api from './client';

export interface Workflow {
  id: string;
  name: string;
  description: string | null;
  status: 'draft' | 'active' | 'paused' | 'completed' | 'failed';
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface WorkflowCreate {
  name: string;
  description?: string;
}

export interface WorkflowUpdate {
  name?: string;
  description?: string;
  status?: Workflow['status'];
}

export const workflowApi = {
  list() {
    return api.get<Workflow[]>('/workflows/');
  },
  get(id: string) {
    return api.get<Workflow>(`/workflows/${id}`);
  },
  create(data: WorkflowCreate) {
    return api.post<Workflow>('/workflows/', data);
  },
  update(id: string, data: WorkflowUpdate) {
    return api.put<Workflow>(`/workflows/${id}`, data);
  },
  delete(id: string) {
    return api.delete(`/workflows/${id}`);
  },
};

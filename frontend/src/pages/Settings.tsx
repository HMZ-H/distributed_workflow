import { Settings as SettingsIcon } from 'lucide-react';

export default function Settings() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-text-primary mb-6">Settings</h1>

      <div className="bg-bg-secondary border border-border rounded-xl p-12 text-center">
        <SettingsIcon size={48} className="text-text-muted mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-text-primary mb-2">Settings</h3>
        <p className="text-sm text-text-secondary max-w-md mx-auto">
          Account settings, API keys, and preferences will be available here.
          This feature is coming in a future phase.
        </p>
      </div>
    </div>
  );
}

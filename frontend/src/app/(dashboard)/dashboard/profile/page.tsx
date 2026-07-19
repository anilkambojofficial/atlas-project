"use client";

// Basic user profile (Sprint-002): identity summary + display-name edit.

import { useState } from "react";
import { authApi } from "@/lib/auth/api";
import { useAuthStore } from "@/store/auth-store";

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user);
  const roles = useAuthStore((s) => s.roles);
  const organizationId = useAuthStore((s) => s.organizationId);
  const setUser = useAuthStore((s) => s.setUser);

  const [displayName, setDisplayName] = useState(user?.displayName ?? "");
  const [status, setStatus] = useState<"idle" | "saving" | "saved" | "error">(
    "idle",
  );

  if (!user) return null;

  const save = async () => {
    setStatus("saving");
    try {
      const updated = await authApi.updateProfile(displayName.trim());
      setUser(updated);
      setStatus("saved");
    } catch {
      setStatus("error");
    }
  };

  return (
    <section className="max-w-xl space-y-6">
      <h1 className="text-2xl font-bold text-foreground">Profile</h1>

      <dl className="space-y-2 rounded-lg border border-border bg-card p-4 text-sm">
        <div className="flex justify-between">
          <dt className="text-muted-foreground">Email</dt>
          <dd className="text-foreground">{user.email}</dd>
        </div>
        <div className="flex justify-between">
          <dt className="text-muted-foreground">Status</dt>
          <dd className="text-foreground">{user.status}</dd>
        </div>
        <div className="flex justify-between">
          <dt className="text-muted-foreground">Email verified</dt>
          <dd className="text-foreground">{user.emailVerified ? "Yes" : "No"}</dd>
        </div>
        <div className="flex justify-between">
          <dt className="text-muted-foreground">Roles</dt>
          <dd className="text-foreground">{roles.join(", ") || "—"}</dd>
        </div>
        <div className="flex justify-between">
          <dt className="text-muted-foreground">Organization</dt>
          <dd className="font-mono text-xs text-foreground">
            {organizationId ?? "—"}
          </dd>
        </div>
      </dl>

      <div className="space-y-2 rounded-lg border border-border bg-card p-4">
        <label
          htmlFor="displayName"
          className="text-sm font-medium text-foreground"
        >
          Display name
        </label>
        <input
          id="displayName"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-ring"
        />
        <button
          type="button"
          onClick={save}
          disabled={status === "saving" || !displayName.trim()}
          className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:opacity-90 disabled:opacity-50"
        >
          {status === "saving" ? "Saving…" : "Save"}
        </button>
        {status === "saved" && (
          <p className="text-xs text-muted-foreground">Saved.</p>
        )}
        {status === "error" && (
          <p className="text-xs text-destructive">Save failed. Try again.</p>
        )}
      </div>
    </section>
  );
}

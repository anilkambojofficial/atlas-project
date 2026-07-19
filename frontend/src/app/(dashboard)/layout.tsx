"use client";

// Dashboard route group layout — sidebar + header shell with the Sprint-002
// route guard and user menu. Full navigation follows in IP-003 onward.

import Link from "next/link";
import { useRouter } from "next/navigation";
import { RouteGuard } from "@/components/auth/route-guard";
import { useAuthStore } from "@/store/auth-store";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  return (
    <RouteGuard>
      <div className="flex min-h-screen">
        <aside className="w-64 border-r border-border bg-card">
          <div className="flex h-16 items-center px-6">
            <span className="font-semibold text-foreground">ATLAS</span>
          </div>
          <nav className="space-y-1 px-3 text-sm">
            <Link
              href="/dashboard"
              className="block rounded-md px-3 py-2 text-foreground hover:bg-accent"
            >
              Dashboard
            </Link>
            <Link
              href="/dashboard/profile"
              className="block rounded-md px-3 py-2 text-foreground hover:bg-accent"
            >
              Profile
            </Link>
          </nav>
        </aside>

        <div className="flex flex-1 flex-col">
          <header className="flex h-16 items-center gap-4 border-b border-border bg-card px-6">
            <div className="flex-1" />
            <span className="text-sm text-muted-foreground">
              {user?.displayName ?? ""}
            </span>
            <button
              type="button"
              onClick={async () => {
                await logout();
                router.replace("/auth/login");
              }}
              className="rounded-md border border-border px-3 py-1.5 text-sm text-foreground hover:bg-accent"
            >
              Sign out
            </button>
          </header>

          <main className="flex-1 overflow-auto p-6">{children}</main>
        </div>
      </div>
    </RouteGuard>
  );
}

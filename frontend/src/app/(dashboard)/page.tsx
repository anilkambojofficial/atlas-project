import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Dashboard",
};

// Dashboard home — module widgets populated by feature IPs (IP-003 onward).
export default function DashboardPage() {
  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* Module cards — populated by IP-003 through IP-010 */}
        <div className="flex h-36 items-center justify-center rounded-lg border border-dashed border-border text-xs text-muted-foreground">
          Module widgets — IP-003 onward
        </div>
      </div>
    </section>
  );
}

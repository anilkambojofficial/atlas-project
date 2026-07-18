// Dashboard route group layout — sidebar + header shell.
// Full navigation implementation follows in IP-002 / IP-003.
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar — implementation defined during IP-002 */}
      <aside className="w-64 border-r border-border bg-card">
        <div className="flex h-16 items-center px-6">
          <span className="font-semibold text-foreground">ATLAS</span>
        </div>
        {/* Navigation links injected per module */}
      </aside>

      <div className="flex flex-1 flex-col">
        {/* Top bar — implementation defined during IP-002 */}
        <header className="flex h-16 items-center border-b border-border bg-card px-6">
          <div className="flex-1" />
          {/* User menu injected by IP-002 */}
        </header>

        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
    </div>
  );
}

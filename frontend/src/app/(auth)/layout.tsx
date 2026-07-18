// Auth route group layout — no sidebar, no header; centered shell only.
export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}

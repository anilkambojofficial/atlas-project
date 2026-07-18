import Link from "next/link";

export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-4xl font-bold text-foreground">404</h1>
      <p className="text-muted-foreground">This page could not be found.</p>
      <Link
        href="/dashboard"
        className="text-primary underline-offset-4 hover:underline"
      >
        Go to dashboard
      </Link>
    </main>
  );
}

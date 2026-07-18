import { redirect } from "next/navigation";

// Root path redirects authenticated users to the dashboard and unauthenticated
// users to the login page.  Session evaluation happens in middleware.ts —
// this redirect is the fallback for direct navigation without a cookie.
export default function RootPage() {
  redirect("/auth/login");
}

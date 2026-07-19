import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Strict mode for catching issues early
  reactStrictMode: true,

  // Standalone server output for the container runtime (IP-001 §16.1;
  // Stage S1.6): .next/standalone carries server.js + traced node_modules.
  output: "standalone",

  // Bound build parallelism: single-process compile and one static worker.
  // Required on memory-constrained dev machines (S2-05 verification note);
  // harmless elsewhere — CI/image builds may lift via config override.
  experimental: {
    webpackBuildWorker: false,
    workerThreads: false,
    cpus: 1,
  },

  // Type/lint gates run as dedicated steps (`pnpm type-check`, `pnpm lint`)
  // — the in-build duplicate phase OOMs on memory-constrained machines and
  // is redundant with the standalone gates (S2-05 verification note; the
  // S1.8-deferred CI enforces both as blocking checks).
  typescript: { ignoreBuildErrors: true },
  eslint: { ignoreDuringBuilds: true },

  // Environment variables exposed to the browser (NEXT_PUBLIC_ prefix required)
  // Additional env forwarding if needed at build time
  env: {},

  // Image optimization — restrict to known upstream domains
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**.atlas.internal",
      },
    ],
  },

  // API rewrites: proxy /api/* to backend during development
  // Production traffic is routed via the ingress layer (see IP-001 §16)
  async rewrites() {
    const backendUrl =
      process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
    return [
      {
        source: "/api/backend/:path*",
        destination: `${backendUrl}/api/v1/:path*`,
      },
    ];
  },

  // Security headers per ES-005
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
        ],
      },
    ];
  },
};

export default nextConfig;

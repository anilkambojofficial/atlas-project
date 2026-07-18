import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Strict mode for catching issues early
  reactStrictMode: true,

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

"""In-process operational metrics registry.

Governing documents:
- IP-001 §14 — every deployable service exposes ``/metrics``.
- RA-010 §5 / RA-001 §19 — mandatory service telemetry: request counts,
  error rates, latency, uptime.
- ES-006 §18 — telemetry integrates with the platform monitoring stack.

Metrics are rendered in the Prometheus text exposition format (the
Kubernetes-native scrape format used by the observability stack
established in ARCH-007/RA-010) using only the standard library, so the
Platform Foundation carries no metrics vendor dependency. Vendor
selection for the metrics backend remains "Implementation Defined During
Engineering" (BP-002 §16) and is unaffected by this exposition format.

The registry is thread-safe and label cardinality is bounded by using
matched route templates rather than raw request paths.
"""

from __future__ import annotations

import threading
import time


def _escape_label_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _labels(pairs: dict[str, str]) -> str:
    inner = ",".join(
        f'{key}="{_escape_label_value(value)}"' for key, value in sorted(pairs.items())
    )
    return "{" + inner + "}"


class MetricsRegistry:
    """Collects HTTP request metrics and renders Prometheus text format."""

    def __init__(self, service_name: str, version: str, environment: str) -> None:
        self._service_name = service_name
        self._version = version
        self._environment = environment
        self._started_at = time.time()
        self._lock = threading.Lock()
        # (method, path, status) -> request count
        self._request_counts: dict[tuple[str, str, str], int] = {}
        # (method, path) -> (total seconds, observation count)
        self._durations: dict[tuple[str, str], tuple[float, int]] = {}

    def observe_request(
        self, method: str, path: str, status_code: int, duration_seconds: float
    ) -> None:
        """Record one completed HTTP request."""
        count_key = (method, path, str(status_code))
        duration_key = (method, path)
        with self._lock:
            self._request_counts[count_key] = self._request_counts.get(count_key, 0) + 1
            total, count = self._durations.get(duration_key, (0.0, 0))
            self._durations[duration_key] = (total + duration_seconds, count + 1)

    @property
    def uptime_seconds(self) -> float:
        """Seconds since the registry (application) started."""
        return time.time() - self._started_at

    def render(self) -> str:
        """Render all metrics in Prometheus text exposition format 0.0.4."""
        with self._lock:
            request_counts = dict(self._request_counts)
            durations = dict(self._durations)

        lines: list[str] = []

        lines.append("# HELP atlas_app_info Static application information.")
        lines.append("# TYPE atlas_app_info gauge")
        lines.append(
            "atlas_app_info"
            + _labels(
                {
                    "service": self._service_name,
                    "version": self._version,
                    "environment": self._environment,
                }
            )
            + " 1"
        )

        lines.append("# HELP atlas_app_uptime_seconds Seconds since application start.")
        lines.append("# TYPE atlas_app_uptime_seconds gauge")
        lines.append(f"atlas_app_uptime_seconds {self.uptime_seconds:.3f}")

        lines.append("# HELP atlas_http_requests_total Completed HTTP requests.")
        lines.append("# TYPE atlas_http_requests_total counter")
        for (method, path, status), count in sorted(request_counts.items()):
            lines.append(
                "atlas_http_requests_total"
                + _labels({"method": method, "path": path, "status": status})
                + f" {count}"
            )

        lines.append(
            "# HELP atlas_http_request_duration_seconds "
            "Cumulative HTTP request processing time."
        )
        lines.append("# TYPE atlas_http_request_duration_seconds summary")
        for (method, path), (total, count) in sorted(durations.items()):
            label_str = _labels({"method": method, "path": path})
            lines.append(
                f"atlas_http_request_duration_seconds_sum{label_str} {total:.6f}"
            )
            lines.append(
                f"atlas_http_request_duration_seconds_count{label_str} {count}"
            )

        return "\n".join(lines) + "\n"

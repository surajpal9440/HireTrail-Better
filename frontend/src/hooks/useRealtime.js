import { useEffect, useState } from "react";

export function useRealtime(onEventReceived) {
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("hiretrail_token");
    if (!token) return;

    let eventSource;
    let retryTimeout;

    function connect() {
      // EventSource doesn't support headers, send JWT in query string
      eventSource = new EventSource(`http://localhost:5000/api/events/stream?token=${token}`);

      eventSource.onopen = () => {
        setConnected(true);
      };

      eventSource.onmessage = (e) => {
        if (!e.data || e.data === ": ping") return;
        try {
          const payload = JSON.parse(e.data);
          if (onEventReceived) {
            onEventReceived(payload);
          }
        } catch (err) {
          console.error("Failed to parse SSE event", err);
        }
      };

      eventSource.onerror = () => {
        setConnected(false);
        eventSource.close();
        // Exponential backoff or simple delay could go here
        retryTimeout = setTimeout(connect, 3000);
      };
    }

    connect();

    return () => {
      if (eventSource) {
        eventSource.close();
      }
      clearTimeout(retryTimeout);
    };
  }, [onEventReceived]);

  return { connected };
}

"""
Public Live Website Server with Cloudflare Tunnel.
Launches the Flask application and exposes it instantly on a public HTTPS URL.
"""

import os
import sys
import time
import threading
from app import app
from pycloudflared import try_cloudflare

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def start_flask(port=5000):
    # Suppress verbose Flask dev logs for cleaner output
    import logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False, threaded=True)


def main():
    port = int(os.environ.get("PORT", 5000))
    
    # 1. Start Flask in daemon thread
    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()
    time.sleep(1.5)

    # 2. Start Cloudflare Tunnel
    print("=" * 72)
    print("  CONNECTING THE DECISION COMPLETENESS ENGINE TO CLOUDFLARE...")
    print("=" * 72)

    tunnel_res = try_cloudflare(port=port, verbose=False)
    public_url = str(tunnel_res.tunnel)

    # Save to file
    with open("LIVE_URL.txt", "w", encoding="utf-8") as f:
        f.write(public_url)

    print("\n" + "=" * 72)
    print("  🚀 LIVE PUBLIC WEBSITE IS ONLINE!")
    print(f"  Public URL: {public_url}")
    print(f"  Local URL:  http://localhost:{port}")
    print("=" * 72 + "\n")

    # Flush stdout so output is captured immediately
    sys.stdout.flush()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down public server...")


if __name__ == "__main__":
    main()

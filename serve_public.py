"""
Resilient Public Live Website Server with Cloudflare Tunnel & Self-Healing Watchdog.
Ensures the public URL stays permanently connected and auto-recovers from edge drops.
"""

import os
import sys
import time
import threading
import subprocess
import urllib.request
from app import app
from pycloudflared import try_cloudflare

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def start_flask(port=5000):
    import logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False, threaded=True)


def update_presentation_url(new_url):
    """Updates the presentation and PDF if the tunnel URL changes."""
    try:
        # Re-run build_visual_presentation.py to update URL in PPTX
        subprocess.run([sys.executable, "build_visual_presentation.py"], check=True, capture_output=True)
        # Re-run convert_to_pdf.ps1
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "convert_to_pdf.ps1"], check=True, capture_output=True)
        # Copy to static
        import shutil
        shutil.copyfile("HackSprint_Decision_Completeness_Engine.pdf", "static/HackSprint_Decision_Completeness_Engine.pdf")
        shutil.copyfile("HackSprint_Decision_Completeness_Engine.pptx", "static/HackSprint_Decision_Completeness_Engine.pptx")
        print(f"  [Watchdog] Presentations synchronized with new live URL: {new_url}")
    except Exception as e:
        print(f"  [Watchdog] Warning during presentation sync: {e}")


def main():
    port = int(os.environ.get("PORT", 5000))
    
    # 1. Start Flask in daemon thread
    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()
    time.sleep(1.5)

    print("=" * 72)
    print("  CONNECTING THE DECISION COMPLETENESS ENGINE TO CLOUDFLARE...")
    print("=" * 72)

    current_url = None
    tunnel_res = None

    while True:
        try:
            # Check if tunnel is active and running
            is_alive = False
            if tunnel_res is not None and hasattr(tunnel_res, "process"):
                if tunnel_res.process.poll() is None:
                    is_alive = True

            if not is_alive:
                print("\n[Tunnel Watchdog] Launching / reconnecting Cloudflare Tunnel...")
                try:
                    try_cloudflare.terminate(port)
                except Exception:
                    pass

                tunnel_res = try_cloudflare(port=port, verbose=False)
                new_url = str(tunnel_res.tunnel)

                if new_url != current_url:
                    current_url = new_url
                    with open("LIVE_URL.txt", "w", encoding="utf-8") as f:
                        f.write(current_url)

                    print("\n" + "=" * 72)
                    print("  🚀 LIVE PUBLIC WEBSITE IS ONLINE!")
                    print(f"  Public URL: {current_url}")
                    print(f"  Local URL:  http://localhost:{port}")
                    print("=" * 72 + "\n")
                    sys.stdout.flush()

                    # Synchronize presentation documents with current URL
                    update_presentation_url(current_url)

            # Check every 10 seconds
            time.sleep(10)

        except Exception as ex:
            print(f"[Tunnel Watchdog Error] {ex}. Reconnecting in 5s...")
            time.sleep(5)


if __name__ == "__main__":
    main()

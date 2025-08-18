import subprocess
import time
import os

# Add extra blank lines here

def test_dashboard_launches():
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    proc = subprocess.Popen(
        [
            "streamlit",
            "run",
            app_path,
            "--server.headless=true",
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(__file__)
    )
    try:
        time.sleep(5)  # Reduced for CI efficiency
        assert proc.poll() is None, (
            f"Streamlit failed to launch: return code={proc.poll()}, "
            f"stderr={proc.stderr.read()}"
        )
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

# Add newline at end
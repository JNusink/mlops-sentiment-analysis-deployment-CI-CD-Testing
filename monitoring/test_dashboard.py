import subprocess
import time
import os
import logging

logging.basicConfig(level=logging.INFO)

# Two blank lines here


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
        time.sleep(20)  # Increased to 20 seconds for CI stability
        assert proc.poll() is None, (
            f"Streamlit failed to launch: return code={proc.poll()}, stderr={proc.stderr.read()}"
        )
        logging.info("Streamlit launched successfully")
    except AssertionError as e:
        logging.error(f"Test failed: {str(e)}")
        raise
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                logging.error("Process killed due to timeout")

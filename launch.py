
import os
import subprocess
import sys

backend_dir = r"c:\Users\student\Desktop\sp\fastapi_with_db-main"
os.chdir(backend_dir)
sys.path.append(backend_dir)

# Run uvicorn as a subprocess so we don't block the launcher
subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])
print("Backend server started in background from", backend_dir)

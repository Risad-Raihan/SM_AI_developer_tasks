import os
import warnings
import subprocess
import sys

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set environment variables to disable file watcher
os.environ["STREAMLIT_SERVER_WATCH_DIRS"] = "false"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

# Run Streamlit
print("Starting MediBot with warnings suppressed...")
cmd = [sys.executable, "-m", "streamlit", "run", "medibot.py", "--server.fileWatcherType", "none"]
subprocess.run(cmd) 
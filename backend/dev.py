import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.argv = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8420"]

from uvicorn.main import main

main()

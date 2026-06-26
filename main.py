import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.utils import load_environment_variables
from frontend.app import main

# Load .env
load_environment_variables()

# Start Streamlit app
main()
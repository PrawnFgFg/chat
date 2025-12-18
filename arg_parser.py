import argparse
import os
from dotenv import load_dotenv

load_dotenv()

path_to_file_history = os.getenv("PATH_TO_FILE_HISTORY")
host = os.getenv("HOST")
port = os.getenv("PORT")

def add_cli_options():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-hs", "--host",
        help="indicate host",
        default=host
    )
    
    parser.add_argument(
        '-p', '--port',
        help="indicate port",
        default=port
    )
    
    parser.add_argument(
        '-ph', '--path_history',
        help="indicate path to history file",
        default=path_to_file_history
    )
    
    return parser.parse_args()
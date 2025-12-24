import argparse
import os
from dotenv import load_dotenv

load_dotenv()

path_to_file_history = os.getenv("PATH_TO_FILE_HISTORY")
host = os.getenv("HOST")
port = os.getenv("PORT_TO_READ")
hash_token = os.getenv("HASH_TOKEN")

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
    
    parser.add_argument(
       "-n", "--nickname",
       help="indicate your name for registration",
       default="No_name"
    )
    
    parser.add_argument(
        "-t", "--token",
        help="indicate required token for authorized",
        default=hash_token
    )
    
    parser.add_argument(
        '-m', '--message',
        help="send any message to chat"
    )
    
    return parser.parse_args()
import argparse
import subprocess
import sys
import os

def install_requirements():
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_file):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_file])
    else:
        print("requirements.txt not found, skipping installation.")

def start_oauth_proxy():
    subprocess.check_call([sys.executable, '-m', 'uvicorn', 'main:app', '--reload', '--port', '8001'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local setup for Comics Timeline OAuth2 Proxy")
    parser.add_argument('-r', '--no-requirements', action='store_true',
                        help="Skip installing requirements")
    args = parser.parse_args()
    
    if not args.no_requirements:
        install_requirements()
    
    print("Starting OAuth2 Proxy on port 8001...")
    start_oauth_proxy()

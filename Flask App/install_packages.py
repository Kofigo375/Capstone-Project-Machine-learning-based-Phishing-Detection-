import subprocess
import sys

packages = [
    "ipaddress",
    "re",
    "urllib.request",
    "bs4",
    "socket",
    "requests",
    "googlesearch-python",
    "python-whois",
    "dateutil",
]

for package in packages:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")

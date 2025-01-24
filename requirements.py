# requirements.py

dependencies = [
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn"
]

def install_dependencies():
    import subprocess
    import sys
    for package in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_dependencies()

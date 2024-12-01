import subprocess
import sys


def setup():
    """Run poetry install and pre-commit install."""
    try:
        print("Installing project dependencies with Poetry...")
        subprocess.check_call(["poetry", "install"])

        print("Installing pre-commit hooks...")
        subprocess.check_call(["poetry", "run", "pre-commit", "install"])

        print("Setup completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup()

import logging
import shutil
from pathlib import Path

# Configure logging with both console and file handlers
logging.basicConfig(
    level=logging.INFO,  # Set the default logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.StreamHandler(),  # Logs will be output to the console
        logging.FileHandler("cleanup.log"),  # Logs will also be written to cleanup.log
    ],
)


def cleanup():
    """
    Cleans up the project by removing:
    - Virtual environments
    - Pre-commit hooks
    - Caches and build artifacts
    """
    project_root = Path(__file__).resolve().parent.parent  # Adjust if scripts directory is elsewhere
    logging.info(f"Project root determined as: {project_root}")

    # Define paths to clean
    paths_to_remove: list[Path] = [
        project_root / ".pytest_cache",  # Pytest cache
        project_root / ".mypy_cache",  # Mypy cache
        project_root / "build",  # Build artifacts
        project_root / "dist",  # Distribution files
        project_root / "*.egg-info",  # Egg info
        project_root / ".cache",  # General cache
    ]

    # Remove specified paths
    for path in paths_to_remove:
        # Handle wildcard patterns
        if "*" in str(path):
            parent = path.parent
            pattern = path.name
            logging.info(f"Processing wildcard pattern: {pattern} in {parent}")
            for matched in parent.glob(pattern):
                try:
                    if matched.is_dir():
                        shutil.rmtree(matched)
                        logging.info(f"Removed directory: {matched}")
                    else:
                        matched.unlink()
                        logging.info(f"Removed file: {matched}")
                except Exception as e:
                    logging.error(f"Failed to remove {matched}: {e}")
        else:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    logging.info(f"Removed directory: {path}")
                elif path.is_file():
                    path.unlink()
                    logging.info(f"Removed file: {path}")
            except FileNotFoundError:
                logging.warning(f"Path not found (skipped): {path}")
            except Exception as e:
                logging.error(f"Failed to remove {path}: {e}")

    # Remove all __pycache__ directories
    for pycache in project_root.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
            logging.info(f"Removed __pycache__: {pycache}")
        except FileNotFoundError:
            logging.warning(f"__pycache__ not found (skipped): {pycache}")
        except Exception as e:
            logging.error(f"Failed to remove __pycache__ {pycache}: {e}")

    logging.info("Cleanup completed successfully!")


if __name__ == "__main__":
    cleanup()

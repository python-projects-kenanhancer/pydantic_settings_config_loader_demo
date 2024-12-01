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
        # project_root / ".venv",  # Virtual environment
        # project_root / ".env",  # .env file
        # project_root / ".env.dev",
        # project_root / ".env.local",
        # project_root / ".env.uat",
        # project_root / ".vscode",  # VS Code settings
        project_root / ".git" / "hooks" / "pre-commit",  # Pre-commit hook
        project_root / ".pytest_cache",  # Pytest cache
        project_root / "__pycache__",  # Python cache
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

    # Optionally, reset other Git hooks to sample hooks
    hooks_dir = project_root / ".git" / "hooks"
    if hooks_dir.exists():
        logging.info(f"Resetting Git hooks in: {hooks_dir}")
        for hook in hooks_dir.iterdir():
            if hook.is_file() and not hook.name.endswith(".sample"):
                try:
                    hook.unlink()
                    logging.info(f"Removed existing hook: {hook.name}")
                    sample_hook = hooks_dir / f"{hook.name}.sample"
                    if sample_hook.exists():
                        shutil.copy(sample_hook, hook)
                        hook.chmod(0o755)
                        logging.info(f"Reset hook: {hook.name} to sample")
                    else:
                        logging.warning(f"Sample hook not found for: {hook.name}")
                except Exception as e:
                    logging.error(f"Failed to reset hook {hook.name}: {e}")
    else:
        logging.warning(f"Hooks directory does not exist: {hooks_dir}")

    logging.info("Cleanup completed successfully!")


if __name__ == "__main__":
    cleanup()

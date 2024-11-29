# Pydantic Settings Config Loader Demo

This project, `pydantic_settings_config_loader_demo`, demonstrates the use of Pydantic for data validation and settings management. It includes configuration using Poetry for dependency management and pytest for testing.

---

## Prerequisites

### Required Programs

Before setting up this project, ensure the following programs are installed:

### Homebrew

Homebrew is a package manager for macOS, used to install other tools like `asdf` and `jq`.  
Installation:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### jq

jq is a lightweight and flexible command-line JSON processor, used for automating JSON file generation.
Installation:

```bash
brew install jq
```

### asdf

asdf is a version manager for multiple runtimes like Python, Node.js, Java, Go, etc.
Installation:

```bash
brew install asdf
```

Add asdf to your shell by adding the following lines to your shell configuration (~/.zshrc or ~/.bashrc):

For `~/.zshrc`:

```bash
echo '. $(brew --prefix asdf)/libexec/asdf.sh' >> ~/.zshrc
```

For `~/.bashrc`:

```bash
echo '. $(brew --prefix asdf)/libexec/asdf.sh' >> ~/.bashrc
```

After adding the line, reload the shell configuration file for the changes to take effect:

For `~/.zshrc`:

```bash
source ~/.zshrc
```

For `~/.bashrc`:

```bash
source ~/.bashrc
```

### python

Install the Python plugin and Python 3.11.8 using asdf:

```bash
asdf plugin add python
asdf install python 3.11.8
asdf global python 3.11.8
```

Verify the installation:

```bash
python --version
```

### poetry

Poetry is a dependency and environment management tool for Python, designed to simplify the process of managing Python packages and virtual environments.

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Automating VS Code Extensions Setup

To ensure all team members use the same set of VS Code extensions, you can automate the generation of the .vscode/extensions.json file. This file contains recommendations for the extensions required for this project.

Generate the extensions.json File
Run the following command in the project directory:

```bash
code --list-extensions | jq -R . | jq -s '{ "recommendations": . }' > .vscode/extensions.json
```

This will create or overwrite the .vscode/extensions.json file with a list of currently installed extensions, formatted for VS Code's recommendations.

## Setting Up the Project

1. Clone the Repository:

```bash
git clone <repository-url>
cd pydantic_settings_config_loader_demo
```

2. Install Dependencies:

```bash
poetry install
```

3. Run Tests: Run the tests using pytest:

```bash
poetry run pytest
```

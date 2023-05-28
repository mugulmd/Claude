# Install

## Claude server

Requirements:
- Git
- Python >= 3.10

It is recommended to install Claude in a virtual environment.

Installation steps:
```
git clone git@github.com:mugulmd/Claude.git
cd Claude
python -m pip install -r requirements.txt
```

## Sardine extension

Copy `sardine-config.json` to the folder of your choice (for example a folder where you keep all your Sardine extensions).

Open the configuration file and edit the `root` field by writing the actual filepath to your Claude repository.

Open Sardine's user configuration file and add the filepath to Claude's configuration file in the `extensions` list field.

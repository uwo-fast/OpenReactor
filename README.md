# OpenReactor
An easily extensible open source turbidostat with pH and dissolved oxygen control, written in python3.

## Installation

### For Linux/macOS
```sh
# Clone and enter repository
git clone https://gitlab.com/mtu-most/most_openreactor
cd most_openreactor

# Update all submodules
git submodule update --init --recursive

# Create and configure python virtual enviroment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### For Windows
```sh
# Clone and enter repository
git clone https://gitlab.com/mtu-most/most_openreactor
cd most_openreactor

# Update all submodules
git submodule update --init --recursive

# Create and configure python virtual enviroment
python3 -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## Running
```sh
export FLASK_APP=app; export FLASK_ENV=development; flask run
```

## Updating
```sh
git pull --all
git submodule foreach git pull
```

## Reseting python enviroment when done running
```sh
deactivate
```

## Credits
Icons from [feathericons](https://feathericons.com)

Opensource logo from [Remix Icom](https://remixicon.com/)

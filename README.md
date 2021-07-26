# OpenReactor
An easily extensible open source turbidostat with pH and dissolved oxygen control, written in python3.

## Installation
```bash
# Clone and enter repository
git clone https://gitlab.com/mtu-most/most_openreactor
cd most_openreactor

# Update all submodules
git submodule update --init --recursive

# Create and configure python virtual enviroment
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running
```bash
export FLASK_APP=app; export FLASK_ENV=development; flask run
```

## Updating
```bash
git pull --all
git submodule foreach git pull
```

## Reseting python enviroment when done running
```bash
deactivate
```

## Credits
Icons from [feathericons](https://feathericons.com)

Opensource logo from [Remix Icom](https://remixicon.com/)

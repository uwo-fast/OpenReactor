# OpenReactor
An easily extensible open source turbidostat with pH and dissolved oxygen control, written in python3.

# Installation

### For Linux Systems
```sh
# Make sure git is installed
sudo apt install -y git

# Clone and enter repository
git clone https://gitlab.com/mtu-most/most_openreactor
cd most_openreactor

# Run setup script
./first_time_setup.sh
```

## Running
```sh
./start.sh
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

# Setup




## Credits
Icons from [feathericons](https://feathericons.com)

Opensource logo from [Remix Icom](https://remixicon.com/)

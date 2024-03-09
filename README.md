## Installation

To active your venv, run `source venv/bin/activate`, to deactivate run `deactivate`

Install dependencies from within a venv

```bash
pip install -r requirements.txt
```

Create a `config.yml` file to specify what modules you want to run (look at `config.yml.example`)

## Running
start the program by running `./run`, stop the program by running `./stop`

## Setting up Systemctl

```
cd /etc/systemd/system
sudo ln -s /home/pi/display/led-display/service
sudo systemctl enable led-display
sudo reboot
```

The display should start at boot now


## Creating a module
To add a module:

1. Create a folder with the name of your module
1. in `__init__.py`, create a class called `Screen(BaseModule)` and implement your screen there
1. in `config.yml`, add your screen along with it's display_name and any other args
1. (optional) include any library code or README.md for any module specific setup


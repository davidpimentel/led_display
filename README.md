## Installation

To active your venv, run `source venv/bin/activate`, to deactivate run `deactivate`

Install dependencies from within a venv

```bash
pip install -r requirements.txt
```

Create a `config.yml` file to specify what modules you want to run

## Running
start the program by running `./run`, stop the program by running `./stop`

## Enable MQTT support
- Create an account at io.adafruit.com. go to Feeds > view all.
- Create a new group called `LED Display`
- Create a feed within that group called `change_display`
- be sure to set the following env variables
  ```
  ENABLE_ADAFRUIT_MQTT=true
  ADAFRUIT_IO_USERNAME=ADAFRUIT_USERNAME
  ADAFRUIT_IO_KEY=ADAFRUIT_KEY
  ```


## Creating a module
To add a module:

1. Create a folder with the name of your module
1. in `__init__.py`, create a class called `Screen(BaseModule)` and implement your screen there
1. in `config.yml`, add your screen along with it's display_name and any other args
1. (optional) include any library code or README.md for any module specific setup


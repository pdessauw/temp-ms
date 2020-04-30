from library.commands.sensors import SensorsCommandfrom library.commands.sensors import SensorsCommand# Temperature Monitor System

## Disclaimer

This temperature monitor system has been tested on Ubuntu 18.04LTS. Other 
distributions are not supported by this tool. Use it at your own risks. 

## Prerequisites

The following package need to be installed:
* lm-sensors
* mailutils

In addition, Python >= 3.6 should be available on the system. If available, use
a virtual environment (venv or conda). Make sure `pip` is available as well.

## Installation

Download this repository with `git clone https://github.com/pdessauw/temp-ms.git`. 

The script `install.sh` will install the script in the desired location. By default, 
this location is defined at:
```shell script
INSTALL_DIR="/usr/local/bin/monitor"
```

Once correctly configured, type: 
```shell script
sudo ./install.sh
pip install -r requirements.txt
```

## Configuration

The file `settings.py` contains the needed configuration keys for the app. If you do not 
have a NVidia Graphic Card, you can change the `COMMANDS` key as this: 
```python
COMMANDS = [
    SensorsCommand,
    # NvidiaSmiCommand
]
```

Configure your email address with the `ALERTS['recipient']` key. Formatting of the email 
can also be changed by editing the files in the **mail/** folder.

## Usage

There are 3 main scripts in this repository:
* `report.py`, logging the values gathered by *lm-sensors*,
* `alerting.py`, notfiying the admin by mail if values are over their baseline,
* `baseline.py`, to configure the baseline for every metric.


### Reporting / Logging

To log an entry, simply type `python ./report.py`. This will append the log file already
existing or create new ones if it needs. Setup a `crontab` entry to automatically log
the temperature reports.

### Alerting

Alerting takes two optional parameters:
* `--time`, which default to the setting `ALERT_TIMEFRAME_MINUTES`, is the number of 
minutes to look at for reporting.
* `--all`, defines if the mail should be sent with values in the normal range.

Here are some examples to launch the alerting script: 
```shell script
# Send a mail summarizing the last 60 minutes with all metrics
python ./alerting.py --time 60 --all  
# Send a mail summarizing the last 15 minutes only with over the limit metrics
python ./alerting.py --time 15
```

### Baseline definition

The baseline script allows to define baseline for the metrics logged on the system. To
initialize the metrics based on the log files type `python ./baseline.py --init`.

These baseline metrics are used by the alerting system to test if metrics are too high.
All the collected baseline can be listed with `python ./baseline.py --list`.

Some baseline metrics might not be well defined. They can be tweaked using:
```shell script
python ./baseline --set baseline_1.name_1=value_1 ... --set baseline_n.name_n=value_n
```

# ch341eeprom-factory
Firmware generation and programming workflow for CH341A / CH341F system EEPROM, adapted for uMesh production.

This project is based on [MtnMesh/ch341eeprom-factory](https://github.com/MtnMesh/ch341eeprom-factory/) and modified to fit the uMesh firmware production process.  
Special thanks to the original author for their code — in the spirit of open source, I am publishing my work here.

⚠️ **Note:** This fork is intended **only for uMesh**. It is **not suitable for other LoRa-USB Meshtastic devices**.  
If you need support for those devices, please refer to [MtnMesh/ch341eeprom-factory](https://github.com/MtnMesh/ch341eeprom-factory/).

## Usage
```
usage: ch341_factory.py [-h] [--major-version MAJORVERSION] [--minor-version MINORVERSION] [-r RANDOM]

CH341 EEPROM Intel HEX generator

options:
  -h, --help            show this help message and exit
  --major-version MAJORVERSION
                        Major version number (default: 1)
  --minor-version MINORVERSION
                        Minor version number (default: 0)
  -r RANDOM, --random RANDOM
                        Specify random digits (00-99). If not provided, a random number between 0-99 will be generated

```


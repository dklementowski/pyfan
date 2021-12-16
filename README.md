# PyFAN

A simple utility for controling PWM fans speed based on NVIDIA GPU temperature (or potentialy based on any other measure) under GNU/Linux. It's made for controling airflow in PC case based on how hot the GPU is getting.

Additionaly, instead of simply using the temperature value, it calculates the avarage temperature in last 30 seconds, so that fans dont't spin quickly for few seconds, which in this case is unnecessary and annoying.

## Disclaimer
**I'M NOT GOING TO TAKE ANY RESPONSIBILITY FOR DAMAGE CAUSED BY THE UTILITY. USE WISELY!**

## Requirements
  * Python 3.9
  * NVIDIA proprietary drivers and nvidia-smi tool
  * Linux compatible motherboard (hwmon interface should expose PWM controls)

## Configuration
Investigate config.json and tweak it to your needs. The fan steps are stored in format [X, Y] where X is the temperature and Y is target fan speed %.

## Usage
Run `./pyfan.py` as root and make it running as a deamon however you want.
I'd like to make it eaier to use, but maybe later?

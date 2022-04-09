#!/usr/bin/env python3

import config, hwmon, nvidia, datacollector
import sys, time, json

fans = config.Config().data['fans']

collector = datacollector.DataCollector(nvidia.temp)
collector.start()

def get_target_speed(fan_steps, compare_value):
    target = None
    for i, val in enumerate(fan_steps):
        item = fan_steps[i][0]
        next_item = fan_steps[i+1][0] if len(fan_steps) >= i+2 else fan_steps[-1][0]

        if item <= compare_value <= next_item:
            target = fan_steps[i]

    return target[1]

def loop():
    devices = hwmon.get_devices()

    while True:
        for fan in fans:
            target_device = None
            for device in devices:
                if device.device_path == fan['device_path']:
                    target_device = device

            if target_device == None:
                sys.stderr.write('hwmon interaface for {0} not found!\nSkipping'.format(fan['device_path']))
                continue

            pwm = hwmon.Pwm(target_device, fan['pwm_id'])
            target_speed = get_target_speed(fan['fan_steps'], collector.average) / 100

            pwm.set_control(True)
            pwm.set_speed(target_speed)

        time.sleep(1)

if __name__ == '__main__':
    loop()

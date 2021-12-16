#!/usr/bin/env python3

import hwmon, nvidia, datacollector, time, json

with open('config.json', 'r') as config_file:
    fans = json.loads(config_file.read())
    config_file.close()

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
            device = None
            for key, val in devices.items():
                if key == fan['device_name']:
                    device = val

            pwm = hwmon.Pwm(device, fan['pwm_id'])
            target_speed = get_target_speed(fan['fan_steps'], collector.average) / 100

            #print('setting {0}% to {1} on {2}'.format(int(target_speed * 100), pwm.pwm_id, device.name))
            pwm.set_control(True)
            pwm.set_speed(target_speed)
        time.sleep(1)
        #print()

if __name__ == '__main__':
    loop()

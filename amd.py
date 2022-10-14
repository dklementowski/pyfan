import hwmon
import os.path

devices = hwmon.get_devices()
amdgpu = None

for dev in devices:
    if dev.name == 'amdgpu':
        amdgpu = dev

if amdgpu == None:
    raise Exception('No AMD GPU found')

def temp():
    with open(os.path.join(amdgpu.hwmon_path, 'temp1_input'), 'r') as f:
        return int(f.read().strip()) / 1000

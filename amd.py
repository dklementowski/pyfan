import hwmon
import os.path

devices = hwmon.get_devices()
amdgpu = None

for dev in devices:
<<<<<<< HEAD
    if dev.name == 'amdgpu':
        amdgpu = dev
=======
    print(dev.name)
    if dev.name == 'amdgpu':
        amdgpu = dev
        break
>>>>>>> 4e6366c (Switch to AMD)

if amdgpu == None:
    raise Exception('No AMD GPU found')

def temp():
    with open(os.path.join(amdgpu.hwmon_path, 'temp1_input'), 'r') as f:
        return int(f.read().strip()) / 1000

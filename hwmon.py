import os.path, os, re, math

HWMON_BASE_PATH = '/sys/class/hwmon'

def get_devices():
    devices = []

    for root, dirs, files in os.walk(HWMON_BASE_PATH):
        for dir in dirs:
            devices.append(HwmonDevice(dir))

    return devices

class HwmonDevice:
    def __init__(self, hwmon_id):
        hwmon_path = os.path.join(HWMON_BASE_PATH, hwmon_id)

        if not os.path.isdir(hwmon_path):
            raise Exception('Wrong hwmon_id: {0}'.format(hwmon_id))

        self.hwmon_id = hwmon_id
        self.hwmon_path = hwmon_path

    @property
    def id(self):
        return self.hwmon_id

    @property
    def device_path(self):
        return os.path.realpath(os.path.join(self.hwmon_path, 'device'))

    @property
    def controlable(self):
        for root, dirs, files in os.walk(self.hwmon_path):
            for file in files:
                if file.startswith('pwm'):
                    return True
        return False

    @property
    def has_fans(self):
        for root, dirs, files in os.walk(self.hwmon_path):
            for file in files:
                if file.startswith('fan'):
                    return True
        return False

    @property
    def fans(self):
        fans = []
        for root, dirs, files in os.walk(self.hwmon_path):
            for file in files:
                if re.match('^fan[0-9]+_input$', file):
                    fans.append(file.replace('_input', ''))
        return fans

    @property
    def pwms(self):
        pwms = []
        for root, dirs, files in os.walk(self.hwmon_path):
            for file in files:
                if re.match('^pwm[0-9]+$', file):
                    pwms.append(file)
        return pwms

class Pwm:
    def __init__(self, hwmon_device: HwmonDevice, pwm_id: int):
        if not hwmon_device.controlable:
            raise Exception('{0} is not controlable'.format(hwmon_device.id))

        if 'pwm{0}'.format(pwm_id) not in hwmon_device.pwms:
            raise Exception('No PWM {0} in {1}'.format(pwm_id, hwmon_device.id))

        self.hwmon_device = hwmon_device
        self.pwm_id = pwm_id

    @property
    def controled(self):
        with open(os.path.join(self.hwmon_device.hwmon_path, 'pwm{0}_enable'.format(self.pwm_id)), 'r') as file:
            state = file.readline().strip()
            file.close()
            return state == '1'

    def set_control(self, state = True):
        with open(os.path.join(self.hwmon_device.hwmon_path, 'pwm{0}_enable'.format(self.pwm_id)), 'w') as file:
            file.write('1' if state else '2')
            file.close()

    def set_speed(self, speed: float):
        with open(os.path.join(self.hwmon_device.hwmon_path, 'pwm{0}'.format(self.pwm_id)), 'w') as file:
            file.write(str(math.ceil(speed * 255)))
            file.close()

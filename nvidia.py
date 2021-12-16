import subprocess

def temp():
    return int(subprocess.check_output(
        ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader']
    ).decode().strip())

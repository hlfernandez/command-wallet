import subprocess
from threading import Thread
 
# res = subprocess.run('nohup ls -lh /tmp', shell=True, check=True, capture_output=True)
# res = subprocess.run('nohup ls -lh /tmp > /tmp/out.txt', shell=True, check=True)
 
# print("Returned Value: ", res)

import subprocess

def run_command(command, output_callback=None):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if output_callback is not None:
        thread = Thread(target = output_callback, args = (process, ))
        thread.start()
    return process

if __name__ == '__main__':
    command = "ls /tmp/awsdasd"

    def process_command_output(process):
        # Monitor the command's output
        while True:
            # Read a line of output from the process
            output = process.stdout.readline()
            error = process.stderr.readline()
            # Check if the process has finished
            if process.poll() is not None:
                break
            
            # Print the output
            print(output, end='')
            print(error, end='')

    process = run_command(command, process_command_output)

    print('After run')

    while process.poll() is None:
        continue
    print('Finished: {}'.format(process.returncode))
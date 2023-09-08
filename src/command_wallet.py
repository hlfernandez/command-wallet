import tkinter as tk
import datetime

from src.runner import run_command
from src.gui_components import LabelInput


class ControlFrame(tk.Frame):

    def __init__(self, parent, app_name_label, on_run_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.columnconfigure(0, weight=1)

        tk.Label(self, text=app_name_label,
                 font=('TkDefaultFont', 15)).grid()

        self.command_input = tk.StringVar()
        self.command_input.set('docker run --rm hello-world')
        LabelInput(self, 'Command', tk.Entry,
                   {'bg': 'white', 'textvariable': self.command_input}
                   ).grid(sticky=tk.E + tk.W)

        subframe_buttons = tk.Frame(self)
        subframe_buttons.grid(sticky=tk.E + tk.W)
        run_btn = tk.Button(subframe_buttons, text='Run',
                            command=on_run_callback)
        run_btn.pack(side=tk.LEFT)

    def get_input_command(self):
        return self.command_input.get()


class CommandWalletApplication(tk.Tk):
    APP_NAME = 'Command Wallet v0.1.0'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(self.APP_NAME)
        self.attributes('-zoomed', True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.frame_top = ControlFrame(self, self.APP_NAME, self.on_run)
        self.frame_top.grid(row=0, column=0, sticky='WENS', padx=10, pady=20)

        frame_console = tk.LabelFrame(self, text='Log')
        frame_console.grid(row=1, column=0, sticky='WENS', padx=10, pady=10)
        frame_console.columnconfigure(0, weight=1)
        frame_console.columnconfigure(1, weight=0)
        frame_console.rowconfigure(1, weight=1)

        self.console_log = tk.Text(frame_console, bg='white')
        console_log_scroll = tk.Scrollbar(
            frame_console, command=self.console_log.yview)
        self.console_log.configure(yscrollcommand=console_log_scroll.set)
        self.console_log.grid(row=1, column=0, sticky='WENS')
        console_log_scroll.grid(row=1, column=1, sticky='NS')

    def on_run(self):
        cmd = self.frame_top.get_input_command()

        self.log_message('Started: {}'.format(cmd))

        run_command(cmd, self.process_command_output)

    def process_command_output(self, process):
        while True:
            output = process.stdout.readline()
            error = process.stderr.readline()

            if not output and not error:
                break

            if output:
                self.append_log_console('[stdout] {}'.format(output))
            if error:
                self.append_log_console('[stderr] {}'.format(error))

        process.poll()
        self.log_message('Finished: {}'.format(process.returncode))

    def log_message(self, message):
        self.append_log_console(
            '\n[command-wallet] ({date}) {message}\n\n'.format(date=self.get_timestamp(), message=message))

    def append_log_console(self, message):
        self.console_log.insert(tk.END, message)
        self.console_log.yview_moveto(1)

    def get_timestamp(self):
        return str(datetime.datetime.now())


if __name__ == '__main__':
    CommandWalletApplication().mainloop()

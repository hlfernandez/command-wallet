import tkinter as tk
from src.runner import run_command
from src.gui_components import LabelInput


class CommandWalletApplication(tk.Tk):
    APP_NAME = 'Command Wallet v0.1.0'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(self.APP_NAME)
        self.attributes('-zoomed', True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        frame_top = tk.Frame(self)
        frame_top.columnconfigure(0, weight=1)
        frame_top.grid(row=0, column=0, sticky='WENS', padx=10, pady=20)

        tk.Label(frame_top, text=self.APP_NAME,
                 font=('TkDefaultFont', 15)).grid()

        command_input = tk.StringVar()
        command_input.set('docker run --rm hello-world')
        LabelInput(frame_top, 'Command', tk.Entry,
                   {'bg': 'white', 'textvariable': command_input}
                   ).grid(sticky=tk.E + tk.W)

        subframe_buttons = tk.Frame(frame_top)
        subframe_buttons.grid(sticky=tk.E + tk.W)
        run_btn = tk.Button(subframe_buttons, text='Run')
        run_btn.grid(sticky=tk.E)

        frame_console = tk.LabelFrame(self, text='Log')
        frame_console.grid(row=1, column=0, sticky='WENS', padx=10, pady=10)
        frame_console.columnconfigure(0, weight=1)
        frame_console.columnconfigure(1, weight=0)
        frame_console.rowconfigure(1, weight=1)

        console_log = tk.Text(frame_console, bg='white')
        console_log_scroll = tk.Scrollbar(
            frame_console, command=console_log.yview)
        console_log.configure(yscrollcommand=console_log_scroll.set)
        console_log.grid(row=1, column=0, sticky='WENS')
        console_log_scroll.grid(row=1, column=1, sticky='NS')

        def process_command_output(process):
            while True:
                output = process.stdout.readline()
                error = process.stderr.readline()

                if not output and not error:
                    break

                if output:
                    console_log.insert(tk.END, '[stdout] {}'.format(output))
                if error:
                    console_log.insert(tk.END, '[stderr] {}'.format(error))
                console_log.yview_moveto(1)

            process.poll()
            # TODO: insert timestamp in log messages
            console_log.insert(
                tk.END, '\n[command-wallet] Finished: {}\n'.format(process.returncode))
            console_log.yview_moveto(1)

        def on_run():
            console_log.insert(
                tk.END, '\n[command-wallet] Started: {}\n\n'.format(command_input.get()))

            run_command(command_input.get(), process_command_output)

        run_btn.configure(command=on_run)


if __name__ == '__main__':
    CommandWalletApplication().mainloop()

import tkinter as tk
import subprocess
import threading
import sys
import os

class ConsoleRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.config(text=str)
        self.text_widget.update_idletasks()

    def flush(self):
        pass

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.output_label = tk.Label(self, text="")
        self.output_label.pack()

        sys.stdout = ConsoleRedirector(self.output_label)

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Atacar cidadelas"
        self.hi_there["command"] = self.atacar_cidadelas
        self.hi_there.pack(side="top")

        self.calibrar = tk.Button(self)
        self.calibrar["text"] = "Calibrar"
        self.calibrar["command"] = self.calibrar
        self.calibrar.pack(side="top")

        self.quit = tk.Button(self, text="Fechar", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def atacar_cidadelas(self):
        def run_script():
            process = subprocess.Popen(['venv\Scripts\python', 'cidadelas.py'], stdout=subprocess.PIPE)
            output, error = process.communicate()
            print(output.decode())
        thread = threading.Thread(target=run_script)
        thread.start()

    def calibrar(self):
        def run_script():
            process = subprocess.Popen(['venv\Scripts\python', 'calibrar.py'], stdout=subprocess.PIPE)
            output, error = process.communicate()
            print(output.decode())
        thread = threading.Thread(target=run_script)
        thread.start()

root = tk.Tk()
app = Application(master=root)
app.mainloop()

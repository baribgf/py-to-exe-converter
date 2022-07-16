import os
import shutil
import subprocess
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from resources.pygubu.widgets.pathchooserinput import PathChooserInput
from tkinter.scrolledtext import ScrolledText

class ProcessThread(threading.Thread):
    def __init__(self, ThreadName, ExeName, OutDirPath):
        threading.Thread.__init__(self)
        self.ThreadName = ThreadName
        self.ExeName = ExeName
        self.OutDirPath = OutDirPath

    def run(self):
        print(f"Starting Process: {self.ThreadName}\n")
        subprocess.call([".\\batch_call.bat"], shell=False)
        print(f"Finishing Process: {self.ThreadName}\n")

        # <Finalizing Operation>
        # Moving "EXE's" dir to the path specified in "OutDirPath"
        src_dir = "./dist"
        dest_dir = ""
            
        if self.OutDirPath != "":
            dest_dir = self.OutDirPath
            try:
                os.mkdir(dest_dir)
            except FileExistsError:
                pass
            try:
                shutil.move(os.path.join(src_dir, self.ExeName), dest_dir)
            except:
                shutil.move(os.path.join(src_dir, f"{self.ExeName}.exe"), dest_dir)

        else:
            dest_dir = os.path.dirname(__file__)+src_dir.replace('.', '')
                
        # Remove cache files
        try:
            os.remove(".\\batch_call.bat")
            os.remove(f".\\{self.ExeName}.spec")
        except FileNotFoundError:
            pass
        # </Finalizing Operation>

        # Prompting Operation Result
        messagebox.showinfo("Operation End", f"The operation ended succesfully.\nYour output is in : {dest_dir}")

class MainFrame:
    MainImplementationVar = 0
    def __init__(self, master):
        self.master = master
        self.master.title("Py to exe Converter")
        self.frm_main = tk.Frame(self.master, height=300, width=400)

        self.lbl_header = tk.Label(self.frm_main, font="{JetBrains Mono} 12 {bold}", text="--------------------\nPY to EXE Converter\n--------------------")
        self.lbl_header.grid(column=0, columnspan=2, row=0)

        self.lbl_script_loc = tk.Label(self.frm_main, text="Script location ->")
        self.lbl_script_loc.grid(column=0, pady=5, row=1)

        self.pathchooser_script_loc = PathChooserInput(self.frm_main)
        self.pathchooser_script_loc.configure(type="file")
        self.pathchooser_script_loc.grid(column=1, row=1, ipadx=40, padx=10)

        self.radbtn_onedir_var = tk.IntVar()
        self.radbtn_onefile_var = tk.IntVar()
        self.radbtn_console_based_var = tk.BooleanVar()
        self.radbtn_window_based_var = tk.BooleanVar()

        self.radbtn_onedir = ttk.Radiobutton(self.frm_main, text="One Directory", variable=self.radbtn_onedir_var, command=lambda:self.radbtn_onefile_var.set(0))
        self.radbtn_onedir.grid(column=0, padx=10, pady=5, row=2, sticky="w")
        self.radbtn_onedir_var.set(1)

        self.radbtn_onefile = ttk.Radiobutton(self.frm_main, text="One File", variable=self.radbtn_onefile_var , command=lambda:self.radbtn_onedir_var.set(0))
        self.radbtn_onefile.grid(column=1, padx=10, pady=5, row=2, sticky="w")

        self.radbtn_console_based = ttk.Radiobutton(self.frm_main, text="Console Based", variable=self.radbtn_console_based_var, command=lambda:self.radbtn_window_based_var.set(False))
        self.radbtn_console_based.grid(column=0, padx=10, pady=2, row=3, sticky="w")
        self.radbtn_console_based_var.set(True)

        self.radbtn_window_based = ttk.Radiobutton(self.frm_main, text="Window Based (hide the console)", variable=self.radbtn_window_based_var, command=lambda:self.radbtn_console_based_var.set(False))
        self.radbtn_window_based.grid(column=1, padx=10, pady=2, row=3, sticky="w")

        self.lbl_name = tk.Label(self.frm_main, text="Name ->")
        self.lbl_name.grid(column=0, pady=5, row=4)

        self.entry_name = ttk.Entry(self.frm_main)
        self.entry_name.grid(column=1, padx=10, pady=5, row=4, sticky="w", ipadx=20)
        self.entry_name.insert(0, "out-exe")

        self.lbl_out_dir = tk.Label(self.frm_main, text="Output Directory ->")
        self.lbl_out_dir.grid(column=0, pady=5, row=5)

        self.pathchooser_out_dir = PathChooserInput(self.frm_main)
        self.pathchooser_out_dir.configure(type="dir")
        self.pathchooser_out_dir.grid(column=1, row=5, ipadx=40, padx=10)

        self.lbl_icon = tk.Label(self.frm_main, text="Icon ->")
        self.lbl_icon.grid(column=0, pady=5, row=6)

        self.pathchooser_icon = PathChooserInput(self.frm_main)
        self.pathchooser_icon.configure(type="file")
        self.pathchooser_icon.grid(column=1, row=6, ipadx=40, padx=10)

        self.lbl_add_data = tk.Label(self.frm_main, text="Add files and folders (Every path ends with ';' )")
        self.lbl_add_data.grid(column=0, columnspan=2, padx=10, row=7, sticky="w")

        self.txtfiled_add_data = ScrolledText(self.frm_main, font="{Consolas} 10 {italic}", height=5, width=48, wrap="word")
        self.txtfiled_add_data.grid(column=0, columnspan=2, padx=10, pady=2, row=8, sticky="w")

        self.btn_convert = ttk.Button(self.frm_main, text="Convert", command=self.convert)
        self.btn_convert.grid(column=0, padx=10, pady=8, row=9, sticky="w")

        self.btn_about = ttk.Button(self.frm_main, text="About", command=lambda:messagebox.showinfo("About", "Developed by : Bari BGF\nE-mail : bougafa.005@gmail.com\nFor any Feedback, please contact me."))
        self.btn_about.grid(column=1, padx=10, pady=8, row=9, sticky="e")

        self.frm_main.pack(expand="true", fill="both", side="top")

    def convert(self):
        try:
            OnedirOrOnefile = None
            ConsoleOrWindowed = None
            Icon = ""
            AddData = ""
            Name = "out-exe"

            if self.radbtn_onedir_var.get() == 0:
                OnedirOrOnefile = "--onefile"
            else:
                OnedirOrOnefile = "--onedir"

            if self.radbtn_console_based_var.get() == 0:
                ConsoleOrWindowed = "--windowed"
            else:
                ConsoleOrWindowed = "--console"

            # <Checking data validation>
            try:
                assert os.path.isfile(self.pathchooser_script_loc.cget('path'))
            except AssertionError:
                messagebox.showerror("Error", "Please specify valid Script location path!")
                raise AssertionError
            try:
                assert self.entry_name.get() != ""
                Name = self.entry_name.get()
            except AssertionError:
                messagebox.showwarning("Warning", "The Name entry is empty so it will take the default value")
            try:
                if self.pathchooser_icon.cget('path') != "":
                    assert os.path.isfile(self.pathchooser_icon.cget('path'))
                    Icon = f"{self.pathchooser_icon.cget('path')}"
            except AssertionError:
                messagebox.showwarning("Warning", "The Icon path is not valid, so it will take the default value")
            try:
                list_of_paths = self.txtfiled_add_data.get("0.0", tk.END).split(';')
                list_of_paths.pop(-1)
                for path in list_of_paths:
                    if os.path.isdir(path):
                        AddData += f' --add-data "{path};{os.path.basename(path)}/"'
                    elif os.path.isfile(path):
                        AddData += f' --add-data "{path};."'
                    elif path == "":
                        pass
                    else:
                        messagebox.showerror("Error", "Please specify valid locations paths!")
                        raise AssertionError
            except AssertionError:
                raise AssertionError
            # </Checking data validation>
            
            # <Performing Converting Operation>
            with open(".\\batch_call.bat", 'w+') as bat_file:
                bat_file.write(f""" "./resources/pyinsta.exe" --noconfirm {OnedirOrOnefile} {ConsoleOrWindowed} {AddData} --name "{Name}" --icon "{Icon}" "{self.pathchooser_script_loc.cget('path')}"
                pause """)

            self.MainImplementationVar += 1
            ProcessThread(f"Process ~{self.MainImplementationVar}~", Name, self.pathchooser_out_dir.cget('path')).start()
            # </Performing Converting Operation>

        except Exception as ex:
            if ex.__repr__() == "AssertionError()":
                pass
            else:
                messagebox.showerror("Error", "Something went wrong! Restart the App")
                raise ex

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)
    try:
        root.iconbitmap("./resources/root_ico.ico")
    except tk.TclError:
        pass
    app = MainFrame(root)
    app.run()

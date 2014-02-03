import Tkinter as tk
import tkFileDialog
import tkMessageBox
import tkFont

from .equipment import CAMERAS
from .plomo import manipulate_files


class PlomoApp(tk.Frame):
    def __init__(self, master=None, path=None, camera=None):
        if master is None:
            master = tk.Tk()
        master.minsize(400, 100)
        tk.Frame.__init__(self, master)
        self.grid()
        self.customFont = tkFont.Font(weight=tkFont.BOLD)
        self.path = tk.StringVar()
        self.camera = tk.StringVar()
        self.create_widgets()

        if path:
            self.path.set(path)
        if camera:
            self.camera.set(camera)

    def create_widgets(self):
        self.path_title_label = tk.Label(self, text='Directory:',
                                         font=self.customFont)
        self.path_title_label.grid(row=0, column=0, sticky='W')

        self.select_path_button = tk.Button(self, text='Select directory',
                                            command=self.ask_directory)
        self.select_path_button.grid(row=0, column=1)

        self.path_label = tk.Label(self, textvariable=self.path)
        self.path_label.grid(row=1, column=0, columnspan=4)

        self.camera_title_label = tk.Label(self, text='Camera:',
                                           font=self.customFont)
        self.camera_title_label.grid(row=2, column=0, sticky='W')

        options = CAMERAS.keys()
        options.sort()
        self.camera_option = tk.OptionMenu(self, self.camera, *options)
        self.camera_option.grid(row=2, column=1)

        self.save_button = tk.Button(self, text='Save', command=self.save)
        self.save_button.grid(row=2, column=3, sticky='E')

        self.quit_button = tk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid(row=2, column=4, sticky='W')

    def ask_directory(self):
        title = 'Select the folder containing your photos'
        self.path.set(tkFileDialog.askdirectory(mustexist=True, title=title))

    def save(self):
        if not self.path.get() or not self.camera.get():
            tkMessageBox.showwarning('Plomo',
                                     'You must select directory and a camera')
            return

        if manipulate_files(self.path.get(), CAMERAS[self.camera.get()]):
            tkMessageBox.showinfo('Plomo', 'Successfully saved')
        else:
            tkMessageBox.showwarning('Plomo', 'Could not save Exif data')

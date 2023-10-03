from setup_source.commands import *
from tkinterdnd2 import TkinterDnD, DND_ALL
from tkinter import filedialog as fd
import customtkinter as ctk
from CTkToolTip import *
from PIL import Image
import webbrowser
import os


installed = None


class InstallFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        path = resource_path_finder(rf"setup_source\images\plus.png")
        self.folder_img = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        # ------------------------------------------------------------------------
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(9, weight=1)
        # ------------------------------------------------------------------------ top title and buttons
        title_font = ctk.CTkFont(family="Terminal", size=36, weight="bold")
        font = ctk.CTkFont(family="Roboto", size=14)
        bigger_font = ctk.CTkFont(family="Roboto", size=20)
        self.label_title = ctk.CTkLabel(self, text="Wicogen setup", font=title_font)
        self.label_title.grid(padx=0, pady=(20, 10), columnspan=3, sticky='new')
        # ------------------------------------------------------------------------ Destination folder
        row = 1
        # -------------------------------------------------- label
        self.dst_label = ctk.CTkLabel(self, text='Installation folder:', font=bigger_font)
        self.dst_label.grid(row=row, column=0, columnspan=3, padx=20, pady=(0, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.dst_path_box = ctk.CTkTextbox(self, height=20, state="disabled")
        self.dst_path_box.grid(row=row + 1, column=0, columnspan=3, padx=(20, 135), pady=(0, 10), sticky='ew')
        self.dst_path_string = "C:\\Program Files\\Wicogen"
        self.dst_path_box.configure(state="normal")
        self.dst_path_box.delete("0.0", "end")
        self.dst_path_box.insert("0.0", "C:\\Program Files\\Wicogen")
        self.dst_path_box.configure(state="disabled")
        self.dst_path_box.drop_target_register(DND_ALL)
        self.dst_path_box.dnd_bind("<<Drop>>", self.set_destination_folder)
        # -------------------------------------------------- button
        self.dst_path_btn = ctk.CTkButton(self, width=20, height=20, text="Add folder", image=self.folder_img,
                                          command=self.set_destination_folder, font=font)
        self.dst_path_btn.grid(row=row + 1, column=0, columnspan=3, padx=(0, 20), pady=(0, 10), sticky='e')
        # ------------------------------------------------------------------------ check boxes
        row = 3
        self.btn_1 = ctk.CTkCheckBox(self, text='Create a desktop shortcut', font=font)
        self.btn_2 = ctk.CTkCheckBox(self, text='Context menu entry', font=font)
        self.btn_3 = ctk.CTkCheckBox(self, text='Create a start menu shortcut', font=font)
        self.btn_4 = ctk.CTkCheckBox(self, text='Create an uninstaller', font=font)
        self.btn_1.select()
        self.btn_2.select()
        self.btn_3.select()
        self.btn_4.select()
        self.btn_1.grid(row=row, column=0, padx=20, pady=(0, 10), sticky='w')
        self.btn_2.grid(row=row, column=1, padx=0, pady=(0, 10), sticky='w')
        self.btn_3.grid(row=row + 1, column=0, padx=20, pady=0, sticky='w')
        self.btn_4.grid(row=row + 1, column=1, padx=0, pady=0, sticky='w')
        # ------------------------------------------------------------------------ install button
        row = 5
        self.script_btn = ctk.CTkButton(self, text="Install", command=self.install, font=bigger_font)
        self.script_btn.grid(row=row, column=0, columnspan=3, padx=120, pady=20, sticky='news')
        # ------------------------------------------------------------------------ bottom buttons images
        path = resource_path_finder(rf"setup_source\images\github.png")
        self.github_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        path = resource_path_finder(rf"setup_source\images\heart.png")
        self.heart_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        path = resource_path_finder(rf"setup_source\images\info.png")
        self.info_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        # ------------------------------------------------------------------------ bottom buttons
        row = 3
        column = 2
        self.github_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.github_btn_image,
                                        command=self.github)
        self.github_btn.grid(row=row, column=column, rowspan=2, padx=(0, 20), pady=0, sticky="e")
        self.info_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.info_btn_image,
                                      command=lambda: info_menu(self))
        self.info_btn.grid(row=row, column=column, rowspan=2, padx=(0, 19), pady=0, sticky="")
        self.heart_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.heart_btn_image,
                                       command=self.heart)
        self.heart_btn.grid(row=row, column=column, rowspan=2, padx=(0, 29), pady=0, sticky="w")
        # ------------------------------------------------------------------------------------- Tooltips
        tooltips(self.dst_path_box, "Drag&Drop also supported!")
        tooltips(self.dst_path_btn, "Drag&Drop also supported!")
        tooltips(self.btn_1, "Make a shortcut to the program in the desktop.")
        tooltips(self.btn_2, "Add an entry in the windows explorer context menu.\n"
                             "Right clicking on folder or file will display a new option.")
        tooltips(self.btn_3, "Add a start menu entry.")
        tooltips(self.btn_4, 'Create an uninstaller in the Documents folder\n'
                             'By default the setup can act as uninstaller.')

    def set_destination_folder(self, event=None):
        if self.btn_1.cget("state") == 'normal':
            if event is None:
                temp_path = fd.askdirectory(mustexist=True, title='Please choose the destination directory!')
                folder = temp_path if os.path.isdir(temp_path) else "C:\\Program Files"
                folder = f'{folder}\\Wicogen'.replace('/', '\\')
            else:  # Drag&Drop
                folder = event.data.strip('{}') if os.path.isdir(event.data.strip('{}')) else "C:\\Program Files"
                folder = f'{folder}\\Wicogen'.replace('/', '\\')
            self.dst_path_string = folder
            self.dst_path_box.configure(state="normal")
            self.dst_path_box.delete("0.0", "end")
            self.dst_path_box.insert("0.0", folder)
            self.dst_path_box.configure(state="disabled")

    def install(self):
        btn_1 = int(self.btn_1.get())  # desktop shortcut
        btn_2 = int(self.btn_2.get())  # context menu
        btn_3 = int(self.btn_3.get())  # start menu
        btn_4 = int(self.btn_4.get())  # uninstaller
        installation_folder = self.dst_path_string.strip()
        if installation_folder is not None and installation_folder.replace(' ', '') != '':
            self.btn_1.configure(state="disabled")
            self.btn_2.configure(state="disabled")
            self.btn_3.configure(state="disabled")
            self.btn_4.configure(state="disabled")
            self.dst_path_btn.configure(state="disabled")
            self.script_btn.configure(text="Setting up...", state="disabled")
            try:
                if btn_2:
                    install_extensions(installation_folder)
                install_main(installation_folder, btn_1, btn_3, btn_4)
                save_in_file(installation_folder, 'Installation_path')
                self.script_btn.configure(require_redraw=True, text="Finish", state="normal",
                                          command=self.master.destroy)
            except Exception as excep:
                save_in_file(str(excep), 'Installation_crash')
                self.script_btn.configure(text="Installation failed...", state="disabled")
                tooltips(self.script_btn, 'Error message saved in "Documents\\Wicogen\\Installation_crash.txt"!')

    @staticmethod
    def github():
        webbrowser.open('https://github.com/idanach/windows-folder-icon')

    @staticmethod
    def heart():
        webbrowser.open('https://www.buymeacoffee.com/idanach')


class UninstallFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)
        # ------------------------------------------------------------------------ top title and buttons
        title_font = ctk.CTkFont(family="Terminal", size=36, weight="bold")
        bigger_font = ctk.CTkFont(family="Roboto", size=20)
        self.label_title = ctk.CTkLabel(self, text="Wicogen Uninstaller", font=title_font)
        self.label_title.grid(padx=0, pady=(20, 10), sticky='new')
        # ------------------------------------------------------------------------ Destination folder
        row = 1
        # -------------------------------------------------- label
        self.dst_label = ctk.CTkLabel(self, text='Installation folder:', font=bigger_font)
        self.dst_label.grid(row=row, column=0, padx=20, pady=(0, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.dst_path_box = ctk.CTkTextbox(self, height=20, state="disabled")
        self.dst_path_box.grid(row=row + 1, column=0, padx=(20, 20), pady=(0, 10), sticky='ew')
        self.dst_path_string = installed
        self.dst_path_box.configure(state="normal")
        self.dst_path_box.delete("0.0", "end")
        self.dst_path_box.insert("0.0", installed)
        self.dst_path_box.configure(state="disabled")
        # ------------------------------------------------------------------------ install button
        row = 5
        self.script_btn = ctk.CTkButton(self, text="Uninstall", command=self.uninstall, font=bigger_font)
        self.script_btn.grid(row=row, column=0, padx=120, pady=20, sticky='news')
        # ------------------------------------------------------------------------ bottom buttons images
        path = resource_path_finder(rf"setup_source\images\github.png")
        self.github_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        path = resource_path_finder(rf"setup_source\images\heart.png")
        self.heart_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        path = resource_path_finder(rf"setup_source\images\info.png")
        self.info_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        # ------------------------------------------------------------------------ bottom buttons
        row = 3
        column = 0
        self.github_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.github_btn_image,
                                        command=self.github)
        self.github_btn.grid(row=row, column=column, rowspan=2, padx=(90, 0), pady=0)
        self.info_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.info_btn_image,
                                      command=lambda: info_menu(self))
        self.info_btn.grid(row=row, column=column, rowspan=2, padx=(0, 0), pady=0)
        self.heart_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.heart_btn_image,
                                       command=self.heart)
        self.heart_btn.grid(row=row, column=column, rowspan=2, padx=(0, 90), pady=0)
        # ------------------------------------------------------------------------------------- Tooltips

    def uninstall(self):
        uninstall_folder = self.dst_path_string.strip()
        if uninstall_folder is not None and uninstall_folder.replace(' ', '') != '':
            self.script_btn.configure(text="Uninstalling...", state="disabled")
            try:
                uninstall(uninstall_folder)
                self.script_btn.configure(require_redraw=True, text="Finished", state="normal",
                                          command=self.master.destroy)
            except Exception as excep:
                save_in_file(str(excep), 'Uninstall_crash')
                self.script_btn.configure(text="Uninstall failed...", state="disabled")
                tooltips(self.script_btn, 'Error message saved in "Documents\\Wicogen\\Uninstall_crash.txt"!')

    @staticmethod
    def github():
        webbrowser.open('https://github.com/idanach/windows-folder-icon')

    @staticmethod
    def heart():
        webbrowser.open('https://www.buymeacoffee.com/idanach')


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
        if installed is None:
            self.title("Wicogen setup")
        else:
            self.title("Wicogen uninstaller")
        self.geometry("720x275")
        path = resource_path_finder(rf"setup_source\images\app_icon.ico")
        self.wm_iconbitmap(path)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # ---------------------------------------------------------------- frames
        if installed is None:
            self.frame = InstallFrame(master=self)
            self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        else:
            self.frame = UninstallFrame(master=self)
            self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        # ---------------------------------------------------------------- tabs


def info_menu(master):
    def close_toplevel():
        about_window.destroy()

    title_font = ctk.CTkFont(family="Roboto", size=26, weight="bold")
    second_title_font = ctk.CTkFont(family="Roboto", size=18, weight="bold")
    font = ctk.CTkFont(family="Roboto", size=13)
    font_under_line = ctk.CTkFont(family="Roboto", size=13, underline=True)
    bigger_font = ctk.CTkFont(family="Roboto", size=16)

    about_window = ctk.CTkToplevel(master)
    about_window.title("About Wicogen setup")
    about_window.transient(master)
    about_window.geometry("600x400")
    about_window.resizable(False, False)
    about_window.protocol("WM_DELETE_WINDOW", close_toplevel)
    path = resource_path_finder(rf"setup_source\images\app_icon.ico")
    about_window.wm_iconbitmap(path)
    about_window.after(200, lambda: about_window.wm_iconbitmap(rf"setup_source\images\app_icon.ico"))
    about_window.grid_columnconfigure(0, weight=1)
    about_window.grid_rowconfigure(10, weight=1)
    label_title = ctk.CTkLabel(about_window, text="Wicogen - Windows icon generator", font=title_font)
    label_title.grid(row=0, column=0, padx=20, pady=(10, 0), sticky='news')
    link_color = "cyan"
    # ----------------------------------------------------------------------------------------------------------
    freeware_title = ctk.CTkLabel(about_window, text="(Wicogen is a Freeware)", font=second_title_font)
    freeware_title.grid(row=1, column=0, padx=20, pady=(0, 10), sticky='news')
    # ----------------------------------------------------------------------------------------------------------
    row = 2
    info = "This is a setup for the Wicogen app.\n\n" \
           "Created and developed by Idan Achrak"
    label_info = ctk.CTkLabel(about_window, text=info, justify="left", font=bigger_font)
    label_info.grid(row=row, column=0, padx=20, pady=10, sticky='w')
    # ----------------------------------------------------------------------------------------------------------
    row = 11
    icon_text = "Icons made by                ,"
    icon_text = ctk.CTkLabel(about_window, text=icon_text, font=font)
    icon_text.grid(row=row, column=0, padx=20, pady=(10, 0), sticky='w')
    # ----------------------------------------------------------------------------------------------------------
    flaticon_1 = "Freepik"
    flaticon_1 = ctk.CTkLabel(about_window, text=flaticon_1, font=font, text_color=link_color)
    flaticon_1.grid(row=row, column=0, padx=(107, 0), pady=(11, 0), sticky='w')
    flaticon_1.bind("<Button-1>", lambda event: webbrowser.open_new_tab("https://www.flaticon.com/authors/freepik"))
    flaticon_1.bind("<Enter>", lambda event: flaticon_1.configure(font=font_under_line, cursor="hand2"))
    flaticon_1.bind("<Leave>", lambda event: flaticon_1.configure(font=font, cursor="arrow"))
    # ----------------------------------------------------------------------------------------------------------
    flaticon_2 = "riajulislam"
    flaticon_2 = ctk.CTkLabel(about_window, text=flaticon_2, font=font, text_color=link_color)
    flaticon_2.grid(row=row, column=0, padx=(158, 0), pady=(11, 0), sticky='w')
    flaticon_2.bind("<Button-1>", lambda event: webbrowser.open_new_tab("https://www.flaticon.com/authors/riajulislam"))
    flaticon_2.bind("<Enter>", lambda event: flaticon_2.configure(font=font_under_line, cursor="hand2"))
    flaticon_2.bind("<Leave>", lambda event: flaticon_2.configure(font=font, cursor="arrow"))
    # ----------------------------------------------------------------------------------------------------------
    flaticon_text = "Sourced and licensed by "
    flaticon_text = ctk.CTkLabel(about_window, text=flaticon_text, font=(font, 13))
    flaticon_text.grid(row=row, column=0, padx=20, pady=(50, 0), sticky='w')
    # ----------------------------------------------------------------------------------------------------------
    flaticon_link = "www.flaticon.com"
    flaticon_link = ctk.CTkLabel(about_window, text=flaticon_link, font=font, text_color=link_color)
    flaticon_link.grid(row=row, column=0, padx=(166, 0), pady=(52, 0), sticky='w')
    flaticon_link.bind("<Button-1>", lambda event: webbrowser.open_new_tab("https://www.flaticon.com"))
    flaticon_link.bind("<Enter>", lambda event: flaticon_link.configure(font=font_under_line, cursor="hand2"))
    flaticon_link.bind("<Leave>", lambda event: flaticon_link.configure(font=font, cursor="arrow"))
    # ----------------------------------------------------------------------------------------------------------
    row = 12
    copyright_text = "This software is under the                                       license!"
    copyright_label = ctk.CTkLabel(about_window, text=copyright_text, font=(font, 13))
    copyright_label.grid(row=row, column=0, padx=20, pady=(5, 10), sticky='w')
    # ----------------------------------------------------------------------------------------------------------
    copyright_name = "Mozilla Public License 2.0"
    copyright_link = ctk.CTkLabel(about_window, text=copyright_name, font=font, text_color=link_color)
    copyright_link.grid(row=row, column=0, padx=(172, 0), pady=(7, 10), sticky='w')
    copyright_link.bind("<Button-1>", lambda event: webbrowser.open_new_tab("https://www.mozilla.org/en-US/MPL/2.0/"))
    copyright_link.bind("<Enter>", lambda event: copyright_link.configure(font=font_under_line, cursor="hand2"))
    copyright_link.bind("<Leave>", lambda event: copyright_link.configure(font=font, cursor="arrow"))
    # ----------------------------------------------------------------------------------------------------------
    version_text = f"Version {version}"
    version_label = ctk.CTkLabel(about_window, text=version_text, font=(font, 13))
    version_label.grid(row=row, column=0, padx=20, pady=(5, 10), sticky='e')


def tooltips(tab_object, text):
    font = ctk.CTkFont(family="Roboto", size=16)
    CTkToolTip(tab_object, delay=0.4, message=text, padding=(10, 10), font=font, justify='left', y_offset=25)


def main():
    global installed
    # ----------------------------------------------------- check if the program is already installed
    installation_location_file = os.path.expanduser("~\\Documents\\Wicogen\\Installation_path.txt")
    if os.path.isfile(installation_location_file):
        with open(installation_location_file, 'r') as file:
            location = file.read()
        if os.path.isdir(location):
            installed = location
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()

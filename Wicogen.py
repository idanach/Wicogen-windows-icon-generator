import threading
import customtkinter as ctk
from CTkToolTip import *
from source.scripts import from_folder, from_net
from source.scripts.source_commands import *
from PIL import Image
import webbrowser


class Tabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        path = resource_path_finder(rf"source\images\plus.png")
        self.folder_img = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        self.font_name = ctk.ThemeManager.theme["CTkFont"]["family"]
        # Tab 1 - From folder
        tab = r"From Folder\File"
        self.add(tab)
        # ------------------------------------------------------------------------------------- Grid management
        self.tab(tab).grid_columnconfigure(1, weight=1)
        self.tab(tab).grid_rowconfigure(9, weight=1)
        # ------------------------------------------------------------------------------------- Page Label
        row = 0
        self.t1_settings_label = ctk.CTkLabel(self.tab(tab), text='Settings:')
        self.t1_settings_label.grid(row=row, column=0, columnspan=2, padx=20, pady=(10, 10), sticky='w')
        # ------------------------------------------------------------------------------------- Check buttons
        row = 1
        self.t1_btn_1 = ctk.CTkCheckBox(self.tab(tab), text='Keep image aspect ratio')
        self.t1_btn_2 = ctk.CTkCheckBox(self.tab(tab), text='Overwrite existing icons')
        self.t1_btn_3 = ctk.CTkCheckBox(self.tab(tab), text='Crete new folders', state='disabled')
        self.t1_btn_4 = ctk.CTkCheckBox(self.tab(tab), text='Separator', onvalue='normal',
                                        offvalue='disabled', command=self.t1_set_separator_state, state='disabled')
        self.t1_btn_1.select()
        self.t1_btn_1.grid(row=row, column=0, padx=20, pady=(0, 10), sticky='w')
        self.t1_btn_2.grid(row=row, column=1, padx=20, pady=(0, 10), sticky='w')
        self.t1_btn_3.grid(row=row + 1, column=0, padx=20, pady=0, sticky='w')
        self.t1_btn_4.grid(row=row + 1, column=1, padx=20, pady=0, sticky='w')
        # ------------------------------------------------------------------------------------- Style
        row = 3
        # -------------------------------------------------- label
        self.t1_style_label = ctk.CTkLabel(self.tab(tab), text='Style:')
        self.t1_style_label.grid(row=row, column=0, padx=20, pady=(30, 10), sticky='nws')
        # -------------------------------------------------- drop list
        self.t1_drop_list = ctk.CTkOptionMenu(self.tab(tab), values=['None', 'Disk'], command=self.t1_set_style)
        self.t1_drop_list.grid(row=row, column=0, padx=(60, 0), pady=(30, 10), sticky='w')
        # ------------------------------------------------------------------------------------- Separator
        row = 3
        # -------------------------------------------------- label
        self.colors = ['gray', 'white']
        self.t1_separator_label = ctk.CTkLabel(self.tab(tab), text='Separator:', text_color='gray')
        self.t1_separator_label.grid(row=row, column=1, padx=20, pady=(30, 10), sticky='nws')
        # -------------------------------------------------- text box
        self.t1_separator_box = ctk.CTkTextbox(self.tab(tab), height=20, width=160)
        self.t1_separator_box.grid(row=row, column=1, padx=(90, 20), pady=(30, 10), sticky='w')
        self.t1_separator_box.configure(state='disabled')
        # ------------------------------------------------------------------------------------- Source folder/file
        row = 5
        # -------------------------------------------------- Check button
        self.t1_destination_type = ctk.CTkCheckBox(self.tab(tab), text='Single folder mode',
                                                   command=self.t1_set_bulk_mode)
        self.t1_destination_type.grid(row=row, column=0, padx=20, pady=(10, 0), sticky='w')
        self.t1_destination_type.select()
        # -------------------------------------------------- label
        self.t1_src_folder_or_file_label = ctk.CTkLabel(self.tab(tab), text='Source file:')
        self.t1_src_folder_or_file_label.grid(row=row + 1, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.t1_src_folder_or_file_path_box = ctk.CTkTextbox(self.tab(tab), height=20, state="disabled")
        self.t1_src_folder_or_file_path_box.grid(row=row + 2, column=0, columnspan=2, padx=(20, 130), pady=(0, 10),
                                                 sticky='ew')
        # -------------------------------------------------- button
        self.t1_src_folder_or_file_path_string = ''
        self.t1_src_folder_or_file_path_btn = ctk.CTkButton(self.tab(tab), width=20, height=20, text="Add file     ",
                                                            image=self.folder_img, command=self.t1_set_source_folder)
        self.t1_src_folder_or_file_path_btn.grid(row=row + 2, column=0, columnspan=2, padx=(0, 20), pady=(0, 10),
                                                 sticky='e')
        # ------------------------------------------------------------------------------------- Destination folder
        row = 8
        # -------------------------------------------------- label
        self.t1_dst_folder_label = ctk.CTkLabel(self.tab(tab), text='Destination folder:')
        self.t1_dst_folder_label.grid(row=row, column=0, columnspan=2, padx=20, pady=(0, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.t1_dst_folder_path_box = ctk.CTkTextbox(self.tab(tab), height=20, state="disabled")
        self.t1_dst_folder_path_box.grid(row=row + 1, column=0, columnspan=2, padx=(20, 130), pady=(0, 10), sticky='ew')
        # -------------------------------------------------- button
        self.t1_dst_folder_path_string = ''
        self.t1_dst_folder_path_btn = ctk.CTkButton(self.tab(tab), width=20, height=20, text="Add folder",
                                                    image=self.folder_img, command=self.t1_set_destination_folder)
        self.t1_dst_folder_path_btn.grid(row=row + 1, column=0, columnspan=2, padx=(0, 20), pady=(0, 10), sticky='e')
        # ------------------------------------------------------------------------------------- Generate button
        row = 10
        self.t1_script_btn = ctk.CTkButton(self.tab(tab), text="Generate", command=self.t1_from_folder)
        self.t1_script_btn.grid(row=row, column=0, columnspan=2, padx=20, pady=20, sticky='news')
        # --------------------------------------------------------------------------------------------------------------
        # Tab 2 - From net
        tab = "From the net"
        self.add(tab)
        # ------------------------------------------------------------------------------------- Grid management
        self.tab(tab).grid_columnconfigure(1, weight=1)
        self.tab(tab).grid_rowconfigure(9, weight=1)
        # ------------------------------------------------------------------------------------- Page Label
        row = 0
        self.t2_settings_label = ctk.CTkLabel(self.tab(tab), text='Settings:')
        self.t2_settings_label.grid(row=row, column=0, columnspan=2, padx=20, pady=(10, 10), sticky='w')
        # ------------------------------------------------------------------------------------- Check buttons
        row = 1
        self.t2_btn_1 = ctk.CTkCheckBox(self.tab(tab), text='Keep image aspect ratio')
        self.t2_btn_2 = ctk.CTkCheckBox(self.tab(tab), text='Overwrite existing icons')
        self.t2_btn_3 = ctk.CTkCheckBox(self.tab(tab), text='Select image manually')
        self.t2_btn_1.select()
        self.t2_btn_3.select()
        self.t2_btn_1.grid(row=row, column=0, padx=20, pady=(0, 10), sticky='w')
        self.t2_btn_2.grid(row=row, column=1, padx=20, pady=(0, 10), sticky='w')
        self.t2_btn_3.grid(row=row+1, column=0, padx=20, pady=0, sticky='w')
        # ------------------------------------------------------------------------------------- Style
        row = 3
        # -------------------------------------------------- label
        self.t2_style_label = ctk.CTkLabel(self.tab(tab), text='Style:')
        self.t2_style_label.grid(row=row, column=0, padx=20, pady=(30, 10), sticky='nws')
        # -------------------------------------------------- drop list
        self.t2_style_list = ctk.CTkOptionMenu(self.tab(tab), values=['None', 'Disk'])
        self.t2_style_list.configure(command=self.t2_set_style)
        self.t2_style_list.grid(row=row, column=0, padx=(60, 0), pady=(30, 10), sticky='w')
        # ------------------------------------------------------------------------------------- Destination folder
        row = 5
        # -------------------------------------------------- Check button
        self.t2_destination_type = ctk.CTkCheckBox(self.tab(tab), text='Single folder mode',
                                                   command=self.t2_set_bulk_mode)
        self.t2_destination_type.select()
        self.t2_destination_type.grid(row=row, column=0, padx=20, pady=(10, 0), sticky='w')
        # -------------------------------------------------- label
        self.t2_dst_folder_label = ctk.CTkLabel(self.tab(tab), text='Destination folder: ')
        self.t2_dst_folder_label.grid(row=row + 1, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.t2_dst_folder_path_box = ctk.CTkTextbox(self.tab(tab), height=20, state="disabled")
        self.t2_dst_folder_path_box.grid(row=row + 2, column=0, columnspan=2, padx=(20, 130), pady=(0, 10), sticky='ew')
        # -------------------------------------------------- button
        self.t2_dst_folder_path_string = ''
        self.t2_dst_folder_path_btn = ctk.CTkButton(self.tab(tab), width=20, height=20, text="Add folder",
                                                    image=self.folder_img, command=self.t2_set_destination_folder)
        self.t2_dst_folder_path_btn.grid(row=row + 2, column=0, columnspan=2, padx=(0, 20), pady=(0, 10), sticky='e')
        # ------------------------------------------------------------------------------------- Image source
        row = 8
        # -------------------------------------------------- label
        self.t2_source_label = ctk.CTkLabel(self.tab(tab), text='Source:')
        self.t2_source_label.grid(row=row, column=0, padx=20, pady=(10, 0), sticky='nws')
        # -------------------------------------------------- drop list
        self.t2_source_list = ctk.CTkOptionMenu(self.tab(tab), values=['Google', 'Bing', 'IMDB'],
                                                command=self.t2_change_image_source)
        self.t2_source_list.set('Choose!')
        self.t2_source_list.grid(row=row, column=0, padx=(67, 0), pady=(10, 0), sticky='w')
        # ------------------------------------------------------------------------------------- Looking for(search term)
        # -------------------------------------------------- label
        self.t2_search_term_label = ctk.CTkLabel(self.tab(tab), text='Looking for:', text_color='gray')
        self.t2_search_term_label.grid(row=row, column=1, padx=20, pady=(10, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.t2_search_term_box = ctk.CTkTextbox(self.tab(tab), height=20, width=160, state='disabled')
        self.t2_search_term_box.grid(row=row, column=1, padx=(100, 20), pady=(10, 0), sticky='we')
        # ------------------------------------------------------------------------------------- Generate button
        row = 10
        self.t2_force_search_net = ctk.CTkCheckBox(self.tab(tab), text='Search net again', state='disabled')
        self.t2_force_search_net.grid(row=row, column=0, padx=20, pady=(0, 0), sticky='w')
        self.t2_script_btn = ctk.CTkButton(self.tab(tab), text="Generate", command=self.t2_from_net)
        self.t2_script_btn.grid(row=row+1, column=0, columnspan=2, padx=20, pady=20, sticky='news')
        # --------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------- Tooltips
        pad = (10, 10)
        font = (self.font_name, 16)
        # -------------------------------------------------------------------------- Tab 1
        text = 'Prevent image distortion (stretching)\n(Disabled for the "disk" folder style)'
        CTkToolTip(self.t1_btn_1, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = 'Warning!\nThis deletes the file:\n"icon.ico"'
        CTkToolTip(self.t1_btn_2, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = 'Create new folders with the names of the files from the source folder.\n' \
               '(From IMDB the first result is chosen automatically)\n' \
               '(If separator is enabled it will create the whole folder path)'
        CTkToolTip(self.t1_btn_3, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = 'Use separator when a name of an\nimage relates to a folder path.\nExample:\n\n' \
               '"Archive_TV show_Season 1.png"\n\n' \
               'The separator in this case is "_"\n' \
               'The resulting path for the folder will be:\n\n' \
               '"./Archive/TV show/Season 1"'
        CTkToolTip(self.t1_btn_4, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = "Styles aren't compatible with '.ico' files."
        CTkToolTip(self.t1_drop_list, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        # -------------------------------------------------------------------------- Tab 2
        text = 'Prevent image distortion (stretching)\n(Disabled for the "disk" folder style)'
        CTkToolTip(self.t2_btn_1, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = 'Warning!\nThis deletes the file:\n"icon.ico"'
        CTkToolTip(self.t2_btn_2, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = 'When left unchecked a random image\nfrom the source will be chosen.'
        CTkToolTip(self.t2_btn_3, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = '"{folder name} {search term}"\nDefault search term is "folder icon".'
        CTkToolTip(self.t2_search_term_box, delay=0.4, message=text, padding=pad, font=font, justify='left',
                   y_offset=25)
        text = 'Force re-download images from the net.'
        CTkToolTip(self.t2_force_search_net, delay=0.4, message=text, padding=pad, font=font, justify='left',
                   y_offset=25)

    # ------------------------------------------------------------------------------------- Tab 1 - From folder
    def t1_from_folder(self):
        crete_new_folders = int(self.t1_btn_3.get())
        keep_image_dimensions = int(self.t1_btn_1.get())
        overwrite_files = int(self.t1_btn_2.get())
        include_seperator = 0 if self.t1_btn_4.get() == 'disabled' else 1
        only_dst_folder = int(self.t1_destination_type.get())
        temp_string = self.t1_separator_box.get('0.0', 'end').strip()
        file_name_seperator = '?' if temp_string == '' else temp_string
        folder_style = self.t1_drop_list.get().strip()
        src_folder = self.t1_src_folder_or_file_path_string.strip()
        dst_folder = self.t1_dst_folder_path_string.strip()
        if os.path.exists(src_folder) and os.path.isdir(dst_folder):
            threading.Thread(target=from_folder.main,
                             args=(src_folder, dst_folder, file_name_seperator, folder_style, crete_new_folders,
                                   keep_image_dimensions, overwrite_files, include_seperator, only_dst_folder)).start()
        self.t1_btn_2.deselect()

    def t1_set_bulk_mode(self):
        self.t1_src_folder_or_file_path_string = ''
        self.t1_src_folder_or_file_path_box.configure(state="normal")
        self.t1_src_folder_or_file_path_box.delete("0.0", "end")
        self.t1_src_folder_or_file_path_box.configure(state="disabled")
        self.t1_dst_folder_path_string = ''
        self.t1_dst_folder_path_box.configure(state="normal")
        self.t1_dst_folder_path_box.delete("0.0", "end")
        self.t1_dst_folder_path_box.configure(state="disabled")
        mode = int(self.t1_destination_type.get())
        if mode:  # single mode
            # -------------------------------------------------------------------------------- src label and btn
            text = 'Source file:'
            self.t1_src_folder_or_file_label.configure(require_redraw=True, text=text)
            self.t1_src_folder_or_file_path_btn.configure(require_redraw=True, text="Add file     ")
            # -------------------------------------------------------------------------------- dst label
            text = 'Destination folder:'
            self.t1_dst_folder_label.configure(require_redraw=True, text=text)
            # -------------------------------------------------------------------------------- create new folder
            self.t1_btn_3.deselect()
            self.t1_btn_3.configure(require_redraw=True, state='disabled')
            # -------------------------------------------------------------------------------- separator
            self.t1_btn_4.deselect()
            self.t1_btn_4.configure(require_redraw=True, state='disabled')
            self.t1_set_separator_state()
            # --------------------------------------------------------------------------------
        else:  # bulk mode
            # -------------------------------------------------------------------------------- src label and btn
            text = 'Source folder:   (Folder containing images)'
            self.t1_src_folder_or_file_label.configure(require_redraw=True, text=text)
            self.t1_src_folder_or_file_path_btn.configure(require_redraw=True, text="Add folder")
            # -------------------------------------------------------------------------------- dst label
            text = 'Destination folder:   (Folder containing the sub folders)'
            self.t1_dst_folder_label.configure(require_redraw=True, text=text)
            # -------------------------------------------------------------------------------- create new folder
            self.t1_btn_3.configure(require_redraw=True, state='normal')
            # -------------------------------------------------------------------------------- separator
            self.t1_btn_4.configure(require_redraw=True, state='normal')
            self.t1_set_separator_state()
            # --------------------------------------------------------------------------------

    def t1_set_style(self, style=''):
        if style == 'None':
            self.t1_btn_1.configure(require_redraw=True, state='normal')
            self.t1_btn_1.select()
        if style == 'Disk':
            self.t1_btn_1.deselect()
            self.t1_btn_1.configure(require_redraw=True, state='disabled')

    def t1_set_source_folder(self):
        mode = int(self.t1_destination_type.get())
        if mode:
            path = choose_image_dialog()
        else:
            path = fd.askdirectory(mustexist=True, title='Please choose the source directory!')
        if path is None:
            path = ''
        self.t1_src_folder_or_file_path_string = path
        self.t1_src_folder_or_file_path_box.configure(state="normal")
        self.t1_src_folder_or_file_path_box.delete("0.0", "end")
        self.t1_src_folder_or_file_path_box.insert("0.0", path)
        self.t1_src_folder_or_file_path_box.configure(state="disabled")

    def t1_set_destination_folder(self):
        folder = fd.askdirectory(mustexist=True, title='Please choose the destination directory!')
        self.t1_dst_folder_path_string = folder
        self.t1_dst_folder_path_box.configure(state="normal")
        self.t1_dst_folder_path_box.delete("0.0", "end")
        self.t1_dst_folder_path_box.insert("0.0", folder)
        self.t1_dst_folder_path_box.configure(state="disabled")

    def t1_set_separator_state(self):
        button_status = self.t1_btn_4.get()
        self.t1_separator_box.configure(state="normal")
        self.t1_separator_box.delete("0.0", "end")
        self.t1_separator_box.configure(state=button_status)
        temp = 1 if button_status == 'normal' else 0
        self.t1_separator_label.configure(text_color=self.colors[temp])

    # ------------------------------------------------------------------------------------- Tab 2 - From net
    def t2_from_net(self):
        image_source = self.t2_source_list.get().strip()
        if image_source == 'Choose!':
            self.t2_source_list.configure(fg_color='dark red')
        else:
            keep_image_dimensions = int(self.t2_btn_1.get())
            overwrite_files = int(self.t2_btn_2.get())
            folder_style = self.t2_style_list.get().strip()
            dst_folder = self.t2_dst_folder_path_string.strip()
            only_dst_folder = int(self.t2_destination_type.get())
            manual_selection = int(self.t2_btn_3.get())
            force_re_search = int(self.t2_force_search_net.get())
            temp_string = self.t2_search_term_box.get('0.0', 'end').strip()
            looking_for = 'folder icon' if temp_string.replace(' ', '') == '' else temp_string
            if os.path.isdir(dst_folder):
                arguments = (dst_folder, folder_style, keep_image_dimensions, overwrite_files, only_dst_folder,
                             image_source, manual_selection, force_re_search, looking_for, self.t2_script_btn)
                threading.Thread(target=from_net.main, args=arguments).start()
                self.t2_force_search_net.configure(state='normal')
                self.t2_force_search_net.deselect()
            self.t2_btn_2.deselect()

    def t2_change_image_source(self, source=''):
        self.t2_source_list.configure(fg_color='#1F6AA5')
        if source == 'Google' or source == 'Bing':
            self.t2_btn_3.select()
            self.t2_search_term_box.configure(require_redraw=True, state='normal', text_color='white')
            self.t2_search_term_box.delete("0.0", "end")
            self.t2_search_term_box.insert("0.0", "folder icon")
            self.t2_search_term_label.configure(text_color='white')
        else:
            self.t2_btn_3.deselect()
            self.t2_search_term_box.delete("0.0", "end")
            self.t2_search_term_box.configure(require_redraw=True, state='disabled', text_color='gray')
            self.t2_search_term_label.configure(text_color='gray')

    def t2_set_style(self, style=''):
        if style == 'None':
            self.t2_btn_1.configure(require_redraw=True, state='normal')
            self.t2_btn_1.select()
        if style == 'Disk':
            self.t2_btn_1.deselect()
            self.t2_btn_1.configure(require_redraw=True, state='disabled')

    def t2_set_bulk_mode(self):
        mode = int(self.t2_destination_type.get())
        if mode:
            text = 'Destination folder:'
            self.t2_dst_folder_label.configure(require_redraw=True, text=text)
        else:
            text = 'Destination folder:   (Choose the folder containing the sub folders)'
            self.t2_dst_folder_label.configure(require_redraw=True, text=text)

    def t2_set_destination_folder(self):
        folder = fd.askdirectory(mustexist=True, title='Please choose the destination directory!')
        self.t2_dst_folder_path_string = folder
        self.t2_dst_folder_path_box.configure(state="normal")
        self.t2_dst_folder_path_box.delete("0.0", "end")
        self.t2_dst_folder_path_box.insert("0.0", folder)
        self.t2_dst_folder_path_box.configure(state="disabled")


class SideBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.grid_rowconfigure(6, weight=1)
        # ------------------------------------------------------------------------ top title and buttons
        title_font = ctk.CTkFont(size=20, weight="bold")
        s_f = ctk.CTkFont(size=14, weight="bold")
        str_l = ["Custom folder\nicons",
                 "Thumb/icon cache:",
                 "Windows explorer:",
                 "Clear",
                 "Refresh",
                 "Restart",
                 "Dark/Light mode"]
        self.label_title = ctk.CTkLabel(self, text=str_l[0], font=title_font)
        self.label_title.grid(padx=20, pady=(20, 20))
        self.label_cache = ctk.CTkLabel(self, text=str_l[1], font=s_f)
        self.label_cache.grid(row=1, padx=20, pady=(0, 0))
        self.label_explorer = ctk.CTkLabel(self, text=str_l[2], font=s_f)
        self.label_explorer.grid(row=3, padx=20, pady=(0, 0))
        self.btn_clear = ctk.CTkButton(self, text=str_l[3], command=clear_thumbnail_cache)
        self.btn_clear.grid(row=2, padx=20, pady=(0, 20))
        self.btn_refresh = ctk.CTkButton(self, text=str_l[4], command=refresh_explorer)
        self.btn_refresh.grid(row=4, padx=20, pady=0)
        self.btn_restart = ctk.CTkButton(self, text=str_l[5], command=restart_explorer)
        self.btn_restart.grid(row=5, padx=20, pady=10)
        # ------------------------------------------------------------------------ bottom buttons images
        path = resource_path_finder(rf"source\images\github.png")
        self.github_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        path = resource_path_finder(rf"source\images\heart.png")
        self.heart_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        path = resource_path_finder(rf"source\images\info.png")
        self.info_btn_image = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        # ------------------------------------------------------------------------ bottom buttons
        self.github_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.github_btn_image,
                                        command=self.github)
        self.github_btn.grid(row=7, column=0, padx=(0, 25), pady=20, sticky="nes")
        self.info_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.info_btn_image,
                                      command=lambda: info_menu(self))
        self.info_btn.grid(row=7, column=0, padx=(1, 0), pady=20, sticky="")
        self.heart_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.heart_btn_image,
                                       command=self.heart)
        self.heart_btn.grid(row=7, column=0, padx=(25, 0), pady=20, sticky="nws")
        # ------------------------------------------------------------------------ tooltips
        pad = (10, 10)
        font = (ctk.ThemeManager.theme["CTkFont"]["family"], 16)
        text = 'Clear windows thumbnail and icon cache.'
        CTkToolTip(self.btn_clear, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = 'Refresh windows file explorer.'
        CTkToolTip(self.btn_refresh, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)
        text = 'Restart windows file explorer.'
        CTkToolTip(self.btn_restart, delay=0.4, message=text, padding=pad, font=font, justify='left', y_offset=25)

    @staticmethod
    def github():
        webbrowser.open('https://github.com/idanach/windows-folder-icon')

    @staticmethod
    def heart():
        webbrowser.open('https://www.buymeacoffee.com/idanach')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wicogen")
        self.geometry("750x520")
        path = resource_path_finder(rf"source\images\app_icon.ico")
        self.wm_iconbitmap(path)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # ---------------------------------------------------------------- sidebar
        self.side_bar = SideBar(master=self)
        self.side_bar.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        # ---------------------------------------------------------------- tabs
        self.tab_view = Tabs(master=self)
        self.tab_view.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        # ----------------------------------------------------------------


def info_menu(master):
    def close_toplevel():
        about_window.destroy()
    font = ctk.ThemeManager.theme["CTkFont"]["family"]
    about_window = ctk.CTkToplevel(master)
    about_window.title("About Wicogen")
    about_window.transient(master)
    about_window.geometry("600x400")
    about_window.resizable(False, False)
    about_window.protocol("WM_DELETE_WINDOW", close_toplevel)
    path = resource_path_finder(rf"source\images\app_icon.ico")
    about_window.wm_iconbitmap(path)
    about_window.after(200, lambda: about_window.wm_iconbitmap(rf"source\images\app_icon.ico"))
    about_window.grid_columnconfigure(0, weight=1)
    about_window.grid_rowconfigure(10, weight=1)
    label_title = ctk.CTkLabel(about_window, text="Wicogen - Windows icon generator", font=(font, 20, "bold"))
    label_title.grid(row=0, column=0, padx=20, pady=(10, 0), sticky='news')
    # ----------------------------------------------------------------------------------------------------------
    freeware_title = ctk.CTkLabel(about_window, text="(Wicogen is a Freeware)", font=(font, 16, "bold"))
    freeware_title.grid(row=1, column=0, padx=20, pady=(0, 10), sticky='news')
    # ----------------------------------------------------------------------------------------------------------
    row = 2
    info = "A custom icon generator for windows folders. \n" \
           "\nCreated and developed by Idan Achrak\n"
    label_info = ctk.CTkLabel(about_window, text=info, justify="left", font=(font, 16))
    label_info.grid(row=row, column=0, padx=20, pady=10, sticky='w')
    # ----------------------------------------------------------------------------------------------------------
    row = 11
    icon_text = "Icons made by                ,"
    icon_text = ctk.CTkLabel(about_window, text=icon_text, font=(font, 13))
    icon_text.grid(row=row, column=0, padx=20, pady=(10, 0), sticky='w')
    # ----------------------------------------------------------------------------------------------------------
    icon_link_1 = "Freepik"
    icon_link_1 = ctk.CTkLabel(about_window, text=icon_link_1, font=(font, 13), text_color="cyan")
    icon_link_1.grid(row=row, column=0, padx=(107, 0), pady=(10, 0), sticky='w')
    icon_link_1.bind("<Button-1>",
                     lambda event: webbrowser.open_new_tab("https://www.flaticon.com/authors/freepik"))
    icon_link_1.bind("<Enter>", lambda event: icon_link_1.configure(font=(font, 13, "underline"),
                                                                    cursor="hand2"))
    icon_link_1.bind("<Leave>", lambda event: icon_link_1.configure(font=(font, 13), cursor="arrow"))
    # ----------------------------------------------------------------------------------------------------------
    icon_link_2 = "riajulislam"
    icon_link_2 = ctk.CTkLabel(about_window, text=icon_link_2, font=(font, 13), text_color="cyan")
    icon_link_2.grid(row=row, column=0, padx=(158, 0), pady=(10, 0), sticky='w')
    icon_link_2.bind("<Button-1>",
                     lambda event: webbrowser.open_new_tab("https://www.flaticon.com/authors/riajulislam"))
    icon_link_2.bind("<Enter>", lambda event: icon_link_2.configure(font=(font, 13, "underline"),
                                                                    cursor="hand2"))
    icon_link_2.bind("<Leave>", lambda event: icon_link_2.configure(font=(font, 13), cursor="arrow"))
    # ----------------------------------------------------------------------------------------------------------
    flaticon_text = "Sourced and licensed by "
    flaticon_text = ctk.CTkLabel(about_window, text=flaticon_text, font=(font, 13))
    flaticon_text.grid(row=row, column=0, padx=20, pady=(50, 0), sticky='w')
    # ----------------------------------------------------------------------------------------------------------
    flaticon_link = "www.flaticon.com"
    flaticon_link = ctk.CTkLabel(about_window, text=flaticon_link, font=(font, 13), text_color="cyan")
    flaticon_link.grid(row=row, column=0, padx=(161, 0), pady=(50, 0), sticky='w')
    flaticon_link.bind("<Button-1>",
                       lambda event: webbrowser.open_new_tab("https://www.flaticon.com"))
    flaticon_link.bind("<Enter>", lambda event: flaticon_link.configure(font=(font, 13, "underline"),
                                                                        cursor="hand2"))
    flaticon_link.bind("<Leave>", lambda event: flaticon_link.configure(font=(font, 13), cursor="arrow"))
    # ----------------------------------------------------------------------------------------------------------
    row = 12
    copyright_text = "This software is under the                                                    license!"
    copyright_label = ctk.CTkLabel(about_window, text=copyright_text, font=(font, 13))
    copyright_label.grid(row=row, column=0, padx=20, pady=(5, 10), sticky='w')
    # ----------------------------------------------------------------------------------------------------------
    copyright_name = "Mozilla Public License 2.0"
    copyright_link = ctk.CTkLabel(about_window, text=copyright_name, font=(font, 13), text_color="cyan")
    copyright_link.grid(row=row, column=0, padx=(172, 0), pady=(5, 10), sticky='w')
    copyright_link.bind("<Button-1>",
                        lambda event: webbrowser.open_new_tab("https://www.mozilla.org/en-US/MPL/2.0/"))
    copyright_link.bind("<Enter>", lambda event: copyright_link.configure(font=(font, 13, "underline"),
                                                                          cursor="hand2"))
    copyright_link.bind("<Leave>", lambda event: copyright_link.configure(font=(font, 13), cursor="arrow"))
    # ----------------------------------------------------------------------------------------------------------
    version_text = "Version 1.0.1"
    version_label = ctk.CTkLabel(about_window, text=version_text, font=(font, 13))
    version_label.grid(row=row, column=0, padx=20, pady=(5, 10), sticky='e')


def main():
    # run_with_admin_privileges()
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()

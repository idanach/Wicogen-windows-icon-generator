from source.scripts import from_folder, from_net
from source.scripts.source_commands import *
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
from CTkToolTip import *
from PIL import Image
import webbrowser
import threading
import os


class Tabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        path = resource_path_finder(rf"source\images\plus.png")
        self.folder_img = ctk.CTkImage(dark_image=Image.open(path), size=(23, 23))
        title_font = ctk.CTkFont(family="Roboto", size=16, weight="bold")
        btn_font = ctk.CTkFont(family="Roboto", size=14)
        gen_btn_font = ctk.CTkFont(family="Roboto", size=18)
        # Tab 1 - From folder
        tab = r"From Folder\File"
        self.add(tab)
        # ------------------------------------------------------------------------------------- Grid management
        self.tab(tab).grid_columnconfigure(1, weight=1)
        self.tab(tab).grid_rowconfigure(10, weight=1)
        # ------------------------------------------------------------------------------------- Page Label
        row = 0
        self.t1_settings_label = ctk.CTkLabel(self.tab(tab), text='Settings:', font=title_font)
        self.t1_settings_label.grid(row=row, column=0, columnspan=2, padx=20, pady=(10, 10), sticky='w')
        # ------------------------------------------------------------------------------------- Check buttons
        row = 1
        self.t1_btn_1 = ctk.CTkCheckBox(self.tab(tab), text='Keep image aspect ratio', font=btn_font)
        self.t1_btn_2 = ctk.CTkCheckBox(self.tab(tab), text='Overwrite existing icons', font=btn_font)
        self.t1_btn_3 = ctk.CTkCheckBox(self.tab(tab), text='Crete new folders', state='disabled', font=btn_font)
        self.t1_btn_4 = ctk.CTkCheckBox(self.tab(tab), text='Separator', onvalue='normal', offvalue='disabled',
                                        command=self.t1_set_separator_state, state='disabled', font=btn_font)
        self.t1_btn_1.select()
        self.t1_btn_1.grid(row=row, column=0, padx=20, pady=(0, 10), sticky='w')
        self.t1_btn_2.grid(row=row, column=1, padx=20, pady=(0, 10), sticky='w')
        self.t1_btn_3.grid(row=row + 1, column=0, padx=20, pady=0, sticky='w')
        self.t1_btn_4.grid(row=row + 1, column=1, padx=20, pady=0, sticky='w')
        # ------------------------------------------------------------------------------------- Style
        row = 3
        # -------------------------------------------------- label
        self.t1_style_label = ctk.CTkLabel(self.tab(tab), text='Style:', font=title_font)
        self.t1_style_label.grid(row=row, column=0, padx=20, pady=(30, 10), sticky='nws')
        # -------------------------------------------------- drop list
        self.t1_style_list = ctk.CTkOptionMenu(self.tab(tab), values=styles, font=btn_font, command=self.t1_set_style)
        self.t1_style_list.grid(row=row, column=0, padx=(75, 0), pady=(23, 0), sticky='w')
        # ------------------------------------------------------------------------------------- Separator
        row = 3
        # -------------------------------------------------- label
        self.colors = [ctk.ThemeManager.theme["CTkCheckBox"]["text_color_disabled"],
                       ctk.ThemeManager.theme["CTkCheckBox"]["text_color"]]
        self.t1_separator_label = ctk.CTkLabel(self.tab(tab), text='Separator:', font=title_font,
                                               text_color=self.colors[0])
        self.t1_separator_label.grid(row=row, column=1, padx=20, pady=(30, 10), sticky='nws')
        # -------------------------------------------------- text box
        self.t1_separator_box = ctk.CTkTextbox(self.tab(tab), height=20, width=160, font=btn_font)
        self.t1_separator_box.grid(row=row, column=1, padx=(110, 20), pady=(23, 0), sticky='w')
        self.t1_separator_box.configure(state='disabled')
        # ------------------------------------------------------------------------------------- Source folder/file
        row = 5
        # -------------------------------------------------- Check button
        self.t1_destination_type = ctk.CTkCheckBox(self.tab(tab), text='Single folder mode', font=btn_font,
                                                   command=self.t1_set_bulk_mode)
        self.t1_destination_type.grid(row=row, column=0, padx=20, pady=(10, 0), sticky='w')
        self.t1_destination_type.select()
        # -------------------------------------------------- label
        self.t1_src_label = ctk.CTkLabel(self.tab(tab), text='Source file:', font=title_font)
        self.t1_src_label.grid(row=row + 1, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.t1_src_path_box = ctk.CTkTextbox(self.tab(tab), height=20, state="disabled")
        self.t1_src_path_box.grid(row=row + 2, column=0, columnspan=2, padx=(20, 130), pady=(0, 10),
                                  sticky='ew')
        self.t1_src_path_box.drop_target_register(DND_ALL)
        self.t1_src_path_box.dnd_bind("<<Drop>>", self.t1_set_source)
        # -------------------------------------------------- button
        self.t1_src_path_string = ''
        self.t1_src_path_btn = ctk.CTkButton(self.tab(tab), width=20, height=20, text="Add file     ",
                                             image=self.folder_img, command=self.t1_set_source)
        self.t1_src_path_btn.grid(row=row + 2, column=0, columnspan=2, padx=(0, 20), pady=(0, 10), sticky='e')
        # ------------------------------------------------------------------------------------- Destination folder
        row = 8
        # -------------------------------------------------- label
        self.t1_dst_label = ctk.CTkLabel(self.tab(tab), text='Destination folder:', font=title_font)
        self.t1_dst_label.grid(row=row, column=0, columnspan=2, padx=20, pady=(0, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.t1_dst_path_box = ctk.CTkTextbox(self.tab(tab), height=20, state="disabled")
        self.t1_dst_path_box.grid(row=row + 1, column=0, columnspan=2, padx=(20, 130), pady=(0, 10), sticky='ew')
        self.t1_dst_path_box.drop_target_register(DND_ALL)
        self.t1_dst_path_box.dnd_bind("<<Drop>>", self.t1_set_destination_folder)
        # -------------------------------------------------- button
        self.t1_dst_path_string = ''
        self.t1_dst_path_btn = ctk.CTkButton(self.tab(tab), width=20, height=20, text="Add folder",
                                             image=self.folder_img, command=self.t1_set_destination_folder)
        self.t1_dst_path_btn.grid(row=row + 1, column=0, columnspan=2, padx=(0, 20), pady=(0, 10), sticky='e')
        # ------------------------------------------------------------------------------------- Generate button
        row = 11
        self.t1_script_btn = ctk.CTkButton(self.tab(tab), text="Generate", font=gen_btn_font,
                                           command=self.t1_from_folder)
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
        self.t2_settings_label = ctk.CTkLabel(self.tab(tab), text='Settings:', font=title_font)
        self.t2_settings_label.grid(row=row, column=0, columnspan=2, padx=20, pady=(10, 10), sticky='w')
        # ------------------------------------------------------------------------------------- Check buttons
        row = 1
        self.t2_btn_1 = ctk.CTkCheckBox(self.tab(tab), text='Keep image aspect ratio', font=btn_font)
        self.t2_btn_2 = ctk.CTkCheckBox(self.tab(tab), text='Overwrite existing icons', font=btn_font)
        self.t2_btn_3 = ctk.CTkCheckBox(self.tab(tab), text='Select image manually', font=btn_font)
        self.t2_btn_1.select()
        self.t2_btn_3.select()
        self.t2_btn_1.grid(row=row, column=0, padx=20, pady=(0, 10), sticky='w')
        self.t2_btn_2.grid(row=row, column=1, padx=20, pady=(0, 10), sticky='w')
        self.t2_btn_3.grid(row=row + 1, column=0, padx=20, pady=0, sticky='w')
        # ------------------------------------------------------------------------------------- Style
        row = 3
        # -------------------------------------------------- label
        self.t2_style_label = ctk.CTkLabel(self.tab(tab), text='Style:', font=title_font)
        self.t2_style_label.grid(row=row, column=0, padx=20, pady=(30, 10), sticky='nws')
        # -------------------------------------------------- drop list
        self.t2_style_list = ctk.CTkOptionMenu(self.tab(tab), values=styles, font=btn_font, command=self.t2_set_style)
        self.t2_style_list.grid(row=row, column=0, padx=(75, 0), pady=(23, 0), sticky='w')
        # ------------------------------------------------------------------------------------- Text limiter
        row = 3
        # -------------------------------------------------- label
        self.t2_text_limiter_label = ctk.CTkLabel(self.tab(tab), text='Text limiter:', font=title_font)
        self.t2_text_limiter_label.grid(row=row, column=1, padx=20, pady=(30, 10), sticky='nws')
        # -------------------------------------------------- text box
        self.t2_text_limiter_box = ctk.CTkTextbox(self.tab(tab), height=20, width=80, font=btn_font)
        self.t2_text_limiter_box.grid(row=row, column=1, padx=(122, 20), pady=(23, 0), sticky='w')
        self.t2_text_limiter_box.insert("0.0", "20")
        # ------------------------------------------------------------------------------------- Destination folder
        row = 5
        # -------------------------------------------------- Check button
        self.t2_destination_type = ctk.CTkCheckBox(self.tab(tab), text='Single folder mode', font=btn_font)
        self.t2_destination_type.select()
        self.t2_destination_type.grid(row=row, column=0, padx=20, pady=(10, 0), sticky='w')
        # -------------------------------------------------- label
        self.t2_dst_label = ctk.CTkLabel(self.tab(tab), text='Destination folder: ', font=title_font)
        self.t2_dst_label.grid(row=row + 1, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.t2_dst_path_box = ctk.CTkTextbox(self.tab(tab), height=20, state="disabled")
        self.t2_dst_path_box.grid(row=row + 2, column=0, columnspan=2, padx=(20, 130), pady=(0, 10), sticky='ew')
        self.t2_dst_path_box.drop_target_register(DND_ALL)
        self.t2_dst_path_box.dnd_bind("<<Drop>>", self.t2_set_destination_folder)
        # -------------------------------------------------- button
        self.t2_dst_path_string = ''
        self.t2_dst_path_btn = ctk.CTkButton(self.tab(tab), width=20, height=20, text="Add folder",
                                             image=self.folder_img, command=self.t2_set_destination_folder)
        self.t2_dst_path_btn.grid(row=row + 2, column=0, columnspan=2, padx=(0, 20), pady=(0, 10), sticky='e')
        # ------------------------------------------------------------------------------------- Image source
        row = 8
        # -------------------------------------------------- label
        self.t2_src_label = ctk.CTkLabel(self.tab(tab), text='Source:', font=title_font)
        self.t2_src_label.grid(row=row, column=0, padx=20, pady=(10, 0), sticky='nws')
        # -------------------------------------------------- drop list
        self.t2_src_list = ctk.CTkOptionMenu(self.tab(tab), values=['Google', 'Bing', 'IMDB', 'MyAnimeList'],
                                             command=self.t2_change_image_source, font=btn_font)
        self.t2_src_list.set('Choose!')
        self.t2_src_list.grid(row=row, column=0, padx=(85, 0), pady=(11, 0), sticky='w')
        # ------------------------------------------------------------------------------------- Looking for(search term)
        # -------------------------------------------------- label
        self.t2_search_term_label = ctk.CTkLabel(self.tab(tab), text='Looking for:', font=title_font,
                                                 text_color=self.colors[0])
        self.t2_search_term_label.grid(row=row, column=1, padx=20, pady=(10, 0), sticky='nws')
        # -------------------------------------------------- text box
        self.t2_search_term_box = ctk.CTkTextbox(self.tab(tab), height=20, width=160, state='disabled', font=btn_font)
        self.t2_search_term_box.grid(row=row, column=1, padx=(124, 20), pady=(11, 0), sticky='we')
        # ------------------------------------------------------------------------------------- Generate button
        row = 10
        self.t2_only_search = ctk.CTkCheckBox(self.tab(tab), text='Only download images', font=btn_font,
                                              command=self.t2_only_download)
        self.t2_only_search.grid(row=row, column=0, padx=20, pady=(0, 0), sticky='w')
        self.t2_script_btn = ctk.CTkButton(self.tab(tab), text="Generate", font=gen_btn_font, command=self.t2_from_net)
        self.t2_script_btn.grid(row=row + 1, column=0, columnspan=2, padx=20, pady=20, sticky='news')
        # --------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------- Tooltips
        # -------------------------------------------------------------------------- Tab 1
        tooltips(self.t1_btn_1, 'Prevent image distortion (stretching)\n(Disabled for the "disk" folder style)')
        tooltips(self.t1_btn_2, 'Warning!\nThis deletes the file:\n"icon.ico"')
        tooltips(self.t1_btn_3, 'Create new folders with the names of the files from the source folder.\n'
                                '(If separator is enabled it will create the whole folder path)\n'
                                'Disabled in single folder mode.')
        tooltips(self.t1_btn_4, 'Use separator when a name of an\nimage relates to a folder path.\nExample:\n\n'
                                '"Archive_TV show_Season 1.png"\n\n'
                                'The separator in this case is "_"\n'
                                'The resulting path for the folder will be:\n\n'
                                '".\\Archive\\TV show\\Season 1"')
        tooltips(self.t1_style_list, "Styles aren't compatible with '.ico' files.")
        tooltips(self.t1_destination_type, "- Single mode: (Checked)\n\n"
                                           "    Source image --> Destination folder's icon\n"
                                           "-------------------------------------------------------------------------"
                                           "--------------------------------------------------------\n"
                                           "- Bulk mode: (Unchecked)\n\n"
                                           "    Source folder images --> Destination folder's sub folder icons\n\n"
                                           "    Example:\n"
                                           '    "src_folder\\{file_name}.png" --> "dst_folder\\{file_name}\\icon.ico"\n'
                                           '\n    When "Create new folders" is enabled, new sub-folders with the name\n'
                                           '    of the corresponding files will be created.')
        tooltips(self.t1_src_path_box, "Drag&Drop also supported!")
        tooltips(self.t1_src_path_btn, "Drag&Drop also supported!")
        tooltips(self.t1_dst_path_box, "Drag&Drop also supported!")
        tooltips(self.t1_dst_path_btn, "Drag&Drop also supported!")
        # -------------------------------------------------------------------------- Tab 2
        tooltips(self.t2_btn_1, 'Prevent image distortion (stretching)\n(Disabled for the "disk" folder style)')
        tooltips(self.t2_btn_2, 'Warning!\nThis deletes the file:\n"icon.ico"')
        tooltips(self.t2_btn_3, 'When left unchecked a random image from the source will be chosen.\n'
                                '(From IMDB and MyAnimeList, the first result is chosen automatically)')
        tooltips(self.t2_search_term_box, '"{folder name} {search term}"\nDefault search term is "folder icon".')
        tooltips(self.t2_only_search, "Only download images. Doesn't edit any folder files."
                                      "When choosing the bulk option it can save time to download the images first.")
        tooltips(self.t2_destination_type, "- Single mode: (Checked)\n\n"
                                           "    Searching the net for images by the name of the selected folder.\n"
                                           "-------------------------------------------------------------------------"
                                           "----------------------------------------------\n"
                                           "- Bulk mode: (Unchecked)\n\n"
                                           "    Will iterate through the sub-folders of the selected folder and\n"
                                           "    search for each of them images.")
        tooltips(self.t2_dst_path_box, "Drag&Drop also supported!")
        tooltips(self.t2_dst_path_btn, "Drag&Drop also supported!")
        tooltips(self.t2_text_limiter_label, "Image search works better with shorter phrases in most cases.\n"
                                             "if the program didn't find you desired result, try changing the limiter.")
        tooltips(self.t2_text_limiter_box, "Image search works better with shorter phrases in most cases.\n"
                                           "if the program didn't find you desired result, try changing the limiter.")
        # default tab
        self.set("From the net")

    # ------------------------------------------------------------------------------------- Tab 1 - From folder
    def t1_from_folder(self):
        crete_new_folders = int(self.t1_btn_3.get())
        keep_image_dimensions = int(self.t1_btn_1.get())
        overwrite_files = int(self.t1_btn_2.get())
        include_seperator = 0 if self.t1_btn_4.get() == 'disabled' else 1
        only_dst_folder = int(self.t1_destination_type.get())
        temp_string = self.t1_separator_box.get('0.0', 'end').strip()
        file_name_seperator = '?' if temp_string == '' else temp_string
        folder_style = self.t1_style_list.get().strip()
        src_folder = self.t1_src_path_string.strip()
        dst_folder = self.t1_dst_path_string.strip()
        if os.path.exists(src_folder) and os.path.isdir(dst_folder):
            threading.Thread(target=from_folder.main,
                             args=(src_folder, dst_folder, file_name_seperator, folder_style, crete_new_folders,
                                   keep_image_dimensions, overwrite_files, include_seperator, only_dst_folder)).start()
        self.t1_btn_2.deselect()

    def t1_set_bulk_mode(self):
        self.t1_src_path_string = ''
        self.t1_src_path_box.configure(state="normal")
        self.t1_src_path_box.delete("0.0", "end")
        self.t1_src_path_box.configure(state="disabled")
        self.t1_dst_path_string = ''
        self.t1_dst_path_box.configure(state="normal")
        self.t1_dst_path_box.delete("0.0", "end")
        self.t1_dst_path_box.configure(state="disabled")
        mode = int(self.t1_destination_type.get())
        if mode:  # single mode
            # -------------------------------------------------------------------------------- create new folder
            self.t1_btn_3.deselect()
            self.t1_btn_3.configure(state='disabled')
            # -------------------------------------------------------------------------------- separator
            self.t1_btn_4.deselect()
            self.t1_btn_4.configure(state='disabled')
            self.t1_set_separator_state()
            # --------------------------------------------------------------------------------
        else:  # bulk mode
            # -------------------------------------------------------------------------------- create new folder
            self.t1_btn_3.configure(state='normal')
            # -------------------------------------------------------------------------------- separator
            self.t1_btn_4.configure(state='normal')
            self.t1_set_separator_state()
            # --------------------------------------------------------------------------------

    def t1_set_style(self, style=''):
        if style == 'None':
            self.t1_btn_1.configure(state='normal')
            self.t1_btn_1.select()
        if style == 'Disk':
            self.t1_btn_1.deselect()
            self.t1_btn_1.configure(state='disabled')

    def t1_set_source(self, event=None):
        mode = int(self.t1_destination_type.get())
        path = None
        if event is None:
            if mode:
                path = choose_image_dialog()
            else:
                path = fd.askdirectory(mustexist=True, title='Please choose the source directory!')
            if path is None:
                path = ''
        else:  # Drag&Drop
            temp_path = event.data.strip('{}')
            if mode:
                file_name, file_extension = os.path.splitext(temp_path)
                if os.path.isfile(temp_path) and file_extension in supported_file_types:
                    path = temp_path
            else:
                if os.path.isdir(temp_path):
                    path = temp_path
            path = '' if path is None else path
        self.t1_src_path_string = path
        self.t1_src_path_box.configure(state="normal")
        self.t1_src_path_box.delete("0.0", "end")
        self.t1_src_path_box.insert("0.0", path)
        self.t1_src_path_box.configure(state="disabled")

    def t1_set_destination_folder(self, event=None):
        if event is None:
            folder = fd.askdirectory(mustexist=True, title='Please choose the destination directory!')
        else:  # Drag&Drop
            folder = event.data.strip('{}') if os.path.isdir(event.data.strip('{}')) else ''
        self.t1_dst_path_string = folder
        self.t1_dst_path_box.configure(state="normal")
        self.t1_dst_path_box.delete("0.0", "end")
        self.t1_dst_path_box.insert("0.0", folder)
        self.t1_dst_path_box.configure(state="disabled")

    def t1_set_separator_state(self):
        button_status = self.t1_btn_4.get()
        self.t1_separator_box.configure(state="normal")
        self.t1_separator_box.delete("0.0", "end")
        self.t1_separator_box.configure(state=button_status)
        temp = 1 if button_status == 'normal' else 0
        self.t1_separator_label.configure(text_color=self.colors[temp])

    # ------------------------------------------------------------------------------------- Tab 2 - From net
    def t2_from_net(self):
        image_source = self.t2_src_list.get().strip()
        if image_source == 'Choose!':
            self.t2_src_list.configure(fg_color='#9c0000')
        else:
            keep_image_dimensions = int(self.t2_btn_1.get())
            overwrite_files = int(self.t2_btn_2.get())
            folder_style = self.t2_style_list.get().strip()
            dst_folder = self.t2_dst_path_string.strip()
            only_dst_folder = int(self.t2_destination_type.get())
            manual_selection = int(self.t2_btn_3.get())
            only_search = int(self.t2_only_search.get())
            temp_string = self.t2_search_term_box.get('0.0', 'end').strip()
            looking_for = '' if temp_string.replace(' ', '') == '' else temp_string
            try:
                text_limiter = int(self.t2_text_limiter_box.get('0.0', 'end').strip())
            except ValueError:
                text_limiter = 1000
            if os.path.isdir(dst_folder):
                arguments = (dst_folder, folder_style, keep_image_dimensions, overwrite_files, only_dst_folder,
                             image_source, manual_selection, only_search, looking_for, text_limiter,
                             self.t2_script_btn)
                threading.Thread(target=from_net.main, args=arguments).start()
            self.t2_btn_2.deselect()

    def t2_change_image_source(self, source=''):
        only_search = int(self.t2_only_search.get())
        self.t2_src_list.configure(fg_color=ctk.ThemeManager.theme["CTkOptionMenu"]["fg_color"])
        if source == 'Google' or source == 'Bing':
            if not only_search:
                self.t2_btn_3.select()
            self.t2_search_term_box.configure(require_redraw=True, state='normal', text_color=self.colors[1])
            self.t2_search_term_box.delete("0.0", "end")
            self.t2_search_term_box.insert("0.0", "folder icon")
            self.t2_search_term_label.configure(text_color=self.colors[1])
        else:
            if not only_search:
                self.t2_btn_3.deselect()
            self.t2_search_term_box.delete("0.0", "end")
            self.t2_search_term_box.configure(require_redraw=True, state='disabled', text_color=self.colors[0])
            self.t2_search_term_label.configure(text_color=self.colors[0])

    def t2_set_style(self, style=''):
        if style == 'None':
            self.t2_btn_1.configure(state='normal')
            self.t2_btn_1.select()
        if style == 'Disk':
            self.t2_btn_1.deselect()
            self.t2_btn_1.configure(state='disabled')

    def t2_set_destination_folder(self, event=None):
        if event is None:
            folder = fd.askdirectory(mustexist=True, title='Please choose the destination directory!')
        else:  # Drag&Drop
            folder = event.data.strip('{}') if os.path.isdir(event.data.strip('{}')) else ''
        self.t2_dst_path_string = folder
        self.t2_dst_path_box.configure(state="normal")
        self.t2_dst_path_box.delete("0.0", "end")
        self.t2_dst_path_box.insert("0.0", folder)
        self.t2_dst_path_box.configure(state="disabled")

    def t2_only_download(self):
        only_search = int(self.t2_only_search.get())
        if only_search:
            self.t2_btn_1.deselect()
            self.t2_btn_1.configure(state='disabled')
            self.t2_btn_2.deselect()
            self.t2_btn_2.configure(state='disabled')
            self.t2_btn_3.deselect()
            self.t2_btn_3.configure(state='disabled')
            self.t2_style_list.set('None')
            self.t2_style_list.configure(state='disabled')
        else:
            self.t2_btn_1.configure(state='normal')
            self.t2_btn_1.select()
            self.t2_btn_2.configure(state='normal')
            self.t2_btn_3.configure(state='normal')
            self.t2_btn_3.select()
            self.t2_style_list.configure(state='normal')


class SideBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(10, weight=1)
        # ------------------------------------------------------------------------ top title and buttons
        title_font = ctk.CTkFont(family="Roboto", size=20, weight="bold")
        second_title_font = ctk.CTkFont(family="Roboto", size=14, weight="bold")
        btn_font = ctk.CTkFont(family="Roboto", size=18)
        self.label_title = ctk.CTkLabel(self, text="Custom folder\nicons", font=title_font)
        self.label_title.grid(padx=20, pady=(20, 20))
        # -------------------------------- Thumb/icon cache
        self.label_cache = ctk.CTkLabel(self, text="Thumb/icon cache:", font=second_title_font)
        self.label_cache.grid(row=1, padx=20, pady=(0, 0))
        self.btn_clear = ctk.CTkButton(self, text="Clear", command=clear_thumbnail_cache, font=btn_font)
        self.btn_clear.grid(row=2, padx=20, pady=(0, 10))
        # -------------------------------- Windows explorer
        self.label_explorer = ctk.CTkLabel(self, text="Windows explorer:", font=second_title_font)
        self.label_explorer.grid(row=3, padx=20, pady=(0, 0))
        self.btn_refresh = ctk.CTkButton(self, text="Refresh", command=refresh_explorer, font=btn_font)
        self.btn_refresh.grid(row=4, padx=20, pady=0)
        self.btn_restart = ctk.CTkButton(self, text="Restart", command=restart_explorer, font=btn_font)
        self.btn_restart.grid(row=5, padx=20, pady=10)
        # -------------------------------- temp downloads
        self.label_clear_downloads = ctk.CTkLabel(self, text="temp downloads:", font=second_title_font)
        self.label_clear_downloads.grid(row=6, padx=20, pady=(0, 0))
        self.btn_clear_downloads = ctk.CTkButton(self, text="Clear", command=clear_old_download_folder, font=btn_font)
        self.btn_clear_downloads.grid(row=7, padx=20, pady=(0, 10))
        # ------------------------------------------------------------------------ Themes
        # -------------------------------------------------- label
        self.theme_label = ctk.CTkLabel(self, text="Themes:", font=second_title_font)
        self.theme_label.grid(row=8, padx=20, pady=(0, 0))
        # -------------------------------------------------- drop list
        self.theme_drop_list = ctk.CTkOptionMenu(self, values=themes[1], command=change_theme, font=btn_font)
        self.theme_drop_list.set(themes[0])
        self.theme_drop_list.grid(row=9, column=0, padx=20, pady=(0, 10), sticky='w')
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
        self.github_btn.grid(row=11, column=0, padx=(0, 25), pady=20, sticky="nes")
        self.info_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.info_btn_image,
                                      command=lambda: info_menu(self))
        self.info_btn.grid(row=11, column=0, padx=(1, 0), pady=20, sticky="")
        self.heart_btn = ctk.CTkButton(self, width=20, height=37, text="", image=self.heart_btn_image,
                                       command=self.heart)
        self.heart_btn.grid(row=11, column=0, padx=(25, 0), pady=20, sticky="nws")
        # ------------------------------------------------------------------------ tooltips
        tooltips(self.btn_clear, 'Clear windows thumbnail and icon cache.')
        tooltips(self.btn_refresh, 'Refresh windows file explorer.')
        tooltips(self.btn_restart, 'Restart windows file explorer.')
        tooltips(self.btn_clear_downloads, "Delete Wicogen's temp downloads folder.")
        tooltips(self.theme_drop_list, 'Relaunch the program to load the theme.\n'
                                       'For a custom theme, save a theme file like this:\n'
                                       '"\\Documents\\Wicogen\\theme.json"')

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

    title_font = ctk.CTkFont(family="Roboto", size=26, weight="bold")
    second_title_font = ctk.CTkFont(family="Roboto", size=18, weight="bold")
    font = ctk.CTkFont(family="Roboto", size=13)
    font_under_line = ctk.CTkFont(family="Roboto", size=13, underline=True)
    bigger_font = ctk.CTkFont(family="Roboto", size=16)

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
    label_title = ctk.CTkLabel(about_window, text="Wicogen - Windows icon generator", font=title_font)
    label_title.grid(row=0, column=0, padx=20, pady=(10, 0), sticky='news')
    link_color = "cyan"
    # ----------------------------------------------------------------------------------------------------------
    freeware_title = ctk.CTkLabel(about_window, text="(Wicogen is a Freeware)", font=second_title_font)
    freeware_title.grid(row=1, column=0, padx=20, pady=(0, 10), sticky='news')
    # ----------------------------------------------------------------------------------------------------------
    row = 2
    info = "A custom icon generator for windows.\n" \
           "Customize windows icons to your liking!\n\n" \
           "Created and developed by Idan Achrak\n"
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
    def set_theme():
        global themes
        theme_settings_path = os.path.expanduser("~\\Documents\\Wicogen\\theme.txt")
        themes = ['Default', ['Default', 'NightTrain', 'Harlequin', 'Custom']]
        if os.path.exists(theme_settings_path) and os.path.isfile(theme_settings_path):
            with open(theme_settings_path, 'r') as file:
                theme = file.read()
            if theme == 'Harlequin':
                ctk.set_default_color_theme(resource_path_finder("source/themes/Harlequin.json"))
                themes[0] = 'Harlequin'
            elif theme == 'NightTrain':
                ctk.set_default_color_theme(resource_path_finder("source/themes/NightTrain.json"))
                themes[0] = 'NightTrain'
            elif theme == 'Custom':
                path = os.path.expanduser("~\\Documents\\Wicogen\\Theme.json")
                if os.path.exists(path) and os.path.isfile(path):
                    ctk.set_default_color_theme(path)
                themes[0] = 'Custom'
    set_theme()
    app = App()
    app.mainloop()


if __name__ == '__main__':
    themes = list()
    main()

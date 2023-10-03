from .source_commands import *


def main(dst_folder: str,
         folder_style: str,
         keep_image_dimensions: bool | int = 0,
         overwrite_files: bool | int = 0,
         single_folder_mode: bool | int = 0,
         source: str = '',
         manual_selection: bool | int = 1,
         only_search: bool | int = 0,
         looking_for: str = 'folder icon',
         limiter: int = 20,
         btn=None):

    def script(single_mode=False):
        # ----------------------------------------------------- Print to console working file in light green
        search_term = ''
        for char in folder_name[:limiter]:
            if char == ' ':
                search_term += char
            elif char.isalnum():
                search_term += char
        temp_string = f'{search_term} {looking_for}' if looking_for != '' else search_term
        print(f'{Fore.LIGHTBLUE_EX}-------- {folder_name}{Style.RESET_ALL} | Search term: "{temp_string}"')
        dst_folder_path = dst_folder if single_mode else f'{dst_folder}/{folder_name}'
        icon_path = f'{dst_folder_path}/icon.ico'
        if btn:
            btn.configure(text="Downloading...")
        if only_search:
            download_images(search_term, source, only_search, 0, looking_for)
            if btn:
                btn.configure(text="Downloading...")
            return None
        if not overwrite_files and os.path.isfile(icon_path):
            return None
        found_cover = download_images(search_term, source, only_search, manual_selection, looking_for)
        if btn:
            btn.configure(text="Generating...")
        if found_cover:
            temp_path, file_name_with_extension = os.path.split(found_cover)
            file_name, file_extension = os.path.splitext(file_name_with_extension)
            if file_extension.lower() in supported_file_types:
                if os.path.exists(dst_folder_path):
                    write_desktop_ini_file(dst_folder_path)
                    generate_icon(found_cover, dst_folder_path, keep_image_dimensions, folder_style, overwrite_files)
            else:
                print(f'{Fore.LIGHTRED_EX}[Error] Code_10: Unsupported file type:{Style.RESET_ALL}{folder_name}')

    os.system('cls')
    if btn:
        btn.configure(text="Downloading...", state="disabled")
    # ----------------------------------------------------- Print to console working destiny folder in light white
    length = len(f'{"-" * 25}Current folder: {dst_folder}{"-" * 25}')
    print(f'{Fore.LIGHTWHITE_EX}{"*" * length}{Style.RESET_ALL}\n'
          f'{Fore.LIGHTWHITE_EX}{"-" * 25}Current folder: {dst_folder}{"-" * 25}{Style.RESET_ALL}\n'
          f'{Fore.LIGHTWHITE_EX}{"*" * length}{Style.RESET_ALL}')
    print(f'{Fore.LIGHTGREEN_EX}# Downloading from {source} images{Style.RESET_ALL}')
    if single_folder_mode:
        folder_name = os.path.basename(dst_folder)
        script(single_mode=True)
    else:
        for folder_name in os.listdir(dst_folder):
            if os.path.isdir(f'{dst_folder}/{folder_name}'):
                script()
    clear_thumbnail_cache()
    if btn:
        btn.configure(text="Generate", state="normal")

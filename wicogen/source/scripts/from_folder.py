from .source_commands import *


def main(source_path: str,
         dst_folder: str,
         file_name_seperator: str,
         folder_style: str,
         crete_new_folders: bool | int = 0,
         keep_image_dimensions: bool | int = 0,
         overwrite_files: bool | int = 0,
         include_seperator: bool | int = 0,
         single_folder_mode: bool | int = 0,
         btn=None):

    def bulk_mode(file):
        # ----------------------------------------------------- Print to console working file in light green
        print(f'{Fore.LIGHTBLUE_EX}----------{file}{Style.RESET_ALL}')
        # ----------------------------------------------------- extract file name and extension for later use
        file_name, file_extension = os.path.splitext(file)
        if file_extension.lower() in supported_file_types:
            if include_seperator:
                file_name = file_name.replace(file_name_seperator, '/')  # separate name to folder path
            dst_folder_path = f'{dst_folder}/{file_name}'  # new destination
            if crete_new_folders:
                make_dir_tree(dst_folder_path)
            if os.path.exists(dst_folder_path):
                write_desktop_ini_file(dst_folder_path)
                generate_icon(f'{source_path}/{file}', dst_folder_path, keep_image_dimensions, folder_style,
                              overwrite_files)
        elif os.path.isdir(f'{source_path}/{file}'):
            print(f"{Fore.LIGHTYELLOW_EX}[Error] Code_9: Unsupported file type. (folder){Style.RESET_ALL}")
        else:
            print(f'{Fore.LIGHTRED_EX}[Error] Code_10: Unsupported file type.{Style.RESET_ALL}{file}')

    def single_mode():
        file_path, file = os.path.split(source_path)
        file_name, file_extension = os.path.splitext(file)
        # ----------------------------------------------------- Print to console working file in light green
        print(f'{Fore.LIGHTBLUE_EX}----------{file}{Style.RESET_ALL}')
        # ----------------------------------------------------- extract file name and extension for later use
        if file_extension.lower() in supported_file_types:
            if os.path.exists(dst_folder):
                write_desktop_ini_file(dst_folder)
                generate_icon(source_path, dst_folder, keep_image_dimensions, folder_style, overwrite_files)
        elif os.path.isdir(f'{source_path}/{file}'):
            print(f"{Fore.LIGHTYELLOW_EX}[Error] Code_9: Unsupported file type. (folder){Style.RESET_ALL}")
        else:
            print(f'{Fore.LIGHTRED_EX}[Error] Code_10: Unsupported file type.{Style.RESET_ALL}{file}')

    os.system('cls')
    if btn:
        btn.configure(text="Generating...", state="disabled")
    # ----------------------------------------------------- Print to console working destiny folder in light white
    length = len(f'{"-" * 25}Current folder: {dst_folder}{"-" * 25}')
    print(f'{Fore.LIGHTWHITE_EX}{"*" * length}{Style.RESET_ALL}\n'
          f'{Fore.LIGHTWHITE_EX}{"-" * 25}Current folder: {dst_folder}{"-" * 25}{Style.RESET_ALL}\n'
          f'{Fore.LIGHTWHITE_EX}{"*" * length}{Style.RESET_ALL}')
    if single_folder_mode:
        single_mode()
    else:
        print(f'{Fore.LIGHTGREEN_EX}Files detected in the selected folder:{Style.RESET_ALL}\n'
              f'{os.listdir(source_path)}\n'
              f'{Fore.LIGHTGREEN_EX}# ---------------------------------------------------------------{Style.RESET_ALL}')
        for temp_file in os.listdir(source_path):
            bulk_mode(temp_file)
    clear_thumbnail_cache()
    if btn:
        btn.configure(text="Generate", state="normal")

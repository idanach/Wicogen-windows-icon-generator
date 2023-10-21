import os
import sys
import shutil
import winreg
import patoolib
from win32com.client import Dispatch

files = '.bmp OR .cur OR .dds OR .dng OR .fts OR .nef OR .tga OR .pbm OR .pcd OR ' \
        '.pcx OR .pgm OR .pnm OR .ppm OR .psd OR .ras OR .sgi OR .xbm OR .jpg OR ' \
        '.jpeg OR .jpe OR .jif OR .jfif OR .jfi OR .jp2 OR .jps OR .png OR .gif OR .webp OR .tiff OR .tif OR .ico'
version = '1.2.1'


def resource_path_finder(relative_path: str, verbose: bool = False):
    """Get absolute path to resource (exe attributes), works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as path_error_code:
        if verbose:
            print(path_error_code)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path).replace('\\', '/')


def make_dir_tree(folder: str):
    """Make directory tree."""
    try:
        exist = os.path.exists(folder)
        os.makedirs(folder, exist_ok=True)
        if not exist:
            print(f'#. Created folder: {folder}')
    except Exception as exception:
        print("Directory maker | ", exception, ' | ', folder, ' | Continuing normally')


def copy_file(src: str,
              dst: str,
              overwrite_files: bool | int = 1):
    """Move a file from the source path to destination path."""
    try:
        shutil.copy(src, dst)
        print(f'-> Moved file: {src}  ----->  {dst}')
    except PermissionError:
        if overwrite_files:
            try:
                os.remove(dst)
                shutil.copy(src, dst)
                print(f'-> Moved file (Overwrite): {src}  ----->  {dst}')
            except Exception as exception:
                print("File mover |", exception, rf'| {src}  ----->  {dst} |', 'Filed to overwrite file')
        else:
            print("File mover |", FileExistsError(), rf'| {src}  ----->  {dst} |', 'Continuing normally')
    except Exception as exception:
        print(exception)


def copy_dir(src: str,
             dst: str,
             overwrite_files: bool | int = 1):
    """Move a file from the source path to destination path."""
    try:
        shutil.copytree(src, dst)
        print(f'-> Moved file: {src}  ----->  {dst}')
    except PermissionError:
        if overwrite_files:
            try:
                os.remove(dst)
                shutil.copy(src, dst)
                print(f'-> Moved file (Overwrite): {src}  ----->  {dst}')
            except Exception as exception:
                print("File mover |", exception, rf'| {src}  ----->  {dst} |', 'Filed to overwrite file')
        else:
            print("File mover |", FileExistsError(), rf'| {src}  ----->  {dst} |', 'Continuing normally')
    except Exception as exception:
        print(exception)


# -------------------------------------------------------------------------------------
def add_to_context_menu(file_type: str,
                        registry_title: str = "key_name",
                        command: str = None,
                        title: str = None,
                        icon: str = None,
                        applies_to: str = None):
    """
    file_type: "Directory" or "*" for files.
    registry_title: The title of the subkey in the registry.
    command: The command that will run in the shell.
    title: The text that will show up in the context menu. If left empty the text wil be the -registry_title-.
    icon: Icon that will show besides the context menu entry.
    applies_to: limits the context menu entry to show only in certain times.

    to limit to certain file types:
        filetype = "*"
        applies_to = ".jpg OR .png OR..."

    Modifier: Idan Achrak
    Link: https://github.com/idanach
    -----------------------------------
    Original creator: Sam Birch
    Link: http://sbirch.net/tidbits/context_menu.html
    """
    reg_tree = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"SOFTWARE\\Classes\\{file_type}", 0, winreg.KEY_SET_VALUE)
    shell_folder = winreg.CreateKey(reg_tree, "shell")
    title_folder = winreg.CreateKey(shell_folder, registry_title)
    command_key = winreg.CreateKey(title_folder, "command")
    if title is not None:
        winreg.SetValueEx(title_folder, None, 0, winreg.REG_SZ, title)  # set title
    if icon is not None:
        winreg.SetValueEx(title_folder, 'icon', 0, winreg.REG_SZ, icon)  # set icon
    if applies_to is not None:
        winreg.SetValueEx(title_folder, 'AppliesTo', 0, winreg.REG_SZ, applies_to)  # set limitations
    if command is not None:
        winreg.SetValueEx(command_key, None, 0, winreg.REG_SZ, command)
    # Close the Registry keys
    winreg.CloseKey(command_key)
    winreg.CloseKey(title_folder)
    winreg.CloseKey(shell_folder)
    winreg.CloseKey(reg_tree)


def remove_from_context_menu(file_type: str, registry_title: str = "key_name"):
    reg_tree = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"SOFTWARE\\Classes\\{file_type}", 0, winreg.KEY_SET_VALUE)
    shell_folder = winreg.CreateKey(reg_tree, "shell")
    title_folder = winreg.CreateKey(shell_folder, registry_title)
    winreg.DeleteKey(title_folder, 'command')
    winreg.CloseKey(title_folder)
    winreg.DeleteKey(shell_folder, registry_title)
    winreg.CloseKey(shell_folder)
    winreg.CloseKey(reg_tree)


def create_shortcut(dst_folder: str = 'folder',
                    shortcut_path: str = 'C:\\',
                    shortcut_name: str = 'Shortcut'):
    """
    dst_folder: This is where the shortcut will be created
    shortcut_path: This is where the shortcut will lead to
    shortcut_name: At the destination folder, "{dst_folder}/{shortcut_name}.lnk"
    """
    make_dir_tree(dst_folder)
    path = f"{dst_folder}\\{shortcut_name}.lnk"
    # -----------------------------
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = shortcut_path
    shortcut.save()


def delete_shortcut(dst_folder: str = 'folder',
                    shortcut_name: str = 'Shortcut',
                    start_menu_flag: bool = True):
    """
    dst_folder: This is where the shortcut is located
    shortcut_name: delete --> "{dst_folder}/{shortcut_name}.lnk"
    start_menu_flag: if the shortcut is in the start menu delete the whole folder containing the link to the program
    """
    if start_menu_flag and os.path.isdir(dst_folder):
        shutil.rmtree(dst_folder)
    else:
        path = f"{dst_folder}\\{shortcut_name}.lnk"
        if os.path.isfile(path):
            os.remove(path)


# -------------------------------------------------------------------------------------
def install_extensions(install_location: str = 'Wicogen'):
    print("install_extensions")
    make_dir_tree(install_location)
    src_rar = resource_path_finder(rf'setup_source\Wicogen_extensions-V{version}.rar')
    patoolib.extract_archive(src_rar, outdir=install_location, interactive=False)
    # --------------------------------------------------------------------------- context menu additions
    exe_path = rf'"{install_location}\Wicogen_extensions-V{version}\Wicogen_extensions-V{version}.exe"'
    command_extension = rf'{exe_path} "%V"'
    command_reset_icon = rf'{exe_path} reset "%V"'
    command_clear_cache = rf'{exe_path} clear'
    # -------------- add extensions to Windows explorer context menu
    keys = [['*', 'Wicogen_set_image', command_extension, 'Set image as folder icon', exe_path, files],
            ['Directory', '1_Wicogen_choose_image', command_extension, 'Choose a folder icon', exe_path],
            ['Directory', '2_Wicogen_reset_icon', command_reset_icon, 'Reset folder icon', exe_path],
            ['Directory', '3_Wicogen_clear_cache', command_clear_cache, 'Clear icon cache', exe_path],
            ['Directory\\Background', '1_Wicogen_choose_image', command_extension, 'Choose a folder icon', exe_path],
            ['Directory\\Background', '2_Wicogen_reset_icon', command_reset_icon, 'Reset folder icon', exe_path],
            ['Directory\\Background', '3_Wicogen_clear_cache', command_clear_cache, 'Clear icon cache', exe_path]]
    for key in keys:
        add_to_context_menu(key[0], key[1], key[2], key[3], key[4])


def install_main(install_location: str = 'Wicogen',
                 desktop: bool | int = 0,
                 start_menu: bool | int = 0,
                 uninstaller: bool | int = 0):
    print("install_main")
    make_dir_tree(install_location)
    src_rar = resource_path_finder(rf'setup_source\Wicogen-V{version}.rar')
    patoolib.extract_archive(src_rar, outdir=install_location, interactive=False)
    exe_path = rf'{install_location}\Wicogen-V{version}\Wicogen-V{version}.exe'
    if desktop:
        create_shortcut(os.path.expanduser("~\\Desktop"), exe_path, "Wicogen")
    if start_menu:
        create_shortcut(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Wicogen", exe_path, "Wicogen")
    if uninstaller:
        dir_path = os.path.expanduser("~\\Documents\\Wicogen")
        make_dir_tree(dir_path)
        setup_exe = rf"{dir_path}\\Wicogen_setup-V{version}.exe"
        src_file = sys.argv[0]
        copy_file(src_file, setup_exe)
        if start_menu:
            create_shortcut(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Wicogen", setup_exe,
                            "Wicogen_uninstaller")


def save_in_file(string: str = 'Wicogen', file_name: str = 'Error'):
    # save the installation path for future uninstall
    dir_path = os.path.expanduser("~\\Documents\\Wicogen")
    make_dir_tree(dir_path)
    file_path = rf"{dir_path}\\{file_name}.txt"
    with open(file_path, 'w') as file:
        file.write(string)


def uninstall(install_location: str = 'Wicogen'):
    delete_shortcut(os.path.expanduser("~\\Desktop"), "Wicogen", False)
    delete_shortcut(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Wicogen", "Wicogen")
    delete_shortcut(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Wicogen", "Wicogen_uninstaller")
    shutil.rmtree(install_location)
    keys = [['*', 'Wicogen_set_image'],
            ['Directory', '1_Wicogen_choose_image'],
            ['Directory', '2_Wicogen_reset_icon'],
            ['Directory', '3_Wicogen_clear_cache'],
            ['Directory\\Background', '1_Wicogen_choose_image'],
            ['Directory\\Background', '2_Wicogen_reset_icon'],
            ['Directory\\Background', '3_Wicogen_clear_cache']]
    # remove keys created by the installer
    for key in keys:
        try:
            remove_from_context_menu(key[0], key[1])
        except FileNotFoundError:
            pass
        except Exception as excep:
            raise excep
    dir_path = os.path.expanduser("~\\Documents\\Wicogen")
    if os.path.isdir(dir_path):
        dir_path = os.path.expanduser("~\\Documents\\Wicogen")
        os.system(rf'rmdir /s /q  "{dir_path}" >nul 2>&1')

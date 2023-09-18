import os
import sys
import shutil
import random
from PIL import Image, ImageDraw
from colorama import Fore
from colorama import Style
from tkinter import filedialog as fd
from . import image_downloader
from . import imdb_image_downloader


icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
supported_file_types = ('.bmp', '.cur', '.dds', '.dng', '.fts', '.nef', '.tga', '.pbm', '.pcd',
                        '.pcx', '.pgm', '.pnm', '.ppm', '.psd', '.ras', '.sgi', '.xbm',
                        '.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.jp2', '.jps',
                        '.png', '.gif', '.webp', '.tiff', '.tif', '.ico')


# ---------------------------------------------------------------------------------------------------------- misc
def clear_thumbnail_cache():
    """Clear windows thumbnail and icon cache."""
    os.system(r'c:\Windows\System32\ie4uinit.exe -show >nul 2>&1')
    os.system(r'DEL /A /Q "%localappdata%\IconCache.db" >nul 2>&1')
    os.system(r'del /f /s /q /a %LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db >nul 2>&1')
    os.system(r'del /f /s /q /a %LocalAppData%\Microsoft\Windows\Explorer\iconcache_*.db >nul 2>&1')
    os.system(r'c:\Windows\System32\ie4uinit.exe -ClearIconCache >nul 2>&1')
    print(f'{Fore.LIGHTCYAN_EX}----------------------------Cleared cache----------------------------{Style.RESET_ALL}')


def refresh_explorer():
    """Refresh file explorer."""
    os.system(r"c:\Windows\System32\ie4uinit.exe -show >nul 2>&1")
    print(f'{Fore.LIGHTCYAN_EX}----------------------------Refreshed explorer----------------'
          f'------------{Style.RESET_ALL}')


def restart_explorer():
    """Restart file explorer."""
    os.system(r"taskkill /F /IM explorer.exe & start explorer >nul 2>&1")
    print(f'{Fore.LIGHTCYAN_EX}----------------------------Restarted explorer----------------'
          f'------------{Style.RESET_ALL}')


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


def error_codes(error_source, error_code, error_path, error_source2=''):
    """Print to screen color coded error codes."""
    if type(error_code) is FileNotFoundError:
        # print folder not found error in light cyan color
        print(f'{Fore.LIGHTYELLOW_EX}[Error] Code_1: Folder not found '
              f'[{error_source}][{error_source2}]:{Style.RESET_ALL} {error_path}')
    elif type(error_code) is PermissionError:
        # print permission denied error in light cyan color (can be caused by Windows folder settings)
        print(f'{Fore.LIGHTRED_EX}[Error] Code_2: Permission denied '
              f'[{error_source}][{error_source2}]:{Style.RESET_ALL} {error_path}')
    elif type(error_code) is FileExistsError:
        print(f'{Fore.LIGHTCYAN_EX}[Error] Code_3: File exists '
              f'[{error_source}][{error_source2}]:{Style.RESET_ALL} {error_path}')
    else:
        # print unknown error type in light red color
        print(f'{Fore.LIGHTRED_EX}[Error] Code_0: Failed, printing full error output '
              f'[{error_source}][{error_source2}]:{Style.RESET_ALL} {error_path} --> {error_code}')


def make_dir_tree(folder: str):
    """Make directory tree."""
    try:
        os.makedirs(folder, exist_ok=True)
        print(f'{Fore.LIGHTGREEN_EX}#. Created folder: {Style.RESET_ALL}{folder}')
    except Exception as exception:
        error_codes("Directory maker", exception, folder, 'Continuing normally')


def copy_file(src: str,
              dst: str,
              overwrite_files: bool | int = 0,
              make_hidden: bool | int = 1):
    """Move a file from the source path to destination path."""
    try:
        shutil.copy(src, dst)
        if make_hidden:
            os.system(rf'attrib +h "{dst}"')
        print(f'{Fore.LIGHTGREEN_EX}-> Moved file: {Style.RESET_ALL}{src}  ----->  {dst}')
    except PermissionError:
        if overwrite_files:
            try:
                os.remove(dst)
                shutil.copy(src, dst)
                if make_hidden:
                    os.system(rf'attrib +h "{dst}"')
                print(f'{Fore.LIGHTGREEN_EX}-> Moved file (Overwrite): {Style.RESET_ALL}{src}  ----->  {dst}')
            except Exception as exception:
                error_codes("File mover", exception, rf'{src}  ----->  {dst}', 'Filed to overwrite file')
        else:
            error_codes("File mover", FileExistsError(), rf'{src}  ----->  {dst}', 'Continuing normally')
    except Exception as exception:
        error_codes("File mover", exception, rf'{src}  ----->  {dst}', 'Continuing normally')


# ---------------------------------------------------------------------------------------------------------- gen app
def write_desktop_ini_file(dst_folder: str):
    """Write a desktop.ini file in the destination folder and set its attributes (+s +h).
    After that set the attributes of the folder (+r).
    """
    def write_ini():
        with open(dst_file, 'wb') as w_ini_file:
            w_ini_file.write(ini_contents)  # Write shell info to ini file
        print(f'{Fore.LIGHTGREEN_EX}@. Generating new desktop.ini file:{Style.RESET_ALL} {dst_file}')
        os.system(rf'attrib +s +h "{dst_file}"')  # Add 'system' and 'hidden' attributes to desktop.ini file
        os.system(rf'attrib +r "{dst_folder}"')  # Add 'read' attribute to folder

    ini_contents = b'[.ShellClassInfo]\r\nIconResource=icon.ico\r\n'
    dst_file = f'{dst_folder}/desktop.ini'
    if os.path.isfile(dst_file):
        with open(dst_file, 'rb') as ini_file:
            temp_contents = ini_file.read()
        if temp_contents != ini_contents:
            print(f'{Fore.LIGHTYELLOW_EX}@. Deleting old desktop.ini file:{Style.RESET_ALL} {dst_file}')
            os.remove(dst_file)
            write_ini()
    else:
        write_ini()


def generate_icon(src_image_path: str,
                  dst_icon_path: str,
                  keep_image_dimensions: bool = 1,
                  folder_style: str = '',
                  overwrite_file: bool | int = True):
    """Generates an icon from a source image to destination path."""
    def add_corners(im, rad):
        """Rounds corners of an image by radius."""
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    if os.path.exists(dst_icon_path) and not overwrite_file:
        return None
    image = Image.open(src_image_path)
    if folder_style == 'Disk':
        path = resource_path_finder("source/images/back.png")
        back = Image.open(path)
        size = (308, 461)
        if keep_image_dimensions:
            image.thumbnail(size, Image.ANTIALIAS)
        else:
            image = image.resize(size)
        image = add_corners(image, 11)
        path = resource_path_finder("source/images/front.png")
        front = Image.open(path)
        image.paste(front, (0, 0), front)
        back.paste(image, (59, 24), image)
        image = back
    elif keep_image_dimensions:
        width, height = image.size
        square_size = max(width, height)
        transparent_square = Image.new("RGBA", (square_size, square_size), (0, 0, 0, 0))
        x_offset, y_offset = (square_size - width) // 2, (square_size - height) // 2
        transparent_square.paste(image, (x_offset, y_offset))  # past the banner on the transparent square
        image = transparent_square
    else:
        image = image.resize((256, 256))
    try:
        if os.path.exists(dst_icon_path):
            print(f'{Fore.LIGHTYELLOW_EX}@. Deleting old icon:{Style.RESET_ALL} {dst_icon_path}')
            os.remove(dst_icon_path)
        print(f'{Fore.LIGHTGREEN_EX}@. Generating icon:{Style.RESET_ALL} {dst_icon_path}')
        image.save(dst_icon_path, bitmap_format='bmp', mode='RGBA', sizes=icon_sizes)
        os.system(rf'attrib +h "{dst_icon_path}"')
    except Exception as exc:
        error_codes('Icon generator', exc, dst_icon_path)


def choose_image_dialog(start_folder: str = ''):
    """Pick image file dialog."""
    image = ''
    file_extension = ''
    while file_extension not in supported_file_types:
        image = fd.askopenfilename(initialdir=start_folder, title='Please choose an image!',
                                   filetypes=[('Image files', supported_file_types)])
        file_name, file_extension = os.path.splitext(image)
        if file_name == '':
            return None
    return image


# ----------------------------------------------------------------
# download image from a search engine
def download_images(query_string: str,
                    search_engine: str = 'google',
                    overwrite: bool | int = False,
                    manual_selection: bool | int = False,
                    looking_for: str = 'folder icon'):
    if search_engine == 'IMDB':
        path = imdb_image_downloader.downloader(query_string[:20], overwrite=overwrite)
        if manual_selection:
            return choose_image_dialog(path)
        else:
            file_list = os.listdir(path)
            print(file_list)
            if file_list:
                return f'{path}/{file_list[0]}'
            else:
                return None

    else:
        path = image_downloader.downloader(search_engine, f'{query_string[:20]} {looking_for}', overwrite=overwrite)
        if manual_selection:
            return choose_image_dialog(path)
        else:
            file_list = os.listdir(path)
            print(file_list)
            if file_list:
                return f'{path}/{random.choice(file_list)}'
            else:
                return None
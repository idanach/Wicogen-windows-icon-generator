import os
import sys
import subprocess
import time
import ctypes
from PIL import Image
from tkinter import filedialog as fd


icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
supported_file_types = ('.bmp', '.cur', '.dds', '.dng', '.fts', '.nef', '.tga', '.pbm', '.pcd',
                        '.pcx', '.pgm', '.pnm', '.ppm', '.psd', '.ras', '.sgi', '.xbm',
                        '.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.jp2', '.jps',
                        '.png', '.gif', '.webp', '.tiff', '.tif', '.ico',
                        '.BMP', '.CUR', '.DDS', '.DNG', '.FTS', '.NEF', '.TGA', '.PBM', '.PCD',
                        '.PCX', '.PGM', '.PNM', '.PPM', '.PSD', '.RAS', '.SGI', '.XBM',
                        '.JPG', '.JPEG', '.JPE', '.JIF', '.JFIF', '.JFI', '.JP2', '.JPS',
                        '.PNG', '.GIF', '.WEBP', '.TIFF', '.TIF', '.ICO')


def clear_thumbnail_cache():
    """Clear windows thumbnail and icon cache."""
    subprocess.call(r'c:\Windows\System32\ie4uinit.exe -show >nul 2>&1', shell=True)
    subprocess.call(r'DEL /A /Q "%localappdata%\IconCache.db" >nul 2>&1', shell=True)
    subprocess.call(r'del /f /s /q /a %LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db >nul 2>&1', shell=True)
    subprocess.call(r'del /f /s /q /a %LocalAppData%\Microsoft\Windows\Explorer\iconcache_*.db >nul 2>&1', shell=True)
    subprocess.call(r'c:\Windows\System32\ie4uinit.exe -ClearIconCache >nul 2>&1', shell=True)
    time.sleep(2)
    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)


def refresh_explorer():
    """Refresh file explorer."""
    subprocess.call(r"c:\Windows\System32\ie4uinit.exe -show >nul 2>&1")
    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
    time.sleep(2)
    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
    time.sleep(2)
    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)


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


def write_desktop_ini_file(dst_folder: str):
    """
    Write a desktop.ini file in the destination folder and set its attributes (+s +h).
    After that set the attributes of the folder (+r).
    """
    def write_ini():
        with open(dst_ini, 'wb') as w_ini_file:
            w_ini_file.write(ini_contents)  # Write shell info to ini file
        os.system(rf'attrib +s +h "{dst_ini}"')  # Add 'system' and 'hidden' attributes to desktop.ini file
        os.system(rf'attrib +r "{dst_folder}"')  # Add 'read' attribute to folder

    ini_contents = b'[.ShellClassInfo]\r\nIconResource=icon.ico\r\n'
    dst_ini = f'{dst_folder}/desktop.ini'
    try:
        if os.path.isfile(dst_ini) and os.path.exists(dst_ini):
            with open(dst_ini, 'rb') as ini_file:
                temp_contents = ini_file.read()
            if temp_contents != ini_contents:
                os.remove(dst_ini)
                write_ini()
                return None
        else:
            write_ini()
    except Exception as exc:
        with open(rf'{dst_folder}\wicogen_error.txt', "w") as file:
            file.write(f'{exc}')


def generate_icon(src_image_path: str,
                  dst_directory: str,
                  file_name: str = 'icon'):
    """Generates an icon from a source image to destination path."""
    dst_icon_path = rf'{dst_directory}\{file_name}.ico'
    if os.path.isfile(src_image_path) and os.path.isdir(dst_directory):
        try:
            image = Image.open(src_image_path)
            width, height = image.size
            square_size = max(width, height)
            transparent_square = Image.new("RGBA", (square_size, square_size), (0, 0, 0, 0))
            x_offset, y_offset = (square_size - width) // 2, (square_size - height) // 2
            transparent_square.paste(image, (x_offset, y_offset))  # past the banner on the transparent square
            image = transparent_square
            if os.path.isfile(dst_icon_path) and os.path.exists(dst_icon_path):
                os.remove(dst_icon_path)
            image.save(dst_icon_path, bitmap_format='bmp', mode='RGBA', sizes=icon_sizes)
            subprocess.call(rf'attrib +h "{dst_icon_path}"', shell=True)
            image.close()
        except Exception as exc:
            with open(rf'{dst_directory}\wicogen_error.txt', "w") as file:
                file.write(f'{exc}')


def script(destination_dir: str, source_image: str):
    image_name, image_extension = os.path.splitext(os.path.basename(source_image))
    if image_extension in supported_file_types:
        write_desktop_ini_file(destination_dir)
        generate_icon(source_image, destination_dir)
        refresh_explorer()


def reset_folder(dst_folder: str):
    """Reset folder icon. Delete the icon.ico file, the desktop.ini and reset folder attribute."""
    try:
        if os.path.isdir(dst_folder):
            subprocess.call(rf'attrib -r "{dst_folder}"', shell=True)
            ini_file = f'{dst_folder}/desktop.ini'
            ico_file = f'{dst_folder}/icon.ico'
            if os.path.isfile(ini_file):
                subprocess.call(rf'attrib +s +h "{ini_file}"', shell=True)
                os.remove(ini_file)
            if os.path.isfile(ico_file):
                subprocess.call(rf'attrib +h "{ico_file}"', shell=True)
                os.remove(ico_file)
    except Exception as exc:
        with open(rf'{dst_folder}\wicogen_error.txt', "w") as file:
            file.write(f'{exc}')


def main():
    argument = arguments[1]  # Path to folder or file or command
    if os.path.isdir(argument):  # path is a directory
        temp_image_path = choose_image_dialog(argument)
        if temp_image_path is not None:
            script(destination_dir=argument, source_image=temp_image_path)
    elif os.path.isfile(argument):  # path is a file
        temp_dir_path = os.path.dirname(argument)
        script(destination_dir=temp_dir_path, source_image=argument)
    elif argument == 'clear':
        clear_thumbnail_cache()
    elif argument == 'reset':
        reset_folder(arguments[2])
    else:
        print('something went wrong')


if __name__ == '__main__':
    arguments = sys.argv
    # for argument in arguments:
    #     print(argument)
    if len(arguments) != 1:
        main()

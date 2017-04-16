from cx_Freeze import setup, Executable
import os.path
import sys

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
if sys.platform == "win32":
    base = "Win32GUI"
executables = [Executable("wallpaper.py", base=base)]
options = {"build_exe": {"packages": ["PIL", "bs4", "requests", "ctypes", "os", "datetime"],
                         "include_files": [
                            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                            "wallpapers"
                         ] + os.listdir("required dlls")}}


setup(
    name="wallpaperAuto",
    options=options,
    version="1.0.1",
    description="Searches the Wallpaper of the Day and sets it as the desktop background",
    executables=executables
)

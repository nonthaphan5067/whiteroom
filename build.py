import os
import PyInstaller.__main__
import shutil

if __name__ == "__main__":
    print("Remove dist dir...")
    shutil.rmtree("dist")

    print("Building program...")
    PyInstaller.__main__.run(
        ["main.py", "--clean", "--onedir", "--windowed", "--name", "WhiteRoom"]
    )

    print("Zip file...")
    shutil.make_archive("WhiteRoom", "zip", "dist/WhiteRoom")

    print("Build success.")

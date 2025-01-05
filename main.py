import pystyle
import os
import time
import requests
from android_py_modules import android_py_adb

def cs():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("[WARNING] Unable to determine system!")
        time.sleep(5)

choices = r"""

 [1] Reboot device (you can select the mode!)
 [2] Flash Custom ROM locally
 [3] Flash Custom ROM via URL
 [4] Root device (requires custom recovery to be installed!)
 [5] Brick device (be careful!)
 [99] Exit
 
"""

cs()

banner = r"""
 ________  ________   ________  ________  ________  ___  ________      ________  ___    ___ 
|\   __  \|\   ___  \|\   ___ \|\   __  \|\   __  \|\  \|\   ___ \    |\   __  \|\  \  /  /|
\ \  \|\  \ \  \\ \  \ \  \_|\ \ \  \|\  \ \  \|\  \ \  \ \  \_|\ \   \ \  \|\  \ \  \/  / /
 \ \   __  \ \  \\ \  \ \  \ \\ \ \   _  _\ \  \\\  \ \  \ \  \ \\ \   \ \   ____\ \    / / 
  \ \  \ \  \ \  \\ \  \ \  \_\\ \ \  \\  \\ \  \\\  \ \  \ \  \_\\ \ __\ \  \___|\/  /  /  
   \ \__\ \__\ \__\\ \__\ \_______\ \__\\ _\\ \_______\ \__\ \_______\\__\ \__\ __/  / /    
    \|__|\|__|\|__| \|__|\|_______|\|__|\|__|\|_______|\|__|\|_______\|__|\|__||\___/ /     
                                                                               \|___|/      
"""

reboot_choices = r"""

 [1] Regular reboot
 [2] [MTK ONLY] Reboot to preloader (same as regular reboot as preloader gets started there)
 [3] Reboot to recovery
 [4] Reboot to sideload
 [5] Reboot to bootloader
 [6] Reboot to fastbootd
 [7] [QUALCOMM ONLY] Reboot to EDL
 [99] Return to main menu
 
"""

def reboot_options():
    cs()
    pystyle.Write.Print(banner, pystyle.Colors.blue_to_green, interval=0)
    pystyle.Write.Print("android.py | The best ADB and fastboot Python toolkit for modifying Android devices. | Alpha 1.1", pystyle.Colors.blue_to_green, interval=0)

    print()
    print()

    pystyle.Write.Print("Reboot choices:", pystyle.Colors.blue_to_white, interval=0)
    pystyle.Write.Print(reboot_choices, pystyle.Colors.blue_to_white, interval=0)
    reboot_choice = int(pystyle.Write.Input("Which option would you like to select? ", pystyle.Colors.red_to_yellow, interval=0))

    if reboot_choice == 1:
        android_py_adb.reboot("system")
        cs()
        main()
    elif reboot_choice == 2:
        android_py_adb.reboot("preloader")
        cs()
        main()
    elif reboot_choice == 3:
        android_py_adb.reboot("recovery")
        cs()
        main()
    elif reboot_choice == 4:
        android_py_adb.reboot("sideload")
        cs()
        main()
    elif reboot_choice == 5:
        android_py_adb.reboot("bootloader")
        cs()
        main()
    elif reboot_choice == 6:
        android_py_adb.reboot("fastbootd")
        cs()
        main()
    elif reboot_choice == 7:
        android_py_adb.reboot("edl")
        cs()
        main()
    elif reboot_choice == 99:
        cs()
        main()

def flash_local():
    cs()
    rom_path = pystyle.Write.Input("Specify path to the Custom ROM you want to flash: ", pystyle.Colors.red_to_yellow, interval=0)
    rom_boot_path = pystyle.Write.Input("Specify path to the Custom ROM's boot/recovery.img you want to flash: ", pystyle.Colors.red_to_yellow, interval=0)
    android_py_adb.reboot("bootloader")
    android_py_adb.flash_rom(rom_boot_path, rom_path)
    pystyle.Write.Print("Done! Returning to main menu in 3 seconds.", pystyle.Colors.red_to_yellow, interval=0)
    time.sleep(3)
    main()

def flash_via_url():
    cs()
    rom_url = pystyle.Write.Input("Specify URL to the Custom ROM you want to flash: ", pystyle.Colors.red_to_yellow, interval=0)
    rom_boot_url = pystyle.Write.Input("Specify URL to the Custom ROM's boot/recovery.img you want to flash: ", pystyle.Colors.red_to_yellow, interval=0)
    if os.name == "nt":
        with open(os.path.join(os.getenv("TEMP"), "rom.zip"), 'wb') as file:
            response = requests.get(rom_url, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        with open(os.path.join(os.getenv("TEMP"), "boot.img"), 'wb') as file:
            response = requests.get(rom_boot_url, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        with open("/tmp/rom.zip", 'wb') as file:
            response = requests.get(rom_url, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        with open("/tmp/boot.img", 'wb') as file:
            response = requests.get(rom_boot_url, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    android_py_adb.reboot("bootloader")
    if os.name == "nt":
        android_py_adb.flash_rom("%temp%\\boot.img", "%temp%\\rom.zip")
    elif os.name == "posix":
        android_py_adb.flash_rom("/tmp/boot.img", "/tmp/rom.zip")
    if os.name == "nt":
        os.system("del %temp%\\boot.img")
        os.system("del %temp%\\rom.zip")
    else:
        os.remove("/tmp/boot.img")
        os.remove("/tmp/rom.zip")
    pystyle.Write.Print("Done! Returning to main menu in 3 seconds.", pystyle.Colors.red_to_yellow, interval=0)
    time.sleep(3)
    main()

def root():
    print()
    android_py_adb.reboot("sideload")
    if os.name == "nt":
        with open(os.path.join(os.getenv("TEMP"), "magisk.apk"), 'wb') as file:
            response = requests.get("https://github.com/topjohnwu/Magisk/releases/download/v28.1/Magisk-v28.1.apk", stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    elif os.name == "posix":
        with open("/tmp/magisk.apk", 'wb') as file:
            response = requests.get("https://github.com/topjohnwu/Magisk/releases/download/v28.1/Magisk-v28.1.apk", stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    if os.name == "nt":
        android_py_adb.sideload("%temp%\\magisk.apk")
    elif os.name == "posix":
        android_py_adb.sideload("/tmp/magisk.apk")
    if os.name == "nt":
        os.system("del %temp%\\magisk.apk")
    elif os.name == "posix":
        os.remove("/tmp/magisk.apk")
    pystyle.Write.Print("Done! Returning to main menu in 3 seconds.", pystyle.Colors.red_to_yellow, interval=0)
    time.sleep(3)
    cs()
    main()

def brick():
    cs()
    brick_choice = pystyle.Write.Input("[WARNING] This will erase the Linux kernel from your device! Are you sure you wanna continue? (yes/anything else = no) ", pystyle.Colors.red_to_yellow, interval=0)
    if brick_choice == "yes":
        android_py_adb.fastboot_erase("boot")
    else:
        cs()
        main()

def main():
    pystyle.Write.Print(banner, pystyle.Colors.blue_to_green, interval=0)
    pystyle.Write.Print("android.py | The best ADB and fastboot Python toolkit for modifying Android devices. | Alpha 1.0", pystyle.Colors.blue_to_green, interval=0)
    time.sleep(3)

    print()
    print()

    pystyle.Write.Print("Choices (WIP):", pystyle.Colors.blue_to_white, interval=0)
    pystyle.Write.Print(choices, pystyle.Colors.blue_to_white, interval=0)
    choice = int(pystyle.Write.Input("Which option would you like to select? ", pystyle.Colors.red_to_yellow, interval=0))

    if choice == 1:
        reboot_options()
    elif choice == 2:
        flash_local()
    elif choice == 3:
        flash_via_url()
    elif choice == 4:
        root()
    elif choice == 5:
        brick()
    elif choice == 99:
        exit()
    else:
        print("Invalid choice.")
        time.sleep(3)
        cs()
        main()

main()

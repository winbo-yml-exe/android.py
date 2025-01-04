import pystyle
import os
import time
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
    pystyle.Write.Print("android.py | The best ADB and fastboot Python toolkit for modifying Android devices. | Alpha 1.0", pystyle.Colors.blue_to_green, interval=0)

    print()
    print()

    pystyle.Write.Print("Reboot choices:", pystyle.Colors.blue_to_white, interval=0)
    pystyle.Write.Print(reboot_choices, pystyle.Colors.blue_to_red, interval=0)
    reboot_choice = int(pystyle.Write.Input("Which option would you like to select? ", pystyle.Colors.red_to_yellow, interval=0))

    if reboot_choice == 1:
        android_py_adb.reboot("system")
    elif reboot_choice == 2:
        android_py_adb.reboot("preloader")
    elif reboot_choice == 3:
        android_py_adb.reboot("recovery")
    elif reboot_choice == 4:
        android_py_adb.reboot("sideload")
    elif reboot_choice == 5:
        android_py_adb.reboot("bootloader")
    elif reboot_choice == 6:
        android_py_adb.reboot("fastbootd")
    elif reboot_choice == 7:
        android_py_adb.reboot("edl")
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
        os.system(f"curl -Lo %temp%\\rom.zip {rom_url}")
        os.system(f"curl -Lo %temp%\\boot.img {rom_boot_url}")
    else:
        os.system(f"curl -Lo /tmp/rom.zip {rom_url}")
        os.system(f"curl -Lo /tmp/boot.img {rom_boot_url}")
    android_py_adb.reboot("bootloader")
    android_py_adb.flash_rom("%temp%\\boot.img", "%temp%\\rom.zip")
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
        os.system("curl -Lo %temp%\\magisk.apk https://github.com/topjohnwu/Magisk/releases/download/v28.1/Magisk-v28.1.apk")
    elif os.name == "posix":
        os.system("curl -Lo /tmp/magisk.apk https://github.com/topjohnwu/Magisk/releases/download/v28.1/Magisk-v28.1.apk")
    android_py_adb.sideload("%temp%\\magisk.apk")
    if os.name == "nt":
        os.system("del %temp%\\magisk.apk")
    elif os.name == "posix":
        os.remove("/tmp/magisk.apk")
    pystyle.Write.Print("Done! Returning to main menu in 3 seconds.", pystyle.Colors.red_to_yellow, interval=0)
    time.sleep(3)
    cs()
    main()

def main():
    pystyle.Write.Print(banner, pystyle.Colors.blue_to_green, interval=0)
    pystyle.Write.Print("android.py | The best ADB and fastboot Python toolkit for modifying Android devices. | Alpha 1.0", pystyle.Colors.blue_to_green, interval=0)
    time.sleep(3)

    print()
    print()

    pystyle.Write.Print("Choices (WIP):", pystyle.Colors.blue_to_white, interval=0)
    pystyle.Write.Print(choices, pystyle.Colors.blue_to_red, interval=0)
    choice = int(pystyle.Write.Input("Which option would you like to select? ", pystyle.Colors.red_to_yellow, interval=0))

    if choice == 1:
        reboot_options()
    elif choice == 2:
        flash_local()
    elif choice == 3:
        flash_via_url()
    elif choice == 4:
        root()
    elif choice == 99:
        exit()
    else:
        print("Invalid choice.")
        time.sleep(3)
        cs()
        main()

main()
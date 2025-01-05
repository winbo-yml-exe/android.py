import os
import time
import platform

if platform.system() == "Windows":
    adb_exe = "adb-windows\\adb.exe"
    fastboot_exe = "adb-windows\\fastboot.exe"
elif platform.system() == "Linux":
    os.system("chmod a+x adb-linux/adb")
    os.system("chmod a+x adb-linux/fastboot")
    adb_exe = "adb-linux/adb"
    fastboot_exe = "adb-linux/fastboot"
elif platform.system() == "Darwin":
    os.system("chmod a+x adb-linux/adb")
    os.system("chmod a+x adb-linux/fastboot")
    adb_exe = "adb-darwin/adb"
    fastboot_exe = "adb-darwin/fastboot"
else:
    print("Error! Unsupported system has been detected. This tool depends on ADB which is only compatible with MacOS, Windows or Linux. Please try using this tool on one of these OSes.")
    exit()

def reboot(target):
    if target.lower() == "bootloader":
        print("Rebooting to bootloader...")
        print()
        os.system(f"{adb_exe} reboot bootloader")
    elif target.lower() == "fastbootd":
        print("Rebooting to fastbootd...")
        print()
        os.system(f"{adb_exe} reboot fastboot")
    elif target.lower() == "edl":
        print("This does not work on every phone, but let's try anyways.")
        print("Rebooting to EDL...")
        print()
        reboot("bootloader")
        os.system(f"{fastboot_exe} oem edl")
    elif target.lower() == "brom":
        print("Booting to BROM is not supported by this tool.")
    elif target.lower() == "preloader":
        print("Rebooting to preloader...")
        os.system(f"{adb_exe} reboot")
    elif target.lower() == "system":
        print("Rebooting...")
        os.system(f"{adb_exe} reboot")
    elif target.lower() == "recovery":
        print("Rebooting to recovery...")
        os.system(f"{adb_exe} reboot recovery")
    elif target.lower() == "sideload":
        print("Rebooting to sideload...")
        os.system(f"{adb_exe} reboot sideload")
    elif target.lower() == "download":
        print("Rebooting to download mode...")
        os.system(f"{adb_exe} reboot download")
    else:
        print("The mode you specified doesn't exist.")

def flash_rom(boot_path, sideload_path):
    os.system(f"{fastboot_exe} -w")
    os.system(f"{fastboot_exe} flash boot {boot_path}")
    os.system(f"{fastboot_exe} flash recovery {boot_path}")
    os.system(f"{fastboot_exe} reboot recovery")
    input("Enter sideloading mode in the recovery and press enter to continue.")
    os.system(f"{adb_exe} sideload {sideload_path}")

def sideload(package):
    time.sleep(20)
    os.system(f"{adb_exe} sideload {package}")

def fastboot_erase(partition):
    os.system(f"{adb_exe} reboot bootloader")
    os.system(f"{fastboot_exe} erase {partition}")

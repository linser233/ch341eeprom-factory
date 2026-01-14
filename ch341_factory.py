import os
import subprocess
import argparse
import datetime
import random
import os
import argparse
from intelhex import IntelHex

class eepCH341(object):
    """
    :param size_str: EEPROM size string      - default "24c02"
    :param size_bytes: EEPROM size in bytes  - default 256
    :param majorVersion: Major version number
    :param minorVersion: Minor version number
    :param serial: Serial number (8 bytes)
    :param product: Product string (up to 95 bytes)
    :param MODE: Mode byte            - default 0x12
    :param CFG: Configuration byte    - default 0xCC
    :param VID: Vendor ID (2 bytes)   - default (0x1A, 0x86)
    :param PID: Product ID (2 bytes)  - default (0x55, 0x12)
    """

    def __init__(
            self, majorVersion: bytes, minorVersion: bytes, serial: str, product: str,
            size_str: str = "24c02", size_bytes: int = 256,
            MODE: bytes = 0x12, CFG: bytes = 0xCC, VID: bytearray = (0x1A, 0x86), PID: bytearray = (0x55, 0x12)
    ):
        self.size = size_str
        self.size_bytes = size_bytes
        self.majorVersion = majorVersion
        self.minorVersion = minorVersion
        if len(serial) == 8:
            self.serial = serial
        else:
            raise ValueError("Serial number must be 8 digits")
        if len(product) < 95:
            self.product = product
        else:
            raise ValueError("Product string too long, max 95 characters")
        self.MODE = MODE
        self.CFG = CFG
        self.VID = VID
        self.PID = PID
        self.device_id = os.urandom(16)

    def __str__(self):
        return f"EEPROM: {self.majorVersion}.{self.minorVersion} {self.serial} {self.product}"
    
    def bytes(self):
        """
        Generate the EEPROM bytes
        :return: bytearray of EEPROM
        """
        rom = bytearray(self.size_bytes-1)
        rom[0] = 0x53
        rom[1] = self.MODE
        rom[2] = self.CFG
        rom[3] = 0x00
        rom[4] = self.VID[1]
        rom[5] = self.VID[0]
        rom[6] = self.PID[1]
        rom[7] = self.PID[0]
        rom[8] = self.minorVersion
        rom[9] = self.majorVersion
        # Bytes 10-15 are padding
        # Serial number (bytes 16-23)
        serial_bytes = bytearray(self.serial.encode('ascii'))
        rom[16:23] = serial_bytes
        # Bytes 24-31 are padding
        # Product String bytes (32-127)
        product_bytes = bytearray(self.product.encode('ascii'))
        rom[32:32 + len(product_bytes)] = product_bytes
        rom[32 + len(product_bytes) + 1:32 + len(product_bytes) + 16 + 1] = self.device_id

        return rom

    def hex(self):
        return self.bytes().hex()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CH341 EEPROM Intel HEX generator")
    parser.add_argument("--major-version", type=int, default=1, dest="majorVersion",
                        help="Major version number (default: 1)")
    parser.add_argument("--minor-version", type=int, default=0, dest="minorVersion",
                        help="Minor version number (default: 0)")
    parser.add_argument("-r", "--random", type=str, default=None,
                        help="Specify random digits (00-99). If not specified, automatically generate 0-99 random number")
    args = parser.parse_args()

    # Check if -r argument is numeric and within 0-99 range
    if args.random is not None:
        if not args.random.isdigit():
            raise ValueError("Random digits must be numeric (0-99)")
        rand_num = int(args.random)
        if rand_num < 0 or rand_num > 99:
            raise ValueError("Random digits must be within 0-99 range")
    else:
        rand_num = random.randint(0, 99)

    # Automatically generate serial number
    now = datetime.datetime.now()
    year_digit = now.year - 2026   # 2026=0, 2027=1...
    week_num = now.isocalendar()[1]  # ISO week number
    hour_num = now.hour

    serial_str = f"{year_digit}{week_num:02d}{hour_num:03d}{rand_num:02d}"

    eeprom = eepCH341(args.majorVersion, args.minorVersion, serial_str, "uMesh")

    # Ensure output directory exists
    output_dir = "./firmware-output"
    os.makedirs(output_dir, exist_ok=True)

    # Include serial number in filename
    output_filename = os.path.join(output_dir, f"eeprom_{serial_str}.hex")

    # Use IntelHex to output standard HEX file
    ih = IntelHex()
    data = eeprom.bytes()
    for i, b in enumerate(data):
        ih[i] = b
    ih.write_hex_file(output_filename)

    print(f"Generated serial: {serial_str}")
    print(f"Intel HEX file written to {output_filename}")

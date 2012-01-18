# Simple program which recovers lost picture from SD cards
# Copyright (C) 2012  Angelo Marletta
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import logging
import argparse

class ImageScanner:

    def __init__(self, device):
        self.fd = open(device, "rb")
        self.pointer = 0

    def read_byte(self):
        char = self.fd.read(1)
        if char == "": raise Exception("EOF")
        self.pointer += 1
        return ord(char)

    def next_start_of_image(self):
        while (True):
            if self.read_byte() == 0xFF and self.read_byte() == 0xD8:
                return self.pointer - 2
        
    def next_end_of_image(self):
        while (True):
            if self.read_byte() == 0xFF and self.read_byte() == 0xD9:
                return self.pointer - 2
    
class Apolla:

    MAX_FILESIZE = 10*2**20

    def __init__(self, device):
        self.device = device
        self.scanner = ImageScanner(self.device)
        self.devicesize = self.get_file_size(self.device)

    def recover(self):
        with open(self.device, "rb") as fd:
            for picture in self.find_pictures():
                self.export_file(picture[0], picture[1])

    def find_pictures(self):
        while (True):
            start_of_image = self.scanner.next_start_of_image()
            end_of_image = self.scanner.next_end_of_image()
            size = end_of_image + 2 - start_of_image
            if size <= Apolla.MAX_FILESIZE:
                yield (start_of_image, size)

    def export_file(self, start, size):
        with open(self.device, "rb") as input_file:
            input_file.seek(start)
            bytes = input_file.read(size)
            output_filename = "%d.jpg" % start
        with open(output_filename, "w") as output_file:
            output_file.write(bytes)
        print "File %s exported" % output_filename

    def get_file_size(self, filename):
        fd = os.open(filename, os.O_RDONLY)
        try:
            return os.lseek(fd, 0, os.SEEK_END)
        finally:
            os.close(fd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Recovers logs pictures.')
    parser.add_argument('--device', help='block device file')
    args = parser.parse_args()
    r = Apolla(args.device)
    r.recover()
    r.close()

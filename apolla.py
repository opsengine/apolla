import sys
import os
import logging

class FileReader:

    def __init__(self, fd):
        self.fd = fd

    def read_byte(self):
        return ord(self.fd.read(1))

class ImageScanner:

    def __init__(self, fd):
        self.fd = fd
        self.reader = FileReader(fd)

    def next_start_of_image(self):
        while (True):
            if self.reader.read_byte() == 0xFF and self.reader.read_byte() == 0xD8:
                return self.pointer - 2
        
    def next_end_of_image(self):
        while (True):
            if self.reader.read_byte() == 0xFF and self.reader.read_byte() == 0xD9:
                return self.pointer - 2
    
class Apolla:

    MAX_FILESIZE = 10*2**20

    def __init__(self, device):
        self.device = open(device, "rb")
        self.scanner = ImageScanner(device)
        self.devicesize = self.get_file_size(self.device)

    def recover(self):
        with open(self.device, "rb") as fd:
            reader = Reader(self.device)
            self.fd = fd
            for picture in self.find_pictures():
                print picture
                #self.export_file(picture)

    def find_pictures(self):
        while (True):
            start_of_image = self.scanner.next_start_of_image()
            end_of_image = self.scanner.next_end_of_image()
            if start_of_image == None or end_of_image == None:
                break
            size = end_of_image + 2 - start_of_image
            if size <= Apolla.MAX_FILESIZE:
                yield (start_of_image, size)

    def export_file(self):
        with open(self.filename, "rb") as input_file:
            input_file.seek(start)
            bytes = input_file.read(size)
            output_filename = "%d.jpg" % start
        with open(output_filename, "w") as output_file:
            output_file.write(bytes)
        print "File %s exported" % output_filename

    def get_file_size(self, filename):
        "Get the file size by seeking at end"
        fd= os.open(filename, os.O_RDONLY)
        try:
            return os.lseek(fd, 0, os.SEEK_END)
        finally:
            os.close(fd)

r = Apolla("/dev/mmcblk0p1")

r.recover()

r.close()

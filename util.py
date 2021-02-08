
import logging
import sys

def first_not_none(lst):
    for item in lst:
        if item is not None:
            return item
    return None

class LoggerAsFile:
    # From: https://stackoverflow.com/a/36296215
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        temp_linebuf = self.linebuf + buf
        self.linebuf = ''
        for line in temp_linebuf.splitlines(True):
            # From the io.TextIOWrapper docs:
            #   On output, if newline is None, any '\n' characters written
            #   are translated to the system default line separator.
            # By default sys.stdout.write() expects '\n' newlines and then
            # translates them so this is still cross platform.
            if line[-1] == '\n':
                self.logger.log(self.log_level, line.rstrip())
            else:
                self.linebuf += line

    def flush(self):
        if self.linebuf != '':
            self.logger.log(self.log_level, self.linebuf.rstrip())
        self.linebuf = ''

def dummy_class(name):
    return type(name, (), {})

def main():
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    sys.stdout = LoggerAsFile(logger)

    print('Print!')
    print('Another print to INFO!')
    print(dummy_class('Point')())
if __name__ == "__main__":
    main()

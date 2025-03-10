import abc

class Scanner(abc.ABC):
    def __init__(self):
        self.max_resolution = 1
        self.serial_number = 'asd'
    def scan_document(self):
        return 'The document has been scanned'
    def get_scanner_status(self):
        return f'max_resolution: {self.max_resolution}\nserial: {self.serial_number}'

class Printer(abc.ABC):
    def __init__(self):
        self.printer_max_resolution = 1
        self.printer_serial_number = 'asd'

    @abc.abstractmethod
    def print_document(self):
        return 'The document has been printed'
    def get_printer_status(self):
        return f'max_resolution: {self.printer_max_resolution}\nserial: {self.printer_serial_number}'
        
class MFD1(Printer, Scanner):
    def __init__(self, printer_serial_number: str, printer_max_resolution: int):
        self.printer_max_resolution = printer_max_resolution
        self.printer_serial_number = printer_serial_number
    def print_document(self):
        return 'The document has been printed from MFD1'
   
m1 = MFD1('aa', 111)
print(m1.get_printer_status())
print(m1.print_document())
     
        
import csv
import os

class ConsoleView:

    ERROR_FORMAT = '!!! {} !!!'
    SUPPORTED_FILE_EXTENSION = ('.csv', '.txt')

    def __init__(self, c):
        self._c = c

    def print_(self, result):
        if isinstance(result, (list, tuple)):
            for i in result:
                self._c.sendall(bytes(str(i), encoding='utf-8'))
        elif isinstance(result, Exception):
            self._c.sendall(bytes(self.ERROR_FORMAT.format(result), encoding='utf-8'))
        else:
            self._c.sendall(bytes(result, encoding='utf-8'))

    def imputer(self, msg):
        text = b''
        self._c.sendall(msg)
        while True:
            data = self._c.recv(1024)

            if not data:
                self._c.close()
                return

            if data == b'\r\n':
                return text.decode('utf8')
            text += data
            if len(text) >= 2 and data == b'\x08':
                text = text[:-2]
            elif len(text) == 1 and data == b'\x08':
                text = text[:-1]
            print(text)

    def print_to_file(self, result, filename='phonebook.csv'):
        extension = os.path.splitext(filename)[1]
        if extension not in self.SUPPORTED_FILE_EXTENSION:
            self.print_(PhoneBookError('File extension must be one of ({})'.
                                       format(self.SUPPORTED_FILE_EXTENSION)))
        if extension == '.csv':
            with open(filename, 'w') as csv_file:
                writer = csv.writer(csv_file)
                for contact in result:
                    writer.writerow(list(contact))

        else:
            with open(filename, 'w') as file:
                for contact in result:
                    file.write('{}\n'.format(str(contact)))

        self.print_("Done. You can get your file {}".format(filename))
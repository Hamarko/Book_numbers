import csv
import os
import sys
from functools import wraps
from BookPhone import PhoneBook


def contact_attribute(msg, attr):
    def set_value_decorator(func):
        @wraps(func)
        def wrapper(self, **kwargs):
            kwargs[attr] = input(msg)
            func(self, **kwargs)
        return wrapper
    return set_value_decorator

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.actions = {'c': self.add_new_contact,
                        'r': self.read,
                        'u': self.update,
                        'd': self.del_,
                        'a': self.read_all,
                        'f': self.to_file,
                        'h': self.help_,
                        'q': exit_}

    @contact_attribute(msg='Set name: ', attr='name')
    @contact_attribute(msg='Set phone number: ', attr='phone_number')
    def add_new_contact(self, **kwargs):
        self.view.print_(self.model.add_contact(**kwargs))

    @contact_attribute(msg='Set name: ', attr='name')
    def read(self, **kwargs):
        self.view.print_(self.model[kwargs['name']])

    @contact_attribute(msg='Set OLD name: ', attr='old_name')
    @contact_attribute(msg='Set OLD phone number: ', attr='old_phone_number')
    @contact_attribute(msg='Set NEW name: ', attr='new_name')
    @contact_attribute(msg='Set NEW phone number: ', attr='new_phone_number')
    def update(self, **kwargs):
        self.model.update(kwargs)

    def read_all(self):
        self.view.print_(self.model.read_all())

    @contact_attribute(msg='Set file name: ', attr='file_name')
    def to_file(self, file_name):
        """Save as... all records."""
        self.view.print_to_file(self.model.read_all(), file_name)

    @contact_attribute(msg='Set name: ', attr='name')
    @contact_attribute(msg='Set phone number: ', attr='phone_number')
    def del_(self, **kwargs):
        self.view.print_(self.model.delete_(**kwargs))

    def help_(self):
        helps = ["Use 'c' -> {}".format(self.model.add_contact.__doc__),
                 "Use 'r' -> {}".format(self.model.read.__doc__),
                 "Use 'u' -> {}".format(self.model.update.__doc__),
                 "Use 'd' -> {}".format(self.model.delete_.__doc__),
                 "Use 'a' -> {}".format(self.model.read_all.__doc__),
                 "Use 'f' -> {}".format(self.to_file.__doc__),
                 "Use 'q' -> {}".format(exit_.__doc__)]
        self.view.print_(helps)

    def do_actions(self, command):
        try:
            self.actions[command]()
        except KeyError:
            self.view.print_(PhoneBookError("Wrong command. Use 'h' to "
                                            "get help."))

    def run(self):
        while True:
            command = input("Select command (use h get help): ").lower()
            self.do_actions(command)


class ConsoleView:
    ERROR_FORMAT = '!!! {} !!!'
    SUPPORTED_FILE_EXTENSION = ('.csv', '.txt')

    def print_(self, result):
        if isinstance(result, (list, tuple)):
            for i in result:
                print(i)
        elif isinstance(result, Exception):
            print(self.ERROR_FORMAT.format(result))
        else:
            print(result)

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


def exit_():
    """Exit."""

    print('Goodbye!')
    sys.exit()


def main():
    controller = Controller(PhoneBook(), ConsoleView())
    controller.run()


if __name__ == '__main__':
    main()
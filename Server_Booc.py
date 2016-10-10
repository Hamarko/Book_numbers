import sys
import socket
import threading
import time
from BookBD import PhoneBook, PhoneBookError
from ConsolView import ConsoleView

class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.actions = {'c': self.add_new_contact,
                        'r': self.read,
                        'u': self.update,
                        'd': self.del_,
                        'a': self.read_all,
                        'h': self.help_,
                        'q': exit_}

    def add_new_contact(self, **kwargs):
        kwargs["name"] = self.view.imputer(b'Set name: ')
        kwargs['phone_number'] = self.view.imputer(b'Set phone number: ')
        self.view.print_(self.model.add_contact(**kwargs))

    def read(self, **kwargs):
        self.view.print_('Set name: ')
        self.view.print_(self.model[kwargs['name']])

    def update(self, **kwargs):
        kwargs["old_name"] = self.view.imputer(b'Set OLD name: ')
        kwargs['old_phone_number'] = self.view.imputer(b'Set OLD phone number: ')
        kwargs["new_name"] = self.view.imputer(b'Set NEW name: ')
        kwargs['new_phone_number'] = self.view.imputer(b'Set NEW phone number: ')
        self.model.update(kwargs)

    def read_all(self):
        self.view.print_(self.model.read_all())

    def del_(self, **kwargs):
        kwargs['name'] = self.view.imputer(b'Set name: ')
        kwargs['phone_number'] = self.view.imputer(b'Set phone number: ')
        self.view.print_(self.model.delete_(**kwargs))

    def help_(self):
        helps = ["Use 'c' -> {}\r\n".format(self.model.add_contact.__doc__),
                 "Use 'r' -> {}\r\n".format(self.model.read.__doc__),
                 "Use 'u' -> {}\r\n".format(self.model.update.__doc__),
                 "Use 'd' -> {}\r\n".format(self.model.delete_.__doc__),
                 "Use 'a' -> {}\r\n".format(self.model.read_all.__doc__),
                 "Use 'q' -> {}\r\n".format(exit_.__doc__)]
        self.view.print_(helps)

    def do_actions(self, command):
        try:
            self.actions[command]()
        except KeyError:
            self.view.print_(PhoneBookError("Wrong command. Use 'h' to "
                                            "get help."))

    def run(self):
        while True:
            print("run")
            command = self.view.imputer(b"Select command (use h get help): ").lower()
            self.do_actions(command)



def exit_():
    """Exit."""
    print('Goodbye!')
    sys.exit()


def hendle(c):
    view = ConsoleView(c)
    controller = Controller(PhoneBook(), view)
    controller.run()


def main():
    s = socket.socket()
    s.bind(("localhost", 8000))
    s.listen(5)
    print("Server is wating")
    while True:
        c, a = s.accept()
        print("Connected:{}".format(a))
        t = threading.Thread(target=hendle, args=(c,))
        t.start()
        time.sleep(1)


if __name__ == '__main__':
    main()
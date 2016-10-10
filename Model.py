

class ContactError(Exception):
    pass


class Contact:
    STR_CONTACT_FORMAT = '{:.<20}{:.>20}\r\n'

    def __init__(self, name, phone_number):
        self._name = name
        self._phone_number = phone_number

    @property
    def name(self):
        return self._name

    @property
    def phone_number(self):
        return self._phone_number

    def __str__(self):
        return self.STR_CONTACT_FORMAT.format(self.name, self.phone_number)

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({}, {})'.format(class_name, self._name, self.phone_number)

    def __hash__(self):
        return hash(self.name) ^ hash(self.phone_number)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.phone_number == other.phone_number and \
                   self.name == self.phone_number
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.name < other.name
        else:
            raise ContactError("We can't compare {} object with {} object".
                               format(type(self).__name__,
                                      type(other).__name__))

    def __iter__(self):
        return (i for i in (self.name, self.phone_number))

    def __getitem__(self, key):
        if key == self._name:
            return True
        elif key == self._phone_number:
            return True
        return False
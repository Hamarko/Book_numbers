import pickle
from Model import Contact, ContactError


class PhoneBookError(Exception):
    pass


class PhoneBook:
    def __init__(self, base_file='phonebook.pickle'):
        self.file = base_file
        self.contacts = self.init_contacts()

    def init_contacts(self):
        try:
            with open(self.file, 'rb') as base_file:
                return pickle.load(base_file)
        except (EOFError, FileNotFoundError):
            return set()

    # TODO Ask Denys. How use 'save' as decorator inside class?
    def save(self):
        with open(self.file, 'wb') as f:
            pickle.dump(self.contacts, f)

    def add_contact(self, **kwargs):
        """Add contact to the phone book."""
        if self.check_contact(**kwargs):
            return PhoneBookError('A contact with this name and phone number, '
                                  'already exists')
        try:
            self.contacts.add(Contact(**kwargs))
        except ContactError as e:
            return e
        self.save()
        return 'Add contact {name} with phone number: {phone_number} to the ' \
               'phone book. Successfully!'.format(**kwargs)

    def read(self, name):
        """Read phone number from the phone book by contact name."""
        for contact in self.contacts:
            if contact[name]:
                return contact
        return 'No found contact by name={}'.format(name)

    def __getitem__(self, key):
        """Read phone number from the phone book by contact name."""
        for contact in self.contacts:
            if contact[key]:
                return contact
        return 'No found contact by name={}'.format(key)

    # TODO change read and this method
    def check_contact(self, name, phone_number):
        for contact in self.contacts:
            if contact[name] and contact[phone_number]:
                return contact

    def read_all(self):
        """Print all records."""

        contacts = [contact for contact in sorted(self.contacts)]
        return contacts if contacts else \
            PhoneBookError('The phone book is empty.')

    def update(self, kwargs):
        """Update contact"""
        old_contact = self.check_contact(kwargs['old_name'],
                                         kwargs['old_phone_number'])
        new_contact = Contact(kwargs['new_name'], kwargs['new_phone_number'])
        self.contacts.discard(old_contact)
        self.contacts.add(new_contact)
        self.save()
        return 'Contact with old name {old_name} and old number ' \
               '{old_phone_number} has been changed. New name {new_name} and' \
               ' new number {new_phone_number}. Successfully!'.\
            format(**kwargs)

    def delete_(self, name, phone_number):
        """Delete contact from the phone book by name."""
        contact = self.check_contact(name, phone_number)
        if contact:
            self.contacts.remove(contact)
            self.save()
            return 'Delete contact {} with phone number {}. Successfully!'.\
                format(name, phone_number)
        return PhoneBookError('No found contact with name={} and phone={}'.
                              format(name, phone_number))
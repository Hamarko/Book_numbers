import sqlite3

class PhoneBookError(Exception):
    pass


class PhoneBook:
    STR_CONTACT_FORMAT = '{:.<20}{:.>20}\r\n'

    def __init__(self):
        self.contacts = self.init_contacts()

    def init_contacts(self):
       c =sqlite3.connect('book.db')
       try:
           curs = c.cursor()
           curs.execute('''CREATE TABLE phonbook
                        (name varchar unique, phone_number varchar)''')
           curs.close()
           return c
       except sqlite3.OperationalError:
           return c

    def add_contact(self, **kwargs):
        """Add contact to the phone book."""
        curs = self.contacts.cursor()
        try:
            curs.execute(" INSERT INTO phonbook VALUES(?,?)",(kwargs['name'],kwargs['phone_number']))
        except sqlite3.IntegrityError:
            curs.close()
            return PhoneBookError('A contact with this name and phone number, '
                                  'already exists')
        curs.close()
        self.contacts.commit()
        return 'Add contact {name} with phone number: {phone_number} to the ' \
               'phone book. Successfully!'.format(**kwargs)

    def read(self, key):
        """Read phone number from the phone book by contact name."""
        curs = self.contacts.cursor()
        data = curs.execute('SELECT * FROM phonbook WHERE name ="{}"'.format(key)).fetchone()
        curs.close()
        if data:
            return self.STR_CONTACT_FORMAT.format(data[0], data[1])
        return 'No found contact by name={}'.format(key)

    def read_all(self):
        """Print all records."""
        curs = self.contacts.cursor()
        data = curs.execute('SELECT * FROM phonbook ')
        contacts = ["{:.<20}{:.>20}\r\n".format(contact[0], contact[1]) for contact in data]
        curs.close()
        return contacts if contacts else \
            PhoneBookError('The phone book is empty.')

    def update(self, kwargs):
        """Update contact"""
        curs = self.contacts.cursor()
        old_contact = curs.execute('SELECT * FROM phonbook WHERE name ="{}"'.format(kwargs['old_name'])).fetchone()
        if old_contact:
            return 'No found contact by name={}'.format(kwargs['old_name'])
        curs.execute('DELETE FROM phonbook WHERE name ="{}"'.format(kwargs['old_name']))
        curs.close()
        self.contacts.commit()
        self.add_contact(name=kwargs['new_name'],phone_number= kwargs['new_phone_number'])
        return 'Contact with old name {old_name} and old number ' \
               '{old_phone_number} has been changed. New name {new_name} and' \
               ' new number {new_phone_number}. Successfully!'.\
            format(**kwargs)

    def delete_(self, **kwargs):

        """Delete contact from the phone book by name."""
        curs = self.contacts.cursor()
        old_contact = curs.execute('SELECT * FROM phonbook WHERE name ="{}"'.format(kwargs['name'])).fetchone()
        print ("old_contact=",old_contact)
        if not old_contact:
            curs.close()
            return 'No found contact by name={}'.format(kwargs['name'])
        curs.execute('DELETE FROM phonbook WHERE name ="{}"'.format(kwargs['name']))
        curs.close()
        self.contacts.commit()
        return 'Delete contact {} with phone number {}. Successfully!'.\
                format(kwargs['name'], kwargs ['phone_number'])
    def end_db(self):
        self.contacts.close()




"""

PhoneBook
Trying to create a console version of the PhoneBook apps. using knowledge after two lessons:
    loop
    exceptions
    list comprehension
    defining a function (with default values)
    doc string
    LEGB
    decorators

"""

import functools
import sys
import pickle

class PhoneBookError(Exception):
    pass


try:
    with open('phonebook.pickle','rb') as f:

        phonebook = pickle.load(f)
except:
    phonebook = {}
    


def set_name(fn):
    @functools.wraps(fn)
    def wrapped(**kwargs):
        while True:
            contact_name = input('Set contact name: ')
            if not contact_name.isdigit() and contact_name.isalnum() :
                return fn(name=contact_name, **kwargs)
            print('For creating or updating   new contact you must set name, use return letters!')
    return wrapped


def set_phone(fn):
    @functools.wraps(fn)
    def wrapped(**kwargs):
        while True:
            phone_number = input('Set phone number: ')
            if phone_number:
                if phone_number.isdigit() or phone_number[0] is "+" and phone_number[1:].isdigit():
                    return fn(number=phone_number, **kwargs)
            print('For creating or updating   new contact you must set phone number, use return figures!')
    return wrapped

def set_ried(fn):
    @functools.wraps(fn)
    def wrapped(**kwargs):
        f=fn(**kwargs)
        with open('phonebook.pickle','wb') as f:
            pickle.dump(phonebook,f)
        return "auto save"
    return wrapped

        


@set_name
@set_phone
@set_ried
def create(name, number):
    """Add contact to the phone book."""
    if name not in phonebook:
        phonebook[name] = number        
        return 'Add contact {} with phone number: {} to the phone book. Successfully!'.format(name, number)
    else:
        raise PhoneBookError('Sorry. We already have contact with "{}" name.'.format(name))


@set_name
def read(name):
    """Read phone number from the phone book by contact name."""
    try:
        return '{:.<20}{:.>20}'.format(name, phonebook[name])
    except KeyError:
        raise PhoneBookError('Sorry. Contact with name {} is absent in our phone book.'.format(name))


@set_name
@set_phone
@set_ried
def update(name, number):
    """Update phone number by name."""
    if name in phonebook:
        old_number = phonebook[name]
        phonebook[name] = number
        return 'Contact {}, old number {} has been changed to {}. Successfully!'.format(name, old_number, number)
    else:
        raise PhoneBookError('Contact with the name {} is absent in our phone book.'.format(name))


@set_name
@set_ried
def delete(name):
    """Delete contact from the phone book by name."""
    try:
        number = phonebook[name]
        del phonebook[name]
        return 'Delete contact {} with phone number {}. Successfully!'.format(name, number)
    except KeyError:
        raise PhoneBookError('Contact with the name {} is absent in our phone book.'.format(name))


def view_all():
    """Print all records."""
    print(phonebook)
    if phonebook:
        info = ['The phone book contains {} record(s).'.format(phonebook.__len__())]
        info.extend('{:.<20}{:.>20}'.format(name, number) for name, number in sorted(phonebook.items()))
        return '\n'.join(info)
    else:
        raise PhoneBookError('The phone book is empty.')


def help_():
    """Get list of commands."""
    return '\n'.join(['Press {} and Enter -> {}'.format(key, command.__doc__) for key, command in _action.items()])


def exit_():
    """Exit."""
    print('Goodbye!')
    sys.exit()

_action = {'c': create,
           'r': read,
           'u': update,
           'd': delete,
           '.': view_all,
           'h': help_,
           'q': exit_}


def controller():
    """Controller and view."""
    print('Welcome to our Phone book apps.')
    while True:
        command = input("Select command (c, r, u, d, ., q) or h to get help): ").lower()
        try:
            print(_action.get(command, help_)())
        except PhoneBookError as e:
            print(e)


# if __name__ == '__main__': # __name__ == builtins
controller()

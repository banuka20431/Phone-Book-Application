from Contact import Contact
from DateTime import DateTime
import re


class ContactHandler:

    @staticmethod
    def displayMenus(headers: tuple | list) -> int:
        for i, header in enumerate(headers):
            print(f" [{i + 1}] {header}")
        while True:
            try:
                id = int(input("\n>_ ")) - 1
            except ValueError:
                print('(-) Error : Invalid Input!')
                continue
            if id not in range(0, len(headers)):
                print('(-) Error : Invalid Selection!')
            else:
                break
        return id
    
    @staticmethod
    def validate(data_field_name: str, data: str) -> bool:
        match data_field_name:
            case 'name':
                valid_pattern = re.compile(r"^([a-zA-Z]+\s?)+$")
            case 'email':
                valid_pattern = re.compile(r"^(www.)?[A-Za-z0-9_.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
            case 'phone_number':
                valid_pattern = re.compile(r"^(\+94|0)[0-9]{9}")
        if valid_pattern.fullmatch(data):
            return True
        return False

    def __init__(self, contact_list: list[Contact], contact_types_arr: tuple, PASSKEY: str, ) -> None:
        self.contact_list = contact_list
        self.contact_type_names = contact_types_arr
        self.PASSKEY = PASSKEY

    def create_new_contact(self, inf: tuple=None) -> Contact:
        if inf is None:
            contact_name = self.__getcontactname()
            contact_email = self.__getemail()
            contact_phoneNumbers = [self.__getphonenumber(), ]
            contact_types = [self.__getcontacttype(), ]
            return Contact(contact_name, contact_email, contact_phoneNumbers, contact_types, DateTime.getdatetime(), DateTime.getdatetime())
        else:
            return Contact(*inf)
    
    def search_contact(self) -> Contact | None:
        method = self.__getsearchmethod()
        match method:
            case 'Name':
                return self.search_byname(self.__getcontactname())
            case 'Email':
                return self.__search_byemail(self.__getemail())
            case 'Phone Number':
                return self.__search_byphone_number(self.__getphonenumber())

    def update_contact(self, contact: Contact) -> Contact:
        update_field = self.__getupdatefieldname()
        match update_field:
            case 'Name':
                contact.setname(self.__getcontactname())
            case 'Email':
                contact.setEmail(self.__getemail())
            case 'Phone Number':
                print('\nSELECT AN ACTION >\n')
                action_id = self.displayMenus(('Add new phone number', 'Change existing phone number'))
                if action_id == 0:
                    contact.setPhoneNumber(self.__getphonenumber(), self.__getcontacttype())
                else:
                    existing_phone_numbers = contact.get_contact_Phone_numbers()
                    print('\nSELECT A PHONE NUMBER TO CHANGE >\n')
                    selected_phone_number = existing_phone_numbers[self.displayMenus(existing_phone_numbers)]
                    contact.setPhoneNumber(selected_phone_number, self.__getcontacttype(), self.__getphonenumber(),
                                            True)
        contact.set_modified_date()
        return contact

    def __getupdatefieldname(self) -> str:
        fields = ("Name", "Phone Number", "Email")
        print('\nSELECT A FIELD FOR THE UPDATE >\n')
        return fields[self.displayMenus(fields)]

    def search_byname(self, search_str: str) -> Contact | None:
        for contact in self.contact_list:
            if contact.get_contact_name().lower() == search_str.lower():
                return contact
        return None

    def __search_byemail(self, search_str: str) -> Contact | None:
        for contact in self.contact_list:
            if contact.get_contact_email() == search_str:
                return contact
        return None

    def __search_byphone_number(self, search_str: str) -> Contact | None:
        for contact in self.contact_list:
            if search_str in contact.get_contact_Phone_numbers():
                return contact
        return None

    def __getsearchmethod(self) -> str:
        methods = ("Name", "Phone Number", "Email")
        print('\nSELECT A METHOD FOR THE SEARCH >\n')
        return methods[self.displayMenus(methods)]

    def __getcontactname(self) -> str:
        while True:
            name = input("\nENTER CONTACT'S NAME : ")
            if self.validate('name', name):
                return name
            print('(-) Error : Invalid Input!')

    def __getemail(self) -> str:
        while True:
            email = input("\nENTER CONTACT'S EMAIL ADDRESS : ")
            if self.validate('email', email):
                return email
            print('(-) Error : Invalid Input!')

    def __getphonenumber(self) -> str:
        while True:
            phone_number = input("\nENTER THE CONTACT'S PHONE NUMBER [07********] : ")
            if self.validate('phone_number', phone_number):
                return phone_number
            print('(-) Error : Invalid Input!')

    def __getcontacttype(self) -> str:
        print('\nSELECT THE CONTACT TYPE >\n')
        return self.contact_type_names[self.displayMenus(self.contact_type_names)]
    
if __name__ == '__main__':
    print("\n\tRun 'main.py'\n")
    
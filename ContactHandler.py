from Contact import Contact
from DateTime import DateTime
import re
from tkinter.ttk import Treeview


class ContactHandler:

    @staticmethod
    def displayMenus(headers: tuple | list) -> int:
        for i, header in enumerate(headers):
            print(f" [{i + 1}] {header}")
        while True:
            try:
                id = int(input("\n>_ ")) - 1
            except ValueError:
                print("(-) Error : Invalid Input!")
                continue
            if id not in range(0, len(headers)):
                print("(-) Error : Invalid Selection!")
            else:
                break
        return id

    @staticmethod
    def validate(data_field_name: str, data: str) -> bool:
        match data_field_name:
            case "Name":
                valid_pattern = re.compile(r"^([a-zA-Z]+\s?)+$")
            case "Email":
                valid_pattern = re.compile(
                    r"^(www.)?[A-Za-z0-9_\.%+-]+@[A-Za-z0-9\.-]+\.[A-Za-z]{2,}"
                )
            case "Phone Number":
                valid_pattern = re.compile(r"^(\+94|0)[0-9]{9}")
        if valid_pattern.fullmatch(data) is not None:
            return True
        return False

    def __init__(
        self,
        contact_list: list[Contact],
        contact_types_arr: tuple,
        PASSKEY: str,
    ) -> None:
        self.contact_list = contact_list
        self.contact_type_names = contact_types_arr
        self.PASSKEY = PASSKEY

    def create_new_contact(self, inf: tuple = None) -> Contact:
        if inf is None:
            contact_name = self.__getcontactname()
            contact_email = self.__getemail()
            contact_phoneNumbers = [
                self.__getphonenumber(),
            ]
            contact_types = [
                self.__getcontacttype(),
            ]
            return Contact(
                contact_name,
                contact_email,
                contact_phoneNumbers,
                contact_types,
                DateTime.getdatetime(),
                DateTime.getdatetime(),
            )
        else:
            return Contact(*inf)

    def search_contact(self) -> Contact | None:
        method = self.__getsearchmethod()
        match method:
            case "Name":
                return self.search_byname(self.__getcontactname())
            case "Email":
                return self.__search_byemail(self.__getemail())
            case "Phone Number":
                return self.__search_byphone_number(self.__getphonenumber())

    def update_contact(self, contact: Contact) -> Contact:
        update_field = self.__getupdatefieldname()
        match update_field:
            case "Name":
                contact.setname(self.__getcontactname())
            case "Email":
                contact.setEmail(self.__getemail())
            case "Phone Number":
                print("\nSELECT AN ACTION >\n")
                action_id = self.displayMenus(
                    ("Add new phone number", "Change existing phone number")
                )
                if action_id == 0:
                    contact.setPhoneNumber(
                        self.__getphonenumber(), self.__getcontacttype()
                    )
                else:
                    existing_phone_numbers = contact.get_contact_Phone_numbers()
                    print("\nSELECT A PHONE NUMBER TO CHANGE >\n")
                    selected_phone_number = existing_phone_numbers[
                        self.displayMenus(existing_phone_numbers)
                    ]
                    contact.setPhoneNumber(
                        selected_phone_number,
                        self.__getcontacttype(),
                        self.__getphonenumber(),
                        True,
                    )
        contact.set_modified_date()
        return contact

    def __getupdatefieldname(self) -> str:
        fields = ("Name", "Phone Number", "Email")
        print("\nSELECT A FIELD FOR THE UPDATE >\n")
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
        print("\nSELECT A METHOD FOR THE SEARCH >\n")
        return methods[self.displayMenus(methods)]

    def __getcontactname(self) -> str:
        while True:
            name = input("\nENTER CONTACT'S NAME : ")
            if self.validate("Name", name):
                return name
            print("(-) Error : Invalid Input!")

    def __getemail(self) -> str:
        while True:
            email = input("\nENTER CONTACT'S EMAIL ADDRESS : ")
            if self.validate("Email", email):
                return email
            print("(-) Error : Invalid Input!")

    def __getphonenumber(self) -> str:
        while True:
            phone_number = input("\nENTER THE CONTACT'S PHONE NUMBER [07********] : ")
            if self.validate("Phone Number", phone_number):
                return phone_number
            print("(-) Error : Invalid Input!")

    def __getcontacttype(self) -> str:
        print("\nSELECT THE CONTACT TYPE >\n")
        return self.contact_type_names[self.displayMenus(self.contact_type_names)]


class ContactList:

    def __init__(self, existing_contact_list: list[Contact]) -> None:
        self.contact_list: list[Contact] = existing_contact_list

    def display_all(self) -> None:
        print(self.contact_list)

    def get_contact_names(self) -> list[str]:

        contact_names = []
        for contact in self.contact_list:
            contact_names.append(
                self.capitalize_contact_name(contact.get_contact_name())
            )
        return contact_names

    def get_primary_numbers(self) -> list[str]:

        primary_numbers = []
        for contact in self.contact_list:
            primary_numbers.append(self.format_contact_phone_number(contact.get_primary_phone_number()))

        return primary_numbers

    def get_contact_index(
        self, req_contact_name: str
    ) -> int | bool:
        try:
            return self.get_contact_names().index(req_contact_name)
        except ValueError:
            return -1

    def get_selected_contact(
        self,
        table: Treeview,
        arr_size: int = 1,
        column_id: int = 0,
    ) -> Contact | list[Contact]:

        selection_ids = table.selection()
        if arr_size < 2:
            selected_contact_name = table.item(selection_ids[0])["values"][column_id]
            return self.get_contact(selected_contact_name)
        else:
            return_arr = []
            for id in selection_ids():
                selected_contact_name = table.item(id)["values"][column_id]
                return_arr.append(
                    self.get_contact(selected_contact_name)
                )
            return return_arr

    def get_contact(self, req_contact_name: str) -> Contact:
        contact_index = self.get_contact_index(req_contact_name)
        if contact_index >= 0:
            return self.contact_list[contact_index]
        return False

    def insert_new_contact(self, contact: Contact, contact_index: int=-1) -> None:
        if contact_index < 0:
            self.contact_list.append(contact)
        else:
            self.contact_list.pop(contact_index)
            self.contact_list.insert(contact_index, contact)

    def capitalize_contact_name(self, contact_name: str) -> str:
        # nimal perera -> Nimal Perera
        return " ".join([n.capitalize() for n in contact_name.split(" ")])

    def format_contact_phone_number(self, contact_phone_number: str) -> str:
        # +94701234567 / 0711234567 -> 071-1234567
        service_digits_count = 3
        if contact_phone_number.startswith("+94"):
            contact_phone_number = "07" + contact_phone_number.removeprefix("+94")

        try:
            return "-".join(
                [
                    contact_phone_number[:service_digits_count],
                    contact_phone_number[service_digits_count:],
                ]
            )
        except IndexError:
            return contact_phone_number


if __name__ == "__main__":
    print("\n\tRun 'main.py'\n")

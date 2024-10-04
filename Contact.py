class Contact:

    def __init__(self, contact_name: str, contact_email: str, contact_phone_numbers: list[str], contact_types: list[str]):
        self.__Name = contact_name
        self.__Email = contact_email
        self.__PhoneNumbers = contact_phone_numbers
        self.__ContactTypes = contact_types
        
    def get_contact_name(self) -> str:
        return self.__Name
    
    def get_contact_email(self) -> str:
        return self.__Email
    
    def get_contact_Phone_numbers(self) -> list[str]:
        return self.__PhoneNumbers
    
    def get_contact_contact_type(self, phone_number: str) -> str:
        return self.__ContactTypes[self.__PhoneNumbers.index(phone_number)]
    
    def get_contact_type_list(self) -> list[str]:
        return self.__ContactTypes

    def display_contact(self) -> None:
        
        print(
            f"""\n
+---------------------------------------------------------+

\t Name : {self.__Name}
\t Email : {self.__Email}
\t\t Phone Numbers 
"""
        )
        index_no = 1
        for phone_number, contact_type in zip(self.__PhoneNumbers, self.__ContactTypes):
            print(f"\t{index_no}. {phone_number} [ {contact_type} ]")
            index_no += 1
        print('\n+---------------------------------------------------------+\n')
    
    def setPhoneNumber(self, phone_number: str, contact_type: str, new_number: str=None, replace=False) -> None:
        if not replace:
            self.__PhoneNumbers.append(phone_number)
            self.setContactType(contact_type)
        else:
            index_of_existing_number = self.__PhoneNumbers.index(phone_number)
            self.__PhoneNumbers[index_of_existing_number] = new_number
            self.__ContactTypes[index_of_existing_number] = contact_type

    def setPhoneNumberList(self, new_phone_no_list: list[str]) -> None:
        self.__PhoneNumbers = new_phone_no_list
            
    def setContactType(self, contactType: str) -> None:
        self.__ContactTypes.append(contactType)
    
    def setContactTypes(self, new_contact_types_list: list[str]) -> None:
        self.__ContactTypes = new_contact_types_list
        
    def setEmail(self, new_email: str) -> None:
        self.__Email = new_email
        
    def setname(self, new_name: str) -> None:
        self.__Name = new_name

if __name__ == '__main__':
    print("\n\tRun 'main.py'\n")
    
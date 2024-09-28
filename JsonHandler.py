from Contact import Contact as Contact
import json


class JsonHandler:

    @staticmethod
    def write(contact_list: list) -> None:
        with open("Contacts.json", "a") as JSONfile:
            # preparing json file to serialization
            JSONfile.seek(0)
            JSONfile.truncate()
            JSONfile.write('[')
            for contact in contact_list:
                json.dump(contact.__dict__, JSONfile, indent=2)
                if not contact == contact_list[-1]:
                    JSONfile.write(',')
            JSONfile.write(']')

    @staticmethod
    def read() -> list[object]:
        contact_list = []
        with open("Contacts.json", "r") as JSONfile:
            json_data = json.load(JSONfile)  
        for contact_info in json_data:
            contact_list.append(Contact(*list(contact_info.values())))
        
        return contact_list

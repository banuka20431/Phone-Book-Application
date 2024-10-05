from Contact import Contact
from ContactHandler import ContactHandler
from JsonHandler import JsonHandler
import os
import gui


def do_continue() -> bool:
    try:
        if list(input())[0] in ("N", "n"):
            return False
    except IndexError:
        return False
    return True


def contactexists(matched_contact: Contact):
    if matched_contact is None:
        print("\nContact couldn't be found!")
        return False
    print("\nContact found!\n")
    return True


def main(selected_action: str, contact_list) -> list[Contact]:
    print()
    match selected_action:
        case 'SAVE':
            new_contact = contact_handler.create_new_contact()
            contact_list.append(new_contact)
        case 'SEARCH':
            matched_contact = contact_handler.search_contact()
            if contactexists(matched_contact):
                matched_contact.display_contact()
        case 'DELETE':
            matched_contact = contact_handler.search_contact()
            if contactexists(matched_contact):
                matched_contact.display_contact()
                print("\nContinue deletion (Y/N) : ", end='')
                if do_continue():
                    try:
                        contact_list.remove(matched_contact)
                        print("\nContact deleted successfully!")
                    except Exception:
                        print("whtfk")
                else:
                    print("\nDeletion canceled!")
        case 'UPDATE':
            matched_contact = contact_handler.search_contact()
            if contactexists(matched_contact):
                matched_contact.display_contact()
                print("\nContinue update (Y/N) : ", end='')
                if do_continue():
                    try:
                        updated_contact = contact_handler.update_contact(matched_contact)
                        contact_list.remove(matched_contact)
                        contact_list.append(updated_contact)
                        print("\nContact updated successfully!")
                    except Exception as e:
                        print(e)
                else:
                    print('\nUpdate canceled!')
        case 'CLEAR':
            print("\nPASSKEY >_ ", end='')
            if input() == PASSKEY:
                contact_list.clear()
                with open(JSON_FILE_PATH, 'w+') as file:
                    file.flush()
                print("\nAll contacts cleared!")
            else:
                print("\nIncorrect passkey!")
        case 'Run GUI':
            contact_list = gui.runGUI(contact_list)
    return contact_list


if __name__ == "__main__":
    
    PASSKEY = "1234"
    JSON_FILE_PATH = r'Contacts.json'
    contact_types = ("HOME", "WORK", "PUBLIC", "SERVICE", "PERSONAL")
    main_menu = ("SAVE", "DELETE", "UPDATE", "SEARCH", "CLEAR", "Run GUI")
    contact_list: list[Contact] = []

    print(
        '''
        -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
        =================================================
        +---------------+  PHONE BOOK  +----------------+
        =================================================
        _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
        
        '''
    )

    print('Importing existing contacts..: ', end='')
    if not os.path.exists(JSON_FILE_PATH):
        print('FAILED -> file couldn\'t be found')
        print('Creating new file for saving contacts..: ', end='')
        open(JSON_FILE_PATH, 'w').close()
        print('OK')
    else:
        print('OK')

    contact_list = JsonHandler.read()
    
    contact_handler = ContactHandler(contact_list, contact_types, PASSKEY)

    # Main-block begins here

    iterate = True
    while iterate:
        try:
            print('\nSELECT AN ACTION > \n')
            action = main_menu[ContactHandler.displayMenus(main_menu)]
            contact_list = main(action, contact_list)
            print("\nQuit (Y/N): ", end="")
            iterate = not do_continue()
            print()
        except KeyboardInterrupt:
            print('\n\nExiting...\n')
            exit(0)
        finally:
            JsonHandler.write(contact_list)

    # Main-block ends here

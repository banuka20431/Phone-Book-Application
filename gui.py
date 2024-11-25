import os
import tkinter as tk
import tkinter.ttk as ttk
from JsonHandler import JsonHandler
from Contact import Contact
from ContactHandler import ContactHandler, ContactList
from DateTime import DateTime
from tkinter import *
from tkinter import messagebox
from typing import Literal


class App:

    def __init__(
        self,
        ROOT_WINDOW_WIDTH: int,
        ROOT_WINDOW_HEIGHT: int,
        LAYER_OFFSET: int,
        Contact_List: list[Contact],
        CONTACT_TYPES_NAMES: list[str],
    ) -> None:

        self.LAYER_OFFSET = LAYER_OFFSET
        self.ROOT_WINDOW_WIDTH = ROOT_WINDOW_WIDTH
        self.ROOT_WINDOW_HEIGHT = ROOT_WINDOW_HEIGHT
        self.Contact_List = Contact_List
        self.CONTACT_TYPES_NAMES = CONTACT_TYPES_NAMES

    def run_gui(self) -> Tk:

        ROOT_WINDOW = tk.Tk()
        ROOT_WINDOW.attributes("-topmost", True)
        ROOT_WINDOW.title("Phone Book")
        ROOT_POSITION_X = (
            ROOT_WINDOW.winfo_screenwidth() / 2 - self.ROOT_WINDOW_WIDTH / 2
        )
        ROOT_POSITION_Y = (
            ROOT_WINDOW.winfo_screenheight() / 2 - self.ROOT_WINDOW_HEIGHT / 2
        )
        ROOT_WINDOW.geometry(
            f"{self.ROOT_WINDOW_WIDTH}x{self.ROOT_WINDOW_HEIGHT}+{int(ROOT_POSITION_X)}+{int(ROOT_POSITION_Y - self.LAYER_OFFSET)}"
        )
        ROOT_WINDOW.resizable(False, False)

        return self.construct_root_window(ROOT_WINDOW)

    def get_geometry(
        self, root: BaseWidget | Tk, box_width: int, box_height: int
    ) -> str:
        """
        Calculate popup windows' x and y points on the screen for suitable positioning
        """

        base_x_position: int = root.winfo_x()
        base_y_positiion: int = root.winfo_y()
        base_width: int = root.winfo_width()
        base_height: int = root.winfo_height()

        if base_height == box_height and base_width == box_width:
            box_x_pos = base_x_position + self.LAYER_OFFSET
            box_y_pos = base_y_positiion + self.LAYER_OFFSET
        elif base_height > box_height:
            box_y_pos = base_y_positiion + (base_height - box_height) // 2
            if base_width == box_width:
                box_x_pos = base_x_position
            elif base_width > box_width:
                box_x_pos = base_x_position + (base_width - box_width) // 2
            else:
                box_x_pos = base_x_position - (box_width - base_width) // 2
        else:
            box_y_pos = base_y_positiion + self.LAYER_OFFSET
            box_x_pos = base_x_position + self.LAYER_OFFSET

        return f"{box_width}x{box_height}+{box_x_pos}+{box_y_pos}"

    def construct_root_window(self, root_window) -> Tk:

        def action_button_handler(action: str):
            if action != "Save" and len(main_contact_table.selection()) == 0:
                self.show_messagebox(
                    root_window, "Warning", "Warning", "0 Contacts Seleted", (300, 150)
                )
            else:
                match action:
                    case "Save":
                        self.save_contact(root_window)
                    case "Update":
                        self.update_contact(root_window)
                    case "Delete":
                        self.delete_contact(root_window)
                    case "Info":
                        self.view_contact_info(root_window)

        global main_contact_table, button_update, button_delete, button_info

        ACTION_BTN_WIDTH = 12
        ACTION_BTN_MGN = 8
        ACTION_BTN_PDN = 8

        action_button_frame = self.get_frame(root_window)
        main_contact_table_frame = self.get_frame(root_window)
        action_button_frame.pack(padx=10, pady=15)
        main_contact_table_frame.pack(expand=True, fill="both")

        button_save = self.get_button(
            action_button_frame,
            ACTION_BTN_WIDTH,
            "Save",
            lambda: action_button_handler("Save"),
            ACTION_BTN_PDN,
        )

        button_update = self.get_button(
            action_button_frame,
            ACTION_BTN_WIDTH,
            "Update",
            lambda: action_button_handler("Update"),
            ACTION_BTN_PDN,
        )

        button_delete = self.get_button(
            action_button_frame,
            ACTION_BTN_WIDTH,
            "Delete",
            lambda: action_button_handler("Delete"),
            ACTION_BTN_PDN,
        )

        button_info = self.get_button(
            action_button_frame,
            ACTION_BTN_WIDTH,
            "Info",
            lambda: action_button_handler("Info"),
            ACTION_BTN_PDN,
        )

        button_save.pack(side="left", padx=ACTION_BTN_MGN)
        button_update.pack(side="left", padx=ACTION_BTN_MGN)
        button_delete.pack(side="left", padx=ACTION_BTN_MGN)
        button_info.pack(side="left", padx=ACTION_BTN_MGN)

        main_contact_table_data = {
            "Contact Names": self.Contact_List.get_contact_names(),
            "Primary Phone Numbers": self.Contact_List.get_primary_numbers(),
        }

        main_contact_table = self.get_table(
            main_contact_table_frame, main_contact_table_data
        )

        main_contact_table.pack(fill="both", expand=True)

        return root_window

    def save_contact(self, root_window: Tk) -> None:

        def reset_input_variables() -> None:
            contact_name_var.set("")
            contact_email_var.set("")
            contact_phone_number_var.set("")
            contact_contact_type_var.set(self.CONTACT_TYPES_NAMES[0])

        def validate_inputs() -> tuple | bool:
            input_fields = ("Name", "Email", "Phone Number")
            inputs = (
                contact_name_var.get(),
                contact_email_var.get(),
                contact_phone_number_var.get(),
            )

            for input, field_name in zip(inputs, input_fields):
                if not ContactHandler.validate(field_name, input):
                    self.show_messagebox(
                        save_contact_window,
                        "Error",
                        "Invalid Input",
                        f"Invalid {field_name}",
                        dimensions=(280, 100),
                    )
                    return False
            else:
                if (
                    Contact_List.get_contact_index(
                        Contact_List.capitalize_contact_name(contact_name_var.get()),
                    )
                    >= 0
                ):
                    self.show_messagebox(
                        save_contact_window,
                        "Warning",
                        "Warning",
                        "Contact Exists",
                        dimensions=(300, 100),
                    )
                    return False
                else:

                    current_date_time = DateTime.getdatetime()

                    new_contact_info = [
                        Contact_List.capitalize_contact_name(contact_name_var.get()),
                        contact_email_var.get(),
                        [contact_phone_number_var.get()],
                        [contact_contact_type_var.get()],
                        current_date_time,
                        current_date_time,
                    ]

                    return new_contact_info

        def create_new_contact() -> None:
            if contact_info := validate_inputs():
                new_contact = Contact_Handler.create_new_contact(contact_info)
                Contact_List.insert_new_contact(new_contact)
                self.show_messagebox(
                    save_contact_window,
                    "Info",
                    "Success",
                    "Contact Saved",
                    dimensions=(300, 150),
                )

                reset_input_variables()

                new_table_row = (
                    Contact_List.capitalize_contact_name(
                        new_contact.get_contact_name()
                    ),
                    Contact_List.format_contact_phone_number(
                        new_contact.get_primary_phone_number()
                    ),
                )

                self.append_table_data(main_contact_table, new_table_row)

        ACTION_BTN_WIDTH = 12

        save_contact_window = self.get_toplevel_window(
            root_window, "Create New Contact", (320, 280)
        )

        save_contact_frame = self.get_frame(save_contact_window)
        save_contact_frame.pack(padx=30, pady=5, fill="both", expand=True)
        save_contact_frame.columnconfigure((0, 1, 2, 3), weight=1)
        save_contact_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        contact_name_var = tk.StringVar()
        contact_email_var = tk.StringVar()
        contact_phone_number_var = tk.StringVar()
        contact_contact_type_var = tk.StringVar(value=self.CONTACT_TYPES_NAMES[0])

        self.get_label(save_contact_frame, "Name : ").grid(column=0, row=0, sticky="we")
        self.get_entry(save_contact_frame, contact_name_var).grid(
            row=0, column=1, columnspan=3, sticky="we"
        )

        self.get_label(save_contact_frame, "Email : ").grid(
            column=0, row=1, sticky="we"
        )
        self.get_entry(save_contact_frame, contact_email_var).grid(
            row=1, column=1, columnspan=3, sticky="we"
        )

        self.get_label(save_contact_frame, "Phone No").grid(
            column=0, row=2, columnspan=2, sticky="we"
        )
        self.get_entry(save_contact_frame, contact_phone_number_var).grid(
            row=3, column=0, columnspan=2, sticky="we"
        )

        self.get_label(save_contact_frame, "Contact Type").grid(
            column=3, row=2, columnspan=2, sticky="we"
        )
        self.get_option_menu(
            save_contact_frame, contact_contact_type_var, self.CONTACT_TYPES_NAMES
        ).grid(row=3, column=2, columnspan=2, sticky="we")

        self.get_button(
            save_contact_frame,
            ACTION_BTN_WIDTH,
            "Enter",
            create_new_contact,
            padding=5,
        ).grid(row=4, column=0, columnspan=2)

        self.get_button(
            save_contact_frame,
            ACTION_BTN_WIDTH,
            "Clear",
            reset_input_variables,
            padding=5,
        ).grid(row=4, column=2, columnspan=2)

        save_contact_window.mainloop()

    def view_contact_info(self, root_window: Tk) -> None:

        def get_selected_phone_number() -> str | bool:
            try:
                selected_phone_number_id = info_contact_table.selection()[0]
                return "0" + str(
                    info_contact_table.item(selected_phone_number_id)["values"][0]
                )

            except IndexError:
                self.show_messagebox(
                    contact_info_window,
                    "Warning",
                    "Warning",
                    "0 Phone Numbers Seleted",
                    (330, 150),
                )

                return False

        def delete_selected_number() -> None:
            if selected_phone_number := get_selected_phone_number():
                if len(selected_contact.get_contact_Phone_numbers()) == 1:
                    self.show_messagebox(
                        contact_info_window,
                        "Warning",
                        "Warning",
                        "Must have atleast one phone number \nTip : Use update button to replace the number",
                        (500, 120),
                    )
                else:
                    selected_contact_phone_numbers = (
                        selected_contact.get_contact_Phone_numbers()
                    )
                    selected_contact_contact_types = (
                        selected_contact.get_contact_type_list()
                    )

                    selected_phone_number_index = selected_contact_phone_numbers.index(
                        selected_phone_number
                    )

                    selected_contact_phone_numbers.pop(selected_phone_number_index)
                    selected_contact_contact_types.pop(selected_phone_number_index)

                    selected_contact.setPhoneNumberList(selected_contact_phone_numbers)
                    selected_contact.setContactTypes(selected_contact_contact_types)

                    info_contact_table.delete(info_contact_table.selection()[0])

                    message = f"Deleted {selected_phone_number} from {Contact_List.capitalize_contact_name(selected_contact.get_contact_name())}'s Phone Numbers"

                    self.show_messagebox(
                        contact_info_window,
                        "Info",
                        "Deleted Successfully",
                        message,
                        (520, 120),
                    )

        def change_to_default_number() -> None:
            if selected_phone_number := get_selected_phone_number():
                if len(selected_contact.get_contact_Phone_numbers()) > 1:

                    selected_contact_phone_numbers = (
                        selected_contact.get_contact_Phone_numbers()
                    )
                    selected_contact_contact_types = (
                        selected_contact.get_contact_type_list()
                    )

                    selected_phone_number_index = selected_contact_phone_numbers.index(
                        selected_phone_number
                    )

                    selected_contact_phone_numbers.insert(
                        0,
                        selected_contact_phone_numbers.pop(selected_phone_number_index),
                    )

                    selected_contact_contact_types.insert(
                        0,
                        selected_contact_contact_types.pop(selected_phone_number_index),
                    )

                    selected_contact.setPhoneNumberList(selected_contact_phone_numbers)
                    selected_contact.setContactTypes(selected_contact_contact_types)

                    main_contact_table.delete(main_contact_table.selection()[0])
                    
                    self.append_table_data(
                        main_contact_table,
                        (
                            Contact_List.capitalize_contact_name(selected_contact.get_contact_name()),
                            Contact_List.format_contact_phone_number(selected_contact.get_primary_phone_number())                     
                        ),
                        row_index=0
                    )
                    
                    contact_info_window.destroy()
                    
                    message = f'Default Number of the Contact {Contact_List.capitalize_contact_name(selected_contact.get_contact_name())} changed to {selected_phone_number}'
                    
                    self.show_messagebox(
                        root_window, 'Info', 'Default Number Changed', message, (600, 120)
                    )

        selected_contact = Contact_List.get_selected_contact(main_contact_table)

        contact_info_window = self.get_toplevel_window(
            root_window,
            f"Contact Info ({selected_contact.get_contact_name()})",
            (470, 500),
        )

        info_frame = self.get_frame(contact_info_window)
        info_frame.rowconfigure((0, 1, 2, 3), uniform="u", weight=1)
        info_frame.columnconfigure((0, 1), uniform="u", weight=1)
        info_frame.pack(padx=20, pady=20)

        info_contact_table_frame = self.get_frame(contact_info_window)
        info_contact_table_frame.pack()

        self.get_label(info_frame, "Contact's Name : ").grid(
            row=0, column=0, pady=(5, 10)
        )
        self.get_label(info_frame, "Contact's Email : ").grid(
            row=1, column=0, pady=(5, 10)
        )
        self.get_label(info_frame, "Contact Created on : ").grid(
            row=2, column=0, pady=(5, 10)
        )
        self.get_label(info_frame, "Contact Modified on : ").grid(
            row=3, column=0, pady=(5, 10)
        )

        self.get_label(info_frame, selected_contact.get_contact_name()).grid(
            row=0, column=1, pady=(5, 10)
        )
        self.get_label(info_frame, selected_contact.get_contact_email()).grid(
            row=1, column=1, pady=(5, 10)
        )
        self.get_label(info_frame, selected_contact.get_created_date()).grid(
            row=2, column=1, pady=(5, 10)
        )
        self.get_label(info_frame, selected_contact.get_modified_date()).grid(
            row=3, column=1, pady=(5, 10)
        )

        info_contact_table_data = {
            "Phone Number": selected_contact.get_contact_Phone_numbers(),
            "Contact Type": selected_contact.get_contact_type_list(),
        }

        info_contact_table = self.get_table(
            info_contact_table_frame, info_contact_table_data
        )
        info_contact_table.pack()

        info_action_buttons_frame = self.get_frame(contact_info_window)
        info_action_buttons_frame.pack()

        self.get_button(
            info_action_buttons_frame,
            23,
            "Delete Selected Number",
            delete_selected_number,
            10,
        ).pack(side="left", pady=10, padx=(0, 10))

        self.get_button(
            info_action_buttons_frame,
            23,
            "Change to Default",
            change_to_default_number,
            10,
        ).pack(pady=10, padx=(10, 0))

    def delete_contact(self, root_window: Tk) -> None:
        root_window.attributes("-topmost", False)

        selected_contact = Contact_List.get_selected_contact(main_contact_table)

        message = f"Do you want to delete '{Contact_List.capitalize_contact_name(selected_contact.get_contact_name())}' from the contacts"

        if messagebox.askyesno("Delete Contact", message):
            main_contact_table.delete(main_contact_table.selection()[0])
            Contact_List.contact_list.remove(selected_contact)

    def update_contact(self, root_window: Tk) -> None:

        def change_contact_name() -> None:
            old_contact_name = selected_contact.get_contact_name()
            if not Contact_Handler.validate("Name", new_contact_name_var.get()):
                self.show_messagebox(
                    update_contact_window,
                    "Error",
                    "Invalid Input",
                    f"Invalid Name",
                    dimensions=(280, 100),
                )
            else:
                if (
                    Contact_List.get_contact_index(
                        Contact_List.capitalize_contact_name(new_contact_name_var.get())
                    )
                    > -1
                ):
                    self.show_messagebox(
                        update_contact_window,
                        "Warning",
                        "Warning",
                        "Contact Exists",
                        dimensions=(300, 100),
                    )
                else:
                    selected_contact.setname(
                        Contact_List.capitalize_contact_name(new_contact_name_var.get())
                    )
                    main_contact_table.delete(main_contact_table.selection()[0])
                    self.append_table_data(
                        main_contact_table,
                        (
                            selected_contact.get_contact_name(),
                            Contact_List.format_contact_phone_number(
                                selected_contact.get_primary_phone_number()
                            ),
                        ),
                        row_index=0,
                    )

                msg = f"Contact Name '{Contact_List.capitalize_contact_name(old_contact_name)}' \nChanged to '{Contact_List.capitalize_contact_name(new_contact_name_var.get())}'"
                self.show_messagebox(
                    update_contact_window,
                    "Info",
                    "Contact Name Changed",
                    msg,
                    (380, 120),
                )

        def change_contact_email() -> None:
            old_email = selected_contact.get_contact_email()
            if not Contact_Handler.validate("Email", new_contact_email_var.get()):
                self.show_messagebox(
                    update_contact_window,
                    "Error",
                    "Invalid Input",
                    f"Invalid Email",
                    dimensions=(280, 100),
                )
            else:
                selected_contact.setEmail(new_contact_email_var.get())
                msg = f"Contact Email '{old_email}' \nChanged to '{new_contact_email_var.get()}'"
                self.show_messagebox(
                    update_contact_window,
                    "Info",
                    "Contact Email Changed",
                    msg,
                    (380, 120),
                )

        def enable_replacing_phone_numbers() -> None:
            existing_phone_number_menu["state"] = "normal"
        
        def clear_update_phone_number_frame() -> None:
            new_contact_phone_number.set('')
            new_contact_contact_type.set(self.CONTACT_TYPES_NAMES[0])
            do_replace_existing_number.set(False)
            selected_existing_number.set(selected_contact.get_primary_phone_number())
            existing_phone_number_menu["state"] = "disable"

        def add_new_contact_phone_number() -> None:
            
            if not Contact_Handler.validate("Phone Number", new_contact_phone_number.get()):
                self.show_messagebox(
                    update_contact_window,
                    "Error",
                    "Invalid Input",
                    f"Invalid Phone Number",
                    dimensions=(280, 100),
                )
            else:
                if not do_replace_existing_number.get():
                    selected_contact.setPhoneNumber(new_contact_phone_number.get(), new_contact_contact_type.get())
                    msg = f'New Phone Number added to the Contact \'{Contact_List.capitalize_contact_name(selected_contact.get_contact_name())}\''
                    self.show_messagebox(
                        update_contact_window,
                        'Info',
                        'New Phone Number Added',
                        msg,
                        (500, 120)
                    )
                else:
                    replace_existing_phone_number()
        
        def replace_existing_phone_number() -> None:
            selected_contact.setPhoneNumber(selected_existing_number.get(), new_contact_contact_type.get(), new_contact_phone_number.get(), replace=True)
            msg = f'Contact Phone Number {selected_existing_number.get()} Changed to {new_contact_phone_number.get()}'
            self.show_messagebox(
                update_contact_window,
                'Info',
                'Phone Number Changed',
                msg,
                (500, 120)
            )
                
        new_contact_name_var = tk.StringVar()
        new_contact_email_var = tk.StringVar()
        new_contact_phone_number = tk.StringVar()
        new_contact_contact_type = tk.StringVar(value=self.CONTACT_TYPES_NAMES[0])
        do_replace_existing_number = tk.BooleanVar(value=False)
        selected_existing_number = tk.StringVar()

        selected_contact = Contact_List.get_selected_contact(main_contact_table)

        update_contact_window = self.get_toplevel_window(
            root_window,
            f"Update Contact ({Contact_List.capitalize_contact_name(selected_contact.get_contact_name())})",
            (400, 220),
        )

        update_contact_tab_wrapper = self.get_tab_wrapper(update_contact_window, 10)

        frame_update_contact_name = self.get_frame(update_contact_window)
        frame_update_contact_email = self.get_frame(update_contact_window)
        frame_update_contact_phone_number = self.get_frame(update_contact_window)

        update_contact_tab_wrapper.add(frame_update_contact_name, text="Contact Name")
        update_contact_tab_wrapper.add(frame_update_contact_email, text="Contact Email")
        update_contact_tab_wrapper.add(
            frame_update_contact_phone_number, text="Contact Phone Number"
        )

        update_contact_tab_wrapper.pack(side="left", fill="both", expand=True)

        frame_update_contact_name.rowconfigure((0, 1, 2, 3, 4), uniform="u", weight=1)
        frame_update_contact_name.columnconfigure((0, 1), uniform="u", weight=1)

        self.get_label(frame_update_contact_name, "Current Contact Name").grid(
            row=0, column=0, columnspan=2
        )

        self.get_label(
            frame_update_contact_name,
            Contact_List.capitalize_contact_name(selected_contact.get_contact_name()),
            font="Monospace 10",
            fg="white",
            bg="black",
        ).grid(row=1, column=0, columnspan=2, ipadx=20, ipady=3)

        self.get_label(frame_update_contact_name, "New Contact Name").grid(
            row=2, column=0, columnspan=2
        )

        self.get_entry(frame_update_contact_name, new_contact_name_var).grid(
            row=3, column=0, columnspan=2, ipadx=30, sticky="ns", pady=5
        )

        self.get_button(
            frame_update_contact_name, 20, "Enter", change_contact_name, 5
        ).grid(row=4, column=0)

        self.get_button(
            frame_update_contact_name,
            20,
            "Cancel",
            lambda: new_contact_name_var.set(""),
            5,
        ).grid(row=4, column=1)

        frame_update_contact_email.rowconfigure((0, 1, 2, 3, 4), uniform="u", weight=1)
        frame_update_contact_email.columnconfigure((0, 1), uniform="u", weight=1)

        self.get_label(frame_update_contact_email, "Current Contact Email").grid(
            row=0, column=0, columnspan=2
        )

        self.get_label(
            frame_update_contact_email,
            selected_contact.get_contact_email(),
            font="Monospace 10",
            fg="white",
            bg="black",
        ).grid(row=1, column=0, columnspan=2, ipadx=20, ipady=3)

        self.get_label(frame_update_contact_email, "New Contact Email").grid(
            row=2, column=0, columnspan=2
        )

        self.get_entry(frame_update_contact_email, new_contact_email_var).grid(
            row=3, column=0, columnspan=2, ipadx=30, sticky="ns", pady=5
        )

        self.get_button(
            frame_update_contact_email, 20, "Enter", change_contact_email, 5
        ).grid(row=4, column=0)

        self.get_button(
            frame_update_contact_email,
            20,
            "Cancel",
            lambda: new_contact_email_var.set(""),
            5,
        ).grid(row=4, column=1)

        frame_update_contact_phone_number.rowconfigure(
            (0, 1, 2, 3), uniform="u", weight=1
        )
        frame_update_contact_phone_number.columnconfigure(
            (0, 1, 2, 3, 4), uniform="u", weight=1
        )

        self.get_label(
            frame_update_contact_phone_number,
            "Enter New Phone Number",
            bg="black",
            fg="white",
        ).grid(row=0, column=0, columnspan=5, ipadx=20, ipady=5, pady=5)

        self.get_entry(
            frame_update_contact_phone_number, new_contact_phone_number
        ).grid(row=1, column=0, columnspan=3, sticky="we", padx=25)

        self.get_option_menu(
            frame_update_contact_phone_number,
            new_contact_contact_type,
            self.CONTACT_TYPES_NAMES,
        ).grid(row=1, column=3, columnspan=2, sticky="we", padx=(0, 10))

        self.get_radio_button(
            frame_update_contact_phone_number,
            "Replace",
            do_replace_existing_number,
            enable_replacing_phone_numbers,
        ).grid(row=2, column=0, columnspan=2)

        self.get_label(
            frame_update_contact_phone_number, "Replace \nWith : "
        ).grid(row=2, column=2, sticky="we")

        existing_phone_number_menu = self.get_option_menu(
            frame_update_contact_phone_number,
            selected_existing_number,
            selected_contact.get_contact_Phone_numbers(),
        )
        
        existing_phone_number_menu.grid(row=2, column=3, columnspan=2, sticky="we", padx=(0, 10))

        existing_phone_number_menu['state'] = 'disable'

        self.get_button(
            frame_update_contact_phone_number, 25, "Enter", add_new_contact_phone_number, 5
        ).grid(row=3, column=0, columnspan=3)
        
        self.get_button(
            frame_update_contact_phone_number, 25, "Clear", clear_update_phone_number_frame, 5
        ).grid(row=3, column=3, columnspan=2)

    def show_messagebox(
        self,
        root: BaseWidget | Tk,
        msg_type: Literal["Warning", "Error", "Info", "Question"],
        msq_title: str,
        msg_body: str,
        dimensions: tuple[int, int],
    ):

        WARNING_ICO = "::tk::icons::warning"
        ERROR_ICO = "::tk::icons::error"
        INFO_ICO = "::tk::icons::information"
        QUESTION_ICO = "::tk::icons::question"

        match msg_type:
            case "Warning":
                icon = WARNING_ICO
            case "Error":
                icon = ERROR_ICO
            case "Info":
                icon = INFO_ICO
            case "Question":
                icon = QUESTION_ICO

        msgbox = self.get_toplevel_window(root, msq_title, dimensions)

        msgbox.rowconfigure((0, 1), uniform="u", weight=1)
        msgbox.columnconfigure((0, 1, 2, 3), uniform="u", weight=1)

        icon_label = Label(msgbox, image=icon)
        icon_label.grid(row=0, column=0, rowspan=2, sticky="e")

        msg_label = Label(
            msgbox, text=msg_body, font="Monospace 10 bold", anchor="center"
        )
        msg_label.grid(row=0, column=1, columnspan=2)

        self.get_button(msgbox, 15, "OK", msgbox.destroy, padding=3).grid(
            row=1, column=1, columnspan=2
        )

    def append_table_data(
        self, table: ttk.Treeview, data_row: tuple[str], row_index=tk.END
    ) -> None:
        table.insert(parent="", index=row_index, values=data_row)

    def get_toplevel_window(
        self, root_window, title: str, dimentions: tuple[int, int]
    ) -> Toplevel:

        root_window.attributes("-topmost", False)
        toplevel_window = tk.Toplevel()
        toplevel_window.title(title)
        width, height = dimentions
        toplevel_window.geometry(self.get_geometry(root_window, width, height))
        toplevel_window.resizable(False, False)

        return toplevel_window

    def get_tab_wrapper(self, root_window, padding) -> ttk.Notebook:
        return ttk.Notebook(root_window, padding=padding)

    def get_option_menu(
        self, master_window: Tk | Toplevel, var, options
    ) -> ttk.OptionMenu:
        return ttk.OptionMenu(master_window, var, *options)

    def get_radio_button(
        self, root_window: Tk | Toplevel, text: str, var, func
    ) -> ttk.Radiobutton:
        return ttk.Radiobutton(
            master=root_window, text=text, variable=var, command=func
        )

    def get_label(
        self,
        master_window: Tk | Toplevel,
        text: str,
        font="monospace 10 bold",
        fg: str = "black",
        bg: str = None,
        justify: Literal["center", "w", "e"] = "center",
    ) -> ttk.Label:
        return ttk.Label(
            master=master_window,
            text=text,
            font=font,
            anchor=justify,
            foreground=fg,
            background=bg,
        )

    def get_entry(self, master_window: Tk | Toplevel, var) -> ttk.Entry:
        return ttk.Entry(master=master_window, textvariable=var)

    def get_button(
        self,
        master_window: Tk | Toplevel,
        width: int,
        text: str,
        func,
        padding: int = 0,
    ) -> ttk.Button:
        return ttk.Button(
            master=master_window, width=width, padding=padding, text=text, command=func
        )

    def get_frame(self, master_window: Tk | Toplevel) -> ttk.Frame:
        return ttk.Frame(master=master_window)

    def get_table(
        self, master_window: Tk | Toplevel, column_data: dict[str:list]
    ) -> ttk.Treeview:

        headings = list(column_data.keys())

        table = ttk.Treeview(master_window, columns=headings, show="headings")

        table_data = []
        for heading in headings:
            """
            Creating columns
            """
            table.heading(heading, text=heading)
            table_data.append(column_data[heading])

        """
        Inserting table data
        """
        for row in zip(*table_data):
            table.insert(parent="", index=tk.END, values=row)

        """
        Centering column texts
        """
        for col in table["columns"]:
            table.column(col, anchor="center")
            table.heading(col, text=col)

        return table


def main() -> None:

    global Contact_List
    global Contact_Handler

    ROOT_WINDOW_WIDTH = 450
    ROOT_WINDOW_HEIGHT = 420
    LAYER_OFFSET = 50
    CONTACT_TYPE_NAMES = ("HOME", "WORK", "PUBLIC", "SERVICE", "PERSONAL")

    Contact_List = ContactList(JsonHandler.read())
    Contact_Handler = ContactHandler(
        Contact_List.contact_list, CONTACT_TYPE_NAMES, "1233"
    )

    app = App(
        ROOT_WINDOW_WIDTH,
        ROOT_WINDOW_HEIGHT,
        LAYER_OFFSET,
        Contact_List,
        CONTACT_TYPE_NAMES,
    )

    root_window = app.run_gui()

    root_window.mainloop()

    JsonHandler.write(Contact_List.contact_list)


if __name__ == "__main__":
    print("\n\nImporting Existing Contacts..: ", end="")
    if not os.path.exists("Contacts.json"):
        print("FAILED -> Contacts File couldn't be Found")
        print("Creating New Contacts File..: ", end="")
        open("Contacts.json", "w").close()
        print("OK")
    else:
        print("OK")

    main()

    print("\n\n")

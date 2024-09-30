import os
import tkinter as tk
import tkinter.ttk as ttk
from JsonHandler import JsonHandler
from Contact import Contact
from ContactHandler import ContactHandler
from tkinter import *
from tkinter import messagebox


def getcontactlist() -> list[Contact]:
    if os.path.getsize(JSON_FILE_PATH):
        return JsonHandler.read()
    return []


def getnamelist() -> list:
    names = []
    for contact in getcontactlist():
        names.append(contact.get_contact_name())
    return names


def getprimaryphnumberlist() -> list:
    phnumbers = []
    for contact in getcontactlist():
        phnumbers.append(contact.get_contact_Phone_numbers()[0])
    return phnumbers


def getgeometry(root: BaseWidget | Tk, box_width: int, box_height: int) -> str:
    base_x: int = root.winfo_x()
    base_y: int = root.winfo_y()
    base_width: int = root.winfo_width()
    base_height: int = root.winfo_height()
    if base_height == box_height and base_width == box_width:
        box_x_pos = base_x + MENU_OFFSET
        box_y_pos = base_y + MENU_OFFSET
    elif base_height > box_height:
        box_y_pos = base_y + (base_height - box_height) // 2
        if base_width == box_width:
            box_x_pos = base_x
        elif base_width > box_width:
            box_x_pos = base_x + (base_width - box_width) // 2
        else:
            box_x_pos = base_x - (box_width - base_width) // 2
    else:
        box_y_pos = base_y + MENU_OFFSET
        box_x_pos = base_x + MENU_OFFSET

    return f"{box_width}x{box_height}+{box_x_pos}+{box_y_pos}"


def show_messagebox(root: BaseWidget | Tk, image_path: str, title: str, msg: str, dimensions: tuple):
    msgbox_width, msgbox_height = dimensions

    msgbox = Toplevel(root)
    msgbox.title(title)

    box_position_cords = getgeometry(root, msgbox_width, msgbox_height)

    msgbox.geometry(box_position_cords)
    msgbox.resizable(False, False)

    icon_label = Label(msgbox, image=image_path)
    icon_label.grid(row=0, column=0, pady=(40, 10), padx=(20, 10))

    msg_label = Label(msgbox, text=msg, font="Monospace 10 bold", anchor='center')
    msg_label.grid(row=0, column=1, columnspan=2)

    b1 = Button(msgbox, text="OK", command=msgbox.destroy, width=15)
    b1.grid(row=1, column=1, sticky='', padx=(55, 0))


def capitalized_name(name: str) -> str:
    return " ".join([n.capitalize() for n in name.split(" ")])


def formatted_ph_number(phno: str) -> str:
    return "-".join([phno[:3], phno[3:]])


def select_item(selected_rows: tuple):
    ct_handler = ContactHandler(getcontactlist(), CONTACT_TYPES, PASSKEY)
    try:
        selected_contact_name, _ = contact_table.item(selected_rows[0])["values"]
    except IndexError:
        # messagebox.showwarning("Phone Book", "0 CONTACTS SELECTED", )
        show_messagebox(root_window, WARNING_ICO, "Warning", "0 Contacts Selected", dimensions=(250, 120))
    else:
        return ct_handler.search_byname(selected_contact_name.lower())


def prompt_save_contact(*_) -> None:
    """
    inner func
    validate entered new contact info
    and shows a message which depending on the invalid data field
    """

    def is_contact_info_valid() -> tuple | bool:
        output_label["background"] = "black"
        if not ContactHandler.validate("name", name_var.get()):
            output_label["foreground"] = "red"
            output_var.set("invalid contact name")
            return False
        if not ContactHandler.validate("email", email_var.get()):
            output_label["foreground"] = "red"
            output_var.set("invalid email")
            return False
        if not ContactHandler.validate("phone_number", phone_number_var.get()):
            output_label["foreground"] = "red"
            output_var.set("invalid phone number")
            return False
        output_label["foreground"] = "lightgreen"
        output_var.set("Contact Saved")
        return (
            name_var.get(),
            email_var.get(),
            [phone_number_var.get(), ],
            [contact_type_var.get(), ],
        )

    """
    inner func
    Saving new contact info locally
    """

    def process_new_contact_info():
        ct_handler = ContactHandler(getcontactlist(), CONTACT_TYPES, PASSKEY)
        output_label["background"] = "black"
        if info := is_contact_info_valid():
            # creates new contact object and saves in the json file
            new_contact = ct_handler.create_new_contact(info)
            update_ct_list = getcontactlist()
            update_ct_list.append(new_contact)
            JsonHandler.write(update_ct_list)
            # formats the info which wil be displayed on the main window
            name = capitalized_name(new_contact.get_contact_name())
            phone_no = formatted_ph_number(new_contact.get_contact_Phone_numbers()[0])
            # displays the contact basic info on the main window
            contact_table.insert(parent="", index=tk.END, values=(name, phone_no))
            # reset the input fields
            name_var.set("")
            email_var.set("")
            phone_number_var.set("")

    """
    inner func
    cleat out any changes of 'save contact' window
    """

    def clear_entered_info():
        name_var.set("")
        email_var.set("")
        phone_number_var.set("")
        output_var.set("")
        output_label["background"] = "white"

    """
    Creating 'save window'
    """
    save_win = tk.Toplevel()
    save_win.title("Create New Contact")
    width = 300
    height = 300
    save_win.geometry(getgeometry(root_window, width, height))
    save_win.resizable(False, False)

    """
    creating a wrapper frame for 'save window'
    """
    save_win_frame = ttk.Frame(master=save_win)
    save_win_frame.pack(padx=30, pady=5, fill="both", expand=True)
    save_win_frame.columnconfigure((0, 1, 2, 3), weight=1)
    save_win_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    """
    initializing entry and label variables
    """
    name_var = tk.StringVar()
    email_var = tk.StringVar()
    phone_number_var = tk.StringVar()
    contact_type_var = tk.StringVar(value=CONTACT_TYPES[0])
    output_var = tk.StringVar()

    name_label = ttk.Label(master=save_win_frame, text="Name :", font=MONOSPACE_BOLD)
    name_label.grid(column=0, row=0, sticky="we")

    name_entry = ttk.Entry(master=save_win_frame, textvariable=name_var)
    name_entry.grid(row=0, column=1, columnspan=3, sticky="we")

    email_label = ttk.Label(master=save_win_frame, text="Email :", font=MONOSPACE_BOLD)
    email_label.grid(row=1, column=0, sticky="we")

    email_entry = ttk.Entry(master=save_win_frame, textvariable=email_var)
    email_entry.grid(row=1, column=1, columnspan=3, sticky="we")

    phnumber_label = ttk.Label(
        master=save_win_frame, text="Phone No", font=MONOSPACE_BOLD, anchor="center"
    )
    phnumber_label.grid(row=2, column=0, columnspan=2, sticky="we")

    phnnumber_entry = ttk.Entry(master=save_win_frame, textvariable=phone_number_var)
    phnnumber_entry.grid(row=3, column=0, columnspan=2, sticky="we")

    contact_type_label = ttk.Label(
        master=save_win_frame, text="Contact Type", font=MONOSPACE_BOLD, anchor="center"
    )
    contact_type_label.grid(row=2, column=3, columnspan=2)

    contact_type_menu = ttk.OptionMenu(save_win_frame, contact_type_var, *CONTACT_TYPES)
    contact_type_menu.grid(row=3, column=2, columnspan=2, sticky="we")

    enter_btn = ttk.Button(
        master=save_win_frame,
        text="Enter",
        width=ACTION_BTN_WIDTH,
        command=process_new_contact_info,
    )
    enter_btn.grid(row=4, column=0, columnspan=2)

    cancel_btn = ttk.Button(
        master=save_win_frame,
        text="Clear",
        width=ACTION_BTN_WIDTH,
        command=clear_entered_info,
    )
    cancel_btn.grid(row=4, column=2, columnspan=2)

    output_label = ttk.Label(
        master=save_win_frame,
        textvariable=output_var,
        anchor="center",
        font=MONOSPACE_BOLD,
        background="white",
    )
    output_label.grid(row=5, column=0, columnspan=4, rowspan=2, sticky="news", pady=15)

    save_win.mainloop()


def prompt_contact_info(*_):
    matched_contact = select_item(contact_table.selection())

    if matched_contact is not None:
        display_contact_info_window = tk.Toplevel()
        width = 500
        height = 180
        display_contact_info_window.title("Contact Info")
        display_contact_info_window.geometry(getgeometry(root_window, width, height))
        display_contact_info_window.resizable(False, False)

        contact_info_frame = ttk.Frame(master=display_contact_info_window)
        contact_info_frame.pack(padx=30, pady=5, fill="both", expand=True)

        text_name = ttk.Label(
            master=contact_info_frame,
            text="Name :",
            font=MONOSPACE_BOLD,
            foreground="red",
        )
        text_name.pack(side="left", padx=10, pady=10)

        name_entry = ttk.Label(
            master=contact_info_frame, text=matched_contact.get_contact_name().upper()
        )
        name_entry.pack(side="left", padx=3, pady=10)

        email_label = ttk.Label(
            master=contact_info_frame,
            text="Email :",
            font=MONOSPACE_BOLD,
            foreground="red",
        )
        email_label.pack(side="left", padx=10, pady=10)

        text_email = ttk.Label(
            master=contact_info_frame, text=matched_contact.get_contact_email()
        )
        text_email.pack(side="left", padx=3, pady=10)

        info_table = ttk.Treeview(
            master=display_contact_info_window,
            columns=("Phone Number", "Contact Type"),
            show="headings",
        )

        info_table.heading("Phone Number", text="Phone Number")
        info_table.heading("Contact Type", text="Contact Type")

        for phone_no in matched_contact.get_contact_Phone_numbers():
            contact_type = matched_contact.get_contact_contact_type(phone_no)
            info_table.insert(parent="", index=tk.END, values=(phone_no, contact_type))

        for column in info_table["columns"]:
            info_table.column(column, anchor="center")
            info_table.heading(column, text=column)

        info_table.pack(fill="both", expand=True)

        display_contact_info_window.mainloop()


def prompt_delete_contact(*_):
    matched_contact = select_item(contact_table.selection())
    if matched_contact is not None:
        if messagebox.askyesno(
                "Phone Book",
                f"Do you want to delete '{capitalized_name(matched_contact.get_contact_name())}' from the contacts",
        ):
            contact_table.delete(contact_table.selection()[0])
            contact_list = getcontactlist()
            for ct in contact_list:
                if ct.get_contact_name() == matched_contact.get_contact_name():
                    contact_list.remove(ct)
                    break
            JsonHandler.write(contact_list)


def prompt_update_contact(*_):
    def save_new_name():
        contact_table.delete(contact_table.selection()[0])
        ct_lst = getcontactlist()
        ct_handler = ContactHandler()
        new_name = capitalized_name(new_name_var.get())
        if ct_handler.validate('name', new_name):
            for contact in ct_lst:
                if matched_contact.get_contact_name() == contact.get_contact_name():
                    old_name = capitalized_name(matched_contact.get_contact_name())
                    contact_index = ct_lst.index(contact)
                    ct_lst.remove(contact)
                    matched_contact.setname(new_name)
                    ct_lst.insert(contact_index, matched_contact)
                    JsonHandler.write(ct_lst)
                    contact_table.insert(parent='', index=0,
                                         values=(new_name, formatted_ph_number(contact.get_contact_Phone_numbers()[0])))
                    msg = f"Contact email '{old_name}' Changed to '{new_name}'"
                    show_messagebox(root_window, INFO_ICO, "Warning", msg, dimensions=(520, 120))
                    break
        else:
            msg = "Invalid Contact Name \nPlease Enter a Valid Name"
            show_messagebox(root_window, ERROR_ICO, "Error", msg, dimensions=(280, 120))
            new_name_var.set('')

        update_contact_window.destroy()

    def save_new_email():
        ct_handler = ContactHandler(None, None, None)
        ct_lst = getcontactlist()
        new_email = new_email_var.get()
        if ct_handler.validate('email', new_email):
            for contact in ct_lst:
                old_email = contact.get_contact_email()
                if matched_contact.get_contact_email() == contact.get_contact_email():
                    contact_index = ct_lst.index(contact)
                    ct_lst.remove(contact)
                    matched_contact.setEmail(new_email)
                    ct_lst.insert(contact_index, matched_contact)
                    JsonHandler.write(ct_lst)
                    msg = f"Contact name '{old_email}' \nChanged to '{new_email}'"
                    show_messagebox(root_window, INFO_ICO, "Warning", msg, dimensions=(520, 120))
                    break
        else:
            msg = "Invalid Email \nPlease Enter a Valid Email"
            show_messagebox(root_window, ERROR_ICO, "Error", msg, dimensions=(280, 120))

        update_contact_window.destroy()

    matched_contact = select_item(contact_table.selection())
    if matched_contact is not None:
        update_contact_window = tk.Toplevel()
        width = 350
        height = 200
        update_contact_window.title("Update Contact")
        update_contact_window.geometry(getgeometry(root_window, width, height))

        update_contact_window.resizable(False, False)

        tab_wrapper = ttk.Notebook(master=update_contact_window, padding=10)

        frame_update_name = ttk.Frame(master=update_contact_window)
        frame_update_email = ttk.Frame(master=update_contact_window)
        frame_update_phone_no = ttk.Frame(master=update_contact_window)

        tab_wrapper.add(frame_update_name, text="Contact Name")
        tab_wrapper.add(frame_update_email, text="Contact Email")
        tab_wrapper.add(frame_update_phone_no, text="Contact Phone Number")

        tab_wrapper.pack(side="left", fill="both", expand=True)

        """
        Update Contact Name
        """
        frame_update_name.columnconfigure((0, 1, 2, 3), weight=1)
        frame_update_name.rowconfigure((0, 1, 2, 3, 4), weight=1)

        text_existing_name = ttk.Label(
            master=frame_update_name,
            text="Current Contact Name",
            anchor="center",
        )

        text_existing_name.grid(row=0, column=1, columnspan=2, sticky="we")

        existing_name_label = ttk.Label(
            master=frame_update_name,
            text=capitalized_name(matched_contact.get_contact_name()),
            anchor="center",
            font=MONOSPACE_BOLD,
            background="black",
            foreground="white",
        )

        existing_name_label.grid(row=1, column=1, columnspan=2)

        new_name_label = ttk.Label(
            master=frame_update_name,
            text="New Contact Name",
            anchor="center",
            font=MONOSPACE_BOLD,
        )

        new_name_label.grid(row=2, column=1, columnspan=2, sticky="we")

        new_name_var = tk.StringVar()

        new_name_entry = ttk.Entry(
            master=frame_update_name, textvariable=new_name_var, width=25
        )

        new_name_entry.grid(row=3, column=1, columnspan=2, sticky='we', padx=5)

        new_name_enter_btn = ttk.Button(
            master=frame_update_name, text="Enter", padding=5, command=save_new_name
        )

        new_name_enter_btn.grid(row=4, column=0, columnspan=2, sticky='we', padx=5)

        new_name_clear_btn = ttk.Button(
            master=frame_update_name, text="Clear", padding=5, command=lambda: new_name_var.set('')
        )

        new_name_clear_btn.grid(row=4, column=2, columnspan=2, sticky="we", padx=5)

        """
        Update Contact Email
        """
        frame_update_email.columnconfigure((0, 1, 2, 3), weight=1)
        frame_update_email.rowconfigure((0, 1, 2, 3, 4), weight=1)

        text_existing_email = ttk.Label(
            master=frame_update_email,
            text="Current Contact Email",
            anchor="center",
            font=MONOSPACE_BOLD,
        )

        text_existing_email.grid(row=0, column=1, columnspan=2, sticky="we")

        existing_email_label = ttk.Label(
            master=frame_update_email,
            text=matched_contact.get_contact_email(),
            anchor="center",
            font=MONOSPACE_BOLD,
            background="black",
            foreground="white",
        )

        existing_email_label.grid(row=1, column=1, columnspan=2)

        new_email_label = ttk.Label(
            master=frame_update_email,
            text="New Contact Email",
            anchor="center",
            font=MONOSPACE_BOLD,
        )

        new_email_label.grid(row=2, column=1, columnspan=2, sticky="we")

        new_email_var = tk.StringVar()

        new_email_entry = ttk.Entry(
            master=frame_update_email, textvariable=new_email_var, width=25
        )

        new_email_entry.grid(row=3, column=1, columnspan=2, sticky='we', padx=5)

        new_email_enter_btn = ttk.Button(
            master=frame_update_email, text="Enter", padding=5, command=save_new_email
        )

        new_email_enter_btn.grid(row=4, column=0, columnspan=2, sticky='we', padx=5)

        new_email_clear_btn = ttk.Button(
            master=frame_update_email, text="Clear", padding=5, command=lambda: new_email_var.set('')
        )

        new_email_clear_btn.grid(row=4, column=2, columnspan=2, sticky="we", padx=5)


def main() -> None:
    """
    # creating main components for the application
    # add widgets to the root window
    # add event listeners to the widgets
    """

    global contact_table

    """
    setup frames in root window for action buttons and contact table
    """
    action_frame = ttk.Frame(master=root_window)
    contact_frame = ttk.Frame(master=root_window)
    action_frame.pack(padx=10, pady=15)
    contact_frame.pack(fill="both", expand=True)

    """
    action buttons [ Save, Update, Delete, Show ]
    """
    save_btn = ttk.Button(
        master=action_frame,
        text="Save",
        width=ACTION_BTN_WIDTH,
        command=prompt_save_contact,
        padding=ACTION_BTN_PDN,
    )

    update_btn = ttk.Button(
        master=action_frame,
        text="Update",
        width=ACTION_BTN_WIDTH,
        command=prompt_update_contact,
        padding=ACTION_BTN_PDN,
    )

    delete_btn = ttk.Button(
        master=action_frame,
        text="Delete",
        width=ACTION_BTN_WIDTH,
        command=prompt_delete_contact,
        padding=ACTION_BTN_PDN,
    )

    show_btn = ttk.Button(
        master=action_frame,
        text="Show",
        width=ACTION_BTN_WIDTH,
        command=prompt_contact_info,
        padding=ACTION_BTN_PDN,
    )

    save_btn.pack(side="left", padx=ACTION_BTN_MGN)
    update_btn.pack(side="left", padx=ACTION_BTN_MGN)
    delete_btn.pack(side="left", padx=ACTION_BTN_MGN)
    show_btn.pack(side="left", padx=ACTION_BTN_MGN)

    """
    setup contact table
    """
    contact_table = ttk.Treeview(
        master=contact_frame,
        columns=("Contact Name", "Primary Phone Number"),
        show="headings",
    )

    contact_table.pack(fill="both", expand=True)

    """
    set headings
    """
    contact_table.heading("Contact Name", text="Contact Name")
    contact_table.heading("Primary Phone Number", text="Primary Phone Number")

    """
    inserting data
    """
    for name, phone_no in zip(CONTACT_NAMES, PHONE_NUMBERS):
        name = capitalized_name(name)
        phone_no = formatted_ph_number(phone_no)

        contact_table.insert(parent="", index=tk.END, values=(name, phone_no))

    """
    centering column texts
    """
    for col in contact_table["columns"]:
        contact_table.column(col, anchor="center")
        contact_table.heading(col, text=col)

    contact_table.bind("<Delete>", prompt_delete_contact)
    contact_table.bind("<Control-n>", prompt_save_contact)
    contact_table.bind("<Control-d>", prompt_contact_info)


def runGUI() -> None:
    global root_window

    root_window = tk.Tk()
    root_window.title("Phone Book")
    ROOT_POSITION_X = root_window.winfo_screenwidth() / 2 - ROOT_WINDOW_WIDTH / 2
    ROOT_POSITION_Y = root_window.winfo_screenheight() / 2 - ROOT_WINDOW_HEIGHT / 2
    root_window.geometry(
        f"{ROOT_WINDOW_WIDTH}x{ROOT_WINDOW_HEIGHT}+{int(ROOT_POSITION_X)}+{int(ROOT_POSITION_Y)}"
    )
    root_window.resizable(False, False)
    main()
    root_window.mainloop()


"""
    # initialing constants
"""
JSON_FILE_PATH = r"Contacts.json"
PASSKEY = "1234"
CONTACT_TYPES = ("HOME", "WORK", "PUBLIC", "SERVICE", "PERSONAL")
CONTACT_NAMES = getnamelist()
PHONE_NUMBERS = getprimaryphnumberlist()
ROOT_WINDOW_WIDTH = 400
ROOT_WINDOW_HEIGHT = 400
MONOSPACE_ITALIC = "monospace 9 italic"
MONOSPACE_BOLD = "monospace 10 bold"
ACTION_BTN_WIDTH = 10
ACTION_BTN_MGN = 8
ACTION_BTN_PDN = 8
WARNING_ICO = "::tk::icons::warning"
ERROR_ICO = "::tk::icons::error"
INFO_ICO = "::tk::icons::information"
QUESTION_ICO = "::tk::icons::question"
MENU_OFFSET = 50
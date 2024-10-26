
# Phone Book App

This project implements a contacts manager application with Python. 

It allows users to,
- Save new contacts
- Add new phone numbers to the existing contacts
- View contacts' information 
- Update contacts' information (Replace existing numbers, Rename contact's name, Change contact's email)
- Delete contacts' information

In addition to those main functionalities, there are a couple of more additional ones,
- users can change the primary contact number if there is more than one phone number (default: phone number entered while saving that specific contact)
 
A graphical user interface (GUI) is also implemented with `python's Tkinter library` to make the application more interactive.


## Requirements

- Python 3.x
- `tkinter` library (usually comes with Python by default)
- The following custom modules must be present:
  - `JsonHandler`
  - `Contact`
  - `ContactHandler`

## How to Run

1. **Install Python**: Ensure Python is installed by running:

    ```bash
    python --version
    ```

2. **Install Required Libraries**: 
    `tkinter` comes by default with most Python installations. However, if it's missing, install it using:

    **For Linux:**
    ```bash
    sudo apt-get install python3-tk
    ```

    **For Windows:**
   ```bash
   pip install tk
   ```

4. **Check External Dependencies**: 
   Ensure the following modules are present in the same directory as `gui.py`:
   - `JsonHandler`
   - `Contact`
   - `ContactHandler`

5. **Run the Script**:
   In the terminal, navigate to the directory containing `gui.py` and run:
    ```bash
    python main.py
    ```


## Application UI Overview

 - Home
 <img alt="Home Window" src="https://github.com/user-attachments/assets/7f7071aa-758c-41fa-b0f3-84bf55c9bdc5">

- Save Contact Window
<img alt="Save Contact Window" src="https://github.com/user-attachments/assets/0cb11fc8-abf4-4ad4-817f-94eb786c06c9">
 
- Contact Info Window
<img alt="Contact Info Window" src="https://github.com/user-attachments/assets/f93e3c40-f2a5-4815-947f-4ed854ad507a">

- Update Contact Window
<img alt="Update Contact Name" src="https://github.com/user-attachments/assets/23b1b107-8529-4e0e-806e-31d615e40187">
<br/>
<img alt="Update Contact Email" src="https://github.com/user-attachments/assets/7ab5fc8e-535f-42d8-b330-46f8b97667e4">
<br/>
<img alt="Update Contact Phone Number" src="https://github.com/user-attachments/assets/b500f5c0-8a56-4e6d-a6b7-581e1458dd24">
<br/>
<img alt="Relace Phone Number" src="https://github.com/user-attachments/assets/4f7a2902-8d37-453a-b561-cb9b649f7cb6">

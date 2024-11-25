
# Phone Book App

This project implements a contacts manager application with python. 

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

- Python 3. x
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
## Applicaion Overveiw
<ul>
 <li>Home</li>
 
 ![image](https://github.com/user-attachments/assets/8f6a50cd-af62-4c7e-9637-7f0f52e0bc89)
 
<li>Save New Contact</li>
 
 ![image](https://github.com/user-attachments/assets/fdef7761-bdd3-476b-a473-45fc5ea26894)
 
 <li>Update Contact</li>
 
 ![image](https://github.com/user-attachments/assets/21eee7dd-5981-41d3-95c6-a3cd09874bda)
 ![image](https://github.com/user-attachments/assets/84d97474-814d-4379-a39f-203cf1d71c0b)
 ![image](https://github.com/user-attachments/assets/3b1a1f61-8823-44b1-8f1b-1c8ba94997ca)
 
 <li>View Contact Info</li>
 
 ![image](https://github.com/user-attachments/assets/adae01a9-fa5e-4d55-acbe-3a8acdc16d3c)
</ul>

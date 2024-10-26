
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

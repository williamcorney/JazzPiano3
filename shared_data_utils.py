# shared_data_utils.py

def get_shared_data_from_window(window):
    """
    Access and return the shared data from the Oralia window instance.
    """
    return window.shared_data

def print_shared_data(window):
    """
    Print the shared data from the Oralia window to the console.
    """
    shared_data = get_shared_data_from_window(window)
    print("Shared Data:", shared_data)

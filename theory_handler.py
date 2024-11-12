# theory_handler.py

def handle_theory_action(theory_mode, theory_list, shared_data_manager):
    """
    Handle the theory action based on the selected theory mode and list, with access to shared data.

    :param theory_mode: The theory mode selected (e.g., "Notes", "Scales", etc.)
    :param theory_list: The list of theory items selected
    :param shared_data_manager: The shared data manager instance to access shared data
    """
    print(f"Handling theory action for {theory_mode}")

    # Example: Print out each item selected
    for item in theory_list:
        print(f"Selected: {item}")

    # Example: Access shared data via shared_data_manager
    shared_data = shared_data_manager.shared_data  # Access the shared data dictionary
    print(f"Shared data: {shared_data}")

    # Example logic based on the theory_mode
    if theory_mode == "Scales":
        return f"Processing scales: {', '.join(theory_list)}"
    elif theory_mode == "Triads":
        return f"Processing triads: {', '.join(theory_list)}"
    else:
        return "Theory action processed"

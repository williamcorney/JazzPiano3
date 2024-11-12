def note_handler(tab_instance, message):
    """
    Handles MIDI messages and prints the note if it is a 'note_on' or 'note_off' message.
    Also updates the 'inversion_label' based on the pressed note.
    """
    if message.type == "note_on":
        # Get the note name from the MIDI note number
        note_name = midi_note_to_name(message.note)

        # Update the inversion label with the pressed note
        tab_instance.labels['inversion_label'].setText(f"Inversion: {note_name}")
        print(f"Note On: {message.note} ({note_name})")

        # Emit the note_on_signal to indicate that a note has been pressed
        tab_instance.note_on_signal.emit(message.note, "green")  # Emit with "green" color for the note

    elif message.type == "note_off":
        # Get the note name from the MIDI note number
        note_name = midi_note_to_name(message.note)

        # Update the inversion label with the released note (or reset to a default value)


        # Emit the note_off_signal to indicate that a note has been released
        tab_instance.note_off_signal.emit(message.note)  # Emit note_off_signal to handle note release


def midi_note_to_name(note):
    """
    Converts a MIDI note number to a note name (e.g., 60 -> 'C4').
    """
    # List of note names, starting from C
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note // 12) - 1  # The octave is calculated by dividing the note by 12 and adjusting
    note_name = notes[note % 12]
    return f"{note_name}{octave}"


# Example usage:
note_number = 60  # This is C4
note_name = midi_note_to_name(note_number)
print(note_name)  # Output: C4

import mido
from PyQt6.QtCore import QThread

class MidiInputThread(QThread):
    def __init__(self, practical_tab, input_name):
        super().__init__()
        self.practical_tab = practical_tab
        self.input_name = input_name
        self.running = True

    def run(self):
        try:
            with mido.open_input(self.input_name, callback=self.practical_tab.handle_midi_message) as inport:
                print(f"MIDI input initialized on {self.input_name}.")
                while self.running:
                    pass
        except Exception as e:
            print(f"Error initializing MIDI input: {e}")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class MidiHandler:
    def __init__(self, practical_tab):
        self.practical_tab = practical_tab
        self.midi_thread = None

    def get_midi_input_name(self):
        available_inputs = mido.get_input_names()
        if available_inputs:
            return available_inputs[0]
        else:
            raise Exception("No MIDI input devices found.")

    def setup_midi_input(self):
        input_name = self.get_midi_input_name()
        self.midi_thread = MidiInputThread(self.practical_tab, input_name)
        self.midi_thread.start()

    def stop_midi_input(self):
        if self.midi_thread:
            self.midi_thread.stop()

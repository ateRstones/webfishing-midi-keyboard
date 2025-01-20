import rtmidi2
import time
#from evdev import UInput, ecodes as e
#from pynput.keyboard import Key, Controller
#import pyautogui
import serial

def main():
    #keyboard = Controller()
    #ui = UInput()
    midi_in = rtmidi2.MidiIn()
    midi_in.open_port(1)
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)

    # let us just handle one octave for now
    midi_note_map = [
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
        "C"
    ]

    # string_note_to_keypresses_map = {
    #     "C": [e.KEY_1, e.KEY_T],
    #     "C#": [e.KEY_2, e.KEY_T],
    #     "D": [e.KEY_0, e.KEY_R],
    #     "D#": [e.KEY_1, e.KEY_E],
    #     "E": [e.KEY_0, e.KEY_Q],
    #     "F": [e.KEY_1, e.KEY_Q],
    #     "F#": [e.KEY_2, e.KEY_Y],
    #     "G": [e.KEY_0, e.KEY_R],
    #     "G#": [e.KEY_1, e.KEY_R],
    #     "A": [e.KEY_0, e.KEY_W],
    #     "A#": [e.KEY_1, e.KEY_W],
    #     "B": [e.KEY_0, e.KEY_T],
    # }


    string_note_to_keypresses_map_old = {
        "C": ["4", "w"],
        "C#": ["5", "w"],
        "D": ["1", "e"],
        "D#": ["2", "e"],
        "E": ["3", "e"],
        "F": ["4", "e"],
        "F#": ["5", "e"],
        "G": ["1", "r"],
        "G#": ["2", "r"],
        "A": ["3", "r"],
        "A#": ["4", "r"],
        "B": ["1", "t"]
    }

    def note_string_note(note):
        print(note)
        return midi_note_map[note-48]

    # def press_keys(string_note):
    #     presses = string_note_to_keypresses_map[string_note]
    #     for press in presses:
    #         print(press)
    #         ui.write(e.EV_KEY, press, 1)
    #         ui.write(e.EV_KEY, press, 0)
    #         ui.syn()
    
    # def press_keys_old(string_note):
    #     presses = string_note_to_keypresses_map_old[string_note]
    #     for press in presses:
    #         print(press)
    #         keyboard.tap(press)

    # def press_keys_ag(string_note):
    #     presses = string_note_to_keypresses_map_old[string_note]
    #     for press in presses:
    #         print(press)
    #         pyautogui.press(press)
    
    def press_keys_serial(string_note):
        presses = string_note_to_keypresses_map_old[string_note]
        for press in presses:
            print(press)
            ser.write(press.encode())
            ser.flush()

    try:
        while True:
            message = midi_in.get_message()
            if message:
                msgtype, channel = rtmidi2.splitchannel(message[0])
                if msgtype == rtmidi2.NOTEON:
                    note, velocity = note_string_note(message[1]), message[2]
                    print(f"Noteon, {channel=}, {note=}, {velocity=}")
                    press_keys_serial(note)
                elif msgtype == rtmidi2.CC:
                    cc, value = message[1:]
                    print(f"Control Change {channel=}, {cc=}, {value=}")
                elif msgtype == rtmidi2.NOTEOFF:
                    note, velocity = note_string_note(message[1]), message[2]
                    print(f"Noteoff, {channel=}, {note=}, {velocity=}")
            else:
                time.sleep(0.01)
    except:
        ser.close()

if __name__ == "__main__":
    main()
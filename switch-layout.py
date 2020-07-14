#!/usr/bin/env python3
import subprocess

from pynput import keyboard

# The shortcuts triggering switch
SWITCH_SHORTCUTS = [
    # For some reason Alt pressed after Shift gets registered as a different
    # key code on my system.
    {keyboard.KeyCode(65511)},  # Shift + Alt
    {keyboard.Key.alt, keyboard.Key.shift},  # Alt + Shift

    # Examples
    # {keyboard.Key.shift, keyboard.Key.ctrl},  # Shift + Ctrl
    # {keyboard.Key.cmd, keyboard.Key.space},  # Super + Space
    # {keyboard.Key.caps_lock},  # CapsLock
]

# How many layouts do you have?
LAYOUTS_COUNT = 2

# If you're having troubles configuring SWITCH_SHORTCUTS, set this to True.
# Script will output pressed keys so you could copy-paste them.
DEBUG = False


def format_key(key):
    """
    Formats a key the way it should be written in SWITCH_SHORTCUTS list.
    """
    if isinstance(key, keyboard.Key):
        return "keyboard.Key.{}".format(key.name)
    else:
        return "keyboard.KeyCode({})".format(key.vk)


class Switcher:
    def __init__(self):
        self.current_keys = set()
        self.keys_pressed = 0

        self.monitored_keys = set()
        for shortcut in SWITCH_SHORTCUTS:
            self.monitored_keys |= shortcut

        self.current_layout = 0

    def on_press(self, key):
        if DEBUG:
            print("Pressed: {}".format(format_key(key)))

        if key not in self.monitored_keys:
            return

        self.current_keys.add(key)
        self.keys_pressed += 1

        if self.is_switch_shortcut():
            self.on_switch()

    def on_release(self, key):
        if DEBUG:
            print("Released: {}".format(format_key(key)))

        self.keys_pressed -= 1

        # Sometimes one key is pressed and another is released.
        # Blame X server.
        if key in self.current_keys:
            self.current_keys.remove(key)

        if self.keys_pressed <= 0:
            self.keys_pressed = 0
            self.current_keys = set()

    def is_switch_shortcut(self):
        for shortcut in SWITCH_SHORTCUTS:
            if self.current_keys.issuperset(shortcut):
                return True

        return False

    def on_switch(self):
        self.current_layout += 1
        if self.current_layout >= LAYOUTS_COUNT:
            self.current_layout = 0

        command = [
            "gsettings",
            "set",
            "org.gnome.desktop.input-sources",
            "current",
            str(self.current_layout),
        ]
        _exitcode = subprocess.call(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    switcher = Switcher()

    with keyboard.Listener(
            on_press=switcher.on_press,
            on_release=switcher.on_release) as listener:
        listener.join()


if __name__ == '__main__':
    main()

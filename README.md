# switch-layout

## What is this?

This is a workaround for keyboard layout switching bug, which occurs, as far as I know, on some Gnome 3 based DEs running on X server, including Pantheon (elementary OS DE). According to some of the reports I've read, it affects mostly users of Russian keyboard layout.

The bug is this: there is an annoying delay between the moment you try to switch layout (either with a shortcut or with the GUI) and the moment the layout is switched. In my case, it's around 1 second when switching from RU to EN. Sometimes the layout doesn't switch at all! This bug makes it impossible to type text both in Russian and English quickly.

This workaround made things easier for me. It's not ideal, but it reduces the delay far enough to make it barely noticable.

Related reports on Launchpad:

* [Delay before you can type after switching input source](https://bugs.launchpad.net/ubuntu/+source/gnome-control-center/+bug/1754702/)
* [Gnome on Xorg freezes for short time on every keyboard layout switch](https://bugs.launchpad.net/ubuntu/+source/ubiquity/+bug/1790335)
* [layout switch is delayed](https://bugs.launchpad.net/ubuntu/+source/console-setup/+bug/1370953)

## How does it work

I've found that I can switch my layout using `gsettings` command without any delay:

```
gsettings set org.gnome.desktop.input-sources current X
```

Where `X` is the index of a layout: `0` for the first one, `1` for the second, etc.

This script listens to the switch shortcut and runs the command itself.

## How to install it

1. Make sure you have `pip` installed.

  ```
  sudo apt install python3-pip
  ```

2. Install [pynput](https://pypi.org/project/pynput/) - the script uses it to listen for key presses.

  ```
  python3 -m pip install --user pynput==1.4
  ```

3. Copy the `switch-layout.py` somewhere in your home folder.
4. Edit the `SWITCH_SHORTCUTS` and `LAYOUTS_COUNT` at the top of the script accordingly to your needs.
5. Disable built-in layout-switch shortcut in your system, so it wouldn't interfere with the script. Also disable CapsLock default behavior in case you use it as switch key.
6. Run the script: `python3 switch-layout.py`. Try pressing the shortcut and see if it works.
  If it doesn't, feel free to open an issue. Maybe I'll be able to help.
  Press `Ctrl+C` to stop the script.
7. If it works, you can add this script to autostart programs in your DE to make it start automatically.

rogdrv
======

rogdrv is a simple ASUS ROG userspace mouse driver for Linux.
The mouse device consists of 2 input devices: mouse and keyboard.
The keyboard part is unsupported on Linux, but it's recognised as HID device.
So this driver maps HID events to the generic keyboard events.

The protocol was reverse-engineered, so everything is experimental. Use at your own risk.

Supported devices
-----------------

* ASUS ROG Pugio (most features work)
* ASUS ROG Strix Impact (switching LED works, everything other is untested)

There is a chance that a driver can be compatible with other mouse devices
from ASUS ROG (Republic of Gamers) series.

Features
--------

* Virtual uinput device
* Button bindings
* LED colors customization
* Profile switching
* DPI setting
* Polling rate setting

Requirements
------------

* python >= 3.0
* python-hidapi + python-cffi (hidapi-cffi)
* python-evdev
* gir-appindicator3

Ubuntu:
```
apt install python3-hidapi python3-evdev gir1.2-appindicator3-0.1
```

Installation
------------

Userspace driver installation:
```
sudo python3 setup.py install
```

You need r/w permissions for /dev/hidrawX file of your mouse.
You can solve this by installing a custom udev rules:
```
sudo cp -f udev/50-rogdrv.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Using
-----

Userspace driver consists of 2 programs: *rogdrv* and *rogdrv-config*

rogdrv is a virtual uinput device driver which converts mouse events into uinput events.
![rogdrv](/screenshot.png)
```
Usage: rogdrv [--console]
  --help       - display help
  --console    - starts in pure console mode, disables tray icon
```

rogdrv-config is a mouse configuration tool.
```
Usage:
  rogdrv-config --help                            - display help

  rogdrv-config actions                           - display list of actions

  rogdrv-config bind [button action]              - bind a button or display list of bindings
    button: button no. (1-10)
    action: action code (241 or 0xF1 or 0xf1)

  rogdrv-config color [name r g b [mode] [brght]] - get/set LED colors
    name: logo, wheel, bottom, all
    r: red (0-255)
    g: green (0-255)
    b: blue (0-255)
    mode: default, breath, rainbow, wave, reactive, flasher
    brght: brightness 0-4

  rogdrv-config profile [value]                   - get/set profile
    value: profile no. (1-3)

  rogdrv-config dpi [value [type]]                - get/set DPI
    value: DPI (50-7200)
    type: 1 (default) or 2

  rogdrv-config rate [rate]                       - get/set polling rate
    rate: rate in Hz (125, 250, 500, 1000)

```

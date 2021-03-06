# Copyright (C) 2018 Kyoken, kyoken@kyoken.ninja

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import os
import signal
import sys
import threading

from . import defs
from .device import EventHandler, DeviceManager


def rogdrv():
    '''
    Virtual uinput device driver which converts mouse events
    into uinput events.
    '''
    if '--help' in sys.argv:
        print('''Usage: rogdrv [--console]
  --help       - display help
  --console    - starts in pure console mode, disables tray icon
''')
        return

    device = DeviceManager.get_device()
    handler = EventHandler()

    def loop():
        while True:
            e = device.next_event()
            handler.handle_event(e)

    if '--console' in sys.argv:
        loop()
    else:
        from .gtk3 import gtk3_main
        thread = threading.Thread(target=loop)
        thread.start()
        gtk3_main(device)
        device.close()
        handler.close()
        os.kill(os.getpid(), signal.SIGTERM)


def rogdrv_config():
    '''
    Mouse configuration tool
    '''
    # device = Pugio()
    # request = [0] * 64
    # request[0] = 0x12
    # request[1] = 0x00
    # print(list(device.query(bytes(request))))

    if len(sys.argv) >= 2:
        if sys.argv[1] == 'actions':
            print('Keyboard actions:')
            for action, name in defs.ACTIONS_KEYBOARD.items():
                print('  {action} (0x{action:02X}): {name}'.format(**{
                    'action': action,
                    'name': name,
                }))

            print('')
            print('Mouse actions:')
            for action, name in defs.ACTIONS_MOUSE.items():
                print('  {action} (0x{action:02X}): {name}'.format(**{
                    'action': action,
                    'name': name,
                }))

            return

        elif sys.argv[1] == 'bind':
            device = DeviceManager.get_device()
            if not device:
                print('Device not found')
                return

            if len(sys.argv) >= 4:
                button = int(sys.argv[2])
                action = sys.argv[3].lower()
                if action.startswith('0x'):
                    action = int(action, 16)
                else:
                    action = int(action)
                device.bind(button, action)
                device.save()

            print(device.get_bindings())
            return

        elif sys.argv[1] == 'color':
            device = DeviceManager.get_device()
            if not device:
                print('Device not found')
                return

            if len(sys.argv) >= 6:
                name = sys.argv[2]

                r = int(sys.argv[3])
                g = int(sys.argv[4])
                b = int(sys.argv[5])

                if len(sys.argv) >= 7:
                    mode = sys.argv[6]
                else:
                    mode = 'default'

                if len(sys.argv) >= 8:
                    brightness = int(sys.argv[7])
                else:
                    brightness = 4

                device.set_color(
                    name, (r, g, b), mode=mode, brightness=brightness)
                device.save()

            print(device.get_colors())
            return

        elif sys.argv[1] == 'profile':
            device = DeviceManager.get_device()
            if not device:
                print('Device not found')
                return

            if not device.profiles:
                print('Profiles not supported')
                return

            if len(sys.argv) >= 3:
                device.set_profile(int(sys.argv[2]))

            profile = device.get_profile()
            print('Profile: {}'.format(profile))
            return

        elif sys.argv[1] == 'dpi':
            device = DeviceManager.get_device()
            if not device:
                print('Device not found')
                return

            if len(sys.argv) >= 3:
                if len(sys.argv) >= 4:
                    type_ = int(sys.argv[3])
                else:
                    type_ = 1

                device.set_dpi(int(sys.argv[2]), type_=type_)
                device.save()

            dpi1, dpi2, rate, undef = device.get_dpi_rate()
            print('DPI 1: {}'.format(dpi1))
            print('DPI 2: {}'.format(dpi2))
            return

        elif sys.argv[1] == 'rate':
            device = DeviceManager.get_device()
            if not device:
                print('Device not found')
                return

            if len(sys.argv) >= 3:
                device.set_rate(int(sys.argv[2]))
                device.save()

            dpi1, dpi2, rate, undef = device.get_dpi_rate()
            print('Polling rate: {}'.format(rate))
            return

        elif sys.argv[1] == 'dump':
            device = DeviceManager.get_device()
            if not device:
                print('Device not found')
                return

            if len(sys.argv) >= 3:
                with open(sys.argv[2], 'w') as f:
                    device.dump(f)

            print('Settings saved into: {}'.format(sys.argv[2]))
            return

        elif sys.argv[1] == 'load':
            device = DeviceManager.get_device()
            if not device:
                print('Device not found')
                return

            if len(sys.argv) >= 3:
                with open(sys.argv[2], 'r') as f:
                    device.load(f)

            print('Settings loaded from: {}'.format(sys.argv[2]))
            return

        elif sys.argv[1] == '--help':
            print('''Usage:
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
    brght: brightness 0-4 (default - 4)

  rogdrv-config profile [value]                   - get/set profile
    value: profile no. (1-3)

  rogdrv-config dpi [value [type]]                - get/set DPI
    value: DPI (50-7200)
    type: 1 (default) or 2

  rogdrv-config rate [rate]                       - get/set polling rate
    rate: rate in Hz (125, 250, 500, 1000)

  rogdrv-config dump file                         - save settings into file
    file: path to json file

  rogdrv-config load file                         - load settings from file
    file: path to json file
''')
            return

    print('Got nothing to do.')
    print("Try 'rogdrv-config --help' for more information.")

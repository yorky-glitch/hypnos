import urwid
import random

# Death scenarios
deaths = [
    "You see a tiny girl with pale skin, white dress, and pitch-black eyes — she looks towards you and...",
    "You see a masked man. He sees you and shoots you.",
    "There is a giant black figure. It looks toward you and hits you with lightning."
]

death = random.choice(deaths)

# Global state
player_name = ""
has_key = False

# UI Widgets
main_text = urwid.Text("")
choices_walker = urwid.SimpleFocusListWalker([])
choices_listbox = urwid.ListBox(choices_walker)

footer = urwid.AttrMap(
    urwid.Text("↑↓ Navigate   ⏎ Select   Esc/Q Quit", align='center'),
    'footer'
)

frame = urwid.Frame(
    header=urwid.Padding(main_text, left=1, right=1),
    body=choices_listbox,
    footer=footer
)


def update_scene(text, options):
    main_text.set_text(text)
    choices_walker.clear()
    for label, callback in options:
        button = urwid.Button(label)
        urwid.connect_signal(button, 'click', lambda _, cb=callback: cb())
        wrapped = urwid.AttrMap(button, None, focus_map='reversed')
        choices_walker.append(wrapped)


def ask_name():
    edit = urwid.Edit("What is your name? ")

    def on_keypress(key):
        if key == 'enter':
            global player_name
            player_name = edit.edit_text.strip()
            main_loop.widget = frame
            main_loop.unhandled_input = handle_keys
            start()

    main_loop.widget = urwid.Filler(edit, valign='middle')
    main_loop.unhandled_input = on_keypress


def handle_keys(key):
    if key.lower() in ('esc', 'q'):
        raise urwid.ExitMainLoop()


def start():
    update_scene(
        "You wake up in an empty room. There is a window.",
        [
            ("Look outside", you_died),
            ("Go to sleep", stage2)
        ]
    )


def stage2():
    update_scene(
        "You woke up and there is a flower vase.",
        [
            ("Break the vase", found_key),
            ("Look outside", you_died)
        ]
    )


def found_key():
    global has_key
    has_key = True
    update_scene(
        "You broke the vase. There is a key inside.",
        [
            ("Look outside", you_died),
            ("Go to sleep", stage3)
        ]
    )


def stage3():
    if has_key:
        update_scene(
            "You wake up. There is a door.",
            [
                ("Try the key", door_opens),
                ("Go to sleep", stage4)
            ]
        )
    else:
        update_scene(
            "You wake up. There is a door, but it's locked.",
            [
                ("Go to sleep", stage4)
            ]
        )


def door_opens():
    update_scene(
        "The door opens. The next room looks exactly like the first one.",
        [
            ("Go into the next room", room_loop),
            ("Go to sleep", stage4)
        ]
    )


def room_loop():
    update_scene(
        "What do you do next?",
        [
            ("Kill yourself", lambda: end_game("You ended it all.")),
            ("Go to sleep", stage4)
        ]
    )


def stage4():
    update_scene(
        "The next room seems to be the exact room you started from.",
        [
            ("Sleep in the next room", stage5_1),
            ("Look outside", you_died),
            ("Sleep in the first room", stage5_2)
        ]
    )


def stage5_1():
    update_scene(
        "You look around in the new room. There is a mirror on the wall, and a strange humming sound.",
        [
            ("Look in the mirror", lambda: end_game("Your reflection pulls you in. You were never seen again.")),
            ("Follow the sound", lambda: end_game("You discover a portal. Maybe this is the way out.")),
            ("Go to sleep", lambda: end_game("But this time, you don't wake up. You died in your sleep."))
        ]
    )


def stage5_2():
    update_scene(
        "You wake up in the same room. There is nothing anymore — only a dark void.",
        [
            ("Go to sleep", lambda: end_game("You died in your sleep."))
        ]
    )


def you_died():
    end_game("You looked outside.\n" + death + "\nYou were killed.")


def end_game(msg):
    update_scene(msg + f"\n\nThank you {player_name} for playing!", [])


# Color palette
palette = [
    ('reversed', 'standout', ''),
    ('footer', 'black', 'light gray'),
]

# Start the application
main_loop = urwid.MainLoop(frame, palette=palette)
ask_name()
main_loop.run()

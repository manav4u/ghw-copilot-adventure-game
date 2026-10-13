#!/usr/bin/env python3
"""
adventure.py

A single-file command-line choose-your-own-adventure game.
- At least 8 rooms
- Inventory (take/use items)
- A key item (Golden Key) required for the win ending
- Multiple win/lose endings

Only uses the Python standard library.
"""

import sys
import textwrap

# Game world definition
rooms = {
    "Foyer": {
        "desc": "You stand in the Foyer of an old manor. Moonlight filters through cracked stained glass.",
        "exits": ["Great Hall"],
        "items": []
    },
    "Great Hall": {
        "desc": "A cavernous Great Hall stretches before you. Tattered banners hang from the rafters.",
        "exits": ["Library", "Armory", "Courtyard", "Tower Foot", "Dungeon"],
        "items": []
    },
    "Library": {
        "desc": "Dusty shelves filled with leather-bound tomes. A draft whispers through a broken window.",
        "exits": ["Great Hall"],
        "items": ["Rope", "Old Map"]
    },
    "Armory": {
        "desc": "Rows of rusted weapons and cold armor stand at attention. A locked glass case catches your eye.",
        "exits": ["Great Hall"],
        "items": ["Sword", "Golden Key"]
    },
    "Courtyard": {
        "desc": "An overgrown courtyard with a dried fountain. Pathways lead into a neglected garden and toward a dangerous ravine.",
        "exits": ["Great Hall", "Garden", "Ravine"],
        "items": []
    },
    "Garden": {
        "desc": "Statues half-swallowed by ivy, fragrant but wilted plants, and a broken lantern on the ground.",
        "exits": ["Courtyard"],
        "items": ["Shield", "Lantern"]
    },
    "Ravine": {
        "desc": "A yawning ravine blocks the path. The stones are slick and the drop is fatal if you slip.",
        "exits": ["Courtyard"],
        "items": []
    },
    "Tower Foot": {
        "desc": "The base of an ancient tower. A spiral staircase creaks upward to the Tower Top.",
        "exits": ["Great Hall", "Tower Top"],
        "items": []
    },
    "Tower Top": {
        "desc": "Wind bites at you near the tower's peak. A single ornate chest sits in the center, locked tight.",
        "exits": ["Tower Foot"],
        "items": []
    },
    "Dungeon": {
        "desc": "A dark, damp dungeon below the manor. The air is thick and you can hear distant dripping.",
        "exits": ["Great Hall"],
        "items": ["Mysterious Coin"]
    },
}

# Game state
state = {
    "location": "Foyer",
    "inventory": [],
    "chest_opened": False,
    "alive": True,
    "won": False,
    "visited": set()
}


# Utility functions
def wrap(text):
    return "\n".join(textwrap.wrap(text, width=78))


def pause():
    input("\n(Press Enter to continue...)")


def show_header():
    print("=" * 78)
    print("ANCIENT MANOR: A CHOOSE-YOUR-OWN-ADVENTURE".center(78))
    print("=" * 78)


def show_location():
    loc = state["location"]
    state["visited"].add(loc)
    print("\nLocation:", loc)
    print("-" * (10 + len(loc)))
    print(wrap(rooms[loc]["desc"]))
    items = rooms[loc]["items"]
    if items:
        print("\nYou see:")
        for it in items:
            print(" -", it)
    print()


def print_inventory():
    if state["inventory"]:
        print("You are carrying:")
        for it in state["inventory"]:
            print(" -", it)
    else:
        print("You are carrying nothing.")


# Game actions
def move_to(destination):
    # Special checks triggered by entering certain rooms
    if destination not in rooms:
        print("You can't go there.")
        return
    # Entering Ravine: must have Rope to survive crossing
    if destination == "Ravine":
        if "Rope" in state["inventory"]:
            print(wrap("You secure the rope and carefully make your way across the ravine. "
                       "The rope holds. You clamber up the other side, heart pounding but alive."))
            state["location"] = destination
        else:
            lose("As you step toward the ravine the ground gives way and you tumble into the darkness below. "
                 "Without a rope you cannot escape the fall.")
            return
    # Entering Dungeon: must have Lantern to see safely
    elif destination == "Dungeon":
        if "Lantern" in state["inventory"]:
            print(wrap("You light the lantern. Its warm glow reveals chained doors and old bones."
                       "A cold wind smells of old iron. You proceed cautiously."))
            state["location"] = destination
        else:
            lose("You stumble into the Dungeon in the pitch dark. You cannot find your footing and a hidden pit claims you.")
            return
    # Entering Tower Top: guardian may appear when you try to interact with the chest (handled in open_chest)
    else:
        state["location"] = destination

    # Describe new location
    show_location()


def take_item(item):
    loc = state["location"]
    if item in rooms[loc]["items"]:
        state["inventory"].append(item)
        rooms[loc]["items"].remove(item)
        print(f"You pick up the {item}.")
    else:
        print("There is no such item here.")


def use_item(item):
    item = item.strip()
    if item not in state["inventory"]:
        print("You don't have that item.")
        return
    loc = state["location"]
    # Using Rope anywhere else just a flavor
    if item == "Rope":
        print("The rope feels sturdy. It could help crossing something dangerous.")
    elif item == "Lantern":
        print("You check the lantern: the glass is cracked but it still gives light.")
    elif item == "Old Map":
        show_map()
    elif item == "Mysterious Coin":
        print("The coin is cold and engraved with a symbol you don't recognize.")
    else:
        print(f"You inspect the {item}. It might be useful.")


def open_chest():
    loc = state["location"]
    if loc != "Tower Top":
        print("There is no chest here to open.")
        return
    if state["chest_opened"]:
        print("The chest is already open. The treasure you found once is gone now.")
        return

    print(wrap("You approach the ornate chest. Gnarled runes frame a lock shaped like an eye."))
    # A guardian animates to defend the chest
    print("\nA stone guardian towers up from the floor to block your path!")
    # Check for Sword to fight
    if "Sword" in state["inventory"]:
        print(wrap("You draw your Sword and face the guardian. Steel rings on stone as you strike; "
                   "with skill and luck you shatter the guardian into rubble."))
    else:
        lose("You have nothing to fight with. The guardian's stone hand crushes you before you can react.")
        return

    # Now try to unlock chest with Golden Key
    if "Golden Key" in state["inventory"]:
        print(wrap("You fit the Golden Key into the lock. It turns with a click. The chest opens to reveal a trove of glittering jewels and an ancient crown."))
        state["chest_opened"] = True
        win()
    else:
        print(wrap("The chest resists. There is a key-shaped slot that looks like it needs a special key."))
        print("You step back, the guardian remains broken, but the chest stays locked.")


def show_map():
    # Give a simple hinting map
    print("\nYou unroll the Old Map. It sketches the manor roughly:")
    print(textwrap.dedent("""
        [Foyer] --> [Great Hall] --> [Library]
                         |           |
                         |           --> (Rope)
                         |
                         --> [Armory] (Sword, Golden Key)
                         |
                         --> [Courtyard] --> [Garden] (Shield, Lantern)
                                         --> [Ravine] (Needs Rope)
                         |
                         --> [Tower Foot] --> [Tower Top] (Locked Chest)
                         |
                         --> [Dungeon] (Dark; needs Lantern)
    """).strip())
    print("The map suggests the Armory and Garden might be important.")


def show_help():
    print(textwrap.dedent("""
    Commands:
     - Enter the number of the option to choose it.
     - take <item>      : pick up an item shown in the room
     - use <item>       : use or inspect an item from your inventory
     - inventory (i)    : show your carried items
     - look (l)         : re-describe your current location
     - map (m)          : view the Old Map (if you have it, or read it from use)
     - help (h)         : show this help
     - quit (q)         : give up and exit
    Tips:
     - The Golden Key is important for the final chest.
     - Bring light into dark places and rope across gaps.
    """).strip())


def lose(message):
    print("\n" + "=" * 78)
    print("YOU HAVE DIED".center(78))
    print("=" * 78 + "\n")
    print(wrap(message))
    state["alive"] = False
    print("\nBetter luck next time.")
    pause()
    sys.exit(0)


def win():
    print("\n" + "=" * 78)
    print("TREASURE! YOU WIN!".center(78))
    print("=" * 78 + "\n")
    print(wrap("With the chest open you claim the ancient crown and radiance fills the room. "
               "A sense of rightness settles over the manor: your name will be told in taverns for years."))
    state["won"] = True
    pause()
    sys.exit(0)


# Helper to list options for the current room
def build_options():
    loc = state["location"]
    opts = []
    # Movement options
    for ex in rooms[loc]["exits"]:
        # Describe special exits a little
        if ex == "Ravine":
            desc = "Approach the Ravine (dangerous)"
        elif ex == "Dungeon":
            desc = "Descend into the Dungeon (dark below)"
        elif ex == "Tower Top":
            desc = "Climb to the Tower Top"
        else:
            desc = f"Go to the {ex}"
        opts.append((desc, lambda dest=ex: move_to(dest)))
    # Item pickup options
    for item in list(rooms[loc]["items"]):
        opts.append((f"Take the {item}", lambda it=item: take_item(it)))
    # Special actions (open chest)
    if loc == "Tower Top":
        opts.append(("Open the ornate chest", open_chest))
    # Generic actions
    opts.append(("Check your inventory", lambda: print_inventory()))
    opts.append(("Look around", lambda: show_location()))
    opts.append(("Use an item from inventory", lambda: prompt_use_item()))
    opts.append(("Help", show_help))
    opts.append(("Quit", lambda: sys.exit(0)))
    return opts


def prompt_use_item():
    if not state["inventory"]:
        print("You have no items to use.")
        return
    print("Which item would you like to use?")
    for i, it in enumerate(state["inventory"], 1):
        print(f" {i}. {it}")
    choice = input("> ").strip()
    if not choice:
        return
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(state["inventory"]):
            use_item(state["inventory"][idx])
        else:
            print("Invalid selection.")
    else:
        # allow typing the name
        use_item(choice)


def parse_command(cmd):
    cmd = cmd.strip()
    if not cmd:
        return None
    # simple direct commands
    if cmd.lower() in ("inventory", "i"):
        print_inventory()
        return None
    if cmd.lower() in ("help", "h"):
        show_help()
        return None
    if cmd.lower() in ("look", "l"):
        show_location()
        return None
    if cmd.lower() in ("map", "m"):
        if "Old Map" in state["inventory"]:
            show_map()
        else:
            print("You don't have a map.")
        return None
    if cmd.lower() in ("quit", "q", "exit"):
        print("You decide to leave the manor for another day. Game over.")
        sys.exit(0)

    # take <item>
    if cmd.lower().startswith("take "):
        item = cmd[5:].strip()
        if item:
            take_item(item)
        else:
            print("Take what?")
        return None

    # use <item>
    if cmd.lower().startswith("use "):
        item = cmd[4:].strip()
        if item:
            use_item(item)
        else:
            print("Use what?")
        return None

    # numeric selection handled elsewhere
    return cmd


def main_loop():
    show_header()
    print(wrap("You awake on the cold stone floor of a manor. Your mission is to find the manor's hidden treasure. "
               "Explore rooms, collect items, and solve hazards. Be careful—some paths are deadly without the right tools."))
    show_location()

    while state["alive"] and not state["won"]:
        opts = build_options()
        print("\nOptions:")
        for i, (desc, _) in enumerate(opts, 1):
            print(f" {i}. {desc}")
        print("\n(Type a number to choose an option, or type a command like 'take Rope' or 'use Lantern'.)")
        cmd = input("> ").strip()
        if not cmd:
            continue

        parsed = parse_command(cmd)
        # If parse_command returned None, it already handled the input
        if parsed is None:
            continue

        # If user entered a number, run that option
        if parsed.isdigit():
            idx = int(parsed) - 1
            if 0 <= idx < len(opts):
                action = opts[idx][1]
                action()
            else:
                print("That's not a valid option number.")
            continue

        # If not numeric and not recognized, try to interpret as "take <item>" earlier; fallback:
        print("I didn't understand that. Try a number or 'help'.")


def setup():
    # Place any initialization logic here. (Rooms already defined above.)
    # Ensure required items exist where intended.
    # (This function exists to make expansion easier.)
    pass


if __name__ == "__main__":
    try:
        setup()
        main_loop()
    except KeyboardInterrupt:
        print("\n\nGoodbye.")
        sys.exit(0)

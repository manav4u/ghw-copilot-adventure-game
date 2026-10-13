<h1 align="center">Manor Escape</h1>

<p align="center">
A text adventure for the terminal. One Python file, no dependencies.<br>
Built with GitHub Copilot for MLH Global Hack Week: Hacktoberfest 2026.
</p>

<p align="center">
<sub>Python 3 &nbsp;|&nbsp; standard library only &nbsp;|&nbsp; single file: <code>adventure.py</code></sub>
</p>

---

## The game

You start in the Foyer of an old manor. Somewhere inside is a locked chest, and a stone guardian that does not want you opening it. Explore the rooms, pick up what you can carry, and work out what the chest needs before you try it.

- 10 rooms to explore, from the Great Hall to the Dungeon and the Tower Top
- An inventory you fill with `take` and use with `use`
- A key item the final chest depends on
- More than one way to lose, and a win ending if you prepare properly

## Run it

You need Python 3.8 or newer. Nothing to install.

```bash
git clone https://github.com/manav4u/ghw-copilot-adventure-game.git
cd ghw-copilot-adventure-game
python3 adventure.py
```

## Commands

Rooms offer numbered choices. Type the number to move. Anything else is a typed command:

| Command | What it does |
| --- | --- |
| `take <item>` | Pick up an item listed in the room |
| `use <item>` | Use or inspect something you carry |
| `inventory` or `i` | List what you are carrying |
| `look` or `l` | Describe the current room again |
| `map` or `m` | Read the Old Map, if you have found it |
| `help` or `h` | Show the command list |
| `quit` or `q` | Leave the manor |

## The manor

| Room | Leads to | Items lying around |
| --- | --- | --- |
| Foyer | Great Hall | none |
| Great Hall | Library, Armory, Courtyard, Tower Foot, Dungeon | none |
| Library | Great Hall | Rope, Old Map |
| Armory | Great Hall | Sword, Golden Key |
| Courtyard | Great Hall, Garden, Ravine | none |
| Garden | Courtyard | Shield, Lantern |
| Ravine | Courtyard | none |
| Tower Foot | Great Hall, Tower Top | none |
| Tower Top | Tower Foot | the chest |
| Dungeon | Great Hall | Mysterious Coin |

Some places in the manor are dangerous. The in-game help has two hints. Everything else is for you to find out.

## About this project

This is my submission for the **Build a Simple App with Copilot** challenge in MLH [Global Hack Week: Hacktoberfest](https://ghw.mlh.com/events/open-source) (October 9 to 15, 2026). The brief was to build a small working app with GitHub Copilot's help.

The world, the commands and the endings were written with Copilot. It is a small game on purpose, so it stays readable top to bottom.

## Project layout

```text
.
|-- adventure.py   the whole game: world data, state, commands, endings
`-- README.md
```

The rooms live in one `rooms` dictionary at the top of `adventure.py`. To add a room, give it a description, a list of exits and a list of items.

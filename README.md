# in-between
## A server for UB Funkeys
### Written by Jake Saunders
### Licence: MIT

> If it's not here, and it's not there, then obviously it must be in between!

This utility emulates the UB Funkeys server, allowing for usage of all online features, including chat, multiplayer games, crib sharing and funkey trunk.

### Requirements
Python 3.6?

### Usage
To set up the server's database, run `python in-between/server.py setup`. You can specify a custom path for the database in `in-between/settings.py`.
To launch the server, run `python in-between/server.py`.

### Features
#### Implemented
* Unique Funkey Names (when pre-registered in database)
* Buddies and private chat
* Leaderboard (partially)
* Trunk (partially)

#### Not Yet Implemented
* Registering new Unique Funkey Names
* Multiplayer chat rooms
* Crib sharing
* Cloud saves
* Update capabilities
* Multiplayer games
* Game-builder sharing
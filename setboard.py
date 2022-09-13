from sys import implementation
if implementation.name.upper() == "MICROPYTHON":
    from os import uname
    envVars["_uname"] = uname().machine
elif implementation.name.upper() == "CIRCUITPYTHON":
    import board
    envVars["_boardID"] = board.board_id

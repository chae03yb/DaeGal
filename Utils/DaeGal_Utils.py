import discord

class EmbedColors:
    Red       = 0xFF0000
    Green     = 0x30E330
    SkyBlue   = 0x7289DA
    Black     = 0x000000
    Yellow    = 0xFFCC00

class Exceptions:
    class NoTargetSpecified(Exception):
        def __init__(self):
            super().__init__("You must specify target")
        def __str__(self):
            return "대상이 지정되지 않았습니다"

class Emoji_id:
    pass
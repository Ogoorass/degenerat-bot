from discord.ext.commands import Bot, Cog, command, Context

class React( Cog ):
    def __init__( self, bot: Bot ):
        self.bot = bot
    
        self.l_to_e = {
            "A": ("🇦", "🅰️"),
            "B": ("🇧", "🅱️"),
            "C": ("🇨",  ),
            "D": ("🇩", "▶️"),
            "E": ("🇪",  ), # need moar!!!
            "F": ("🇫",  ),
            "G": ("🇬",  ),
            "H": ("🇭",  ),
            "I": ("🇮", "ℹ️", "1⃣"),
            "J": ("🇯",  ),
            "K": ("🇰",  ),
            "L": ("🇱",  ),
            "M": ("🇲", "Ⓜ️"),
            "N": ("🇳",  ),
            "O": ("🇴", "🅾️", "0⃣"),
            "P": ("🇵", "🅿️"),
            "Q": ("🇶",  ),
            "R": ("🇷",  ),
            "S": ("🇸", "5⃣"), # kinda meh using 5 as S
            "T": ("🇹",  ),
            "U": ("🇺",  ),
            "V": ("🇻",  ),
            "W": ("🇼",  ),
            "X": ("🇽", "❎", "❌"),
            "Y": ("🇾",  ),
            "Z": ("🇿",  ),
            "0": ("0⃣", "🇴"),
            "1": ("1⃣", "🇮"),
            "2": ("2⃣",  ),
            "3": ("3⃣",  ),
            "4": ("4⃣",  ),
            "5": ("5⃣",  ),
            "6": ("6⃣",  ),
            "7": ("7⃣",  ),
            "8": ("8⃣",  ),
            "9": ("9⃣",  ),
            "?": ("❓", "❔"),
            "!": ("❗", "❕"),
            "#": ("#️⃣", ),
            "*": ("*️⃣", ),
            
            "10":   ("🔟", ),
            "AB":   ("🆎", ),
            "WC":   ("🚾", ),
            "CL":   ("🆑", ),
            "VS":   ("🆚", ),
            "NG":   ("🆖", ),
            "OK":   ("🆗", ),
            "ID":   ("🆔", ),
            "!!":   ("‼️",  ),
            "!?":   ("⁉️",  ),
            "UP":   ("🆙", ),
            
            "ABC":  ("🔤", ),
            "SOS":  ("🆘", ),
            "NEW":  ("🆕", ),
            "UP!":  ("🆙", ),
            
            # basically unreadable as a reaction
            #"COOL": ("🆒", ),
            #"FREE": ("🆓", ),
        }

        self.pl = {
            "Ą": "A",
            "Ć": "C",
            "Ę": "E",
            "Ł": "L",
            "Ń": "N",
            "Ó": "O",
            "Ś": "S",
            "Ź": "Z",
            "Ż": "Z",
        }

    def text_to_emojis( self, text: str ):
        text = text.upper()
        text = "".join( [ self.pl.get( x, x ) for x in text ] )          # replace polish characters
        text = "".join( [ x for x in text if x in self.l_to_e.keys() ] ) # remove any characters we dont have emojis for

        out = []
        
        while text:
            r = 1 # number of chars consumed (for combos)
            
            for i in [ 3, 2, 1 ]:
                s = self.l_to_e.get( text[:i], () )
                e = next( (x for x in s if x not in out), None ) # get first element of tuple that isnt in out, None if all already are
                if e:
                    r = i
                    break

            if not e:
                return []

            out.append( e )
            if len( out ) > 20:
                return []
            
            text = text[r:]

        return out

    @command(
        name = 'react'
    )
    async def _react( self, ctx: Context, *, text: str ): # good luck using slash commands
        if not ctx.message.reference:
            return
        
        tid = ctx.message.reference.message_id
        await ctx.message.delete()
        target = await ctx.channel.fetch_message( tid )
        
        out = self.text_to_emojis( text )
        if not out:
            return

        await target.clear_reactions()

        for x in out:
            await target.add_reaction( x )

def setup( bot: Bot ):
    bot.add_cog( React( bot ) )
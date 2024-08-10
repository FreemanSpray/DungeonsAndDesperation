### GLOBAL: IMPORTS ###

from tkinter import *
from tkinter import ttk
import random as rng
import sys
from PIL import Image, ImageTk
from statistics import mean
from functools import partial

### GLOBAL: REF TABLE ###

g_characters = [{'id':0, 'name':'Reika of the Thousand Days', 'shortName':'Reika', 'color':'goldenrod4', 'portrait':'GenPortrait.png', 'ingenuity':2, 'resolve':3, 'finesse':1, 'passive':'Undertow', 'active':'Anchor', 'passiveDescription':'At end of turn, if Reika has passed action and another player is able to act, she returns to play.', 'activeDescription':'Regain a use of one of the following actions that you have already taken in this room: Attack, Rest, or any room actions that have not yet been succeeded.',
    'revealQuips':['Tomorrow starts now, and you are not welcome there.', 'A million years could not keep me from her.', 'A second chance is not a gift. It is a call to arms.', 'Short-sighted fools. Stand at attention; the future is calling our names.', 'It is not our time.', 'Hush now. It is almost over.']}, 
    {'id':1, 'name':'Endemene Silverblood', 'shortName':'Endemene', 'color':'firebrick4', 'portrait':'GenPortrait.png', 'ingenuity':3, 'resolve':1, 'finesse':2, 'passive':'Inspiration', 'active':'Prototype', 'passiveDescription':'Endemene becomes inspired under various conditions, allowing for the prototyping of inventions which act as permanent buffs to her character.', 'activeDescription':'Prototype an invention.',
    'revealQuips':['Lol. Lmao.', 'WHERE\'S MY WIFE?', 'See you all sooner than you\'d like.', 'Cards on the table: I want you all on my payroll.', 'That got ugly. Let\'s try not to do that again, yeah?', 'I dislike killing probably almost as much as you all dislike dying, so let\'s get this over with quickly.']},
    {'id':2, 'name':'Rainee Haraldsson', 'shortName':'Rainee', 'color':'DeepSkyBlue4', 'portrait':'GenPortrait.png', 'ingenuity':3, 'resolve':2, 'finesse':1, 'passive':'Unraveling Threads', 'active':'Interrogate', 'passiveDescription':'Whenever Rainee Haraldsson rests, learn the identity of a random role that is not actively in play and that has not already been learned.', 'activeDescription':'Attempt to guess a chosen player\'s role. If correct, their role is revealed.',
    'revealQuips':['It is a heavy heart that draws a blade in anger. It is a heavier one that sheaths it in fear. I am not afraid.', 'Would but that I were the oceans, that I might feel your pull more often.', 'I am prepared to die for the cause. All the same, I would much prefer to live for it.', 'I beg you all, consider: what can I do for you?', 'Chin up, comrades. The rest of us may make it through this yet.', 'If I am to be destiny\'s fool, then so be it. We all must make sacrifices sometimes. Let mine be all of you.']},
    {'id':3, 'name':'Elvy, the Heart-Hammerer', 'shortName':'Elvy',  'color':'orchid4', 'portrait':'GenPortrait.png', 'ingenuity':2, 'resolve':1, 'finesse':3, 'passive':'Ward', 'active':'Guard', 'passiveDescription':'As long as Elvy has not attacked, defended, or been attacked, disregard all instructions to reveal their role.', 'activeDescription':'Defend against all attacks.',
    'revealQuips':['Smile, knave. Or dost thou not desire to look thy best for thine open casket?', 'Fair lady, there can be not a light as soft and soothing as thine own.', 'Thou knowest not what thee would do in mine absence. I shall be compelled to return.', 'Thoust owe more to me and mine than thee could ever hope to pay. Be still.', 'Drink, take succhor, be merry my wild ones. Greater challenges still await.', 'Take in all of myself thou are able to. This beauty shall be thy doom.']},
    {'id':4, 'name':'Dredge', 'shortName':'Dredge', 'color':'DarkOliveGreen4', 'portrait':'GenPortrait.png', 'ingenuity':1, 'resolve':3, 'finesse':2, 'passive':'From Below', 'active':'Scout', 'passiveDescription':'Whenever Dredge rests, a random item will find its way to him, to be discovered on waking.', 'activeDescription':'Learn the identity of the next room the party will encounter.',
    'revealQuips':['The time is long past for you to have found redemption. I suggest you look for it in the ground.', 'It is a lonely night, when even the moon must hide. Onto better days and better skies.', 'Life will never taste as sweet as in the moment it is taken from you.', 'Words are fickle things, but in this matter, I am confident they will suffice.', 'The world will still honor your passing millenia after your name is forgotten.', 'Forgive me, everyone, but such is the way of all things.']},
    {'id':5, 'name':'Mantelesse the Far-Dreaming', 'shortName':'Mantelesse', 'color':'RoyalBlue4', 'portrait':'GenPortrait.png', 'ingenuity':1, 'resolve':2, 'finesse':3, 'passive':'Together As One', 'active':'Weird', 'passiveDescription':'Whenever all players in play take the same action, as long as at least two players are able to act, each of those players gain a benefit depending on the action taken.', 'activeDescription':'Nullify the result of the action taken by a chosen player.',
    'revealQuips':['Checkmate, friend.', 'Auspicious timing, love.', 'Death is a stranger and I am far too prickly to make its aquaintance.', 'There is a greater enemy than any one of us lurking out there beyond the veil of the horizon. Don\'t be reckless.', 'We forget about this and carry on. Anything else would be stupid.', 'The beast stirs. Time at last to see what we all are made of.']}]
g_roles = [{'id':0, 'name':'Mnanth, Whose Heart is Glass', 'shortName':'Mnanth', 'color':'goldenrod2', 'reveal':'Bar the Way', 'winCondition':'Vengeance', 'revealDescription':'Whenever you and your pact target are the only players able to act, reveal Mnanth. When you do, the current room gains \'players may not pass action unless they are the only player in the room.\'', 'winConDescription':'When Mnanth becomes your role, a player at random is secretly chosen to be your pact target and you are informed as to what role this player has. You win if you escape and your pact target does not.'}, 
    {'id':1, 'name':'Casglowve, the Captive Moon', 'shortName':'Casglowve', 'color':'firebrick2', 'reveal':'Absolve the Selfish', 'winCondition':'Freedom', 'revealDescription':'Whenever you reach exhaustion level 3, reveal Casglowve. When you do, you immediately pass action and gain the benefit of a rest, ignoring all restrictions. Then, all other players immediately gain a level of exhaustion.', 'winConDescription':'You win if you escape after having Broken the Tower.'},
    {'id':2, 'name':'Cloudblessed', 'shortName':'Cloudblessed', 'color':'DeepSkyBlue2', 'reveal':'Defy the Deathwisher', 'winCondition':'The Bare Minimum', 'revealDescription':'Whenever you are killed by another player, reveal Cloudblessed. The current room gains \'when the last player passes action, return all dead players to play.\'', 'winConDescription':'You win if at least half the total players (rounded up) escape.'},
    {'id':3, 'name':'Marloe, Don of the Downtrodden', 'shortName':'Marloe', 'color':'orchid2', 'reveal':'Call Upon the Family', 'winCondition':'Unconditional Loyalty', 'revealDescription':'While there is another player able to act, you may reveal Marloe as an action. When you do, defend all players against all attacks made this turn. Each player successfully defended this way receives a curse.', 'winConDescription':'You win if you escape and no other player escapes that does not have a curse.'},
    {'id':4, 'name':'Erstwhile, Collector Supreme', 'shortName':'Erstwhile', 'color':'DarkOliveGreen2', 'reveal':'Waste Not the Forgotten', 'winCondition':'Eye for the Unknown', 'revealDescription':'Whenever another player dies, reveal Erstwhile. When you do, each other player receives the benefit of a rest.', 'winConDescription':'You win if you visit every room.'},
    {'id':5, 'name':'The Fisherwoman', 'shortName':'Fisherwoman', 'color':'RoyalBlue2', 'reveal':'Drop the Avalanche', 'winCondition':'Defense of the Heart', 'revealDescription':'Whenever you take the attack action, reveal The Fisherwoman. When you do, each other player skips their next turn and you may take the attack action once more in the current room.', 'winConDescription':'You win if you see the Wandering Heart and no other player escapes that has done so.'}]
g_rooms = [{'id':0, 'name':'The Scrap-Iron Arena', 'actions':['Plumb the Wreckage','Free the Blade','Take the High Ground'], 'requirements':[5,7,3], 'description':'The scent of iron rises like a haze off the arena, which from the stands resembles the most dangerous jungle-gym imaginable. At the center of the mess of scrap stands a single clear dais of stone within which an old competitor\'s wicked blade has long been buried. Many have tried to free it from its place there. Will you try your hand? Or will you scavenge amidst the script for meager resources, or fight your way to the high ground on the edge of the valley of scrap?'}, 
    {'id':1, 'name':'The Tower', 'actions':['Break the Magic','Interrogate the Mirror','Spring the Vaults'], 'requirements':[7,3,5], 'description':'The black tower reaches up like a jagged bolt of lightning to touch the sky. Within its many levels, countless oddities and dangers await, most of them indecipherable even to the greatest scientific and arcane thinkers of the modern age. The tower is watched over ground-to-roof by a wall-length, multi-level mirror that is home to an entity of a particularly wrathful disposition. Will you find a way to break the tower before it breaks you? Or are you better served appeasing the mirror entity or looting what you can from under its proverbial nose?'},
    {'id':2, 'name':'Longway Alley', 'actions':['Follow the Twine','Confront the Beast','Loot the Storefronts'], 'requirements':[7,5,3], 'description':'Longway Alley is a place that defies description. It is to most only as material as a dream, the feeling of cold cobblestones underfoot, the light mist hanging deceptively thick in the air, the sound of too-heavy footsteps thudding somewhere far off, but maybe only as little as a block away. Yet not all who have wandered into the depths of the alley are lost, as evidenced by the silver twine that crops up everywhere, crisscrossing itself two or three times in certain junctions. Will you attempt to trace this twine to its origin, rather than follow the route laid out for you? Or would you rather take your chances with the beast that stalks the haze along with you, or spend your time searching the storefronts that populate the alley for useful materials?'},
    {'id':3, 'name':'The Hall of the Mirthless Queen', 'actions':['Answer the Riddle','Sit at the Table','Raid the Kitchen'], 'requirements':[5,3,7], 'description':'Cobwebs dust every surface in the great hall. Bricks are cracked, the floorboards rotten and splintered. Yet, for all the countless many years this place has lain empty, the table is still set. The hearth is still flickering. And a heavenly smell still wafts from the kitchen. looking out over the great table is a portrait of the woman who once presided over this hall. Her stern face asks a question mirrored in the riddle scrawled below her visage. Will you attempt to answer this riddle? Or will you venture into the kitchen to see what\'s cooking, or better yet, sit at the table and wait to be served?'},
    {'id':4, 'name':'Death\'s Cradle', 'actions':['Analyze the Music','Wish at the Well','Forage in the Marshland'], 'requirements':[3,7,5], 'description':'Within a cradle of rot, mildew, and fungal growth, an oasis of a kind sits largely untouched. Pale flowers spread wisplike petals. A wind that is not wind blows through trees with leaves like windchimes. Leaves curl gently to hide the curve of a stepping-stone path. A wishing well stands upon a hill, the glint of spent coins shining in the light of a bioluminescent sun. Will you cast your own wish in the waters of life and death? Or will you find a way to live off the surrounding marshland in its alien beauty, or seek answers in the song of the wind through the trees?'},
    {'id':5, 'name':'The Icy Cove', 'actions':['Interpret the Sigils','Navigate the Ice','Search for Shelter'], 'requirements':[3,5,7], 'description':'The cove stands tall against time, a thousand days and nights of cold winds weathered by the unflinching rock of its walls. The ocean that sits beside it did not fare as well. The water lies frozen, still as the bodies it used to wash ashore. Little remains to explain the frozen bodies, save for a series of pillars carved with strange and unsettling sigils. A keen eye, however, might notice that there is a faint light glowing underneath the surface of the ice, way out past the safety of the once-shoreline. Will you go to this light? Or would your time be better spent studying the symbols marking the pillars, or seeking out shelter from the cold along the side of the cove?'}]
g_game = 0

### GLOBAL: CLASS GAME ###

class Game:
    def __init__(self, mode):
        # Load global vars
        global g_rooms
        global g_characters
        global g_roles
        # Create list of shuffled rooms
        self.shuffledRooms = rng.sample(g_rooms, 6)
        # Initialize other room vars
        self.roomIndex = 0
        self.location = None
        # Initialize random seed
        rng.seed()
        # Generate random samples for character and role assignment
        randCharacters = rng.sample(g_characters, 4)
        randRoles = rng.sample(g_roles, 4)
        # Initialize player and AI (collectively 'players')
        player1 = Player(randCharacters[0], randRoles[0], mode, mode) # Player1 will be an AI or a player depending on the mode (0 = AI for TEST, 1 = player for DEFAULT)
        player2 = Player(randCharacters[1], randRoles[1], 2, mode)
        player3 = Player(randCharacters[2], randRoles[2], 3, mode)
        player4 = Player(randCharacters[3], randRoles[3], 4, mode)
        # Add player to conveniently accessible variable if there is a player
        if mode == 1:
            self.player = player1
        # Otherwise assign player to None so references to it can be checked for and avoided
        else:
            self.player = None
        # Add all players to conveniently accessible variable
        self.allPlayers = [player1, player2, player3, player4]
        # Initialize stack
        self.eventStack = []
        # Initialize action-tracking vars
        self.investigateTotal = 0
        self.exertTotal = 0
        self.exploreTotal = 0
        self.actions = []
        self.attackTargets = []
        self.attackSources = []
        self.restTargets = []
        self.passingPlayers = []
        self.guardSources = [] # for Elvy's use only
        self.guardTargets = [] # for Elvy's use only
        # Initialize other game vars
        self.partySupplies = 4
        self.randomID = None
        self.isTowerBroken = False
        self.isKeyFound = False
        self.isSwordDrawn = False
        self.isSheltered = False
        self.isCluedIn = False
        self.isWayBarred = False
        self.marloeRevealedThisTurn = False
        # Initialize testing vars
        self.timesAggroed = 0
        # Initialize GUI handling vars
        self.isEventHandling = False
        self.isWaiting = False
        self.isGame = True
        # Initialize GUI vars
        self.root = None
        self.inputFrame = None
        self.textFrame = None
        self.textIndex = 0
        self.portraitFrame = None
        self.portraits = []
    # END __INIT__

    ### GAME: DISPLAY ###

    """
    pre: called at the beginning of the game
    return: root window, input frame, text display frame, and portrait display frame are constructed. Portraits are displayed
    """
    def buildGUI(self):
        # Build root
        self.root = Tk()
        # Size root window
        self.root.geometry('1920x1080')
        # Build input frame
        self.inputFrame = ttk.Frame(self.root, padding=10)
        self.inputFrame.pack(side=LEFT, fill=Y)
        # Build text frame
        self.textFrame = ttk.Frame(self.root, padding=10)
        self.textFrame.pack(side=LEFT, fill=BOTH, expand=True)
        # Add scrollbar to text frame
        textScroll = Scrollbar(self.textFrame)
        textScroll.pack(side=RIGHT, fill=Y)
        # Add textbox to text frame
        textBox = Text(self.textFrame, yscrollcommand=textScroll.set, wrap=WORD)
        textBox.pack(side=LEFT, fill=BOTH, expand=True)
        # Rig scrollbar to scroll listbox
        textScroll.config(command=textBox.yview)
        # Load color information in globals
        global g_characters
        global g_roles
        # Configure text colors
        for c in g_characters:
            textBox.tag_configure(tagName=c['shortName'], foreground=c['color'])
        for r in g_roles:
            textBox.tag_configure(tagName=r['shortName'], background=r['color'])
        # Build portrait frame
        self.portraitFrame = ttk.Frame(self.root, padding=10)
        self.portraitFrame.pack(side=LEFT, fill=Y)
        # Load portraits
        self.loadPortraits()
    # END BUILDGUI

    """
    pre: called when PC action input is requested
    return: begins main loop if it has not already begun.
    """
    def beginEventHandling(self):
        # Only enter event loop if loop has not already been entered and if there is a player. Otherwise, AI can make do with command line
        if not self.isEventHandling and self.player:
            self.isEventHandling = True
            self.root.mainloop()
    # END BEGINEVENTHANDLING

    """
    pre: called when GUI is being built
    return: portraits of all player characters in play are loaded and displayed
    """
    def loadPortraits(self):
        for i in range(len(self.allPlayers)):
            # Read portrait image corresponding to character
            image = Image.open('assets\\' + self.allPlayers[i].character['portrait'])
            portrait = ImageTk.PhotoImage(image)
            # Create and package label containing image
            ttk.Label(self.portraitFrame, image=portrait).grid(row=i, column=0)
            # Store image in a var so it doesn't get destroyed when it leaves scope
            self.portraits.append(portrait)
    # END LOADPORTRAITS

    """
    pre: should be called only when a player dies or escapes to indicate they are no longer in play.
    param: playerID: the ID of the player to have their portrait updated
    post: portrait of player with ID param:playerID is grayed out.
    """
    def dyePortrait(self, playerID):
        for i in range(len(self.allPlayers)):
            if self.allPlayers[i].id == playerID:
               # Read portrait image corresponding to character
                image = Image.open('assets\\' + self.allPlayers[i].character['portrait'])
                # Convert to grayscale
                image = image.convert('L')
                portrait = ImageTk.PhotoImage(image)
                # Create and package label containing image
                ttk.Label(self.portraitFrame, image=portrait).grid(row=i, column=0) 
                # Replace previous portrait with dyed one
                self.portraits[i] = portrait
                # Break
                return
    # END DYEPORTRAIT

    """
    param: output, string containing references to characters and roles only as shortnames
    param: shouldOverride: bool indicating whether param:output should be displayed regardless of whether there is a PC in play. Default: False
    post: param:output is formatted, styled, and displayed.
    """
    def displayText(self, output, shouldOverride=False):
        # Use GUI only if there is a player
        if self.player:
            # Display only if player is alive and not escaped or if it is a game over print
            if self.player.isInDungeon() or shouldOverride:
                # Extract textBox from textFrame
                textBox = self.textFrame.winfo_children()[1]
                # Insert message into textBox
                textBox.insert(INSERT, output + '\n')
                # Apply colors
                for c in g_characters:
                    self.colorText(c['shortName'], c['shortName'])
                for r in g_roles:
                    self.colorText(r['shortName'], r['shortName'])
            # Otherwise print like normal
            else:
                print(output)
        # Otherwise print like normal
        else:
            print(output)
    # END DISPLAYTEXT

    """
    param: pattern, string indicating what term is to have the color applied to
    param: tag, string indicating what color should be applied, based on tag configuration of the text frame
    post: param: all text matching param:pattern has a color applied according to param:tag.
    ref: https://mathcodelife.com/creating-a-chat-log-for-a-game-using-tkinter-in-python/
    """
    def colorText(self, pattern, tag):
        # Extract important variables from textFrame and textBox
        textBox = self.textFrame.winfo_children()[1]
        start = textBox.index('1.0')
        end = textBox.index('end') 
        # Define search parameters
        textBox.mark_set('matchStart', start)
        textBox.mark_set('matchEnd', start)
        textBox.mark_set('searchLimit', end)
        # Initialize intvar
        count = IntVar()
        # Look for patterns until all have been found
        while True:
            # Find location of next pattern in textBox
            index = textBox.search(pattern, "matchEnd", "searchLimit", count=count)
            # Break if pattern is not found
            if index == "":
                break
            # Break if message had length 0
            if count.get() == 0:
                break
            # Add tag to found pattern
            textBox.mark_set("matchStart", index)
            textBox.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            textBox.tag_add(tag, "matchStart", "matchEnd")
    
    ### GAME: HELPERS ###

    """
    param: targetID, string matching a player ID
    return: Player with id param:targetID.
    """
    def lookupPlayerByID(self, targetID) -> object:
        # Look up player from list of all players
        for p in self.allPlayers:
            if p.id == targetID:
                return p
    # END LOOKUPPLAYERBYID

    """
    param: targetRole, string matching a role shortname
    return: Player with shortname param:targetRole.
    """
    def lookupPlayerByRole(self, targetRole) -> object:
        # Look up player from list of all players
        for p in self.allPlayers:
            if p.role['shortName'] == targetRole:
                return p
        # Return error if no player has the role
        return None
    # END LOOKUPPLAYERBYROLE

    """
    param: targetCharacter, string matching a character shortname
    return: Player with shortname param:targetCharacter.
    """
    def lookupPlayerByCharacter(self, targetCharacter) -> object:
        # Look up player from list of all players
        for p in self.allPlayers:
            if p.character['shortName'] == targetCharacter:
                return p
        # Return error if no player has the role
        return None
    # END LOOKUPPLAYERBYCHARACTER

    """
    return: list of all players able to act.
    """
    def getActionablePlayers(self) -> list:
        return list(filter(lambda p: p.isAbleToAct(), self.allPlayers))
    # END GETACTIONABLEPLAYERS

    """
    param: source, the player of interest
    return: list of all players able to act who are not param:source.
    """
    def getOtherActionablePlayers(self, source):
        return list(filter(lambda p: p.isAbleToAct(), source.getOtherPlayers()))
    # END GETOTHERACTIONABLEPLAYERS

    """
    return: list of all players in the dungeon.
    """
    def getPresentPlayers(self) -> list:
        return list(filter(lambda p: p.isInDungeon(), self.allPlayers))
    # END GETPRESENTPLAYERS

    ### GAME: INPUT VISUALS ###

    """
    pre: called when input is requested of the PC deciding on an action.
    post: Constructs input options in input frame.
    """
    def setActionInput(self, options):
        # Loop through options, creating a button for each one at the root
        for i in range(len(options)):
            opt = options[i]
            # Initialize display to be same as opt
            display = opt
            # Adjust display for actions with non-specific names
            if display == 'Investigate':
                display = self.location.room['actions'][0]
            elif display == 'Exert':
                display = self.location.room['actions'][1]
            elif display == 'Explore':
                display = self.location.room['actions'][2]
            elif display == 'Special Active':
                display = self.player.character['active']
            elif display == 'Reveal Active':
                display = self.player.role['reveal']
            # Construct command for call on button press
            loadedCommand = partial(self.getPlayerAction, opt)
            # Create button
            ttk.Button(self.inputFrame, text=display, command=loadedCommand).pack(side=TOP, fill=X)
    # END SETACTIONINPUT

    """
    pre: called when input is requested of the PC taking an action that requires a player target.
    post: Constructs input options in input frame.
    """
    def setOtherActivePlayerInput(self):
        # Loop through active players other than source (PC), creating a button for each one at the root
        otherActivePlayers = self.getOtherActionablePlayers(self.player)
        for i in range(len(otherActivePlayers)):
            opt = otherActivePlayers[i]
            # Set display to be character name of player
            display = opt.character['shortName']
            # Construct command for call on button press
            loadedCommand = partial(self.getPlayerTarget, opt)
            # Create button
            ttk.Button(self.inputFrame, text=display, command=loadedCommand).pack(side=TOP, fill=X)
    # END SETOTHERPLAYERACTIVEINPUT

    """
    pre: called when input is requested of the PC with the character Endemene for their prototype action.
    post: Constructs input options in input frame.
    """
    def setPrototypeInput(self):
        # Loop through source (PC)'s inspiration, creating a button for each one at the root
        inspiration = self.player.inspiration()
        for i in range(len(inspiration)):
            opt = inspiration[i]
            # Construct command for call on button press
            loadedCommand = partial(self.getPlayerTarget, opt)
            # Create button
            ttk.Button(self.inputFrame, text=opt, command=loadedCommand).pack(side=TOP, fill=X)
    # END SETOTHERPLAYERACTIVEINPUT

    """
    pre: called when input is requested of the PC with the character Rainee for their guess while interrogating another player.
    param: options: the list of roles player has not guessed for the param:target.
    param: target, player selected as a target for the interrogate action that prompted the guess
    post: Constructs input options in input frame.
    """
    def setGuessInput(self, options, target):
        # Loop through options, creating a button for each one at the root
        for i in range(len(options)):
            opt = options[i]
            # Load command to finish role guessing process
            loadedCommand = partial(self.getPlayerGuess, opt, target)
            ttk.Button(self.inputFrame, text=opt, command=loadedCommand).pack(side=TOP, fill=X)
    # END SETGUESSINPUT

    """
    pre: called when PC input is requested for a yes or no option.
    param: command: method to be called when input is received.
    post: Constructs input options in input frame.
    """
    def setYNInput(self, command):
        # Load commands
        loadedCommandY = partial(command, True)
        loadedCommandN = partial(command, False)
        # Construct buttons 
        ttk.Button(self.inputFrame, text='Y', command=loadedCommandY).pack(side=TOP, fill=X)
        ttk.Button(self.inputFrame, text='N', command=loadedCommandN).pack(side=TOP, fill=X)
    # END SETYNINPUT

    """
    pre: called when PC input is requested for the Wish at the Well room action.
    param: numVotes, list indicating the number of votes each of the five options received.
    param: playerVotes, list indicating what each player voted for.
    post: Constructs input options in input frame.
    """
    def setVoteInput(self, numVotes, playerVotes):
        # Load commands
        loadedCommand1 = partial(self.getPlayerVote, 1, numVotes, playerVotes)
        loadedCommand2 = partial(self.getPlayerVote, 2, numVotes, playerVotes)
        loadedCommand3 = partial(self.getPlayerVote, 3, numVotes, playerVotes)
        loadedCommand4 = partial(self.getPlayerVote, 4, numVotes, playerVotes)
        loadedCommand5 = partial(self.getPlayerVote, 5, numVotes, playerVotes)
        # Construct buttons 
        ttk.Button(self.inputFrame, text='Wellness', command=loadedCommand1).pack(side=TOP, fill=X)
        ttk.Button(self.inputFrame, text='Freedom', command=loadedCommand2).pack(side=TOP, fill=X)
        ttk.Button(self.inputFrame, text='Knowledge', command=loadedCommand3).pack(side=TOP, fill=X)
        ttk.Button(self.inputFrame, text='Resources', command=loadedCommand4).pack(side=TOP, fill=X)
        ttk.Button(self.inputFrame, text='Doom', command=loadedCommand5).pack(side=TOP, fill=X)
    # END SETVOTEINPUT

    """
    pre: called whenever input is provided.
    post: Input frame is cleared to make way for next input selection.
    """
    def clearPlayerInput(self):
        # Clear frame
        self.clearFrame(self.inputFrame)
    # END CLEARPLAYERINPUT

    """
    pre: called by method:clearPlayerInput.
    param: frame, GUI frame to be cleared
    post: Frame is cleared of all widgets.
    """
    def clearFrame(self, frame):
        # Destroy all widgets in frame
        for widget in frame.winfo_children():
            # Destroy widget
            widget.destroy()
    # END CLEARFRAME

    ### GAME: INPUT HANDLING ###

    """
    pre: called when PC provides input for a choice of action.
    param: action, string selected as an action
    post: Action object is created, then follow-up input (target, or chosen anchored action for Anchor action) is requested, or if there is no necessary follow-up input then advance the stack.
    """
    def getPlayerAction(self, action):
        # Clear player input
        self.clearPlayerInput()
        # Construct action object corresponding to chosen action (without a target) and add to list
        self.actions.append(Action(action, self.player, None))
        # If action is one that targets a player, display options in GUI for player to select
        if action == 'Attack' or (action == 'Special Active' and (self.player.character['id'] == 2 or self.player.character['id'] == 3 or self.player.character['id'] == 5)):
            self.setOtherActivePlayerInput()
        # If action is prototype, display options in GUI for player to select
        elif action == 'Special Active' and self.player.character['id'] == 1:
            self.setPrototypeInput()
        # If action is anchor, immediately take Anchor action, then reset player input
        elif action == 'Special Active' and self.player.character['id'] == 0:
            # Pop anchor action
            self.actions.pop(0)
            # Report anchor
            self.displayText('You anchored yourself.')
            # Mark special active as used
            self.player.hasUsedActive = True
            # Initialize options list
            options = []
            optionNum = 1
            # Determine which options are available to the player and print
            if g_game.player.hasAttacked and len(g_game.getOtherActionablePlayers(g_game.player)):
                options.append('Attack')
                optionNum += 1
            if g_game.player.hasRested and g_game.player.exhaustionLevel > 0:
                options.append('Rest')
                optionNum += 1
            if g_game.player.hasInvestigated and not g_game.location.hasBeenInvestigated:
                options.append('Investigate')
                # Calculate discount for if mirror was successfully interrogated
                discount = 0
                if g_game.isCluedIn:
                    discount = 2
                optionNum += 1
            if g_game.player.hasExerted and not g_game.location.hasBeenExerted:
                options.append('Exert')
                optionNum += 1
            if g_game.player.hasExplored and not g_game.location.hasBeenExplored:
                options.append('Explore')
                optionNum += 1
            options.append('Pass')
            # Display options in GUI for player to select
            self.setActionInput(options)
        # If there is no target, advance stack immediately
        else:
            self.advanceStack()
    # END GETPLAYERACTION

    """
    pre: called when PC provides input for the target of a chosen action.
    param: target, player selected as a target for the action
    post: Action object is updated to reflect the chosen target. Then advance the stack.
    """
    def getPlayerTarget(self, target):
        # Clear player input
        self.clearPlayerInput()
        # Update first action in list (the player's action) to have a target
        self.actions[0].target = target
        # Advance stack
        self.advanceStack()
    # END GETPLAYERTARGET

    """
    pre: called when PC with the character Rainee provides input for their guess while interrogating another player.
    param: guess, boolean indicating what role the Player guessed param:target has.
    param: target, player selected as a target for the interrogate action that prompted the guess
    post: PC is informed as to whether their guess was correct, role is marked as guessed so as not to show as an option for future guesses. Then process next action.
    """
    def getPlayerGuess(self, guess, target):
        # Clear player input
        self.clearPlayerInput()
        # Inform player of the result of their guess
        if guess == target.role['name']:
            self.displayText('Your hunch proved correct. ' + target.character['shortName'] + '\'s role is ' + target.role['shortName'] + '.')   
            # Add target to list of guessed roles.
            self.player.guessedPlayers.append(target.id)  
        else:
            self.displayText('Your hunch did not hold up. Still, you are closer now to unraveling the mystery that is ' + target.character['shortName'] + '.')
        # Release input lock
        self.isWaiting = False
        # Proceed to next action
        self.processAction()
    # END GETPLAYERGUESS

    """
    pre: called when PC provides input for the Break the Magic room action.
    param: choice, boolean indicating whether PC chose to remain or leave
    post: PC escapes if they chose to, then advance stack.
    """
    def getCasglowveOffer(self, choice):
        # Clear player input
        self.clearPlayerInput()
        # Player escapes if they chose to
        if choice:
            self.player.escape()
            self.displayText('You escaped from the dungeon.')
        else:
            self.displayText('You decline the offer, carrying on in your exhaustion.')
        # Advance stack
        self.advanceStack()
    # END GETCASGLOWVEOFFER

    """
    pre: called when PC provides input for the Wandering Heart's offer of freedom.
    param: choice, boolean indicating whether PC chose to remain or leave
    post: PC escapes if they chose to, then advance stack.
    """
    def getHeartOffer(self, choice):
        # Clear player input
        self.clearPlayerInput()
        # Player escapes if they chose to
        if choice:
            self.player.escape()
            self.displayText('You escaped from the dungeon.')
        else:
            self.displayText('You decline the offer, carrying on without the Heart\'s guidance.')
        # Release input lock
        self.isWaiting = False
        # Advance stack
        self.advanceStack()
    # END GETHEARTOFFER

    """
    pre: called when PC provides input for the Take the High Ground room action.
    param: choice, boolean indicating whether PC chose to remain or leave
    post: calls method:highGround
    """
    def getHighGroundOffer(self, choice):
        # Clear player input
        self.clearPlayerInput()
        # Report outcome
        if choice:
            self.displayText('You elected to remain behind.')
        else:
            self.displayText('You elected to leave.')
        # Continue to AI choices and results
        self.highGround(choice)
    # END GETHEARTOFFER

    """
    pre: called when PC provides input for the Wish at the Well room action.
    param: vote, str indicating which option the player voted for
    param: numVotes, list indicating the number of votes each of the five options received.
    param: playerVotes, list indicating what each player voted for.
    post: Updates param:numVotes and param:playerVotes with the PC's choice, then calls method:vote
    """
    def getPlayerVote(self, vote, numVotes, playerVotes):
        # Clear player input
        self.clearPlayerInput()
        # Count and report player vote
        match vote:
            case 1:
                numVotes[0] += 1
                self.displayText('You voted for Wellness.')
                playerVotes[0] = 'Wellness'
            case 2:
                numVotes[1] += 1
                self.displayText('You voted for Freedom.')
                playerVotes[0] = 'Freedom'
            case 3:
                numVotes[2] += 1
                self.displayText('You voted for Knowledge.')
                playerVotes[0] = 'Knowledge'
            case 4:
                numVotes[3] += 1
                self.displayText('You voted for Resources.')
                playerVotes[0] = 'Resources'
            case 5:
                numVotes[4] += 1
                self.displayText('You voted for Doom.')
                playerVotes[0] = 'Doom'
        # Continue to AI votes and results
        self.vote(numVotes, playerVotes)
    # END GETPLAYERVOTE

    ### GAME: INPUT RESULTS ###

    """
    pre: called after receiving PC input for the Wish at the Well room action, or immediately if there is no PC.
    param: numVotes, list indicating the number of votes each of the five options received.
    param: playerVotes, list indicating what each player voted for.
    post: Carries out results of vote, then advances stack.
    """
    def vote(self, numVotes, playerVotes):
        # get AI votes
        for p in self.getOtherActionablePlayers(self.player):
            if p.shouldAiEscape():
                numVotes[0] += 1
                playerVotes[p.id - 1] = 'Wellness'
            elif self.partySupplies < 4:
                numVotes[1] += 1
                playerVotes[p.id - 1] = 'Freedom'
            elif p.exhaustionLevel > 1:
                numVotes[3] += 1
                playerVotes[p.id - 1] = 'Resources'
            else:
                numVotes[2] += 1
                playerVotes[p.id - 1] = 'Knowledge'
        # Report results of vote
        if numVotes[0] > 0:
            if numVotes[1] == 0 and numVotes[2] == 0 and numVotes[3] == 0 and numVotes[4] == 0:
                self.displayText('A unanimous vote for Wellness was receved, so each player receives the benefit of a rest.')
                # Rest
                for p in self.allPlayers:
                    if p.isAbleToAct():
                        p.rest
            else:
                self.displayText('A player voted for wellness, so a random player receives the benefit of a rest.')
                # Choose a random player
                playersAbleToAct = []
                for p in self.allPlayers:
                    if p.isAbleToAct():
                        playersAbleToAct.append(p)
                randomPlayerIndex = rng.randint(0,len(playersAbleToAct)-1)
                randomPlayer = playersAbleToAct[randomPlayerIndex]
                # Player rests
                randomPlayer.rest()
        if numVotes[1] > 0:
            if numVotes[0] == 0 and numVotes[2] == 0 and numVotes[3] == 0 and numVotes[4] == 0:
                self.displayText('A unanimous vote for Freedom was receved, so each player may have their freedom from the dungeon.')
                # Each active player escapes
                for p in self.allPlayers:
                    if p.isAbleToAct():
                        p.escape()
                        # Report outcome
                        if p.isPlayer():
                            self.displayText('In a flash of shimmering lights accompanied by blustering winds, you are born somewhere far from here. You have escaped.')
                        else:
                            self.displayText('In a flash of shimmering lights accompanied by blustering winds, ' + p.character['shortName'] + ' vanishes. They have escaped.')
            else:
                self.displayText('A player voted for Freedom, but a non-unanimous vote for Freedom is about as helpful as you might expect. Better luck next time.')
        if numVotes[2] > 0:
            if numVotes[0] == 0 and numVotes[1] == 0 and numVotes[3] == 0 and numVotes[4] == 0:
                self.displayText('A unanimous vote for Knowledge was receved, so know this: there is no hope for you.')
            else:
                self.displayText('A player voted for Knowledge, but the vote was non-unanimous. Why don\'t I share with them what everyone else voted for?')
                for i in range(len(playerVotes)):
                    vote = playerVotes[i]
                    if vote != None:
                        self.displayText(self.allPlayers[i].character['shortName'] + ' voted for ' + vote + '.')
        if numVotes[3] > 0:
            if numVotes[0] == 0 and numVotes[1] == 0 and numVotes[2] == 0 and numVotes[4] == 0:
                self.displayText('A unanimous vote for Resources was receved, so the party gains 4 supplies.')
                # Add 6 supplies
                self.partySupplies += 4
            else:
                self.displayText('One or more players voted for Resources, so you gain 2 supplies.')
                # Add x supplies
                self.partySupplies += 2
        if numVotes[4] > 0:
            if numVotes[0] == 0 and numVotes[1] == 0 and numVotes[2] == 0 and numVotes[3] == 0:
                self.displayText('A unanimous vote for Doom was received, so all players immediately die.')
                # All active players die
                for p in self.allPlayers:
                    if p.isAbleToAct():
                        p.die()
            else:
                self.displayText('A vote for doom was received, so a random player will die. Such is the cost of such nonsense.')
                # Choose a random player
                playersAbleToAct = []
                for p in self.allPlayers:
                    if p.isAbleToAct():
                        playersAbleToAct.append(p)
                randomPlayerIndex = rng.randint(0,len(playersAbleToAct)-1)
                randomPlayer = playersAbleToAct[randomPlayerIndex]
                # Player dies
                randomPlayer.die()
                self.displayText(randomPlayer.character['shortName'] + ' dropped dead on the spot.')
        # Advance stack
        self.advanceStack()
    # END VOTE

    """
    pre: called after receiving PC input for the Take the High Ground room action, or immediately if there is no PC.
    param: playerChoice, True if the PC chose to remain or False otherwise.
    post: Passes all players that chose to leave as long as at least one chose to stay, then advances stack.
    """
    def highGround(self, playerChoice):
        # Initializing choice lists
        remainingPlayers = []
        leavingPlayers = []
        # Register player choice (False by default)
        if playerChoice:
            remainingPlayers.append(self.player)
        else:
            leavingPlayers.append(self.player)  
        # Get AI choices
        for p in self.getOtherActionablePlayers(self.player):
                if p.role['name'] == 'Cloudblessed':
                    remainingPlayers.append(p)
                else:
                    leavingPlayers.append(p)
        # Determine result
        if len(remainingPlayers) > 0:
            self.displayText('One or more players elected to stay behind. With their help, the following players were able to pass to the next room:')
            # Each leaving player passes
            for p in leavingPlayers:
                p.hasPassed = True
                # Report passed player
                self.displayText(p.character['shortName'])
        else:
            # Report failure of anyone to pass
            self.displayText('No players elected to stay behind, and so all have no choice but to do so.')
        # Advance stack
        self.advanceStack()
    # END HIGHGROUND

    ### GAME: EXECUTIVE ###

    """
    pre: called from main.
    post: constructs the GUI, prints initial info for the PC, advances to the first room.
    """
    def play(self):
        # Build GUI
        self.buildGUI()
        if self.player:
            # print relevant character, role, and ai data
            self.displayText('Welcome, player. Your character is ...')
            self.player.printCharacterInfo()
            self.displayText('Your role is ...')
            self.player.printRoleInfo()
            self.displayText('In the party with you are:')
            for p in self.player.getOtherPlayers():
                self.displayText(p.character['shortName'])
        # Advance to first room
        self.advanceRoom()
    # END PLAY

    """
    pre: called at the beginning of a game and each time the room would change.
    post: ends game if no players remain or no rooms remain. Otherwise updates the room, calls enterRoom on each player in play, then starts the first turn in the room.
    """
    def advanceRoom(self):
        # If all players are dead or escaped, end game
        if len(self.getPresentPlayers()) == None:
            self.displayText('No players remain in the dungeon. Game Over.')
            # Display winners and losers
            _ = [p.checkWinConditions() for p in self.allPlayers]
            # Stop game
            self.isGame = False
        # If all rooms have been cleared, check for key, then end game
        elif self.roomIndex == 6:
            if self.isKeyFound:
                self.displayText('Beyond the dungeon\'s final room you are met only with a wall of stone. Set into the base of this wall is a tiny hatch, openable with the key you have found. Engravings on the wall however reveal that this hatch will only admit one player through before it locks again forever.')
                # Find most exhausted player from among those still alive and not escaped
                randomPlayer = getLeastExhaustedPlayer(self.getPresentPlayers())
                # Player escapes
                randomPlayer.escape()
                # Report outcome
                if randomPlayer.isPlayer():
                    self.displayText('As one of the most alert players still standing, you act quickly, seizing the key, unlocking the hatch, and diving in before anyone else. You hear the hatch click shut behind you, muffling the outraged cries of your companions. You have escaped.')
                else:
                    self.displayText('As one of the most alert players still standing, ' + randomPlayer.character['shortName'] +' acts quickly, seizing the key, unlocking the hatch, and diving in before anyone else. They have escaped, leaving the rest of you to your fates.')
                self.displayText('Game Over.')
            # If key was not found, move straight to game over
            else:
                self.displayText('Beyond the dungeon\'s final room you are met only with a wall of stone. Set into the base of this wall is a tiny hatch, but it is locked, impassible to all. This is your final step in the dungeon. Game Over.')
            # Display winners and losers
            _ = [p.checkWinConditions() for p in self.allPlayers]
            # Stop game
            self.isGame = False
        # Stop playing if the game should be over
        if self.isGame:
            # Enter next room corresponding to room index
            self.location = Location(self.shuffledRooms[self.roomIndex])
            # Increment room index
            self.roomIndex += 1
            # Output room entry message
            self.displayText('Your party enters ' + self.location.room['name'] + '.')
            self.displayText(self.location.room['description'])
            # Reset room-dependent stats for players that are still alive and not escaped
            _ = [q.enterRoom() for q in self.getPresentPlayers()]
            # End Bar the Way effect if it was active
            self.isWayBarred = False
            # Take turn
            self.startTurn()
    # END ADVANCEROOM

    """
    pre: called at the beginning of each turn cycle
    post: calls undertow as needed, triggers reveal on Mnanth, then if no players are able to act, advances to the next room. Otherwise, constructs the event stack for the turn, 
        initializes list for action phase, determines a random player to have their actions randomized if in Alley, then presents action options to PC. 
        Begins display input loop if it is the first turn of the game.
    """
    def startTurn(self):
        # Take turn only if there is a player able to act
        #print(list(map(lambda p: p.character['name'], self.getActionablePlayers()))) # DEBUG PRINT
        if len(self.getActionablePlayers()) > 0:
            # If Reika is in the game and has passed, return her to play
            reikaPlayer = self.lookupPlayerByCharacter('Reika')
            if reikaPlayer:
                if reikaPlayer.hasPassed:
                    reikaPlayer.undertow()
            # If only a player with Mnanth as their role and that player's (revealed) pact target are able to act, trigger Mnanth reveal
            actionablePlayers = self.getActionablePlayers()
            mnanthPlayer = self.lookupPlayerByRole('Mnanth')
            if mnanthPlayer:
                pactTargetID = mnanthPlayer.pactTargetID
                if len(actionablePlayers) == 2:
                    if actionablePlayers[0].id == pactTargetID and actionablePlayers[0].isRevealed:
                        actionablePlayers[1].triggerReveal('Mnanth, Whose Heart is Glass')
                    elif actionablePlayers[1].id == pactTargetID and actionablePlayers[1].isRevealed:
                        actionablePlayers[0].triggerReveal('Mnanth, Whose Heart is Glass')
            # Re-initialize stack
            self.eventStack = []
            # Build stack in reverse order
            self.eventStack.append(self.endTurn)
            self.eventStack.append(self.restResults)
            self.eventStack.append(self.attackResults)
            self.eventStack.append(self.exploreResults)
            self.eventStack.append(self.exertResults)
            self.eventStack.append(self.investigateResults)
            self.eventStack.append(self.actionPhase)
            # Re-initialize actions
            self.actions = []
            # If in the alley, choose a random player from among the active players each turn to have to carry out a random action
            if self.location.room['id'] == 2:
                self.randomID = rng.sample(list(map(lambda p: p.id, self.getActionablePlayers())), 1)[0]
            # If player is able to act and is not stunned, provide a choice of actions
            if self.player.isAbleToAct() and not self.player.isStunned:
                # Initialize options list
                options = []
                optionNum = 1
                # Determine which options are available to the player
                if not self.player.hasAttacked and len(self.getOtherActionablePlayers(self.player)) > 0:
                    options.append('Attack')
                    optionNum += 1
                if not self.player.hasRested and self.player.exhaustionLevel > 0:
                    options.append('Rest')
                    optionNum += 1
                if not self.player.hasInvestigated and not self.location.hasBeenInvestigated:
                    options.append('Investigate')
                    # Calculate discount for if mirror was successfully interrogated
                    discount = 0
                    if self.isCluedIn:
                        discount = 2
                    optionNum += 1
                if not self.player.hasExerted and not self.location.hasBeenExerted:
                    options.append('Exert')
                    optionNum += 1
                if not self.player.hasExplored and not self.location.hasBeenExplored:
                    options.append('Explore')
                    optionNum += 1
                if not self.player.hasUsedActive:
                    isActiveValid = False
                    active =  self.player.character['active']
                    match active:
                        case 'Anchor':
                            if (self.player.hasAttacked and len(self.getOtherActionablePlayers(self.player)) > 0) or (self.player.hasRested and self.player.exhaustionLevel > 0) or (self.player.hasInvestigated and not self.location.hasBeenInvestigated) or (self.player.hasExerted and not self.location.hasBeenExerted) or (self.player.hasExplored and not self.location.hasBeenExplored):
                                isActiveValid = True
                        case 'Prototype':
                            if len(self.player.inspiration) > 0:
                                isActiveValid = True
                        case 'Interrogate':
                            if len(list(filter(lambda p: p.isAbleToAct() and not p.isRevealed, self.player.getOtherPlayers()))) > 0:
                                isActiveValid = True
                        case 'Guard':
                            if len(self.getOtherActionablePlayers(self.player)) > 0:
                                isActiveValid = True
                        case 'Scout':
                            isActiveValid = True
                        case 'Weird':
                            if len(self.getOtherActionablePlayers(self.player)) > 0:
                                isActiveValid = True
                    if isActiveValid:
                        options.append('Special Active')
                        optionNum += 1
                # Marloe reveal action is available to players with the role that have not yet had it revealed
                if self.player.role['id'] == 3 and not self.player.isRevealed:
                    options.append('Reveal Active')
                    optionNum += 1
                options.append('Pass')
                # Display options in GUI for player to select
                self.setActionInput(options)
                # Begin event handling if this is the first action of the game and mode is not test
                self.beginEventHandling()
            # If player cannot act, append blank action and target
            else:
                # Append blank action
                self.actions.append(None)
                # Advance stack
                self.advanceStack()
        # If no player is able to act, advance room
        else:
            self.advanceRoom()
    # END STARTTURN

    """
    pre: called whenever a change in the current turn's phase or step is needed
    post: next step in member:eventStack is called.
    """
    def advanceStack(self):
        # Pop stack
        method = self.eventStack.pop()
        # Call method
        method()
    # END ADVANCESTACK

    """
    pre: called between the decision phase and the results phase.
    post: replaces actions with random actions as needed in Alley, decides AI actions, initializes lists and stats for results phase, call unity as needed, 
        process weirding action first if there is one, then begin processing actions in order.
    """
    def actionPhase(self):
        # If in the alley, if player was randomly chosen and is able to act, override their decision with a random one
        if self.location.room['id'] == 2 and self.randomID == 1 and self.player.isAbleToAct():
            randomAction, randomTarget = self.player.getRandomAction()
            # Report outcome
            self.displayText('A stray thought strikes you, altering your choice of action.')
            # Override original player decision with newly constructed action
            self.actions.pop(0)
            self.actions.append(Action(randomAction, self.player, randomTarget))
        # Determine AI actions and targets
        for p in self.allPlayers:
            if not p.isPlayer():
                if p.isAbleToAct() and not p.isStunned:
                    action, target = p.decideAiAction()
                    self.actions.append(Action(action, p, target))
                else:
                    # Provide blank action if player did not act
                    self.actions.append(None)
            # Remove stun effect after action is skipped (if player was stunned)
            p.isStunned = False
        # Re-initialize source and target lists for use in action handling
        self.attackSources = []
        self.attackTargets = []
        self.guardSources = []
        self.guardTargets = []
        self.restTargets = []
        self.passingPlayers = []
        # Initialize room action stats applied
        self.investigateTotal = 0
        self.exertTotal = 0
        self.exploreTotal = 0
        # Determine if all players took the same action
        isUnity = True
        testAction = self.actions[0]
        for action in self.actions:
            if action != None and testAction != None and testAction.action != action.action:
                isUnity = False
                break
            else:
                if action != None:
                    testAction = action
        # If all actions were the same and not None and Mantelesse took one of them, trigger his passive
        if isUnity and testAction:
            mantelessePlayer = self.lookupPlayerByCharacter('Mantelesse')
            if mantelessePlayer:
                if mantelessePlayer.isAbleToAct():
                    # Call unite on last action verified to not be None
                    mantelessePlayer.unite(testAction)
        # Perform weirding action first
        for i in range(len(self.actions)):
            action = self.actions[i]
            if action:
                if action.action == 'Special Active' and action.source.character['id'] == 5:
                    self.processAction(i)
                    # end loop as only one player will ever be weirding at a time
                    break
        # If no weirding action was taken, start from the beginning of the action list
        self.processAction()
    # END ACTIONPHASE

    """
    pre: called as part of the results phase.
    post: calls investigate on the current room if at least 1 player explored. Advances to next step in results phase.
    """
    def investigateResults(self):
        # Carry out investigate action
        if self.investigateTotal > 0:
            self.location.investigate(self.investigateTotal)
            if self.location.room['id'] == 1:
                return
        # Advance stack unless room action is awaiting player input (in case of Break the Magic)
        self.advanceStack()
    # END INVESTIGATE RESULTS

    """
    pre: called as part of the results phase.
    post: calls exert on the current room if at least 1 player explored. Advances to next step in results phase.
    """
    def exertResults(self):
        # Carry out exert action
        if self.exertTotal > 0:
            self.location.exert(self.exertTotal)
            if self.location.room['id'] == 4:
                return
        # Advance stack unless room action is awaiting player input (in case of Wish at the Well)
        self.advanceStack()
    # END EXERT RESULTS

    """
    pre: called as part of the results phase.
    post: calls explore on the current room if at least 1 player explored. Advances to next step in results phase.
    """
    def exploreResults(self):
        # Carry out explore action
        if self.exploreTotal > 0:
            self.location.explore(self.exploreTotal) 
            if self.location.room['id'] == 0:
                return
        # Advance stack unless room action is awaiting player input (in case of Take the High Ground)
        self.advanceStack()
    # END EXPLORE RESULTS

    """
    pre: called as part of the results phase (must be before the rest phase).
    post: calls attack on all attacking players. Advances to next step in results phase.
    """
    def attackResults(self):
        # Carry out attacks
        for i in range(len(self.attackSources)):
            source = self.lookupPlayerByID(self.attackSources[i])
            target = self.lookupPlayerByID(self.attackTargets[i])
            source.attack(target)   
        # Advance stack
        self.advanceStack()
    # END ATTACKRESULTS

    """
    pre: called as part of the results phase (must be after the attack phase).
    post: if there are enough party supplies for all resting players, calls rest on each of them. Advances to next step in results phase.
    """
    def restResults(self):
        # Deny all rests if there are not enough supplies for each player attempting to rest at once
        numResting = len(self.restTargets)
        if self.partySupplies < numResting:
            self.displayText('Without enough supplies for each resting party member, there can be no consensus, and therefore no rest.')
        else:
            # Carry out rests
            for pid in self.restTargets:
                p = self.lookupPlayerByID(pid)
                if p.isAlive:
                    p.rest()
        # If a player rested, report remaining supplies
        if numResting > 0:
            self.displayText('The party is left with ' + str(self.partySupplies) + ' supplies.')
        # Advance stack unless waiting on player input
        if not self.isWaiting:
            # Advance stack
            self.advanceStack()
    # END RESTRESULTS

    """
    pre: called at the end of the turn cycle.
    post: attempts to pass passing players, ends turn-specific effects, handles turn-count-dependent effects, inspires Endemene if she was attacked by multiple players, begins a new turn.
    """
    def endTurn(self):
        # Carry out passes
        self.location.passPlayers(self.passingPlayers)
        # If Marloe was revealed, the effect ends at end of turn
        self.marloeRevealedThisTurn = False
        # Increment turn counter
        self.location.turnCounter += 1
        # If in cove, handle storm
        currentTurn = self.location.turnCounter
        if self.location.room['id'] == 5:
            if currentTurn == 1:
                # Report if player is active
                self.displayText('You spy a wicked-looking ice storm on the horizon. It will be upon you in 2 turns.')
            elif currentTurn == 2:
                # Report if player is active
                self.displayText('The storm draws nearer. It will be upon you in one turn.')
            elif currentTurn == 3:
                # Report if player is active
                self.displayText('The storm is upon you.')
            # Exhaust players unless they are sheltered
            if currentTurn >= 3:
                if self.isSheltered:
                    # Report outcome regardless of whether player is active
                    self.displayText('The party weathers the storm under the cove\'s natural shelter.')    
                else:
                    # Report outcome regardless of whether player is active
                    self.displayText('The party is battered mercilessly by the razor-sharp ice.')
                    # Active players gain exhaustion
                    _ = [p.gainExhaustion() for p in self.getActionablePlayers()]
        # If Endemene appeared twice in attack targets, trigger inspire on her
        numAppearances = 0
        for pid in self.attackTargets:
            if self.lookupPlayerByID(pid).character['id'] == 1:
                numAppearances += 1
        if numAppearances >= 2:
            # Trigger inspire on Endemene if she is not dead or escaped
            _ = [p.inspire('Net') for p in list(filter(lambda p: p.isInDungeon() and p.character['id'] == 1, self.allPlayers))]
        # Start new turn
        self.startTurn()
    # END ENDTURN

    """
    pre: used to handle actions during the action phase each turn.
    param: index, the index of the action in member:actions to be processed. Default: 0 - the first action in the list
    post: if member:actions is empty, advances the stack to the next turn phase. Otherwise, pops the action in member:actions at param:index, 
        performs the action unless the action's source is weirded, then processes the next action.
    """
    def processAction(self, index=0):
        # Process action at index if there is such an action
        if len(self.actions) > 0:
            # Pop action
            action = self.actions.pop(index)
            if action:
                # Reject action if source is weirded
                if action.source.isWeirded:
                    # Remove weirded effect
                    action.source.isWeirded = False
                    # Report outcome
                    if action.source.isPlayer():
                        self.displayText('Your ' + action.action + ' action was negated by the weirding magic that has taken hold of you this turn.')
                    else:
                        self.displayText(action.source.character['shortName'] + '\'s ' + action.action + ' action was negated by the weirding magic that has taken hold of them this turn.')
                else:
                    # Source takes action
                    action.source.takeAction(action)
            # Process next action if this action was None
            else:
                self.processAction()
        # Advance stack if this was the final action 
        else:
            self.advanceStack()  
    # END PROCESSACTION

    ### GAME: TESTING ###

    """
    pre: called after the end of the game in debug mode.
    return: tuple of character winrate stats, role winrate stats, and character-role-pair winrate stats for the game.
    """
    def tallyStats(self) -> tuple:
        # Initialize tally blocks
        characterTally = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        roleTally = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        pairTally = [[0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]
        for p in self.allPlayers:
            # Extract IDs to use as indices
            characterID = p.character['id']
            roleID = p.role['id']
            # Mark as +1 for wins, 0 for losses
            if p.hasWon:
                characterTally[characterID] = 1
                roleTally[roleID] = 1
                pairTally[characterID][roleID] = 1
            else:
                characterTally[characterID] = 0
                roleTally[roleID] = 0
                pairTally[characterID][roleID] = 0
        # Return results
        return characterTally, roleTally, pairTally
    # END TALLYSTATS
# END CLASS GAME

### GLOBAL: CLASS ACTION ###

class Action:
    def __init__(self, action, source, target):
        self.action = action
        self.source = source
        self.target = target
    # END __INIT__
# END CLASS ACTION

### GLOBAL: CLASS PLAYER ###

class Player:
    def __init__(self, character, role, playerID, mode):
        # initialize player stats
        self.character = character
        self.role = role
        self.id = playerID
        self.hasRested = True
        self.exhaustionLevel = 0
        self.isAlive = True
        self.hasEscaped = False
        self.isRevealed = False
        self.isHostileTowards = [] # for AI use only
        self.timesCursed = 0
        self.numRoomsVisited = 0
        self.timesSeenHeart = 0
        self.hasConqueredFear = False
        self.isAnchored = False # for AI Reika's use only
        self.inspiration = [] # for Endemene's use only
        self.prototypes = [] # for Endemene's use only
        self.hasPrototyped = [] # for Endemene's use only
        self.unraveledRoles = [] # for Rainee's use only
        self.guessedPlayers = [] # for Rainee's use only
        # For Elvy's use only
        if character['id'] == 3:
            self.isWarded = True
        else:
            self.isWarded = False
        # For Mnanth's use only
        if role['id'] == 0:
            # Adjust list of IDs to draw fram depending on whether there is a player
            otherPlayerIDs = [mode,2,3,4]
            otherPlayerIDs.remove(playerID)
            # Select a random other player ID
            self.pactTargetID = rng.sample(otherPlayerIDs, 1)[0]
        else:
            self.pactTargetID = None
        self.isWeirded = False
        self.isStunned = False
        self.hasAttacked = False
        self.hasInvestigated = False
        self.hasExerted = False
        self.hasExplored = False
        self.hasUsedActive = False
        self.hasPassed = False
        self.attemptedToPass = False
        # Determine default mode based on role (FOR AI ONLY)
        if role['id'] in [0, 3, 5]: # Mnanth, Marloe, Fisherwoman
            self.mode = 1 # 1 OPPORTUNISTIC - act collaboratively to an extent that is necessary but seize any opportunity to gain the upper hand towards fulfilling an antagonistic goal
        elif role['id'] == 2: # Cloudblessed
            self.mode = 2 # 2 SELFLESS - act in the benefit of the party towards fulfilling a beneficial goal
        else: # Casglowve, Erstwhile
            self.mode = 0 # 0 COLLABORATIVE - act in the benefit of the party towards fulfilling a neutral goal
        # Other modes:
        # 3 AGGRESSIVE - act antagonistically towards the party towards fulfilling an antagonistic goal (moved to from OPPORTUNISTIC)
        # 4 DEFENSIVE - set aside other goals to countaract antagonistic behavior from another player (moved to from COLLABORATIVE or SELFLESS)
        # 5 BENEVOLENT - act for the good of the entire party without a goal (moved to from COLLABORATIVE or OPPORTUNISTIC)
        # 6 SPITEFUL - act antagonistically towards the party without a goal (moved to from COLLABORATIVE or OPPORTUNISTIC)
        self.hasWon = False # For use in TEST mode only
    # END __INIT__

    ### PLAYER: DISPLAY TOOLS ###

    """
    pre: called at the beginning of the game on the PC.
    post: the player's character-specific info is printed.
    """
    def printCharacterInfo(self):
        # Load Game
        global g_game
        # Print info
        character = self.character
        g_game.displayText(self.character['shortName'])
        g_game.displayText('Ingenuity: ' + str(character['ingenuity']))
        g_game.displayText('Resolve: ' + str(character['resolve']))
        g_game.displayText('Finesse: ' + str(character['finesse']))
        g_game.displayText('Special Passive - ' + character['passive'] + ': ' + character['passiveDescription'])
        g_game.displayText('Special Active - ' + character['active'] + ': ' + character['activeDescription'])
    # END PRINTCHARACTERINFO

    """
    pre: called at the beginning of the game on the PC.
    post: the player's role-specific info is printed.
    """
    def printRoleInfo(self):
        # Load Game
        global g_game
        role = self.role
        g_game.displayText(self.role['shortName'])
        g_game.displayText('Reveal Condition & Ability - ' + role['reveal'] + ': ' + role['revealDescription'])
        g_game.displayText('Win Condition - ' + role['winCondition'] + ': ' + role['winConDescription'])
        # Inform player of pact target's role if their role is Mnanth
        if role['id'] == 0:
            g_game.displayText('Your pact target is ' + g_game.lookupPlayerByID(self.pactTargetID).role['shortName'])
    # END PRINTROLEINFO

    ### PLAYER: BASE MECHANICS ###

    """
    pre: called on each player when the room changes.
    post: room-specific characteristics of the player are reset, each player still in play has their 'number of rooms visited' stat updated, 
        each player still in play gains a level of exhaustion unless they have seen the wandering heart 2+ times.
    """
    def enterRoom(self):
        # Load Game
        global g_game
        # Reset room-specific stats (except hasRested)                      
        self.hasAttacked = False
        self.hasInvestigated = False
        self.hasExerted = False
        self.hasExplored = False
        self.hasUsedActive = False
        self.hasPassed = False
        self.attemptedToPass = False
        # Players do not enter a room when they are dead or escaped
        if not self.isInDungeon():
            return
        # Increment rooms visited
        self.numRoomsVisited += 1
        if not self.hasRested:
            # No exhaustion gained for players who have seen the wandering heart 2 or more times
            if self.timesSeenHeart > 1:
                # Player output
                if self.id == 1:
                    g_game.displayText('The memory of the Heart fills you with that odd sense of wakefulness again. You gain no exhaustion as you cross over to this room.')
            # Gain a level of exhaustion if no rest was taken in the last room
            else:
                self.gainExhaustion()
        # Reset hasRested (needed original value for exhaust gain trigger)
        self.hasRested = False
    # END ENTERROOM

    """
    pre: called on a player whenever they would gain exhaustion.
    post: player's exhaustion level is increased by one, then an appropriate effect is applied, making them vulnerable at level 2 and instantly killing them at level 4.
    """
    def gainExhaustion(self):
        # Load Game
        global g_game
        self.exhaustionLevel += 1
        # Output exhaustion information for the player
        if self.id == 1:
            # Add level of exhaustion
            g_game.displayText('You gain a level of exhaustion.')
            exhaustionLevel = self.exhaustionLevel
            match exhaustionLevel:
                case 1:
                    g_game.displayText('You may now take the Rest action.')
                case 2:
                    g_game.displayText('You are now vulnerable to attack.')
                case 3:
                    g_game.displayText('You will surely perish if you do not take the rest action in this room.')
                    # Trigger Casglowve reveal on self
                    self.triggerReveal('Casglowve, the Captive Moon')
                case 4:
                    g_game.displayText('You collapse from your exhaustion and are left for dead.')
                    # Mark character as dead
                    self.die()
        # Output exhaustion information for AI
        else:
            exhaustionLevel = self.exhaustionLevel
            match exhaustionLevel:
                case 2:
                    g_game.displayText(self.character['shortName'] + ' is visibly weakened by their exhaustion.')
                case 4:
                    g_game.displayText(self.character['shortName'] + ' collapsed from their exhaustion and was left for dead.')
                    # Mark character as dead
                    self.die()
    # END GAINEXHAUSTION

    """
    pre: called on each player that has taken the rest action without dying during the results phase or when they would gain the benefit of a rest by other means
    post: player rests, regaining two levels of exhaustion, decrement party supplies, if this rest is done as part of the results phase, carry out additional triggers.
    """
    def rest(self):
        # Load Game
        global g_game
        # Reduce exhaustion by two levels
        self.exhaustionLevel -= 2
        if self.exhaustionLevel < 0:
            self.exhaustionLevel = 0
        # Decrement supplies
        g_game.partySupplies -= 1
        # Case where you went from 3 -> 1 exhaustion
        if self.exhaustionLevel == 1:
            # Report for player
            if self.isPlayer():
                g_game.displayText('You feel largely back to your normal self.')
            # Report for AI
            else:
                g_game.displayText(self.character['shortName'] + ' is no longer visibly exhausted.')
        # Case where they went from 2 or 1 -> 0 exhaustion
        else:
            # Only report for player
            if self.isPlayer():
                g_game.displayText('You feel fully recovered and ready for everything.')
        # Carry out additional effects only if this is a standard rest (if player is in restTargets)
        if self.id in g_game.restTargets:
            # Show vision if player has lens
            if 'Lens' in self.prototypes:
                # Remove net
                self.prototypes.remove('Lens')
                # Report information for player only
                if self.isPlayer():
                    g_game.displayText('As you lay down for a rest, the lens you crafted grants you insight into the party members resting beside you.')
                    otherRestingPlayers = list(filter(lambda p: p.id in g_game.restTargets, self.getOtherPlayers()))
                    # If no other players resting, report failure
                    if len(otherRestingPlayers) == 0:
                        g_game.displayText('Unfortunately, there are no such party members. Your lens fractures and crumbles to dust in your hands, leaving you no wiser.')
                    else:
                        for p in otherRestingPlayers:
                            providedRoles = []
                            providedRoles.append(p.role) # Add real role
                            rolesInPlayNotSelfOrTarget = list(map(lambda s: s.role, list(filter(lambda q: q.isAbleToAct() and q.id != self.id and q.id != p.id, g_game.allPlayers))))
                            rolesInPlayByID = list(map(lambda s: s.role['id'], g_game.getActionablePlayers()))
                            global g_roles
                            rolesNotInPlay = []
                            for r in g_roles:
                                if r.id not in rolesInPlayByID:
                                    rolesNotInPlay.append(r)
                            providedRoles.append(rng.sample(rolesInPlayNotSelfOrTarget, 1)[0]) # Add a role in play that is not the self's or target's
                            providedRoles.append(rng.sample(rolesNotInPlay, 1)[0]) # Add a role not in play
                            # Randomize selection
                            randomizedRoles = rng.sample(providedRoles, 3)
                            # Report results for player
                            g_game.displayText(p.character['shortName'] + '\'s role is one of the following: ')
                            for r in randomizedRoles:
                                g_game.displayText(r['name'])
            # Unravel if player is Rainee Haraldsson
            if self.character['id'] == 2:
                self.unravel()
            # Discover if player is Dredge
            if self.character['id'] == 4:
                self.discover()
            # If player has not already seen the heart three times, there is a chance to encounter it in dreams
            if self.timesSeenHeart < 3:
                # Calculate chance to see the Wandering Heart in dreams
                heartOdds = 0.1 * g_game.roomIndex + 0.2 * self.timesSeenHeart
                randVal = rng.random()
                # If odds are met, player encounters the Heart
                if randVal < heartOdds:
                    # Report outcome
                    if self.isPlayer():
                        # Output differs if you have seen the Heart before
                        if self.timesSeenHeart > 0:
                            g_game.displayText('In your dreams you follow a light most peculiar to find a great, pulsing hunk of red and pink tissue that hovers impassively above you on the empty plain of unsolidifed dreams. An enormous, beating heart.')
                        else:
                            g_game.displayText('In your dreams you follow a light most peculiar to find a great, pulsing hunk of red and pink tissue that hovers impassively above you on the empty plain of unsolidifed dreams. It is the heart you have seen before.')
                    # Trigger inspire on player if they are Endemene
                    if self.character['id'] == 1:
                        self.inspire('Lens')
                    # Player sees heart
                    self.seeHeart()
    # END REST

    """
    pre: called on each player that has taken the attack action during the results phase.
    param: target, the Player selected as target for the attack.
    post: attack is either resisted due to various effects or is carried out, resulting in the gaining of a level of exhaustion of the target, or death if they are exhausted enough or currently resting.
        Attack can be aided by various effects as well. Trigger reveal on Fisherwoman. 
    """
    def attack(self, target):
        # Load Game
        global g_game
        # If self or target is Elvy and they still are warded, remove ward from respective player
        if self.character['id'] == 3 and self.isWarded:
            self.loseWard()
        if target.character['id'] == 3 and target.isWarded:
            target.loseWard()
        # Trigger Fisherwoman reveal
        self.triggerReveal('The Fisherwoman')
        # Reject attack if target is guarded
        if target.id in g_game.guardTargets:
            # Lookup guard source
            index = g_game.guardTargets.index(target.id)
            guardSourceID = g_game.guardSources[index]
            guardian = g_game.lookupPlayerByID(guardSourceID)
            # Initialize guardian name
            guardianName = guardian.character['shortName']
            # Report outcome
            if target.isPlayer():
                # Change output if player guarded the target
                if guardian.isPlayer():
                    guardianName = 'you'
                g_game.displayText('You were attacked by ' + self.character['shortName'] + ', but ' + guardianName + ' fought them off.')
            elif self.isPlayer():
                g_game.displayText(guardianName + ' fought off your attack on ' + target.character['shortName'] + '.')
            else:
                # Change output if player guarded the target
                if guardian.isPlayer():
                    guardianName = 'You'
                g_game.displayText(guardianName + ' fought off an attack from ' + self.character['shortName'] + ' on ' + target.character['shortName'] + '.')
            # If Marloe revealed this turn, target receives a curse
            if g_game.marloeRevealedThisTurn:
                # Target becomes cursed
                target.timesCursed += 1
                # Report outcome
                if target.isPlayer():
                    g_game.displayText('You were saved from attack by the grace of House Marloethien. This grace did not however come without a cost. You are now cursed.')
                else:
                    g_game.displayText(target.character['shortName'] + ' was saved from attack by the grace of House Marloethien. This grace did not however come without a cost. They are now cursed.')
        # If target is not guarded, reject attack if target is shielded
        elif 'Shield' in target.prototypes:
            # Remove shield
            target.prototypes.remove('Shield')
            # Report outcome
            if target.isPlayer():
                g_game.displayText('You were attacked by ' + self.character['shortName'] + ', but your shield deflected the blow. It will not hold up against another.')
            elif self.isPlayer():
                g_game.displayText(target.character['shortName'] + ' was protected from your attack by her shield. It will not hold up against another.')
            else:
                g_game.displayText(target.character['shortName'] + ' was protected from ' + self.character['shortName'] + '\'s attack by her shield. It will not hold up against another.')
        # Target will die if they took the rest action this turn
        elif target.id in g_game.restTargets:
            # Targets that have confronted the beast become cursed instead of dying.
            if target.hasConqueredFear:
                # Target is cursed
                target.timesCursed += 1
                # Remove effect
                target.hasConqueredFear = False
                # Report outcome
                if target.isPlayer():
                    g_game.displayText('The unnatural strength instilled in you by your close call with the beast in Longway Alley allowed you to survive an attack from ' + self.character['shortName'] + ' that otherwise would have been deadly. Your survival is not without consequence, however. A shiver runs down your spine as the beast\'s call, a haunting whine, reverberates in your mind. You are now cursed.')
                elif self.isPlayer():
                    g_game.displayText('The unnatural strength instilled in ' + target.character['shortName'] + ' by their close call with the beast in Longway Alley allowed them to survive your attack that otherwise would have been deadly. Their survival is not without consequence, however. They are now cursed.')
                else:
                    g_game.displayText('The unnatural strength instilled in ' + target.character['shortName'] + ' by their close call with the beast in Longway Alley allowed them to survive an attack from ' + self.character['shortName'] + ' that otherwise would have been deadly. Their survival is not without consequence, however. They are now cursed.')
            else:
                # Report outcome
                if target.isPlayer():
                    g_game.displayText('You were killed by  ' + self.character['shortName'] + ' in your sleep.')
                elif self.isPlayer():
                    g_game.displayText('You killed ' + target.character['shortName'] + ' in their sleep.')
                else:
                    g_game.displayText(self.character['shortName'] + ' killed ' + target.character['shortName'] + ' in their sleep.')
                # Target dies
                target.die()
        # Target will die if they have more than one level of exhaustion or if the sword is drawn 
        elif target.exhaustionLevel > 1 or g_game.isSwordDrawn:
            # Report Outcome
            if target.isPlayer():
                g_game.displayText('You were killed in a struggle with ' + self.character['shortName'] + '.')
            elif self.isPlayer():
                g_game.displayText('You killed ' + target.character['shortName'] + ' in a struggle.')
            else:
                g_game.displayText(self.character['shortName'] + ' killed ' + target.character['shortName'] + ' in a struggle.')
            # Target dies
            target.die()
        else:
        # Otherwise target gains a level of exhaustion
            # Report outcome
            if target.isPlayer():
                g_game.displayText('You fought off an attack from ' + self.character['shortName'] + '.')
            elif self.isPlayer():
                g_game.displayText(target.character['shortName'] + ' fought off your attack.')
            else:
                g_game.displayText(target.character['shortName'] + ' fought off an attack from ' + self.character['shortName'] + '.')
            # Target gains exhaustion
            target.gainExhaustion()
            # Stun target if self has a Net
            if 'Net' in self.prototypes:
                # Remove net
                self.prototypes.remove('Net')
                # Stun target
                target.isStunned = True
                # Report outcome
                if self.isPlayer():
                    g_game.displayText('Your net entraps ' + target.character['shortName'] + ', stunning them while they cut their way free.')
                elif target.isPlayer():
                    g_game.displayText(self.character['shortName'] + '\'s net entraps you, stunning you while you cut your way free.')
                else:
                    g_game.displayText(self.character['shortName'] + '\'s net entraps ' + target.character['shortName'] + ', stunning them while they cut their way free.')
        # Each AI that is not dead or escaped and is not already aggressive and is not hostile to the attack target and is not the attacker adds the attacker's id to their list of hostiles
        for p in self.getOtherPlayers():
            if p.isInDungeon() and not p.mode == 3 and not p.isPlayer() and target.id not in p.isHostileTowards and ((g_game.location.room['id'] != 0 and g_game.location.room['id'] != 1 and g_game.location.room['id'] != 2) or (self.role['id'] == 5 and self.isRevealed)): # Forgive attacks in Arena, Tower, or Alley unless the attacker is revealed as the Fisherwoman
                # Add to list of hostiles
                p.isHostileTowards.append(self.id)
                # If AI is not already DEFENSIVE, change it to be and report
                if not p.mode == 4:
                    g_game.displayText(p.character['shortName'] + ' takes the defensive.')
                    p.mode = 4
    # END ATTACK

    """
    pre: called on a player when a player successfully passes action.
    post: player is marked as passed.
    """
    def passAction(self):
        # player passes
        self.hasPassed = True
        # Report outcome
        if self.isPlayer():
            g_game.displayText('You passed action.')
        else:
            g_game.displayText(self.character['shortName'] + ' passed action.')
    # END PASSACTION 

    """
    pre: called on a player when they are removed from play by way of escaped.
    post: player is marked as escaped internally and visually, room is checked for cloudblessed delayed trigger
    """
    def escape(self):
        # Load game
        global g_game
        # Player escapes
        self.hasEscaped = True
        # Gray out portrait
        g_game.dyePortrait(self.id)
        # Carry out Cloudblessed delayed trigger if necessary
        attemptCloudblessedRevive()
    # END ESCAPE 

    """
    pre: called on a player when they are removed from play by way of being killed.
    post: player is marked as dead internally and visually, mechanics dependent on player death are adjusted appropriately, Cloudblessed reveal is triggered, room is checked for cloudblessed delayed trigger.
    """
    def die(self):
        # Load game
        global g_game
        # Player dies
        self.isAlive = False
        # Gray out portrait
        g_game.dyePortrait(self.id)
        # If sword is drawn, a player dying removes the effect
        if g_game.isSwordDrawn:
            # Report outcome
            g_game.displayText('Although lethal, the sword is also brittle. With its lust for blood sated, it breaks into pieces to small to reconstitute it from.')
            # End effect
            g_game.isSwordDrawn = False
            # Trigger inspire on Endemene if she is active
            _ = [p.inspire('Shield') for p in list(filter(lambda p: p.isAbleToAct() and p.character['id'] == 1, g_game.allPlayers))]
        # If way is barred, a player dying removes the effect
        g_game.isWayBarred = False
        # mark blood as drawn (for arena use only)
        g_game.location.hasBloodBeenDrawn = True
        # Trigger Cloudblessed reveal on self
        self.triggerReveal('Cloudblessed')
        # Trigger Erstwhile reveal on everyone who is active
        _ = [p.triggerReveal('Erstwhile, Collector Supreme') for p in g_game.getActionablePlayers()]
        # Carry out Cloudblessed delayed trigger if necessary
        attemptCloudblessedRevive()
    # END DIE

    """
    pre: called on a player when they satisfy the conditions needed to encounter the wandering heart.
    post: if this is the third time the player has seen the heart, they are given the option to escape. Otherwise, their exhaustion is reset.
    """
    def seeHeart(self):
        # Load Game
        global g_game
        # If this is the first time an AI has seen heart, notify player if their role is Fisherwoman
        if self.timesSeenHeart == 0:
            otherPlayers = self.getOtherPlayers()
            for p in otherPlayers:
                if p.isPlayer() and p.role['id'] == 5:
                    g_game.displayText(self.character['shortName'] + ' has seen the Wandering Heart. They must not be allowed to leave the dungeon alive.')
        # If this is the second time an AI has seen heart, notify player if their role is Fisherwoman
        if self.timesSeenHeart == 1:
            otherPlayers = self.getOtherPlayers()
            for p in otherPlayers:
                if p.isPlayer() and p.role['id'] == 5:
                    g_game.displayText(self.character['shortName'] + ' has seen the Wandering Heart for a second time. They grow near to escape. Kill them now.')
        # Increment times seen heart
        self.timesSeenHeart += 1
        # If this is the first, second, or greater than third time, exhaustion is reduced to 0
        if self.timesSeenHeart != 3:
            # Reduce exhaustion
            self.exhaustionLevel == 0
            # Report outcome if self is player
            if self.isPlayer():
                g_game.displayText('After a few minutes spent observing the thing\'s rhythmic motion, a peculiar energy fills you. You leave the heart feeling as awake and alert as you have ever been.')
        # Else player is given the opportunity to escape.
        else:
            if self.isPlayer():
                g_game.displayText('On this your third meeting, the heart stretches out a stray strand of fibrous material as if offering a hand to you. Will you take it and escape into the world of dreams?')
                # Set input lock
                g_game.isWaiting = True
                # Set input for player to choose Y/N from
                g_game.setYNInput(g_game.getHeartOffer)
            else:
                # Otherwise decide choice of AI
                shouldEscape = self.shouldAiEscape()
                if shouldEscape:
                    g_game.displayText(self.character['shortName'] + ' disappeared in their rest, vanished from this plane to the sound of a thrumming heartbeat. They have escaped the dungeon.')
                    # AI escapes
                    self.escape()
    # END SEEHEART

    ### PLAYER: HELPERS ###

    """
    return: True if the player is the PC. False otherwise.
    """
    def isPlayer(self) -> bool:
        # Check if player ID is 1, if not, the player is an AI
        if self.id == 1:
            return True
        return False
    # END ISPLAYER

    """
    return: True if the player is in the dungeon and has not passed. False otherwise.
    """
    def isAbleToAct(self) -> bool:
        # Load game
        global g_game
        if not self.isInDungeon():
            return False
        if self.hasPassed:
            return False
        return True
    # END ISABLETOACT

    """
    return: True if the player is alive and has not escaped. False otherwise.
    """
    def isInDungeon(self) -> bool:
        if not self.isAlive or self.hasEscaped:
            return False
        return True
    # END ISINDUNGEON

    """
    return: list of all players that are not the player being called on.
    """
    def getOtherPlayers(self) -> list:
        # Load game
        global g_game
        # Initialize list of other players
        otherPlayers = []
        # Add each player with an ID that is not the caller's ID
        for p in g_game.allPlayers:
            if p.id != self.id:
                otherPlayers.append(p)
        return otherPlayers

    ### PLAYER: ACTION HANDLING ###

    """
    pre: called only one the player randomly chosen to act randomly in the Alley.
    return: tuple of a string representing the action that has been randomly decided on and a second string representing a randomly decided target, or None if there is no target for the chosen action.
    """
    def getRandomAction(self) -> tuple:
        # Load Game
        global g_game
        # Find random other player to target
        try:
            randomTarget = rng.sample(g_game.getOtherActionablePlayers(self), 1)[0]
        except ValueError:
            randomTarget = None
        # Determine valid actions
        validActions = []
        # Must be a valid target in order to attack
        if not self.hasAttacked and randomTarget:
            validActions.append('Attack')
        if not self.hasRested and self.exhaustionLevel > 0:
            validActions.append('Rest')
        if not self.hasPassed:
            validActions.append('Pass')
        # We NEED to allow all characters that do not target with their special active to take this option randomly, or Mnanth reveal in the alley will cause a loop in the game if they are the only player remaining in the room
        if not self.hasUsedActive and (self.character['id'] == 0 or self.character['id'] == 4): # Reika and Dredge. Reika will be allowed to decide her anchored action normally if Anchor is chosen randomly.
            validActions.append('Special Active')
        if not self.hasUsedActive and self.character['id'] == 1 and len(self.inspiration) > 0: # Endemene
            validActions.append('Special Active')
        # Allow for others as well, in fairness
        if not self.hasUsedActive and randomTarget and (self.character['id'] == 2 or self.character['id'] == 3 or self.character['id'] == 5): # Rainee, Elvy, Mantelesse
            validActions.append('Special Active')
        if not self.hasInvestigated and not g_game.location.hasBeenInvestigated:
            validActions.append('Investigate')
        if not self.hasExerted and not g_game.location.hasBeenExerted:
            validActions.append('Exert')
        if not self.hasExplored and not g_game.location.hasBeenExplored:
            validActions.append('Explore')
        # Choose random valid action
        randomAction = rng.sample(validActions, 1)[0]
        # If action is Prototype, adjust target to be an inspiration instead of a player
        if randomAction == 'Special Active' and self.character['id'] == 1:
            randomTarget = rng.sample(self.inspiration, 1)[0]
        # Return
        return (randomAction, randomTarget)
    # END GETRANDOMACTION

    """
    pre: called on each active player as part of the action phase each turn.
    param: action, an action object containing the information for the action taken by the player this turn.
    post: action is carried out, or logged if it has results that need to be handled after all actions have been taken, in the results phase.
    """
    def takeAction(self, action:Action):
        # Load game
        global g_game
        # If action is None, skip directly to next action
        if action:
            match action.action:
                case 'Attack':
                    # Report action
                    if self.isPlayer():
                        g_game.displayText('You attacked ' + action.target.character['shortName'] + '.')
                    elif action.target.isPlayer():
                        g_game.displayText(self.character['shortName'] + ' attacked you.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' attacked ' + action.target.character['shortName'] + '.')
                    # Add self to list of attack sources
                    g_game.attackSources.append(self.id)
                    # Add target to list of attack targets
                    g_game.attackTargets.append(action.target.id)
                    # Remove attack option for future turns in the room
                    self.hasAttacked = True
                case 'Rest':
                    # Report action
                    if self.isPlayer():
                        g_game.displayText('You rested.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' rested.')
                    # Add self to list of rest targets
                    g_game.restTargets.append(self.id)
                    # Remove rest option for future turns in the room
                    self.hasRested = True
                case 'Pass':
                    # Add self to list of passing players
                    g_game.passingPlayers.append(self)
                    # Report intention to pass.
                    if self.isPlayer():
                        g_game.displayText('You attempted to leave the room.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' attempted to leave the room.')
                case 'Investigate':
                    # Report action
                    if self.isPlayer():
                        g_game.displayText('You chose to ' + g_game.location.room['actions'][0] + '.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' chose to ' + g_game.location.room['actions'][0] + '.')
                    # Mark as investigated
                    self.hasInvestigated = True
                    g_game.investigateTotal += self.character['ingenuity'] + self.timesCursed
                case 'Exert':
                    # Report action
                    if self.isPlayer():
                        g_game.displayText('You chose to ' + g_game.location.room['actions'][1] + '.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' chose to ' + g_game.location.room['actions'][1] + '.')
                    # Mark as investigated
                    self.hasExerted = True
                    g_game.exertTotal += self.character['resolve'] + self.timesCursed
                case 'Explore':
                    # Report action
                    if self.isPlayer():
                        g_game.displayText('You chose to ' + g_game.location.room['actions'][2] + '.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' chose to ' + g_game.location.room['actions'][2] + '.')
                    # Mark as explored
                    self.hasExplored = True
                    g_game.exploreTotal += self.character['finesse'] + self.timesCursed
                case 'Special Active':
                    # Mark special active as used
                    self.hasUsedActive = True
                    # Determine what active the character has
                    match self.character['id']:
                        case 0:
                            # This will only ever occur for AI as for PCs, Reika special active is handled prior to taking action
                            # Mark as anchored
                            self.isAnchored = True
                            # Get new AI action and target
                            action, target = self.decideAiAction()
                            # Report outcome
                            g_game.displayText(self.character['shortName'] + ' anchored herself.')
                            # Handle chosen action with recursive call
                            self.takeAction(Action(action, self, target))
                            # Mark as no longer anchored
                            self.isAnchored = False
                        case 1:
                            # Add prototype to list of prototypes available to be used
                            self.prototypes.append(action.target)
                            # Add prototype to list of prototypes that cannot have inspiration gained for them again
                            self.hasPrototyped.append(action.target)
                            # remove prototype from inspiration list
                            self.inspiration.remove(action.target)
                            # Report outcome
                            if self.isPlayer():
                                g_game.displayText('You prototyped ' + action.target + '.')
                            else:
                                g_game.displayText(self.character['shortName'] + ' prototyped ' + action.target + '.')
                        case 2:
                            # Ask player to guess
                            if self.isPlayer():
                                g_game.displayText('Enter your guess for ' + action.target.character['shortName'] + '\'s role.')
                                # List options (excluding roles already known to the player)
                                optionNum = 1
                                options = []
                                roles = ['Mnanth, Whose Heart is Glass', 'Casglowve, the Captive Moon', 'Cloudblessed', 'Marloe, Don of the Downtrodden', 'Erstwhile, Collector Supreme', 'The Fisherwoman']
                                revealedRoles = [self.role['name']]
                                for p in self.getOtherPlayers():
                                    if p.isRevealed:
                                        revealedRoles.append(p.role['name'])
                                for role in roles:
                                    if not role in revealedRoles:
                                        options.append(role)
                                        optionNum += 1
                                # If self is player, set input for them to choose a guess
                                if self.isPlayer():
                                    # Indicate that this function should terminate without proceeding to next action
                                    g_game.isWaiting = True
                                    g_game.setGuessInput(options, action.target)
                                # Else report outcome (without AI guess)
                                else:
                                    if action.target.isPlayer():
                                        g_game.displayText(self.character['shortName'] + ' interrogated you.')
                                    else:
                                        g_game.displayText(self.character['shortName'] + ' interrogated ' + action.target.character['shortName'] + '.')       
                        case 3:
                            # If Elvy is still warded, remove ward
                            if self.isWarded:
                                self.loseWard()
                            # Report action
                            if self.isPlayer():
                                g_game.displayText('You guarded ' + action.target.character['shortName'] + '.')
                            elif action.target.isPlayer():
                                g_game.displayText(self.character['shortName'] + ' guarded you.')
                            else:
                                g_game.displayText(self.character['shortName'] + ' guarded ' + action.target.character['shortName'] + '.')
                            # Add target to list of guarded targets
                            g_game.guardTargets.append(action.target.id)
                            # Add source to list of guarding players
                            g_game.guardSources.append(self.id)
                        case 4:
                            if self.isPlayer():
                                # Print name of next room for player
                                try:
                                    g_game.displayText('Through your scouting you learn that the next room the party will enter is ' + g_game.shuffledRooms[g_game.roomIndex]['name'] + '.')
                                # If there is no such room, report this
                                except IndexError:
                                    g_game.displayText('Through your scouting, you learn that no rooms remain ahead of you. This is the end of the line.')
                            else:
                                g_game.displayText(self.character['shortName'] + ' scouted ahead.')
                        case 5:
                            # Report action
                            if self.isPlayer():
                                g_game.displayText('You weirded ' + action.target.character['shortName'] + '.')
                            elif action.target.isPlayer():
                                g_game.displayText(self.character['shortName'] + ' weirded you.')
                            else:
                                g_game.displayText(self.character['shortName'] + ' weirded ' + action.target.character['shortName'] + '.')
                            # Mark target as weirded
                            action.target.isWeirded = True
                case 'Reveal Active':
                    # Trigger Marloe reveal
                    self.triggerReveal('Marloe, Don of the Downtrodden')
        if not g_game.isWaiting:
            # Take next action
            g_game.processAction()
    # END TAKEACTION

    ### PLAYER: AI ###

    """
    pre: called on each AI as part of each turn's decision phase.
    return: tuple of a string representing the action the AI has decided on and a second string representing the target, or None if there is no target for the chosen action.
    """
    def decideAiAction(self) -> tuple:
        # Load game
        global g_game
        # If room is the alley and ai is the randomly chosen one to act randomly, choose their action randomly from among those that are valid
        if g_game.location.room['id'] == 2 and g_game.randomID == self.id:
            return self.getRandomAction()
        # Determine if OPPORTUNISTIC AI should change to AGGRESSIVE
        if self.mode == 1:
            if self.shouldAiAggro():
                self.mode = 3
                g_game.timesAggroed += 1 # TEST USE ONLY
        # Determine if DEFENSIVE AI should change back to their default
        if self.mode == 4:
            if len(list(filter(lambda pid: g_game.lookupPlayerByID(pid).isInDungeon(), self.isHostileTowards))) == 0:
                if self.role['id'] in [0, 3, 5]: # Mnanth, Marloe, Fisherwoman
                    self.mode = 1 # OPPORTUNISTIC
                if self.role['id'] == 2: # Cloudblessed
                    self.mode = 2 # SELFLESS
                else: # Casglowve, Erstwhile
                    self.mode = 0 # COLLABORATIVE
        # Get other players
        otherPlayers = self.getOtherPlayers()
        # Player's available stats for room actions - factor
        availableStats = [0, 0, 0]
        if (not self.hasInvestigated and not self.isAnchored) or (self.hasInvestigated and self.isAnchored):
            # Mark stat as available
            availableStats[0] = self.character['ingenuity']
        if (not self.hasExerted and not self.isAnchored) or (self.hasExerted and self.isAnchored):
            # Mark stat as available
            availableStats[1] = self.character['resolve']
        if (not self.hasExplored and not self.isAnchored) or (self.hasExplored and self.isAnchored):
            # Mark stat as available
            availableStats[2] = self.character['finesse']
        # room action availability - factor
        availableRoomActions = [not g_game.location.hasBeenInvestigated, not g_game.location.hasBeenExerted, not g_game.location.hasBeenExplored]
        # Other player factors
        knownRoles = []
        othersAreActive = []
        othersAreThreats = []
        otherCharacters = []
        otherExhaustionLevels = []
        otherAvailableStats = [0, 0, 0]
        for p in otherPlayers:
            # Construct list of learned / revealed roles, with None for roles that are not revealed
            if p.isRevealed or p.id in self.guessedPlayers:
                knownRoles.append(p.role['id'])
            else:
                knownRoles.append(None)
            # Construct list of booleans indicating which players are active and whether they can attack
            if p.isAbleToAct():
                othersAreActive.append(True)
                if not p.hasAttacked:
                    othersAreThreats.append(True)
                else:
                    othersAreThreats.append(False)
            else:
                othersAreActive.append(False)
                othersAreThreats.append(False)
            # Construct list of other player characters
            otherCharacters.append(p.character['id'])
            # Construct list of other player exhaustion levels
            otherExhaustionLevels.append(p.exhaustionLevel)
            # Total available stats
            if not p.hasInvestigated:
                otherAvailableStats[0] += p.character['ingenuity']
            if not p.hasExerted:
                otherAvailableStats[1] += p.character['resolve']
            if not p.hasExplored:
                otherAvailableStats[2] += p.character['finesse']
        # Assign factors necessary to determine AI action
        factors = {'mode':self.mode, 'room':g_game.location.room['id'], 'availableRoomActions':availableRoomActions, 'roomRequirements':g_game.location.room['requirements'], 'availableStats':availableStats, 'otherAvailableStats':otherAvailableStats, 'role':self.role['id'], 'character':self.character['id'], 'exhaustionLevel':self.exhaustionLevel, 'shouldEscape':self.shouldAiEscape(), 'knownRoles':knownRoles, 'othersAreActive':othersAreActive, 'othersAreThreats':othersAreThreats, 'otherCharacters':otherCharacters, 'otherExhaustion':otherExhaustionLevels}
        ### DECIDE ACTION ###
        if factors['mode'] == 4 and ((not self.hasAttacked and not self.isAnchored) or (self.hasAttacked and self.isAnchored)): # IF AI is DEFENSIVE, lead with attack on a hostile
            # Randomly select a target among the most exhausted other active players AI is hostile towards
            target = getMostExhaustedPlayer(list(filter(lambda p: p.isAbleToAct(), list(map(lambda pid: g_game.lookupPlayerByID(pid), self.isHostileTowards)))))
            # If such a player exists, attack them player
            if target:
                return ('Attack', target)
        elif factors['mode'] == 3 and ((not self.hasAttacked and not self.isAnchored) or (self.hasAttacked and self.isAnchored)): # IF AI is AGGRESSIVE, lead with attack on a vulnerable player
            # Randomly select a target from among the most exhausted other active players
            target = getMostExhaustedPlayer(g_game.getOtherActionablePlayers(self))
            # If such a player exists, attack them player
            if target:
                return ('Attack', target)
        if factors['room'] == 0: # Arena
            if factors['availableRoomActions'][0] and factors['availableStats'][0] > 0: # plumb the wreckage - default first action
                if factors['roomRequirements'][0] <= factors['availableStats'][0] + factors['otherAvailableStats'][0] or self.attemptedToPass:
                    return ('Investigate', None)
            if factors['availableRoomActions'][2] and factors['availableStats'][2] > 0 and (2 in factors['knownRoles'] or self.attemptedToPass): # take the high ground - only worth doing if another player's role has been revealed to be Cloudblessed
                if factors['roomRequirements'][2] <= factors['availableStats'][2] + factors['otherAvailableStats'][2] or self.attemptedToPass:
                    return ('Explore', None)
            if factors['availableRoomActions'][1] and factors['availableStats'][1] > 0 and self.attemptedToPass: # free the blade - only take action if no others are available
                if factors['roomRequirements'][1] <= factors['availableStats'][1] + factors['otherAvailableStats'][1] or self.attemptedToPass:
                    return ('Exert', None)
        elif factors['room'] == 1: # Tower
            if factors['availableRoomActions'][2] and factors['availableStats'][2] > 0: # spring the vaults - default first action
                if factors['roomRequirements'][2] <= factors['availableStats'][2] + factors['otherAvailableStats'][2] or self.attemptedToPass:
                    return ('Explore', None)
            if factors['availableRoomActions'][1] and factors['availableStats'][1] > 0: # interrogate the mirror - default second action
                if factors['roomRequirements'][1] <= factors['availableStats'][1] + factors['otherAvailableStats'][1] or self.attemptedToPass:
                    return ('Exert', None)
            if factors['availableRoomActions'][0] and factors['availableStats'][0] > 0: # break the magic - default third action
                if factors['roomRequirements'][0] <= factors['availableStats'][0] + factors['otherAvailableStats'][0] or (g_game.isCluedIn and 5 <= factors['availableStats'][0] + factors['otherAvailableStats'][0]) or self.attemptedToPass: # Handle case where mirror has already been interrogated successfully
                    return ('Investigate', None)
        elif factors['room'] == 2: # Alley
            if factors['availableRoomActions'][2] and factors['availableStats'][2] > 0: # loot the storefronts - default first action
                if factors['roomRequirements'][2] <= factors['availableStats'][2] + factors['otherAvailableStats'][2] or self.attemptedToPass:
                    return ('Explore', None)
            if factors['availableRoomActions'][1] and factors['availableStats'][1] > 0: # confront the beast - default second action
                if factors['roomRequirements'][1] <= factors['availableStats'][1] + factors['otherAvailableStats'][1] or self.attemptedToPass:
                    return ('Exert', None)
            if factors['availableRoomActions'][0] and factors['availableStats'][0] > 0: # follow the twine - default third action
                if factors['roomRequirements'][0] <= factors['availableStats'][0] + factors['otherAvailableStats'][0] or self.attemptedToPass:
                    return ('Investigate', None)   
            # Attempt to pass early unless AI has already attempted to pass or it will die if it does or if it is Reika
            if not self.attemptedToPass and not self.character['id'] == 0 and not self.exhaustionLevel == 3: 
                return ('Pass', None) 
        elif factors['room'] == 3: # Hall
            if factors['availableRoomActions'][0] and factors['availableStats'][0] > 0: # answer the riddle - default first action
                if factors['roomRequirements'][0] <= factors['availableStats'][0] + factors['otherAvailableStats'][0] or self.attemptedToPass:
                    return ('Investigate', None)
            # If riddle reveals the last player to pass will receive a curse, pass immediately unless AI has already failed to pass or if they will die if they do
            if g_game.location.riddleAnswer == 2 and g_game.location.isRiddleAnswered and not self.attemptedToPass and not self.isAnchored and not self.exhaustionLevel == 3: 
                return ('Pass', None)
            if factors['availableRoomActions'][1] and factors['availableStats'][1] > 0 and ((self.hasRested and self.exhaustionLevel > 1) or self.attemptedToPass): # sit at the hall - do only if you have 2 or more levels of exhaustion and cannot rest
                if factors['roomRequirements'][1] <= factors['availableStats'][1] + factors['otherAvailableStats'][1] or self.attemptedToPass:
                    return ('Exert', None)
            if factors['availableRoomActions'][2] and factors['availableStats'][2] > 0 and (g_game.partySupplies < 4 or self.attemptedToPass): # raid the kitchen - do only if fewer than 4 party supplies remain
                if factors['roomRequirements'][2] <= factors['availableStats'][2] + factors['otherAvailableStats'][2] or self.attemptedToPass:
                    return ('Explore', None)
        elif factors['room'] == 4: # Cradle
            if factors['availableRoomActions'][2] and factors['availableStats'][2] > 0: # forage in the marshland - default first action
                if factors['roomRequirements'][2] <= factors['availableStats'][2] + factors['otherAvailableStats'][2] or self.attemptedToPass:
                    return ('Explore', None)
            if factors['availableRoomActions'][1] and factors['availableStats'][1] > 0: # wish at the well - default second action
                if factors['roomRequirements'][1] <= factors['availableStats'][1] + factors['otherAvailableStats'][1] or self.attemptedToPass:
                    return ('Exert', None)
            if factors['availableRoomActions'][0] and factors['availableStats'][0] > 0: # analyze the music - default third action
                if factors['roomRequirements'][0] <= factors['availableStats'][0] + factors['otherAvailableStats'][0] or self.attemptedToPass:
                    return ('Investigate', None)
        elif factors['room'] == 5: # Cove
            if factors['availableRoomActions'][2] and factors['availableStats'][2] > 0: # search for shelter - default first action
                if factors['roomRequirements'][2] <= factors['availableStats'][2] + factors['otherAvailableStats'][2] or self.attemptedToPass:
                    return ('Explore', None)
            if factors['availableRoomActions'][0] and factors['availableStats'][0] > 0: # interpret the sigils - default second action
                if factors['roomRequirements'][0] <= factors['availableStats'][0] + factors['otherAvailableStats'][0] or self.attemptedToPass:
                    return ('Investigate', None)
            if factors['availableRoomActions'][1] and factors['availableStats'][1] > 0: # navigate the ice - default third action
                if factors['roomRequirements'][1] <= factors['availableStats'][1] + factors['otherAvailableStats'][1] or self.attemptedToPass:
                    return ('Exert', None)
            # Try passing next unless player is the only one remaining or there is only one other player remaining and player has already attempted to pass (preventing Mnanth loops) or if they will die if they do
            numOtherActivePlayers = len(g_game.getOtherActionablePlayers(self))
            if numOtherActivePlayers != 0 and (numOtherActivePlayers != 1 or not self.attemptedToPass) and not self.isAnchored and self.exhaustionLevel != 3:
                return ('Pass', None)
        if not self.hasUsedActive: # May use special actives depending on character
            if factors['character'] == 0 and ((factors['availableRoomActions'][0] and factors['availableStats'][0] > 0) or (factors['availableRoomActions'][1] and factors['availableStats'][1] > 0) or (factors['availableRoomActions'][2] and factors['availableStats'][2] > 0) or (self.hasAttacked and factors['othersAreActive'] != [False, False, False]) or (self.hasRested and self.exhaustionLevel > 0)): # Reika
                return ('Special Active', None) 
            elif factors['character'] == 1 and len(self.inspiration) > 0: # Endemene
                # Prototype first inspiration
                return ('Special Active', self.inspiration[0])
            elif factors['character'] == 2: # Rainee
                # Interrogate first active player
                for i in range(len(otherPlayers)):
                    if factors['othersAreActive'][i] and not factors['knownRoles'][i]:
                        return('Special Active', otherPlayers[i])
            elif factors['character'] == 3 and self.attemptedToPass: # Elvy
                # Guard first active player (only if a pass attempt has already failed)
                for i in range(len(otherPlayers)):
                    if factors['othersAreActive'][i]:
                        return('Special Active', otherPlayers[i])
            elif factors['character'] == 4: # Dredge
                return ('Special Active', None)
            elif factors['character'] == 5 and self.attemptedToPass: # Mantelesse
                # Weird first active player (only if a pass attempt has already failed)
                for i in range(len(otherPlayers)):
                    if factors['othersAreActive'][i]:
                        return('Special Active', otherPlayers[i])
        if factors['room'] == 0 or factors['room'] == 2 or factors['mode'] == 3 or factors['mode'] == 4: # Arena, Alley, or if AI is DEFENSIVE or AGGRESSIVE
            # Rest in this room only if no other players are able to attack or if the AI will die otherwise or if they have attempted to pass already
            if ((not self.hasRested and not self.isAnchored) or (self.hasRested and self.isAnchored)) and factors['exhaustionLevel'] > 0 and (factors['othersAreThreats'] == [False, False, False] or factors['exhaustionLevel'] == 3 or self.attemptedToPass):
                return ('Rest', None)
        elif factors['room'] == 1 or factors['room'] == 3: # Tower, Hall
            # Rest if AI has 3 or more exhaustion or if they have at least 1 and there are still other players able to act or if they have attempted to pass already
            if ((not self.hasRested and not self.isAnchored) or (self.hasRested and self.isAnchored)) and factors['exhaustionLevel'] > 0 and (factors['exhaustionLevel'] == 3 or factors['othersAreActive'] != [False, False, False] or self.attemptedToPass):
                return ('Rest', None)
        elif factors['room'] == 4 or factors['room'] == 5:
            # Rest if able
            if ((not self.hasRested and not self.isAnchored) or (self.hasRested and self.isAnchored)) and factors['exhaustionLevel'] > 0:
                return ('Rest', None)
        if factors['room'] == 0: # Arena
            # Attack the player most likely to die in order to fulfill the requirement to pass from the room
            if not g_game.location.hasBloodBeenDrawn and ((not self.hasAttacked and not self.isAnchored) or (self.hasAttacked and self.isAnchored)):
                # Randomly select a target among the most exhausted other active players
                target = getMostExhaustedPlayer(g_game.getOtherActionablePlayers(self))
                # If such a player exists, attack them player
                if target:
                    return ('Attack', target)
        # Call Upon Family if role is Marloe when things are getting down to the nitty-gritty in a room
        if factors['role'] == 3 and not self.isRevealed and (self.attemptedToPass or factors['room'] == 0 or factors['room'] == 1 or factors['room'] == 3) and not self.isAnchored:
            return ('Reveal Active', None)
        # If AI has tried and failed to pass, attack to either change the situation or expend its last option, resulting in its death
        if ((not self.hasAttacked and not self.isAnchored) or (self.hasAttacked and self.isAnchored)) and self.attemptedToPass:
            # Randomly select a target among the most exhausted other active players (only if a pass attempt has already failed)
            target = getMostExhaustedPlayer(g_game.getOtherActionablePlayers(self))
            # If such a player exists, attack them player
            if target:
                return ('Attack', target)
        # When nothing is left to do, pass
        return ('Pass', None)
    # END DECIDEAIACTION

    """
    pre: called on an AI whenever they would be given the opportunity to escape.
    return: True if AI has already satisfied it's role's win condition. False otherwise.
    """
    def shouldAiEscape(self) -> bool:
        # Load game
        global g_game
        match self.role['name']:
            case 'Mnanth, Whose Heart is Glass':
                if g_game.lookupPlayerByID(self.pactTargetID).isAlive == False:
                    return True
                return False
            case 'Casglowve, the Captive Moon':
                # Choose to escape if tower is broken
                if g_game.isTowerBroken:
                    return True
                return False
            case 'Cloudblessed':
                # Escape if at least 1 other player has already escaped
                numEscapedPlayers = 0
                for p in g_game.allPlayers:
                    if p.hasEscaped:
                            return True
                return False
            case 'Marloe, Don of the Downtrodden':
                # Escape if all other players are cursed, dead, or escaped
                if len(list(filter(lambda p: p.timesCursed == 0 and p.isInDungeon(), self.getOtherPlayers()))) == 0:
                    return True
                return False
            case 'Erstwhile, Collector Supreme':
                # Erstwhile will never try to escape
                return False
            case 'The Fisherwoman':
                # Escape if all other players are dead or escaped
                if len(list(filter(lambda p: p.isInDungeon(), self.getOtherPlayers()))) == 0:
                    return True
                return False
    # END SHOULDAIESCAPE

    """
    pre: called on each active AI at the beginning of the decision phase of each turn if their mode is OPPORTUNISTIC.
    return: True if algorithm determines it is in the AI's best interest to switch modes to AGGRESSIVE. False otherwise.
    """
    def shouldAiAggro(self) -> bool:
        # Load Game
        global g_game
        # Never aggro if unable to attack
        if self.hasAttacked:
            return False
        # Never aggro if win condition has already been fulfilled
        if self.shouldAiEscape():
            return False
        otherActivePlayers = g_game.getOtherActionablePlayers(self)
        # Initialize stats
        healthState = 3 - self.exhaustionLevel
        dmgPotential = 1
        isDesperate = False
        # Become desperate if room is one that can potentially be escaped from (Tower, Alley) or the end of the dungeon is arriving and the key is found and there is a player that cannot be allowed to escape
        if (g_game.location.room['id'] == 1 or g_game.location.room['id'] == 1 or (g_game.roomIndex == 5 and g_game.isKeyFound)) and ((self.role['id'] == 3 and len(list(filter(lambda p: p.timesCursed == 0, self.getOtherPlayers()))) > 0) or (self.role['id'] == 5 and len(list(filter(lambda p: p.timesSeenHeart > 0, self.getOtherPlayers()))) > 0)):
            isDesperate = True
        # In the Fisherwoman's case, should also become desperate if a player has seen the heart twice
        elif self.role['id'] == 5 and len(list(filter(lambda p: p.timesSeenHeart == 2, self.getOtherPlayers()))) > 0:
            isDesperate = True
        # Gain an additional dmg potential if AI is Reika and can anchor
        if self.character['id'] == 0 and not self.hasUsedActive:
            dmgPotential += 1
        # Gain an additional dmg potential if role is Fisherwoman and can reveal
        if self.role['id'] == 5 and not self.isRevealed:
            dmgPotential += 1
        # Calculate enemy stats
        enemyHealthStates = 0
        enemyDmgPotential = 0
        for p in otherActivePlayers:
            enemyHealthStates += 3 - p.exhaustionLevel
            # Factor in whether enemy is able to rest
            if not p.hasRested:
                enemyHealthStates += 2
            # Add enemy dmg potential if enemy is able to attack
            if not p.hasAttacked:
                enemyDmgPotential += 1
            # Add an additional dmg potential if enemy is Reika and can anchor
            if p.character['id'] == 0 and not p.hasUsedActive:
                enemyDmgPotential += 1
        # Remove one enemy dmg potential if AI can kill an enemy
        for p in otherActivePlayers:
            if p.exhaustionLevel == 1:
                enemyDmgPotential -= 1
        # Remove an enemy dmg potential for each enemy if role is Fisherwoman and can reveal
        if self.role['id'] == 5 and not self.isRevealed:
            for p in otherActivePlayers:
                enemyDmgPotential -= 1
        # Add two health state if you are able to rest and your health state before is already greater than the enemy damage potential
        if not self.hasRested and healthState - enemyDmgPotential > 0:
            healthState += 2
        # add 10 to health state if desperate
        if isDesperate:
            healthState += 10
        # Final calculation
        resultingHealth = healthState - enemyDmgPotential
        if resultingHealth > 0 and resultingHealth > enemyHealthStates - dmgPotential:
            return True
        return False
    # END SHOULDAIAGGRO

    ### PLAYER: ROLE MECHANICS ###

    """
    pre: called on all players at the end of the game.
    post: announces whether a player won or lost, depending on whether their role's win condition was fulfilled.
    """
    def checkWinConditions(self):
        # Load game
        global g_game
        match self.role['name']:
            case 'Mnanth, Whose Heart is Glass':
                if not self.hasEscaped:
                    # Loss output 1 for player
                    if self.isPlayer():
                        g_game.displayText('You failed to escape. You lose the game.', shouldOverride=True)
                        return
                    # Loss output 1 for AI
                    g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', failed to escape. They lose the game.', shouldOverride=True)
                    return
                for p in g_game.allPlayers:
                    if g_game.lookupPlayerByID(self.pactTargetID).hasEscaped == True:
                        # Loss output 2 for player
                        if self.isPlayer():
                            g_game.displayText('You failed to prevent your sworn enemy from escaping the dungeon. You lose the game.', shouldOverride=True)
                            return
                        # Loss output 2 for AI
                        g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', failed to eliminate their sworn enemy, ' + g_game.lookupPlayerByID(self.pactTargetID).character['shortName'] + '. They lose the game.', shouldOverride=True)
                        return
                # Win output for player
                if self.isPlayer():
                    g_game.displayText('You managed to eliminate your sworn enemy and escape to tell the tale. You win the game.', shouldOverride=True)
                    self.hasWon = True # for TEST mode only
                    return
                # Win output for AI
                g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', managed to eliminate their sworn enemy, ' + g_game.lookupPlayerByID(self.pactTargetID).character['shortName'] + ', and escape to tell the tale. They win the game.', shouldOverride=True)
                self.hasWon = True # for TEST mode only
                return
            case 'Casglowve, the Captive Moon':
                if not self.hasEscaped:
                    # Loss output 1 for player
                    if self.isPlayer():
                        g_game.displayText('You failed to escape. You lose the game.', shouldOverride=True)
                        return
                    # Loss output 1 for AI
                    g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', failed to escape. They lose the game.', shouldOverride=True)
                    return
                for p in g_game.allPlayers:
                    if not g_game.isTowerBroken:
                        # Loss output 2 for player
                        if self.isPlayer():
                            g_game.displayText('You failed to break the Tower and free your love. You lose the game.', shouldOverride=True)
                            return
                        # Loss output 2 for AI
                        g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', failed to break the tower and free their love. They lose the game.', shouldOverride=True)
                        return
                # Win output for player
                if self.isPlayer():
                    g_game.displayText('You managed to break the tower, free your love, and escape. You win the game.', shouldOverride=True)
                    self.hasWon = True # for TEST mode only
                    return
                # Win output for AI
                g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', managed to break the tower, free their love, and escape. They win the game.', shouldOverride=True)
                self.hasWon = True # for TEST mode only
                return
            case 'Cloudblessed':
                numEscapedPlayers = 0
                for p in g_game.allPlayers:
                    if p.hasEscaped:
                        numEscapedPlayers += 1
                        if numEscapedPlayers >= 2:
                            # Win output for player
                            if self.isPlayer():
                                g_game.displayText('Half or more of the party managed to escape. You win the game.', shouldOverride=True)
                                self.hasWon = True # for TEST mode only
                                return
                            # Win output for AI
                            g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', managed to see half or more of the party to freedom. They win the game.', shouldOverride=True)
                            self.hasWon = True # for TEST mode only
                            return
                # Loss output for player
                if self.isPlayer():
                    g_game.displayText('Fewer than half of the party managed to escape. You lose the game.', shouldOverride=True)
                    return
                # Loss output for AI
                g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', was not able to see half or more of the party to freedom. They lose the game.', shouldOverride=True)
                return
            case 'Marloe, Don of the Downtrodden':
                if not self.hasEscaped:
                    # Loss output 1 for player
                    if self.isPlayer():
                        g_game.displayText('You failed to escape. You lose the game.', shouldOverride=True)
                        return
                    # Loss output 1 for AI
                    g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', failed to escape. They lose the game.', shouldOverride=True)
                    return
                for p in self.getOtherPlayers():
                    if p.hasEscaped and p.timesCursed == 0:
                        # Loss output 2 for player
                        if self.isPlayer():
                            g_game.displayText('You failed to prevent adventurers from escaping your grasp without being cursed. You lose the game.', shouldOverride=True)
                            return
                        # Loss output 2 for AI
                        g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', failed to prevent adventurers from escaping their grasp without being cursed. They lose the game.', shouldOverride=True)
                        return
                # Win output for player
                if self.isPlayer():
                    g_game.displayText('You managed to escape, which no others managed to do without being cursed. You win the game.', shouldOverride=True)
                    self.hasWon = True # for TEST mode only
                    return
                # Win output for AI
                g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', escaped while preventing any adventurers from doing the same without being cursed. They win the game.', shouldOverride=True)
                self.hasWon = True # for TEST mode only
                return
            case 'Erstwhile, Collector Supreme':
                if self.numRoomsVisited == 6:
                    # Win output for player
                    if self.isPlayer():
                        g_game.displayText('You visited every room in the dungeon. You win the game.', shouldOverride=True)
                        self.hasWon = True # for TEST mode only
                        return
                    # Win output for AI
                    g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', visited every room in the dungeon. They win the game.', shouldOverride=True)
                    self.hasWon = True # for TEST mode only
                    return
                # Loss output for player
                if self.isPlayer():
                    g_game.displayText('You did not visit every room in the dungeon before expiring. You lose the game.', shouldOverride=True)
                    return
                # Loss output for AI
                g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', did not visit every room in the dungeon before expiring. They lose the game.', shouldOverride=True)
                return
            case 'The Fisherwoman':
                if self.timesSeenHeart == 0:
                    # Loss output 1 for player
                    if self.isPlayer():
                        g_game.displayText('You failed to see the heart for yourself. You lose the game.', shouldOverride=True)
                        return
                    # Loss output 1 for AI
                    g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', failed to see the heart for themself. They lose the game.', shouldOverride=True)
                    return
                for p in self.getOtherPlayers():
                    if p.hasEscaped and p.timesSeenHeart > 0:
                        # Loss output 2 for player
                        if self.isPlayer():
                            g_game.displayText('You failed to prevent observers of the Wandering Heart from escaping. You lose the game.', shouldOverride=True)
                            return
                        # Loss output 2 for AI
                        g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', failed to prevent observers of the Wandering Heart from escaping. They lose the game.', shouldOverride=True)
                        return
                # Win output for player
                if self.isPlayer():
                    g_game.displayText('No observers of the Wandering Heart managed to escape, while you managed to observe the Heart for yourseelf. You win the game.', shouldOverride=True)
                    self.hasWon = True # for TEST mode only
                    return
                # Win output for AI
                g_game.displayText(self.character['shortName'] + ', whose role was ' + self.role['shortName'] + ', observed the Wandering Heart and preventing any other observers from escaping. They win the game.', shouldOverride=True)
                self.hasWon = True # for TEST mode only
                return
    # END CHECKWINCONDITIONS

    """
    pre: called on all active players when circumstances are met that could result in a role reveal.
    param: role, the role for which circumstances have been met to reveal
    post: if the player has param:role as their role and is not warded, announces their role and calls method:reveal and method:quip
    """
    def triggerReveal(self, role:str):
        # Load Game
        global g_game
        # Only trigger if self has the role that is being tested for and if self has not already been revealed
        if self.role['name'] == role and not self.isRevealed:
            # If player is warded, prevent reveal unless reveal is intentional or role is Cloudblessed
            if self.isWarded and role != 'Marloe, Don of the Downtrodden' and role != 'Cloudblessed':
                # Report succesful warding (if self is player)
                self.ward()
            else:
                # Report reveal
                if self.isPlayer():
                    g_game.displayText('Your role was revealed to be ' + self.role['shortName'] + '.')
                else:
                    g_game.displayText(self.character['shortName'] + '\'s role was revealed to be ' + self.role['shortName'] + '.')
                # Mark as revealed
                self.isRevealed = True
                # Perform reveal effect
                self.reveal()
                # Quip
                self.quip()
    # END TRIGGERREVEAL

    """
    pre: should only be called on a player when the conditions have been met for their role to be revealed.
    post: reveal effect corresponding to the player's role is carried out.
    """
    def reveal(self):
        # Load game
        global g_game
        match self.role['name']:
            case 'Mnanth, Whose Heart is Glass':
                # Bar way
                g_game.isWayBarred = True
                # Report outcome
                g_game.displayText('Pillars of glass burst up from the ground to deny exit to all who remain in ' + g_game.location.room['name'] + '. They will not yield but for a lone player.')
            case 'Casglowve, the Captive Moon':
                # Pass immediately, ignoring all restrictions
                self.hasPassed = True
                # Report outcome if player has this role
                if self.isPlayer():
                    g_game.displayText('As you exit the room, born aloft on wings of moonlight, you feel a surge of wakefulness flow into you.')
                # Gain the benefit of a rest
                self.rest()
                # Each other active player gains exhaustion
                for p in self.getOtherPlayers():
                    if p.isAbleToAct():
                        # Report outcome if an ai has this role
                        if p.isPlayer():
                            g_game.displayText('As ' + self.character['shortName'] + ' exits the room, born aloft on wings of moonlight, you feel a wave of exhaustion hit you. A part of you was taken to fuel their flight.')
                        # Gain exhaustion
                        p.gainExhaustion()
            case 'Cloudblessed':
                # Mark Cloudblessed as revealed in the current room
                g_game.location.cloudblessedRevealed = True
                # Report outcome
                if self.isPlayer():
                    g_game.displayText('A hallowed mist seeps into the room in the wake of your fall.')
                else:
                    g_game.displayText('A hallowed mist seeps into the room in the wake of ' + self.character['shortName'] + '\'s fall.')
            case 'Marloe, Don of the Downtrodden':
                # Report outcome
                if self.isPlayer():
                    g_game.displayText('You call upon the power of the Fae House Marloethien, guarding all players from attack this turn.')
                else:
                    g_game.displayText(self.character['shortName'] + ' calls upon the power of the Fae House Marloethien, guarding all players from attack this turn.')
                # Add other active players to guard targets and self to guard sources
                for p in g_game.allPlayers:
                    if p.isAbleToAct():
                        g_game.guardTargets.append(p.id)
                        g_game.guardSources.append(self.id)
                # Mark that Marloe was revealed this turn, so anyone successfully guarded can receive a curse
                g_game.marloeRevealedThisTurn = True
            case 'Erstwhile, Collector Supreme':
                # Report outcome
                g_game.displayText('Calming spores descend on the stricken party, granting everyone the strength to fight on a little longer.')
                # Each active player gains the benefit of a rest
                for p in self.getOtherPlayers():
                    if p.isAbleToAct():
                        p.rest()
            case 'The Fisherwoman':
                # Report outcome
                if self.isPlayer():
                    g_game.displayText('The brutality of your attack hits the other players like an avalanche, leaving them too stunned to act during their next turn.')
                elif g_game.player:
                    if g_game.player.isAbleToAct():
                        # Special print for when player is not self but is able to act
                        g_game.displayText('The brutality of ' + self.character['shortName'] + '\'s attack hits you and the other players like an avalanche, leaving you too stunned to act during your next turn.')   
                    else:
                        g_game.displayText('The brutality of  ' + self.character['shortName'] + '\'s attack hits the other players like an avalanche, leaving them too stunned to act during their next turn.')
                # Stun players
                for p in self.getOtherPlayers():
                    if p.isAbleToAct():
                        p.isStunned = True
                # Replenish attack action
                self.hasAttacked = False
    # END REVEAL

    ### PLAYER: CHARACTER MECHANICS ###

    """
    pre: should only be called on a player when their role is revealed.
    post: print a character- and role-specific quip.
    """
    def quip(self):
        # Quip only if self is an AI
        if not self.isPlayer():
            # Lookup character's reveal quip by id
            g_game.displayText(self.character['shortName'] + ': "' + self.character['revealQuips'][self.role['id']] + '"')
    # END QUIP

    """
    pre: should only be called on a player whose character is Reika when they pass.
    post: if there are other players still in play, return Reika to play.
    """
    def undertow(self):
        # Return to play
        self.hasPassed = False
        # Report outcome
        if self.isPlayer():
            g_game.displayText('The undertow of the Piece of Time you wear drags you back to the moment before you left this room behind you. There is still more to do.')
        else:
            g_game.displayText('The undertow of the Piece of Time ' + self.character['shortName'] + ' wears drags her back to the moment before she left this room behind her. There is still more to do.')
    # END UNDERTOW

    """
    pre: should only be called under specific circumstances on a player whose character is Endemene.
    param: inspiration, a string indicating what prototype Endemene has been inspired to be able to produce.
    post: param:inspiration is added to Endemene's list of available inspirations.
    """
    def inspire(self, inspiration:str):
        # Ignore if this inspiration has already been obtained
        if inspiration not in self.hasPrototyped and inspiration not in self.inspiration:
            # Add inspiration
            self.inspiration.append(inspiration)
            # Report outcome
            match inspiration:
                case 'Wings': # # Next time you would fail to pass, pass without instead
                    if self.isPlayer():
                        g_game.displayText('You are inspired in your isolation. You may now prototype wings.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' is inspired by her isolation.')
                case 'Shield': # Next time you would be attacked and are not guarded, prevent the attack 
                    if self.isPlayer():
                        g_game.displayText('You are inspired by the cruel workings of the deadly sword. You may now prototype a shield.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' is inspired by the cruel workings of the deadly sword.')
                case 'Lens': # Next time you rest, see the following for each player that rests at the same time: the role they have, the role another player has, and a role no player has. You will not know which is which
                    if self.isPlayer():
                        g_game.displayText('You are inspired by the sight of the heart in dreams. You may now prototype a lens.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' is inspired by something seen in her dreams.')
                case 'Net':
                    if self.isPlayer(): # The next time you attack a player, that player skips their next action
                        g_game.displayText('You are inspired by the imminent threat upon your life. You may now prototype a net.')
                    else:
                        g_game.displayText(self.character['shortName'] + ' is inspired by the imminent threat upon her life.')
    # END INSPIRE

    """
    pre: should only be called on a player whose character is Elvy when they have been attacked or have taken the attack or guard action.
    post: warded status is removed
    """
    def loseWard(self):
        # Remove ward
        self.isWarded = False
        # Report outcome
        if self.isPlayer():
            g_game.displayText('Your conspicuous action exposes you for what you really are. Your ward evaporates off your body.')
        else:
            g_game.displayText('Their conspicuous action exposes ' + self.character['shortName'] + ' for what they really are. Their ward evaporates off their body.')
    # END LOSEWARD

    """
    pre: should only be called in place of method:reveal on a player whose character is Elvy when their role would be revealed and that role is not Cloudblessed or Marloe.
    post: if player is a PC, they are informed about the warding.
    """
    def ward(self):
        # Report outcome when player would be revealed
        if self.isPlayer():
            g_game.displayText('The ward you wear like a skin protects you from all scrutiny. Your role is not revealed.')
    # END WARD

    """
    pre: should only be called during a rest action, on a resting player whose character is Dredge.
    post: the player receives a randomly chosen benefit.
    """
    def discover(self):
        # Load game
        global g_game
        #roll a d10
        discoveryRoll = rng.randint(1,10)
        # Carry out outcome
        if discoveryRoll < 5:
            # Add 1 party supplies
            g_game.partySupplies += 1
            # Report outcome
            if self.isPlayer():
                g_game.displayText('You discovered 1 supplies at your place of rest.')
            else:
                g_game.displayText(self.character['shortName'] + ' discovered 1 supplies at his place of rest.')
        elif discoveryRoll >= 5 and discoveryRoll < 7:
            # Add 2 party supplies
            g_game.partySupplies += 2
            # Report outcome
            if self.isPlayer():
                g_game.displayText('You discovered 2 supplies at your place of rest.')
            else:
                g_game.displayText(self.character['shortName'] + ' discovered 2 supplies at his place of rest.')
        elif discoveryRoll == 7:
            # Add 3 party supplies
            g_game.partySupplies += 3
            # Report outcome
            if self.isPlayer():
                g_game.displayText('You discovered 3 supplies at your place of rest.')
            else:
                g_game.displayText(self.character['shortName'] + ' discovered 3 supplies at his place of rest.')
        else:
            # Add key
            g_game.isKeyFound = True
            # Report outcome
            if self.isPlayer():
                g_game.displayText('You discovered a mysterious key at your place of rest.')
            else:
                g_game.displayText(self.character['shortName'] + ' discovered a mysterious key at his place of rest.')
    # END DISCOVER

    """
    pre: should only be called during a rest action, on a resting player whose character is Rainee.
    post: resting player is informed as to the identity of one role in the game that is not possessed by a currently active player, unless they have already been informed about every role they can be in this way.
    """
    def unravel(self):
        # Load game
        global g_game
        # Load roles
        global g_roles
        # Create list of roles that have not already been unraveled and that are not currently in play
        rolesInPlay = list(map(lambda p: p.role, g_game.getActionablePlayers()))
        uniqueRolesNotInPlay = list(filter(lambda r: r not in rolesInPlay and r['id'] not in self.unraveledRoles, g_roles))
        # If no roles qualify, report this for player
        if len(uniqueRolesNotInPlay) == 0:
            if self.isPlayer():
                g_game.displayText('Every role either is in the room with you or has been seen by you before in dreams. You learn nothing from this dream.')
        # Otherwise select a role at random to unravel
        else:
            unraveledRole = rng.sample(uniqueRolesNotInPlay, 1)[0]
            # Report outcome if self is player
            if self.isPlayer():
                g_game.displayText('In dreams, you see the face of a role that is alien to you. With nothing to be said about the dungeon as a whole, you wake knowing ' + unraveledRole['shortName'] + ' was not in the room with you as you slept.')
            # Add role to list of unraveled roles
            self.unraveledRoles.append(unraveledRole['id'])
    # END UNRAVEL

    """
    pre: should only be called after the decision phase of each turn sequence, on an active player whose character is Mantelesse if all players took the same action.
    param: action, a string indicating which action the players united to take.
    post: all active players receive a benefit depending on what param:action was taken. 
    """
    def unite(self, action:str):
        # Load game
        global g_game
        # Initialize room action tracker boolean
        isRoomAction = False
        match action:
            # If it's the attack action, each active player gains a level of exhaustion
            case 'Attack':
                # Report outcome
                if self.isPlayer():
                    g_game.displayText('Every player chose the attack action. Charged by your influence and by their common goal, all players gain a level of exhaustion from the intensity of the struggle.')
                else:
                    g_game.displayText('Every player chose the attack action. Charged by ' + self.character['shortName'] + '\'s influence and by their common goal, all players gain a level of exhaustion from the intensity of the struggle.')
                for p in g_game.allPlayers:
                    if p.isAbleToAct():
                        # Gain exhaustion
                        p.gainExhaustion()
            # If it's the rest action, gain 2 party supplies
            case 'Rest':
                # Report outcome
                if self.isPlayer():
                    g_game.displayText('Every player chose the rest action. Charged by your influence and by their common goal, all find their party supplies can be stretched just a little bit more.')
                else:
                    g_game.displayText('Every player chose the rest action. Charged by ' + self.character['shortName'] + '\'s influence and by their common goal, all find their party supplies can be stretched just a little bit more.')
                g_game.partySupplies += 2
            # If it's a room action, add 1 to the total
            case 'Investigate':
                g_game.investigateTotal += 1
                # Mark as room action
                isRoomAction = True
            case 'Exert':
                g_game.exertTotal += 1
                # Mark as room action
                isRoomAction = True
            case 'Explore':
                g_game.exploreTotal += 1
                # Mark as room action
                isRoomAction = True
        if isRoomAction:
        # Report outcome for room action
            if self.isPlayer():
                g_game.displayText('Every player chose to take the same room action. Charged by your influence and by their common goal, all find their efforts mean just that little bit more.')
            else:
                g_game.displayText('Every player chose to take the same room action. Charged by ' + self.character['shortName'] + '\'s influence and by their common goal, all find their efforts mean just that little bit more.')
    # END UNITE
# END CLASS PLAYER

### GLOBAL: CLASS LOCATION ###

class Location:
    def __init__ (self, room):
        self.room = room
        self.hasBeenInvestigated = False
        self.hasBeenExerted = False
        self.hasBeenExplored = False
        self.turnCounter = 0 # for the cove only
        self.hasBloodBeenDrawn = False # for the arena only
        self.riddleAnswer = rng.sample([1,2], 1)[0] # for the hall only
        self.isRiddleAnswered = False # for the hall only
        self.cloudblessedRevealed = False
    # END __INIT__

    """
    pre: should be called at the end of each turn sequence, if one or more players attempted to pass.
    param: players, the list of players that attempted to pass this turn.
    post: if no restrictions prevent them from doing so, all players in param:players pass. If a player has prototyped wings, they pass ignoring any restrictions. 
        If a player is prevented from passing due to a restriction, if there are no actions available to them other than passing, they will die. 
        If Endemene is prevented from passing, she will become inspired to prototype wings.
        If the players in param:players are the first or last batch to pass in the Hall, depending on the randomly generated riddle answer, they will be cursed.
    """
    def passPlayers(self, players:list):
        # Load game
        global g_game
        # Initialize validity of players' passing
        validPass = True
        match self.room['id']:
            case 0:
                # If no one has died in the room, no one may pass
                if not self.hasBloodBeenDrawn:
                    validPass = False
                    # Report failure
                    for p in players:
                        if p.isPlayer():
                            g_game.displayText('You are turned away at the gate when you try to leave the arena. Blood must be drawn before anyone is allowed to proceed.')
                        else:
                            g_game.displayText(p.character['shortName'] + ' is turned away at the gate when they try to leave the arena. Blood must be drawn before anyone is allowed to proceed.')
            case 1:
                # If fewer than two players are trying to pass, no one may pass
                if len(players) > 1:
                    validPass = False
                    # Report failure
                    for p in players:
                        if p.isPlayer():
                            g_game.displayText('The passageway by which one can squeeze down into the sublevels of the tower and onto the next room is narrow enough to only comfortably admit one person. Trying to leave at the same time another player does gets you nowhere.')
                        else:
                            g_game.displayText('The passageway by which one can squeeze down into the sublevels of the tower and onto the next room is narrow enough to only comfortably admit one person. Trying to leave at the same time another player does gets ' + p.character['shortName'] + ' nowhere.')
            case 3: # the hall
                # Determine which of the two randomly generated decorums is in play
                if self.riddleAnswer == 1:
                    # If passing players are the first to do so, they become cursed
                    isFirstBatch = True
                    otherPlayers = list(filter(lambda p: p not in players, g_game.allPlayers))
                    for p in otherPlayers:
                        # If a player not currently passing has passed, the currently passing players are not the first batch
                        if p.hasPassed:
                            isFirstBatch = False
                    if isFirstBatch:
                        for p in players:
                            # Player becomes cursed
                            p.timesCursed += 1
                            # Report outcome
                            if p.isPlayer():
                                g_game.displayText('In line with the decorum of the Mirthless Queen\'s court, you are among the first to leave the hall, and so you take with you a curse.')
                            else:
                                g_game.displayText('In line with the decorum of the Mirthless Queen\'s court, ' + p.character['shortName'] + ' is among the first to leave the hall, and so they take with them a curse.')
                else:
                    # If passing players are the last to do so, they become cursed
                    isLastBatch = True
                    otherPlayers = list(filter(lambda p: p not in players, g_game.allPlayers))
                    for p in otherPlayers:
                        # If a player not currently passing has not passed, the currently passing players are not the last batch
                        if not p.hasPassed:
                            isLastBatch = False
                    if isLastBatch:
                        for p in players:
                            # Player becomes cursed
                            p.timesCursed += 1
                            # Report outcome
                            if p.isPlayer():
                                g_game.displayText('In line with the decorum of the Mirthless Queen\'s court, you are among the last to leave the hall, and so you take with you a curse.')
                            else:
                                g_game.displayText('In line with the decorum of the Mirthless Queen\'s court, ' + p.character['shortName'] + ' is among the last to leave the hall, and so they take with them a curse.')
            case 4:
                # Report outcome
                for p in players:
                    if p.isPlayer():
                        g_game.displayText('Although the cradle was idyllic, the process to extricate yourself from it is anything but. You must fight and strain every inch of the way through miles of foliage that clings to you and rot that makes your head swim.')
                    else:
                        g_game.displayText('Although the cradle was idyllic, the process to extricate yourself from it is anything but. ' + p.character['shortName'] + ' must fight and strain every inch of the way through miles of foliage that clings to them and rot that makes their head swim.')
                # Each passing player gains exhaustion
                _ = [p.gainExhaustion() for p in players]

            case 5:
                # If fewer than two players are trying to pass, no one may pass
                if len(players) < 2:
                    validPass = False
                    # Report failure
                    for p in players:
                        if p.isPlayer():
                            g_game.displayText('The path along the cove is treacherous, and the storm makes it more so. Without at least one other player to help you on the way, you are forced to turn back.')
                        else:
                            g_game.displayText('The path along the cove is treacherous, and the storm makes it more so. Without at least one other player to help them on the way, ' + p.character['shortName'] + ' is forced to turn back.')
        # Prevent passing if way is barred
        if g_game.isWayBarred:
            validPass = False
            # Report outcome
            for p in players:
                if p.isPlayer():
                    g_game.displayText('You strain and strain, but the glass blockade holds firm.')
                else:
                    g_game.displayText(p.character['shortName'] + '  strains and strains, but the glass blockade holds firm.')        
        if not validPass:
            # If there is only player able to act and that player is Endemene, trigger inspiration
            actionablePlayers = g_game.getActionablePlayers()
            if len(actionablePlayers) == 1:
                p = actionablePlayers[0]
                if p.character['id'] == 1:
                    actionablePlayers[0].inspire('Wings')
            # Give Endemene a free pass if she has prototyped Wings
            for p in players:
                if 'Wings' in p.prototypes:
                    # Remove from list of prototypes
                    p.prototypes.remove('Wings')
                    # Report outcome
                    if p.isPlayer():
                        g_game.displayText('For a glorious moment, your wings carry you over the room\'s dangers, allowing you o leave it behind you before smoke begins to billow from the mechanism and you are deposited unceremoniously on the ground.')
                    else:
                        g_game.displayText('For a glorious moment, ' + p.character['shortName'] + '\'s wings carry her over the room\'s dangers, allowing her to leave it behind her before smoke begins to billow from the mechanism and she is deposited unceremoniously on the ground.')
                    # Mark pass as valid
                    validPass = True
            # Mark each player as having attempted to pass, for use in AI decisionmaking
            for p in players:
                p.attemptedToPass = True
            # If no action is available to a passing player except passing, that player dies due to inability to proceed
            for p in players:
                if p.isAbleToAct():
                    # Initialize check var
                    isOptionOtherThanPass = False
                    # Begin checking options
                    if not p.hasAttacked and len(g_game.getOtherActionablePlayers(p)) > 0:
                        #print('Found valid action: attack') # DEBUG PRINT
                        isOptionOtherThanPass = True
                        break
                    if not p.hasRested and p.exhaustionLevel > 0:
                        #print('Found valid action: rest') # DEBUG PRINT
                        isOptionOtherThanPass = True
                        break
                    if not p.hasInvestigated and not g_game.location.hasBeenInvestigated:
                        #print('Found valid action: investigate') # DEBUG PRINT
                        isOptionOtherThanPass = True
                        break
                    if not p.hasExerted and not g_game.location.hasBeenExerted:
                        #print('Found valid action: exert') # DEBUG PRINT
                        isOptionOtherThanPass = True
                        break
                    if not p.hasExplored and not g_game.location.hasBeenExplored:
                        #print('Found valid action: explore') # DEBUG PRINT
                        isOptionOtherThanPass = True
                        break
                    if not p.hasUsedActive:
                        match p.character['active']:
                            case 'Anchor':
                              pass
                            case 'Prototype':
                                if len(p.inspiration) > 0:
                                    #print('Found valid action: prototype') # DEBUG PRINT
                                    isOptionOtherThanPass = True
                                    break
                            case 'Interrogate':
                                if len(list(map(lambda q: q.isAbleToAct() and not q.isRevealed, p.getOtherPlayers()))) > 0:
                                    #print('Found valid action: interrogate') # DEBUG PRINT
                                    isOptionOtherThanPass = True
                                    break
                            case 'Guard':
                                if len(g_game.getOtherActionablePlayers(p)) > 0:
                                    #print('Found valid action: guard') # DEBUG PRINT
                                    isOptionOtherThanPass = True
                                    break
                            case 'Scout':
                                    #print('Found valid action: scout') # DEBUG PRINT
                                    isOptionOtherThanPass = True
                                    break
                            case 'Weird':
                                if len(g_game.getOtherActionablePlayers(p)) > 0:
                                    #print('Found valid action: weird') # DEBUG PRINT
                                    isOptionOtherThanPass = True
                                    break
                    if p.role['id'] == 3 and not p.isRevealed:
                        #print('Found valid action: call upon the family') # DEBUG PRINT
                        isOptionOtherThanPass = True
                        break
                    # All options have been checked, kill player if none were viable
                    if not isOptionOtherThanPass:
                        if p.isPlayer():
                            g_game.displayText('Unable to proceed to the next room and unable to take another action, you slowly waste away until eventually you succumb to the darkness of oblivion.')
                        else:
                            g_game.displayText('Unable to proceed to the next room and unable to take another action, ' + p.character['shortName'] + ' slowly wastes away until eventually they succumb to the darkness of oblivion.')   
                        # Player dies
                        p.die()
        if validPass:
            # Pass players
            _ = [p.passAction() for p in players]
            # Carry out Cloudblessed delayed trigger if necessary
            attemptCloudblessedRevive()
    # END PASSPLAYERS

    """
    pre: should be called exactly once during each turn sequence.
    param: total, the total number of points of ingenuity contributed by all players that took the investigate room action this turn.
    post: if param: total is high enough to succeed the current room's requirements, the party is rewarded in a matter suited to the current room.
    """
    def investigate(self, total:int):
        # Load game
        global g_game
        # Calculate discount for Breaking the Magic if the mirror has been successfully interrogated
        discount = 0
        if g_game.isCluedIn and self.room['id'] == 1:
            discount = 2
        # Report failure
        if total < self.room['requirements'][0] - discount:
            # Calculate discount for if mirror was successfully interrogated
            g_game.displayText('The party failed to ' + self.room['actions'][0] + ' (' + str(total) + ' Ingenuity contributed, ' + str(self.room['requirements'][0] - discount) + ' needed).')
        # Report success and carry out outcome
        else:
            g_game.displayText('The party was able to ' + self.room['actions'][0] + ' (' + str(total) + ' Ingenuity contributed, ' + str(self.room['requirements'][0] - discount) + ' needed).')
            # Update room to disallow future attempts to investigate
            self.hasBeenInvestigated = True
            # Carry out result
            match self.room['actions'][0]:
                case 'Plumb the Wreckage':
                    g_game.displayText('Your careful search rewards you with 2 supplies found among the bodies and scrap.')
                    # Add supplies
                    g_game.partySupplies += 2
                case 'Break the Magic':
                    g_game.displayText('With the removal of a single brick, marked with a symbol pointed to by a long string of clues, the tower begins to crumble around you. Acting quickly, you all manage to escape in time.')
                    # Exhaust players that are in the room when the tower breaks
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.gainExhaustion()
                    # Mark tower as broken
                    g_game.isTowerBroken = True
                    g_game.displayText('Left behind in the place where the Tower\'s highest reaches had stood is another vault, suspended still in midair. As the party looks on, the door to the vault turns, then opens. From within, pale moonlight spills forth, and the light is in the visage of a woman. She descends to you, identifying herself as the physical embodiment of Casglowve. She intends to leave this dungeon right now, and she will take the most exhausted player with her.')
                    # Select random player from among most exhausted players
                    randomPlayer = getMostExhaustedPlayer(g_game.getActionablePlayers())
                    # Check if a player was found since exhaustion could have killed all remaning players
                    if randomPlayer:
                        # If random player is the player, give them the choice to escape
                        if randomPlayer.isPlayer():
                            g_game.displayText('You have been chosen from among the most exhausted players. Will you choose to escape?')
                            # Set input for player to choose Y/N from
                            g_game.setYNInput(g_game.getCasglowveOffer)
                        else:
                            # Otherwise decide choice of AI
                            shouldEscape = randomPlayer.shouldAiEscape()
                            if shouldEscape:
                                g_game.displayText(randomPlayer.character['shortName'] + ' was chosen from among the most exhausted players. They chose to accept the offer and escape.')
                                # AI escapes
                                randomPlayer.escape()
                            else:
                                g_game.displayText(randomPlayer.character['shortName'] + ' was chosen from among the most exhausted players. They chose to decline the offer and remain in their exhaustion.')
                            # Advance stack
                            g_game.advanceStack()
                    else:
                        g_game.displayText('Unfortunately no players remain alive.')
                case 'Follow the Twine':
                    # Roll a D3. On a 1, a random player is cursed. On a 2, all players immediately enter a new room. On a 3, a random player escapes.
                    g_game.displayText('You expertly navigate the twists and turns of the twine and in following it, you come to understand the true nature of the alley as a fulcrum of potential. Chaos, in a word. ')
                    g_game.displayText('What you find at the end of the path is as unexpected for you as it no doubt was for the layer of the twine, if they even encountered the same fate:')
                    randomFate = rng.randint(1,3)
                    match randomFate:
                        case 1:
                            # Choose a random player from among those able to act
                            playersAbleToAct = []
                            for p in g_game.allPlayers:
                                if p.isAbleToAct():
                                    playersAbleToAct.append(p)
                            # If such a player exists
                            if len(playersAbleToAct) > 0:
                                randomPlayerIndex = rng.randint(0,len(playersAbleToAct)-1)
                                randomPlayer = playersAbleToAct[randomPlayerIndex]
                                # Curse player
                                randomPlayer.timesCursed += 1
                                # Output result for player
                                if randomPlayer.id == 1:
                                    g_game.displayText('A vision so densely packed with data as to be physically hazardous leaps from the well of darkness the twine drops into and plants itself inside your head. You become cursed.')
                                # Output result for AI:
                                else:
                                    g_game.displayText('A vision so densely packed with data as to be physically hazardous leaps from the well of darkness the twine drops into and plants itself inside ' + randomPlayer.character['shortName'] + '\'s head. They become cursed.')
                        case 3:
                            # Choose a random player from among those able to act
                            playersAbleToAct = []
                            for p in g_game.allPlayers:
                                if p.isAbleToAct():
                                    playersAbleToAct.append(p)
                            # If such a player exists
                            if len(playersAbleToAct) > 0:
                                randomPlayerIndex = rng.randint(0,len(playersAbleToAct)-1)
                                randomPlayer = playersAbleToAct[randomPlayerIndex]
                                # Player escapes
                                randomPlayer.escape()
                                # Output result for player
                                if randomPlayer.id == 1:
                                    g_game.displayText('A whip of cold energy lashes you, and suddenly you are in another place, the dungeon a distant memory. You have escaped.')
                                # Output result for AI:
                                else:
                                    g_game.displayText('A whip of cold energy lashes out to grab ' + randomPlayer.character['shortName'] + ', and suddenly they are pulled through a tiny gap in the fabric of the road that closes behind them just as quickly as it opened. Have they escaped? It\'s impossible to say for sure.')
                case 'Answer the Riddle':
                    # Determine which answer is needed
                    if self.riddleAnswer == 1:
                        hint = 'Decorum demands that a price be paid by the first guest to leave.'
                    else:
                        hint = 'Decorum demands that a price be paid by the last guest to leave.'
                    g_game.displayText('The riddle asks the following question: \'what owes its likeness to the past, yet is most vibrant in the present? Is to some a prison, to others a stage? To some a mirror, others an open window, still others a blissful mystery? Is the greatest contest to have no prize but countless losers?\' Careful thought yields the answer to the riddle: decorum. When you speak the answer aloud, the writing on the wall changes before your very eyes. It now reads: ' + hint)
                    # Mark riddle as answered
                    self.isRiddleAnswered = True
                case 'Analyze the Music':
                    g_game.displayText('The rhythmic beat of the wind through the trees is almost like drums, peculiarly, and as you listen, you\'re struck with the bizarre notion that this sound is actually louder in some directions than others. You follow the sound until it brings to the very edge of the cradle, where you\'re faced with a wall of soil, detritus, and moving, breathing fungal shelf.')
                    # Output is different if the player has already seen the wandering heart
                    if g_game.player:
                        if g_game.player.timesSeenHeart > 0:
                            g_game.displayText('Peeling away dirt and snaking, tuberous fungal matter, you manage to poke a hole through the wall of the cradle, through which a warm red light shines. Looking through the hole, you see the source of the light is a great, pulsing hunk of red and pink tissue. It is the heart you saw before. What is it doing here?')
                        else:
                            g_game.displayText('Peeling away dirt and snaking, tuberous fungal matter, you manage to poke a hole through the wall of the cradle, through which a warm red light shines. Looking through the hole, you see the source of the light is a great, pulsing hunk of red and pink tissue. An enormous, beating heart.')
                    # Mark each active player as having seen the wandering heart and reset their exhaustion levels to 0
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.seeHeart()
                case 'Interpret the Sigils':
                    g_game.displayText('You piece together the remnants of a warning of what is to come. Two rooms from this one, you will encounter: ')
                    # Print name of the room two indices from the current one (at g_game.roomIndex - 1)
                    try:
                        futureRoom = g_game.shuffledRooms[g_game.roomIndex + 1]
                        g_game.displayText(futureRoom['name'] + '.')
                    # If there is no such room, report this
                    except IndexError:
                        g_game.displayText('nothing. One or fewer rooms remain to be explored.')
    # END INVESTIGATE

    """
    pre: should be called exactly once during each turn sequence.
    param: total, the total number of points of resolve contributed by all players that took the exert room action this turn.
    post: if param: total is high enough to succeed the current room's requirements, the party is rewarded in a matter suited to the current room.
    """
    def exert(self, total:int):
        # Load game
        global g_game
        # Report failure
        if total < self.room['requirements'][1]:
            g_game.displayText('The party failed to ' + self.room['actions'][1] + ' (' + str(total) + ' Resolve contributed, ' + str(self.room['requirements'][1]) + ' needed).')
        # Report success and carry out outcome
        else:
            g_game.displayText('The party was able to ' + self.room['actions'][1] + ' (' + str(total) + ' Resolve contributed, ' + str(self.room['requirements'][1]) + ' needed).')
            # Update room to disallow future attempts to exert
            self.hasBeenExerted = True
            # Carry out result
            match self.room['actions'][1]:
                case 'Free the Blade':
                    g_game.displayText('A cold certainty fills you as the blade is wrested free of its resting place. With this blade drawn, it cannot be put back to rest until blood has been shed. All attacks will incur an extra level of exhaustion on their target until the next time a player dies.')
                    g_game.isSwordDrawn = True
                case 'Interrogate the Mirror':
                    g_game.displayText('The mirror is not cooperative, but through carefully worded questions and a healthy measure of psychology, you manage to trick it into revealing a critical detail about the nature of this tower: it is a prison for the mind as much as it is the body. With this knowledge, you will have an easier time breaking the tower should you choose to do so.')
                    g_game.isCluedIn = True
                case 'Confront the Beast':
                    g_game.displayText('You turn and wait for the beast that lumbers behind you to catch up. Your resolve holds strong as the sounds of its ragged breaths grows louder, and just when the sound is so loud you cannot hear yourself breathe over it, it begins to fade. Soon the breathing and footsteps both have faded to nothing. In their absence, your body swells with a newfound and deeply unnatural strength. You may be able to survive that which is not survivable, now ... though it may come at a cost.')
                    # Mark each active player as having conquered their fear
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.hasConqueredFear = True
                case 'Sit at the Table':
                    g_game.displayText('A tranquil calm settles over you as you seat yourself at the grand dining table and wait for the tides of fate to change. They do not, but after a while you have almost come to terms with this. Each party member gains the benefit of a rest.')
                    # all active players rest
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.rest()
                case 'Wish at the Well':
                    g_game.displayText('The surface of the well shimmers with a barely contained skin of magic. You experiment with all variety of items dropped into it, to no effect. Coins, flowers, trinkets are swallowed whole by the dark waters, giving nothing in return. Finally, you think to feed the well a drop of your blood. Immediately, you feel the price exacted as a curse takes hold of you. You may each make a single wish of the well, so choose wisely.')
                    g_game.displayText('You may secretly vote for one of the following:')
                    numVotes = [0, 0, 0, 0, 0]
                    playerVotes = [None, None, None, None]
                    # Collect vote from player if they are able to act
                    if g_game.player.isAbleToAct():
                        # Set input to process player vote
                        g_game.setVoteInput(numVotes, playerVotes)    
                    # Otherwise move straight to AI votes and result     
                    else:
                        g_game.vote(numVotes, playerVotes)
                case 'Navigate the Ice':
                    # Output is different if the player has already seen the wandering heart
                    if g_game.player:
                        if g_game.player.timesSeenHeart > 0:
                            g_game.displayText('A gentle thrumming clues you into the fact that there is something large and very much alive buried beneath your feet. As you make your way to the center of the enormous shadow under the ice, your steps become more careful, as hair-thin cracks begin to spiral out from them. Yet you make it without a hitch, and are rewarded with a glimpse of what lies beneath. A faint red glow reveals the pulsing of an enormous heart underneath the ice. It is the same heart you saw before. What is it doing here?')
                        else:
                            g_game.displayText('A gentle thrumming clues you into the fact that there is something large and very much alive buried beneath your feet. As you make your way to the center of the enormous shadow under the ice, your steps become more careful, as hair-thin cracks begin to spiral out from them. Yet you make it without a hitch, and are rewarded with a glimpse of what lies beneath. A faint red glow reveals the pulsing of an enormous heart underneath the ice.')
                    # Mark each active player as having seen the wandering heart and reset their exhaustion levels to 0
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.seeHeart()
    # END EXERT

    """
    pre: should be called exactly once during each turn sequence.
    param: total, the total number of points of finesse contributed by all players that took the explore room action this turn.
    post: if param: total is high enough to succeed the current room's requirements, the party is rewarded in a matter suited to the current room.
    """
    def explore(self, total:int):
        # Load game
        global g_game
        # Report failure
        if total < self.room['requirements'][2]:
            g_game.displayText('The party failed to ' + self.room['actions'][2] + ' (' + str(total) + ' Finesse contributed, ' + str(self.room['requirements'][2]) + ' needed).')
        # Report success and carry out outcome
        else:
            g_game.displayText('The party was able to ' + self.room['actions'][2] + ' (' + str(total) + ' Finesse contributed, ' + str(self.room['requirements'][2]) + ' needed).')
            # Update room to disallow future attempts to explore
            self.hasBeenExplored = True
            # Carry out result
            match self.room['actions'][2]:
                case 'Take the High Ground':
                    g_game.displayText('On the edge of the arena, you find a space where the piled junk reaches high enough that a player might be able to make it over the wall and into the next room if they get a boost up. Any number of players may take this opportunity as long as it least one chooses to stay behind.')
                    # For each active player, give the option to stay behind or leave
                    remainingPlayers = []
                    leavingPlayers = []
                    # If player is able to act, take player input
                    if g_game.player.isAbleToAct():
                        g_game.displayText('Will you choose to remain behind?')
                        # Set input for player to choose Y/N from
                        g_game.setYNInput(g_game.getHighGroundOffer)
                    # Else move directly to AI choices and results
                    else:
                        g_game.highGround(False)
                case 'Spring the Vaults':
                    g_game.displayText('You deftly navigate the series of intricate traps and locks in place to wrest open the vaults in the Tower\'s basement. Inside the vast, dark space, you find only a single item, set neatly in the center of the floor. A key, to another door. You pocket the key, hoping that whatever it opens will be found in time.')
                    # Add key to party inventory
                    g_game.isKeyFound = True
                case 'Loot the Storefronts':
                    g_game.displayText('The storefronts have been largely picked over, but an extended search reveals 2 supplies hiding in cabinets and on shelves, in corners and behind locked doors.')
                    # Add supplies
                    g_game.partySupplies += 2
                case 'Raid the Kitchen':
                    g_game.displayText('You barge into the kitchen, interrupting a four-course meal being prepped by no one. All manner of foodstuffs sit out in a state of half or almost complete preparedness, just waiting to be served. You load your arms with all you can carry, walking away with 4 supplies.')
                    g_game.displayText('Each party member also walks away with a curse upon their name.')
                    # Add supplies
                    g_game.partySupplies += 4
                    # Add curse to each active player
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.timesCursed += 1 
                case 'Forage in the Marshland':
                    g_game.displayText('There is much to be found here worth eating, when you know what you are looking for. With a careful eye, you harvest 3 supplies from the wilds.')
                    # Add supplies
                    g_game.partySupplies += 3
                case 'Search for Shelter':
                    g_game.displayText('Through a slight gap the surface of the cove\'s rocky exterior, you find a place where the party can hunker down and weather the storm.')
                    g_game.isSheltered = True
    # END EXPLORE
# END CLASS LOCATION

### GLOBAL METHODS ###

"""
pre: should only be called when the party is moving to a new room.
post: all dead players are marked as passed and returned to play with a reset exhaustion level.
"""
def attemptCloudblessedRevive():
    # Load Game
    global g_game
    # Carry out effect only if Cloudblessed was revealed in the current room
    if g_game.location.cloudblessedRevealed:
        # Determine if all players have passed
        actionablePlayers = g_game.getActionablePlayers()
        if len(actionablePlayers) == 0:
            # If both are true, return all dead players to life
            for p in g_game.allPlayers:
                if not p.isAlive:
                    # Return player to life
                    p.isAlive = True
                    # Mark player as passed so they can be reanimated in the next room
                    p.hasPassed = True
                    # Reset player exhaustion level
                    p.exhaustionLevel = 0
                    # Report outcome
                    if p.isPlayer():
                        g_game.displayText('The cloud-blessed mists grant you another chance at life.')
                    else:
                        g_game.displayText('The cloud-blessed mists grant ' + p.character['shortName'] + ' another chance at life.')
    # END ATTEMPTCLOUDBLESSEDREVEAL

### GLOBAL: HELPERS ###

"""
param: text, the string to be padded.
return: version of param:text in which a space has been placed before every comma, period, apostrophe, and colon.
"""
def padPunctuation(text:str) -> str:
    return text.replace(',', ' ,').replace('.', ' .').replace('\'', ' \'').replace(':', ' :')
# END PADPUNCTUATION

"""
param: players, the list of player objects to find the most exhausted player from.
return: player object randomly chosen from among those in param:players who have the highest exhaustion level.
"""
def getMostExhaustedPlayer(players:list) -> object:
    # Return error if given empty list
    if len(players) == 0:
        return None
    # Find highest exhaustion level among players
    maxExhaustionLevel = 0
    for p in players:
        exhaustionLevel = p.exhaustionLevel
        if exhaustionLevel >= maxExhaustionLevel:
            maxExhaustionLevel = exhaustionLevel
    # Select random player from among players with the highest exhaustion
    return rng.sample(list(filter(lambda p: p.exhaustionLevel == maxExhaustionLevel, players)), 1)[0]
# END GETMOSTEXHAUSTEDPLAYER

"""
param: players, the list of player objects to find the least exhausted player from.
return: player object randomly chosen from among those in param:players who have the lowest exhaustion level.
"""
def getLeastExhaustedPlayer(players:list) -> object:
    # Return error if given empty list
    if len(players) == 0:
        return None
    # Find highest exhaustion level among players
    minExhaustionLevel = 4
    for p in players:
        exhaustionLevel = p.exhaustionLevel
        if exhaustionLevel <= minExhaustionLevel:
            minExhaustionLevel = exhaustionLevel
    # Select random player from among players with the highest exhaustion
    return rng.sample(list(filter(lambda p: p.exhaustionLevel == minExhaustionLevel, players)), 1)[0]
# END GETLEASTEXHAUSTEDPLAYER

### GLOBAL: MAIN ###

if __name__ == '__main__':
    # Initialize number of game instances to be played
    numInstances = 1
    # Initialize mode
    mode = 1 # DEFAULT
    # Read in second argument, update numInstances and set to TEST mode if an int was supplied
    args = sys.argv
    if len(args) > 1:
        try:
            numInstances = int(args[1])
            mode = 0 # TEST
            # Initialize tally blocks to take the average of
            characterFull = [[],[],[],[],[],[]]
            roleFull = [[],[],[],[],[],[]]
            pairFull = [[[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]], [[],[],[],[],[],[]]]
            aggroTot = 0
        except ValueError:
            pass
    # Play game numInstances number of times
    for _ in range(numInstances):
        g_game = Game(mode)
        g_game.play()
        # Tally stats if testing
        if mode == 0:
            rawTally = g_game.tallyStats()
            aggroTot += g_game.timesAggroed
            for i in range(6):
                characterFull[i].append(rawTally[0][i])
                roleFull[i].append(rawTally[1][i])
                for j in range(6):
                    pairFull[i][j].append(rawTally[2][i][j])
    # Report stats if testing
    if mode == 0:
        # Initialize titles
        characterNames = ['Reika of the Thousand Days', 'Endemene Silverblood', 'Rainee Haraldsson', 'Elvy, the Heart-hammer', 'Dredge', 'Mantelesse the Far-Dreaming']
        roleNames = ['Mnanth, Whose Heart is Glass', 'Casglowve, the Captive Moon', 'Cloudblessed', 'Marloe, Don of the Downtrodden', 'Erstwhile, Collector Supreme', 'The Fisherwoman']
        # Write to permanent storage location
        with open('testOutput.txt', 'a') as f:
            for i in range(6):
                f.write(characterNames[i] + ': ' + str(mean(characterFull[i])) + '\n')
            for i in range(6):
                f.write(roleNames[i] + ': ' + str(mean(roleFull[i])) + '\n')
            for i in range(6):
                for j in range(6):
                    f.write('(' + characterNames[i] + ', ' + roleNames[j] + '): ' + str(mean(pairFull[i][j])) + '\n')
            f.write('Times Aggro-ed: ' + str(aggroTot) + '\n')
            f.write('======================================\n')
 # END __MAIN__

 # TODO:

 # BUG:
 # Fisherwoman stun is breaking the turn after along with all future text color display
 # Cloudblessed reveal message is not output when the player dies.
 # Original version bug that seemingly causes players that have attempted to pass and have no other options available to automatically move to next room after one of them kills a player
 # Some text is getting moved to the bottom in display instead of all scrolling in order. Text color displays is screwing up at the same time. - could be due to the escaped single quote in that text?
 # Players that die should not complete any action (passing at least still succeeds as of now)
 # Reached max recursion depth after wasting away in the Tower while two other players are alive
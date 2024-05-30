import random as rng
import sys
from colorama import Fore, Back, Style
from statistics import mean

g_characters = [{'id':0, 'name':'Reika of the Thousand Days', 'ingenuity':2, 'resolve':3, 'finesse':1, 'passive':'Undertow', 'active':'Anchor', 'passiveDescription':'At end of turn, if Reika has passed action and another player is able to act, she returns to play.', 'activeDescription':'Regain a use of one of the following actions that you have already taken in this room: Attack, Rest, or any room actions that have not yet been succeeded.',
    'revealQuips':['Tomorrow starts now, and you are not welcome there.', 'A million years could not keep me from her.', 'A second chance is not a gift. It is a call to arms.', 'Short-sighted fools. Stand at attention; the future is calling our names.', 'It is not our time.', 'Hush now. It is almost over.']}, 
    {'id':1, 'name':'Endemene Silverblood', 'ingenuity':3, 'resolve':1, 'finesse':2, 'passive':'Inspiration', 'active':'Prototype', 'passiveDescription':'Endemene becomes inspired under various conditions, allowing for the prototyping of inventions which act as permanent buffs to her character.', 'activeDescription':'Prototype an invention.',
    'revealQuips':['Lol. Lmao.', 'WHERE\'S MY WIFE?', 'See you all sooner than you\'d like.', 'Cards on the table: I want you all on my payroll.', 'That got ugly. Let\'s try not to do that again, yeah?', 'I dislike killing probably almost as much as you all dislike dying, so let\'s get this over with quickly.']},
    {'id':2, 'name':'Rainee Haraldsson', 'ingenuity':3, 'resolve':2, 'finesse':1, 'passive':'Unraveling Threads', 'active':'Interrogate', 'passiveDescription':'Whenever Rainee Haraldsson rests, learn the identity of a random role that is not actively in play and that has not already been learned.', 'activeDescription':'Attempt to guess a chosen player\'s role. If correct, their role is revealed.',
    'revealQuips':['It is a heavy heart that draws a blade in anger. It is a heavier one that sheaths it in fear. I am not afraid.', 'Would but that I were the oceans, that I might feel your pull more often.', 'I am prepared to die for the cause. All the same, I would much prefer to live for it.', 'I beg you all, consider: what can I do for you?', 'Chin up, comrades. The rest of us may make it through this yet.', 'If I am to be destiny\'s fool, then so be it. We all must make sacrifices sometimes. Let mine be all of you.']},
    {'id':3, 'name':'Elvy, the Heart-Hammerer', 'ingenuity':2, 'resolve':1, 'finesse':3, 'passive':'Ward', 'active':'Guard', 'passiveDescription':'As long as Elvy has not attacked, defended, or been attacked, disregard all instructions to reveal their role.', 'activeDescription':'Defend against all attacks.',
    'revealQuips':['Smile, knave. Or dost thou not desire to look thy best for thine open casket?', 'Fair lady, there can be not a light as soft and soothing as thine own.', 'Thou knowest not what thee would do in mine absence. I shall be compelled to return.', 'Thoust owe more to me and mine than thee could ever hope to pay. Be still.', 'Drink, take succhor, be merry my wild ones. Greater challenges still await.', 'Take in all of myself thou are able to. This beauty shall be thy doom.']},
    {'id':4, 'name':'Dredge', 'ingenuity':1, 'resolve':3, 'finesse':2, 'passive':'From Below', 'active':'Scout', 'passiveDescription':'Whenever Dredge rests, a random item will find its way to him, to be discovered on waking.', 'activeDescription':'Learn the identity of the next room the party will encounter.',
    'revealQuips':['The time is long past for you to have found redemption. I suggest you look for it in the ground.', 'It is a lonely night, when even the moon must hide. Onto better days and better skies.', 'Life will never taste as sweet as in the moment it is taken from you.', 'Words are fickle things, but in this matter, I am confident they will suffice.', 'The world will still honor your passing millenia after your name is forgotten.', 'Forgive me, everyone, but such is the way of all things.']},
    {'id':5, 'name':'Mantelesse the Far-Dreaming', 'ingenuity':1, 'resolve':2, 'finesse':3, 'passive':'Together As One', 'active':'Weird', 'passiveDescription':'Whenever all players in play take the same action, as long as at least two players are able to act, each of those players gain a benefit depending on the action taken.', 'activeDescription':'Nullify the result of the action taken by a chosen player.',
    'revealQuips':['Checkmate, friend.', 'Auspicious timing, love.', 'Death is a stranger and I am far too prickly to make its aquaintance.', 'There is a greater enemy than any one of us lurking out there beyond the veil of the horizon. Don\'t be reckless.', 'We forget about this and carry on. Anything else would be stupid.', 'The beast stirs. Time at last to see what we all are made of.']}]
g_roles = [{'id':0, 'name':'Mnanth, Whose Heart is Glass', 'reveal':'Bar the Way', 'winCondition':'Vengeance', 'revealDescription':'Whenever you and your pact target are the only players able to act, reveal Mnanth. When you do, the current room gains \'players may not pass action unless they are the only player in the room.\'', 'winConDescription':'When Mnanth becomes your role, a player at random is secretly chosen to be your pact target and you are informed as to what role this player has. You win if you escape and your pact target does not.'}, 
    {'id':1, 'name':'Casglowve, the Captive Moon', 'reveal':'Absolve the Selfish', 'winCondition':'Longing', 'revealDescription':'Whenever you reach exhaustion level 3, reveal Casglowve. When you do, you immediately pass action and gain the benefit of a rest, ignoring all restrictions. Then, all other players immediately gain a level of exhaustion.', 'winConDescription':'You win if you escape after having Broken the Tower.'},
    {'id':2, 'name':'Cloudblessed', 'reveal':'Defy the Deathwisher', 'winCondition':'Compassion', 'revealDescription':'Whenever you are killed by another player, reveal Cloudblessed. The current room gains \'when the last player passes action, return all dead players to play.\'', 'winConDescription':'You win if at least half the total players (rounded up) escape.'},
    {'id':3, 'name':'Marloe, Don of the Downtrodden', 'reveal':'Call Upon the Family', 'winCondition':'Loyalty', 'revealDescription':'While there is another player able to act, you may reveal Marloe as an action. When you do, defend all players against all attacks made this turn. Each player successfully defended this way receives a curse.', 'winConDescription':'You win if you escape and no other player escapes that does not have a curse.'},
    {'id':4, 'name':'Erstwhile, Collector Supreme', 'reveal':'Waste Not the Forgotten', 'winCondition':'Curiosity', 'revealDescription':'Whenever another player dies, reveal Erstwhile. When you do, each other player receives the benefit of a rest.', 'winConDescription':'You win if you visit every room.'},
    {'id':5, 'name':'The Fisherwoman', 'reveal':'Drop the Avalanche', 'winCondition':'Territoriality', 'revealDescription':'Whenever you take the attack action, reveal The Fisherwoman. When you do, each other player skips their next turn and you may take the attack action once more in the current room.', 'winConDescription':'You win if you escape and no other player escapes that has seen the Wandering Heart.'}]
g_rooms = [{'id':0, 'name':'The Scrap-Iron Arena', 'actions':['Plumb the Wreckage','Free the Blade','Take the High Ground'], 'requirements':[5,7,3], 'characteristic':'Bloodsport', 'description':'The scent of iron rises like a haze off the arena, which from the stands resembles the most dangerous jungle-gym imaginable. At the center of the mess of scrap stands a single clear dais of stone within which an old competitor\'s wicked blade has long been buried. Many have tried to free it from its place there. Will you try your hand? Or will you scavenge amidst the script for meager resources, or fight your way to the high ground on the edge of the valley of scrap?'}, 
    {'id':1, 'name':'The Tower', 'actions':['Break the Magic','Interrogate the Mirror','Spring the Vaults'], 'requirements':[7,3,5], 'characteristic':'Futility', 'description':'The black tower reaches up like a jagged bolt of lightning to touch the sky. Within its many levels, countless oddities and dangers await, most of them indecipherable even to the greatest scientific and arcane thinkers of the modern age. The tower is watched over ground-to-roof by a wall-length, multi-level mirror that is home to an entity of a particularly wrathful disposition. Will you find a way to break the tower before it breaks you? Or are you better served appeasing the mirror entity or looting what you can from under its proverbial nose?'},
    {'id':2, 'name':'Longway Alley', 'actions':['Follow the Twine','Confront the Beast','Loot the Storefronts'], 'requirements':[7,5,3], 'characteristic':'Confusion', 'description':'Longway Alley is a place that defies description. It is to most only as material as a dream, the feeling of cold cobblestones underfoot, the light mist hanging deceptively thick in the air, the sound of too-heavy footsteps thudding somewhere far off, but maybe only as little as a block away. Yet not all who have wandered into the depths of the alley are lost, as evidenced by the silver twine that crops up everywhere, crisscrossing itself two or three times in certain junctions. Will you attempt to trace this twine to its origin, rather than follow the route laid out for you? Or would you rather take your chances with the beast that stalks the haze along with you, or spend your time searching the storefronts that populate the alley for useful materials?'},
    {'id':3, 'name':'The Hall of the Mirthless Queen', 'actions':['Answer the Riddle','Sit at the Table','Raid the Kitchen'], 'requirements':[5,3,7], 'characteristic':'Destiny', 'description':'Cobwebs dust every surface in the great hall. Bricks are cracked, the floorboards rotten and splintered. Yet, for all the countless many years this place has lain empty, the table is still set. The hearth is still flickering. And a heavenly smell still wafts from the kitchen. looking out over the great table is a portrait of the woman who once presided over this hall. Her stern face asks a question mirrored in the riddle scrawled below her visage. Will you attempt to answer this riddle? Or will you venture into the kitchen to see what\'s cooking, or better yet, sit at the table and wait to be served?'},
    {'id':4, 'name':'Death\'s Cradle', 'actions':['Analyze the Music','Wish at the Well','Forage in the Marshland'], 'requirements':[3,7,5], 'characteristic':'Doom', 'description':'Within a cradle of rot, mildew, and fungal growth, an oasis of a kind sits largely untouched. Pale flowers spread wisplike petals. A wind that is not wind blows through trees with leaves like windchimes. Leaves curl gently to hide the curve of a stepping-stone path. A wishing well stands upon a hill, the glint of spent coins shining in the light of a bioluminescent sun. Will you cast your own wish in the waters of life and death? Or will you find a way to live off the surrounding marshland in its alien beauty, or seek answers in the song of the wind through the trees?'},
    {'id':5, 'name':'The Icy Cove', 'actions':['Interpret the Sigils','Navigate the Ice','Search for Shelter'], 'requirements':[3,5,7], 'characteristic':'Decisiveness', 'description':'The cove stands tall against time, a thousand days and nights of cold winds weathered by the unflinching rock of its walls. The ocean that sits beside it did not fare as well. The water lies frozen, still as the bodies it used to wash ashore. Little remains to explain the frozen bodies, save for a series of pillars carved with strange and unsettling sigils. A keen eye, however, might notice that there is a faint light glowing underneath the surface of the ice, way out past the safety of the once-shoreline. Will you go to this light? Or would your time be better spent studying the symbols marking the pillars, or seeking out shelter from the cold along the side of the cove?'}]
g_game = 0

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
        # Initialize action-tracking vars
        self.investigateTotal = 0
        self.exertTotal = 0
        self.exploreTotal = 0
        self.attackTargets = []
        self.attackSources = []
        self.restTargets = []
        self.passingPlayers = []
        self.guardSources = [] # for Elvy's use only
        self.guardTargets = [] # for Elvy's use only
        # Initialize other vars
        self.partySupplies = 4
        self.randomID = None
        self.isTowerBroken = False
        self.isKeyFound = False
        self.isSwordDrawn = False
        self.isSheltered = False
        self.isCluedIn = False
        self.isWayBarred = False
        self.marloeRevealedThisTurn = False
        self.timesAggroed = 0
    # END __INIT__

    def play(self):
        if self.player:
            # Print relevant character, role, and ai data
            print('Welcome, player.\n\nYour character is', end =' ')
            self.player.printCharacterInfo()
            print('\nYour role is', end =' ')
            self.player.printRoleInfo()
            print('\nIn the party with you are ' + '; '.join(list(map(lambda p: p.styleCharacterName(), self.player.getOtherPlayers()))) + '.\n')
        # Player advances through rooms until game is over
        while True:
            # If all players are dead or escaped, end game
            if list(map(lambda p: not p.isAlive or p.hasEscaped, self.allPlayers)) == [True, True, True, True]:
                print('No players remain in the dungeon. Game Over.')
                # Display winners and losers
                _ = [p.checkWinConditions() for p in self.allPlayers]
                # End current game
                return
            # If all rooms have been cleared, check for key, then end game
            if self.roomIndex == 6:
                if self.isKeyFound:
                    printIfPlayerActive('Beyond the dungeon\'s final room you are met only with a wall of stone. Set into the base of this wall is a tiny hatch, openable with the key you have found. Engravings on the wall however reveal that this hatch will only admit one player through before it locks again forever.')
                    # Find most exhausted player
                    randomPlayer = getLeastExhaustedPlayer(list(filter(lambda p: p.isAlive and not p.hasEscaped, self.allPlayers)))
                    # Player escapes
                    randomPlayer.escape()
                    # Report outcome
                    if randomPlayer.isPlayer():
                        print('As one of the most alert players still standing, you act quickly, seizing the key, unlocking the hatch, and diving in before anyone else. You hear the hatch click shut behind you, muffling the outraged cries of your companions. You have escaped.')
                    else:
                        print('As one of the most alert players still standing, ' + randomPlayer.styleCharacterName() +' acts quickly, seizing the key, unlocking the hatch, and diving in before anyone else. They have escaped, leaving the rest of you to your fates.')
                    print('Game Over.')
                # If key was not found, move straight to game over
                else:
                    print('Beyond the dungeon\'s final room you are met only with a wall of stone. Set into the base of this wall is a tiny hatch, but it is locked, impassible to all. This is your final step in the dungeon. Game Over.')
                # Display winners and losers
                _ = [p.checkWinConditions() for p in self.allPlayers]
                # End current game
                return
            # Enter next room corresponding to room index
            self.location = Location(self.shuffledRooms[self.roomIndex])
            # Increment room index
            self.roomIndex += 1
            # Extract current room information for ease of access
            room = self.location.room
            # Output room entry message
            print('Your party enters ' + room['name'] + '.', end =' ')
            print(room['description'] + '\n')
            # Reset room-dependent stats for players that are still in the dungeon
            _ = [q.enterRoom() for q in list(filter(lambda p: p.isAlive and not p.hasEscaped, self.allPlayers))]
            # End Bar the Way effect if it was active
            self.isWayBarred = False
            # Player takes actions until they are no longer able to
            while list(map(lambda p: p.isAbleToAct(), self.allPlayers)) != [False, False, False, False]:
                #print(list(map(lambda p: p.isAbleToAct(), self.allPlayers))) # DEBUG PRINT
                # If Reika is in the game and has passed, return her to play
                reikaPlayer = lookupPlayerByCharacter('Reika of the Thousand Days')
                if reikaPlayer:
                    if reikaPlayer.hasPassed:
                        reikaPlayer.undertow()
                # If only a player with Mnanth as their role and that player's (revealed) pact target are able to act, trigger Mnanth reveal
                actionablePlayers = list(filter(lambda p: p.isAbleToAct(), self.allPlayers))
                mnanthPlayer = lookupPlayerByRole('Mnanth, Whose Heart is Glass')
                if mnanthPlayer:
                    pactTargetID = mnanthPlayer.pactTargetID
                    if len(actionablePlayers) == 2:
                        if actionablePlayers[0].id == pactTargetID and actionablePlayers[0].isRevealed:
                            actionablePlayers[1].triggerReveal('Mnanth, Whose Heart is Glass')
                        elif actionablePlayers[1].id == pactTargetID and actionablePlayers[1].isRevealed:
                            actionablePlayers[0].triggerReveal('Mnanth, Whose Heart is Glass')
                ### DECISION PHASE ###
                # Initialize actions and targets
                actions = []
                targets = []
                # If in the alley, choose a random player from among the active players each turn to have to carry out a random action
                if room['id'] == 2:
                    self.randomID = rng.sample(list(map(lambda p: p.id, list(filter(lambda p: p.isAbleToAct(), self.allPlayers)))), 1)[0]
                for p in self.allPlayers:
                    # If player is unable to act, skip them
                    if p.isAbleToAct() and not p.isStunned:
                        # Player action
                        if p.isPlayer():
                            # Initialize options list
                            options = []
                            optionNum = 1
                            # Determine which options are available to the players and print
                            if not self.player.hasAttacked and list(map(lambda p: p.isAbleToAct(), self.player.getOtherPlayers())) != [False, False, False]:
                                options.append('Attack')
                                print(str(optionNum) + '. Attack')
                                optionNum += 1
                            if not self.player.hasRested and self.player.exhaustionLevel > 0:
                                options.append('Rest')
                                print(str(optionNum) + '. Rest')
                                optionNum += 1
                            if not self.player.hasInvestigated and not self.location.hasBeenInvestigated:
                                options.append('Investigate')
                                # Calculate discount for if mirror was successfully interrogated
                                discount = 0
                                if self.isCluedIn:
                                    discount = 2
                                print(str(optionNum) + '. ' + room['actions'][0] + ' (' + str(room['requirements'][0] - discount) + ' Ingenuity)')
                                optionNum += 1
                            if not self.player.hasExerted and not self.location.hasBeenExerted:
                                options.append('Exert')
                                print(str(optionNum) + '. ' + room['actions'][1] + ' (' + str(room['requirements'][1]) + ' Resolve)')
                                optionNum += 1
                            if not self.player.hasExplored and not self.location.hasBeenExplored:
                                options.append('Explore')
                                print(str(optionNum) + '. ' + room['actions'][2] + ' (' + str(room['requirements'][2]) + ' Finesse)')
                                optionNum += 1
                            if not self.player.hasUsedActive:
                                isActiveValid = False
                                active =  self.player.character['active']
                                match active:
                                    case 'Anchor':
                                        if (self.player.hasAttacked and len(list(filter(lambda p: p.isAbleToAct(), self.player.getOtherPlayers()))) > 0) or (self.player.hasRested and self.player.exhaustionLevel > 0) or (self.player.hasInvestigated and not self.location.hasBeenInvestigated) or (self.player.hasExerted and not self.location.hasBeenExerted) or (self.player.hasExplored and not self.location.hasBeenExplored):
                                            isActiveValid = True
                                    case 'Prototype':
                                        if len(self.player.inspiration) > 0:
                                            isActiveValid = True
                                    case 'Interrogate':
                                        if list(map(lambda p: p.isAbleToAct() and not p.isRevealed, self.player.getOtherPlayers())) != [False, False, False]:
                                            isActiveValid = True
                                    case 'Guard':
                                        if list(map(lambda p: p.isAbleToAct(), self.player.getOtherPlayers())) != [False, False, False]:
                                            isActiveValid = True
                                    case 'Scout':
                                        isActiveValid = True
                                    case 'Weird':
                                        if list(map(lambda p: p.isAbleToAct(), self.player.getOtherPlayers())) != [False, False, False]:
                                            isActiveValid = True
                                if isActiveValid:
                                    options.append('Special Active')
                                    print(str(optionNum) + '. ' + active)
                                    optionNum += 1
                            # Marloe reveal action is available to players with the role that have not yet had it revealed
                            if self.player.role['id'] == 3 and not self.player.isRevealed:
                                options.append('Reveal Active')
                                print(str(optionNum) + '. Call Upon the Family (reveal role)')
                                optionNum += 1
                            options.append('Pass')
                            print(str(optionNum) + '. Pass')
                            # Read in player's choice of action
                            action = getPlayerInput(options)
                            actions.append(action)
                            # Read in players choice of target as demanded by their chosen action
                            target = self.player.getPlayerTarget(action)
                            targets.append(target)
                            # If in the alley, if player was randomly chosen, override their decision with a random one
                            if room['id'] == 2 and self.randomID == 1:
                                # Choose a random action from those available
                                randomAction = rng.sample(options, 1)[0]
                                # If action is prototype, choose a random prototype
                                if randomAction == 'Special Active' and self.player.character['id'] == 1:
                                    randomTarget = rng.sample(self.inspiration, 1)[0]
                                else:
                                    # Find random other player to target
                                    try:
                                        randomTarget = rng.sample(list(filter(lambda p: p.isAbleToAct(), self.player.getOtherPlayers())), 1)[0]
                                    except ValueError:
                                        randomTarget = None # Never need to worry about having a targeted ability with no valid target as these options will not be presented to player in that situation
                                    # Report outcome
                                    print('A stray thought strikes you, altering your choice of action.')
                                # Override original decision
                                actions.pop()
                                actions.append(randomAction)
                                targets.pop()
                                targets.append(randomTarget)
                        # AI action
                        else:
                            # Determine AI action and target
                            action, target = p.decideAiAction()
                            actions.append(action)
                            targets.append(target)
                    else:
                        # Provide blank action if player did not act
                        actions.append('')
                        targets.append(None)
                    # Remove stun effect after action is skipped
                    p.isStunned = False
                # Separate actions from results with newline
                print('')
                #print(actions) # DEBUG PRINT
                ### ACTION PHASE ###
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
                testAction = actions[0]
                for i in range(1, len(actions)):
                    action = actions[i]
                    if action != '' and testAction != '' and testAction != action:
                        isUnity = False
                        break
                    else:
                        if action != '':
                            testAction = action
                # If all actions were the same and Mantelesse took one of them, trigger his passive
                if isUnity:
                    mantelessePlayer = lookupPlayerByCharacter('Mantelesse the Far-Dreaming')
                    if mantelessePlayer:
                        if mantelessePlayer.isAbleToAct():
                            mantelessePlayer.unite(actions[0])
                # Perform weirding actions first
                for i in range(len(self.allPlayers)):
                    p = self.allPlayers[i]
                    if actions[i] == 'Special Active' and p.character['id'] == 5:
                        p.takeAction(actions[i], targets[i])
                # Perform all other actions next
                for i in range(len(self.allPlayers)):
                    p = self.allPlayers[i]
                    if actions[i] != 'Special Active' or p.character['id'] != 5:
                        # Reject action if player is weirded
                        if p.isWeirded:
                            # Remove weirded effect
                            p.isWeirded = False
                            # Report outcome
                            if p.isPlayer():
                                print('Your ' + actions[i] + ' action was negated by the weirding magic that has taken hold of you this turn.')
                            else:
                                print(p.styleCharacterName() + '\'s ' + actions[i] + ' action was negated by the weirding magic that has taken hold of them this turn.')
                        else:
                            p.takeAction(actions[i], targets[i])    
                # Separate actions from results with newline
                print('')
                ### RESULT PHASE ###
                # Carry out room actions
                if self.investigateTotal > 0:
                    self.location.investigate(self.investigateTotal)
                if self.exertTotal > 0:
                    self.location.exert(self.exertTotal)
                if self.exploreTotal > 0:
                    self.location.explore(self.exploreTotal)
                # Carry out attacks
                for i in range(len(self.attackSources)):
                    source = lookupPlayerByID(self.attackSources[i])
                    target = lookupPlayerByID(self.attackTargets[i])
                    source.attack(target)                                  
                # Deny all rests if there are not enough supplies for each player attempting to rest at once
                numResting = len(self.restTargets)
                if self.partySupplies < numResting:
                    print('Without enough supplies for each resting party member, there can be no consensus, and therefore no rest.')
                else:
                    # Carry out rests
                    for pid in self.restTargets:
                        p = lookupPlayerByID(pid)
                        if p.isAlive:
                            p.rest()
                # If a player rested, report remaining supplies
                if numResting > 0:
                    print('The party is left with ' + str(self.partySupplies) + ' supplies.')
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
                        printIfPlayerActive('You spy a wicked-looking ice storm on the horizon. It will be upon you in 2 turns.')
                    elif currentTurn == 2:
                        # Report if player is active
                        printIfPlayerActive('The storm draws nearer. It will be upon you in one turn.')
                    elif currentTurn == 3:
                        # Report if player is active
                        printIfPlayerActive('The storm is upon you.')
                    # Exhaust players unless they are sheltered
                    if currentTurn >= 3:
                        if self.isSheltered:
                            # Report outcome regardless of whether player is active
                            print('The party weathers the storm under the cove\'s natural shelter.')    
                        else:
                            # Report outcome regardless of whether player is active
                            print('The party is battered mercilessly by the razor-sharp ice.')
                            # Active players gain exhaustion
                            _ = [p.gainExhaustion() for p in list(filter(lambda p: p.isAbleToAct(), self.allPlayers))]
                # If Endemene appeared twice in attack targets, trigger inspire on her
                numAppearances = 0
                for pid in g_game.attackTargets:
                    if lookupPlayerByID(pid).character['id'] == 1:
                        numAppearances += 1
                if numAppearances >= 2:
                    # Trigger inspire on Endemene if she is still able to act
                    _ = [p.inspire('Net') for p in list(filter(lambda p: p.isAlive and not p.hasEscaped and p.character['id'] == 1, g_game.allPlayers))]
                # Separate results from next batch of decisions with newline
                print('')
    # END PLAY

    def tallyStats(self):
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

    def isPlayer(self):
        # Check if player ID is 1, if not, the player is an AI
        if self.id == 1:
            return True
        return False
    # END ISPLAYER

    def styleCharacterName(self):
        name = self.character['name']
        colorMod = ''
        match name:
            case 'Reika of the Thousand Days':
                colorMod = Fore.YELLOW
            case 'Endemene Silverblood':
                colorMod = Fore.RED
            case 'Rainee Haraldsson':
                colorMod = Fore.CYAN
            case 'Elvy, the Heart-Hammerer':
                colorMod = Fore.MAGENTA
            case 'Dredge':
                colorMod = Fore.GREEN
            case 'Mantelesse the Far-Dreaming':
                colorMod = Fore.BLUE
        # return styled name
        return colorMod + name + Style.RESET_ALL
    # END STYLECHARACTERNAME

    def styleRoleName(self):
        name = self.role['name']
        colorMod = ''
        match name:
            case 'Mnanth, Whose Heart is Glass':
                colorMod = Back.YELLOW
            case 'Casglowve, the Captive Moon':
                colorMod = Back.RED
            case 'Cloudblessed':
                colorMod = Back.CYAN
            case 'Marloe, Don of the Downtrodden':
                colorMod = Back.MAGENTA
            case 'Erstwhile, Collector Supreme':
                colorMod = Back.GREEN
            case 'The Fisherwoman':
                colorMod = Back.BLUE
        # return styled name
        return colorMod + name + Style.RESET_ALL
    # END STYLEROLENAME

    def enterRoom(self):
        # Players do not enter a room when they are dead or escaped
        if not self.isAlive or self.hasEscaped:
            return
        # Increment rooms visited
        self.numRoomsVisited += 1
        if not self.hasRested:
            # No exhaustion gained for players who have seen the wandering heart 2 or more times
            if self.timesSeenHeart > 1:
                # Player output
                if self.id == 1:
                    print('The memory of the Heart fills you with that odd sense of wakefulness again. You gain no exhaustion as you cross over to this room.')
            # Gain a level of exhaustion if no rest was taken in the last room
            else:
                self.gainExhaustion()
        # Reset room-specific stats                      
        self.hasAttacked = False
        self.hasRested = False
        self.hasInvestigated = False
        self.hasExerted = False
        self.hasExplored = False
        self.hasUsedActive = False
        self.hasPassed = False
        self.attemptedToPass = False
    # END ENTERROOM

    def gainExhaustion(self):
        self.exhaustionLevel += 1
        # Output exhaustion information for the player
        if self.id == 1:
            # Add level of exhaustion
            print('\nYou gain a level of exhaustion.')
            exhaustionLevel = self.exhaustionLevel
            match exhaustionLevel:
                case 1:
                    print('You may now take the Rest action.')
                case 2:
                    print('You are now vulnerable to attack.')
                case 3:
                    print('You will surely perish if you do not take the rest action in this room.')
                    # Trigger Casglowve reveal on self
                    self.triggerReveal('Casglowve, the Captive Moon')
                case 4:
                    print('You collapse from your exhaustion and are left for dead.')
                    # Mark character as dead
                    self.die()
                    # No need to adjust any other characteristics
                    return
        # Output exhaustion information for AI
        else:
            exhaustionLevel = self.exhaustionLevel
            match exhaustionLevel:
                case 2:
                    print(self.styleCharacterName() + ' is visibly weakened by their exhaustion.')
                case 3:
                    print(self.styleCharacterName() + ' collapsed from their exhaustion and was left for dead.')
                    # Mark character as dead
                    self.die()
                    # No need to adjust any other characteristics
                    return
    # END GAINEXHAUSTION

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
                print('You feel largely back to your normal self.')
            # Report for AI
            else:
                print(self.styleCharacterName() + ' is no longer visibly exhausted.')
        # Case where they went from 2 or 1 -> 0 exhaustion
        else:
            # Only report for player
            if self.isPlayer():
                print('You feel fully recovered and ready for everything.')
        # Carry out additional effects only if this is a standard rest (if player is in restTargets)
        if self.id in g_game.restTargets:
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
                            print('In your dreams you follow a light most peculiar to find a great, pulsing hunk of red and pink tissue that hovers impassively above you on the empty plain of unsolidifed dreams. An enormous, beating heart.')
                        else:
                            print('In your dreams you follow a light most peculiar to find a great, pulsing hunk of red and pink tissue that hovers impassively above you on the empty plain of unsolidifed dreams. It is the heart you have seen before.')
                    # Player sees heart
                    self.seeHeart()
                    # Trigger inspire on player if they are Endemene
                    if self.character['id'] == 1:
                        self.inspire('Lens')
            # Show vision if player has lens
            if 'Lens' in self.prototypes:
                # Remove net
                self.prototypes.remove('Lens')
                # Report information for player only
                if self.isPlayer():
                    print('As you lay down for a rest, the lens you crafted grants you insight into the party members resting beside you.')
                    otherRestingPlayers = list(filter(lambda p: p.id in g_game.restTargets, self.getOtherPlayers()))
                    # If no other players resting, report failure
                    if len(otherRestingPlayers) == 0:
                        print('Unfortunately, there are no such party members. Your lens fractures and crumbles to dust in your hands, leaving you no wiser.')
                    else:
                        for p in otherRestingPlayers:
                            providedRoles = []
                            providedRoles.append(p.role) # Add real role
                            rolesInPlayNotSelfOrTarget = list(map(lambda s: s.role, list(filter(lambda q: q.isAbleToAct() and q.id != self.id and q.id != p.id, g_game.allPlayers))))
                            rolesInPlayByID = list(map(lambda s: s.role['id'], list(filter(lambda q: q.isAbleToAct(), g_game.allPlayers))))
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
                            print(p.styleCharacterName() + '\'s role is one of the following: ')
                            for r in randomizedRoles:
                                print(r['name'])
                            # Separate results with newline
                            print('')
            # Unravel if player is Rainee Haraldsson
            if self.character['id'] == 2:
                self.unravel()
            # Discover if player is Dredge
            if self.character['id'] == 4:
                self.discover()
    # END REST

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
            guardian = lookupPlayerByID(guardSourceID)
            # Initialize guardian name
            guardianName = guardian.styleCharacterName()
            # Report outcome
            if target.isPlayer():
                # Change output if player guarded the target
                if guardian.isPlayer():
                    guardianName = 'you'
                print('You were attacked by ' + self.styleCharacterName() + ', but ' + guardianName + ' fought them off.')
            elif self.isPlayer():
                print(guardianName + ' fought off your attack on ' + target.styleCharacterName() + '.')
            else:
                # Change output if player guarded the target
                if guardian.isPlayer():
                    guardianName = 'You'
                print(guardianName + ' fought off an attack from ' + self.styleCharacterName() + ' on ' + target.styleCharacterName() + '.')
            # If Marloe revealed this turn, target receives a curse
            if g_game.marloeRevealedThisTurn:
                # Target becomes cursed
                target.timesCursed += 1
                # Report outcome
                if target.isPlayer():
                    print('You were saved from attack by the grace of House Marloethien. This grace did not however come without a cost. You are now cursed.')
                else:
                    print(target.styleCharacterName() + ' was saved from attack by the grace of House Marloethien. This grace did not however come without a cost. They are now cursed.')
        # If target is not guarded, reject attack if target is shielded
        elif 'Shield' in target.prototypes:
            # Remove shield
            target.prototypes.remove('Shield')
            # Report outcome
            if target.isPlayer():
                print('You were attacked by ' + self.styleCharacterName() + ', but your shield deflected the blow. It will not hold up against another.')
            elif self.isPlayer():
                print(target.styleCharacterName() + ' was protected from your attack by her shield. It will not hold up against another.')
            else:
                print(target.styleCharacterName() + ' was protected from ' + self.styleCharacterName() + '\'s attack by her shield. It will not hold up against another.')
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
                    print('The unnatural strength instilled in you by your close call with the beast in Longway Alley allowed you to survive an attack from ' + self.styleCharacterName() + ' that otherwise would have been deadly. Your survival is not without consequence, however. A shiver runs down your spine as the beast\'s call, a haunting whine, reverberates in your mind. You are now cursed.')
                elif self.isPlayer():
                    print('The unnatural strength instilled in ' + target.styleCharacterName() + ' by their close call with the beast in Longway Alley allowed them to survive your attack that otherwise would have been deadly. Their survival is not without consequence, however. They are now cursed.')
                else:
                    print('The unnatural strength instilled in ' + target.styleCharacterName() + ' by their close call with the beast in Longway Alley allowed them to survive an attack from ' + self.styleCharacterName() + ' that otherwise would have been deadly. Their survival is not without consequence, however. They are now cursed.')
            else:
                # Report outcome
                if target.isPlayer():
                    print('You were killed by  ' + self.styleCharacterName() + ' in your sleep.')
                elif self.isPlayer():
                    print('You killed ' + target.styleCharacterName() + ' in their sleep.')
                else:
                    print(self.styleCharacterName() + ' killed ' + target.styleCharacterName() + ' in their sleep.')
                # Target dies
                target.die()
        # Target will die if they have more than one level of exhaustion or if the sword is drawn 
        elif target.exhaustionLevel > 1 or g_game.isSwordDrawn:
            # Report Outcome
            if target.isPlayer():
                print('You were killed in a struggle with ' + self.styleCharacterName() + '.')
            elif self.isPlayer():
                print('You killed ' + target.styleCharacterName() + ' in a struggle.')
            else:
                print(self.styleCharacterName() + ' killed ' + target.styleCharacterName() + ' in a struggle.')
            # Target dies
            target.die()
        else:
        # Otherwise target gains a level of exhaustion
            # Report outcome
            if target.isPlayer():
                print('You fought off an attack from ' + self.styleCharacterName() + '.')
            elif self.isPlayer():
                print(target.styleCharacterName() + ' fought off your attack.')
            else:
                print(target.styleCharacterName() + ' fought off an attack from ' + self.styleCharacterName() + '.')
            # Target gains exhaustion
            target.gainExhaustion()
            # Separate exhaustion output with a line break
            print('')
            # Stun target if self has a Net
            if 'Net' in self.prototypes:
                # Remove net
                self.prototypes.remove('Net')
                # Stun target
                target.isStunned = True
                # Report outcome
                if self.isPlayer():
                    print('Your net entraps ' + target.styleCharacterName() + ', stunning them while they cut their way free.')
                elif target.isPlayer():
                    print(self.styleCharacterName() + '\'s net entraps you, stunning you while you cut your way free.')
                else:
                    print(self.styleCharacterName() + '\'s net entraps ' + target.styleCharacterName() + ', stunning them while they cut their way free.')
        # Each AI that is not dead or escaped and is not already aggressive and is not hostile to the attack target and is not the attacker adds the attacker's id to their list of hostiles
        for p in self.getOtherPlayers():
            if p.isAlive and not p.hasEscaped and not p.mode == 3 and not p.isPlayer() and target.id not in p.isHostileTowards and ((g_game.location.room['id'] != 0 and g_game.location.room['id'] != 1 and g_game.location.room['id'] != 2) or (self.role['id'] == 5 and self.isRevealed)): # Forgive attacks in Arena, Tower, or Alley unless the attacker is revealed as the Fisherwoman
                # Add to list of hostiles
                p.isHostileTowards.append(self.id)
                # If AI is not already DEFENSIVE, change it to be and report
                if not p.mode == 4:
                    print(p.styleCharacterName() + ' takes the defensive.')
                    p.mode = 4
    # END ATTACK

    def passAction(self):
        # player passes
        self.hasPassed = True
        # Report outcome
        if self.isPlayer():
            print('You passed action.')
        else:
            print(self.styleCharacterName() + ' passed action.')
    # END PASSACTION 

    def escape(self):
        # Player escapes
        self.hasEscaped = True
        # Carry out Cloudblessed delayed trigger if necessary
        attemptCloudblessedRevive()
    # END ESCAPE 

    def die(self):
        # Load game
        global g_game
        # Player dies
        self.isAlive = False
        # If sword is drawn, a player dying removes the effect
        if g_game.isSwordDrawn:
            # Report outcome
            print('Although lethal, the sword is also brittle. With its lust for blood sated, it breaks into pieces to small to reconstitute it from.')
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
        # Trigger Erstwhile reveal on everyone else who is active
        _ = [p.triggerReveal('Erstwhile, Collector Supreme') for p in list(filter(lambda p: p.isAbleToAct(), self.getOtherPlayers()))]
        # Carry out Cloudblessed delayed trigger if necessary
        attemptCloudblessedRevive()
    # END DIE

    def seeHeart(self):
        # If this is the first time an AI has seen heart, notify player if their role is Fisherwoman
        if self.timesSeenHeart == 0:
            otherPlayers = self.getOtherPlayers()
            for p in otherPlayers:
                if p.isPlayer() and p.role['id'] == 5:
                    print(self.styleCharacterName() + ' saw the Wandering Heart in their dreams as they rested. They must not be allowed to leave the dungeon alive.')
        # If this is the second time an AI has seen heart, notify player if their role is Fisherwoman
        if self.timesSeenHeart == 1:
            otherPlayers = self.getOtherPlayers()
            for p in otherPlayers:
                if p.isPlayer() and p.role['id'] == 5:
                    print(self.styleCharacterName() + ' saw the Wandering Heart for a second time in their dreams as they rested. They grow near to escape. Kill them now.')
        # Increment times seen heart
        self.timesSeenHeart += 1
        # If this is the first, second, or greater than third time, exhaustion is reduced to 0
        if self.timesSeenHeart != 3:
            # Reduce exhaustion
            self.exhaustionLevel == 0
            # Report outcome if self is player
            if self.isPlayer():
                print('After a few minutes spent observing the thing\'s rhythmic motion, a peculiar energy fills you. You leave the heart feeling as awake and alert as you have ever been.')
        # Else player is given the opportunity to escape.
        else:
            if self.isPlayer():
                print('On this your third meeting, the heart stretches out a stray strand of fibrous material as if offering a hand to you. Will you take it and escape into the world of dreams? [y/n]')
                validInput = False
                while not validInput:
                    command = input()
                    try:
                        command = command.lower()
                    except ValueError:
                        pass
                    # Output result of choice
                    match command:
                        case 'y':
                            self.escape()
                            print('You escaped from the dungeon.')
                            validInput = True
                        case 'n':
                            print('You decline the offer, carrying on without the Heart\'s guidance.')
                            validInput = True
            else:
                # Otherwise decide choice of AI
                shouldEscape = self.shouldAiEscape()
                if shouldEscape:
                    print(self.styleCharacterName() + ' disappeared in their rest, vanished from this plane to the sound of a thrumming heartbeat. They have escaped the dungeon.')
                    # AI escapes
                    self.escape()
    # END SEEHEART

    def isAbleToAct(self):
        # Load game
        global g_game
        if not self.isAlive:
            return False
        if self.hasPassed:
            return False
        if self.hasEscaped:
            return False
        if not self.hasAttacked:
            return True
        if not self.hasRested:
            return True
        if not self.hasInvestigated and not g_game.location.hasBeenInvestigated:
            return True
        if not self.hasExerted and not g_game.location.hasBeenExerted:
            return True
        if not self.hasExplored and not g_game.location.hasBeenExplored:
            return True
        if not self.hasUsedActive:
            return True
        return False
    # END ISABLETOACT

    def getOtherPlayers(self):
        # Load game
        global g_game
        # Initialize list of other players
        otherPlayers = []
        # Add each player with an ID that is not the caller's ID
        for p in g_game.allPlayers:
            if p.id != self.id:
                otherPlayers.append(p)
        return otherPlayers

    def decideAiAction(self):
        # Load game
        global g_game
        # If room is the alley and ai is the randomly chosen one to act randomly, choose their action randomly from among those that are valid
        if g_game.location.room['id'] == 2 and g_game.randomID == self.id:
            # Find random other player to target
            try:
                randomTarget = rng.sample(list(filter(lambda p: p.isAbleToAct(), self.getOtherPlayers())), 1)[0]
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
        # Determine if OPPORTUNISTIC AI should change to AGGRESSIVE
        if self.mode == 1:
            if self.shouldAiAggro():
                self.mode = 3
                g_game.timesAggroed += 1 # TEST USE ONLY
        # Determine if DEFENSIVE AI should change back to their default
        if self.mode == 4:
            if len(list(filter(lambda pid: lookupPlayerByID(pid).isAlive and not lookupPlayerByID(pid).hasEscaped, self.isHostileTowards))) == 0:
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
            target = getMostExhaustedPlayer(list(filter(lambda p: p.isAbleToAct(), list(map(lambda pid: lookupPlayerByID(pid), self.isHostileTowards)))))
            # If such a player exists, attack them player
            if target:
                return ('Attack', target)
        elif factors['mode'] == 3 and ((not self.hasAttacked and not self.isAnchored) or (self.hasAttacked and self.isAnchored)): # IF AI is AGGRESSIVE, lead with attack on a vulnerable player
            # Randomly select a target among the most exhausted other active players
            target = getMostExhaustedPlayer(list(filter(lambda p: p.isAbleToAct(), otherPlayers)))
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
            numOtherActivePlayers = len(list(filter(lambda p: p.isAbleToAct(), self.getOtherPlayers())))
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
                target = getMostExhaustedPlayer(list(filter(lambda p: p.isAbleToAct(), otherPlayers)))
                # If such a player exists, attack them player
                if target:
                    return ('Attack', target)
        # Call Upon Family if role is Marloe when things are getting down to the nitty-gritty in a room
        if factors['role'] == 3 and not self.isRevealed and (self.attemptedToPass or factors['room'] == 0 or factors['room'] == 1 or factors['room'] == 3) and not self.isAnchored:
            return ('Reveal Active', None)
        # If AI has tried and failed to pass, attack to either change the situation or expend its last option, resulting in its death
        if ((not self.hasAttacked and not self.isAnchored) or (self.hasAttacked and self.isAnchored)) and self.attemptedToPass:
            # Randomly select a target among the most exhausted other active players (only if a pass attempt has already failed)
            target = getMostExhaustedPlayer(list(filter(lambda p: p.isAbleToAct(), otherPlayers)))
            # If such a player exists, attack them player
            if target:
                return ('Attack', target)
        # When nothing is left to do, pass
        return ('Pass', None)
    # END DECIDEAIACTION

    def getPlayerTarget(self, action):
        # Initialize target to none in case action is one that does not require one
        target = None
        # Get target if there is one associated with the chosen action
        match action:
            case 'Attack':
                print('Choose a player to attack:')
                otherActivePlayers = list(filter(lambda p: p.isAbleToAct(), self.getOtherPlayers()))
                for i in range(len(otherActivePlayers)):
                    print(str(i + 1) + '. ' + otherActivePlayers[i].styleCharacterName())    
                # Read in player's choice of target
                target = getPlayerInput(otherActivePlayers)
            case 'Special Active':
                # Determine what active the character has
                match self.character['name']:
                    case 'Endemene Silverblood':
                        # Give player choice of inspiration
                        print('Choose an inspiration to prototype:')
                        inspiration = self.inspiration
                        for i in range(len(inspiration)):
                            print(str(i + 1) + '. ' + inspiration[i])
                        # Read in player's choice of prototype
                        target = getPlayerInput(inspiration)
                    case 'Rainee Haraldsson':
                        # Give player choice of interrogate target from among active players that have not already been successfully guessed
                        print('Choose a player to guess the role of:')
                        otherActiveUnguessedPlayers = list(filter(lambda p: p.isAbleToAct() and p.id not in self.guessedPlayers, self.getOtherPlayers()))
                        for i in range(len(otherActiveUnguessedPlayers)):
                            print(str(i + 1) + '. ' + otherActiveUnguessedPlayers[i].styleCharacterName())
                        # Read in player's choice of target
                        target = getPlayerInput(otherActiveUnguessedPlayers)
                    case 'Elvy, the Heart-Hammerer':
                        # Give player choice of guard target
                        print('Choose a player to guard:')
                        otherActivePlayers = list(filter(lambda p: p.isAbleToAct(), self.getOtherPlayers()))
                        for i in range(len(otherActivePlayers)):
                            print(str(i + 1) + '. ' + otherActivePlayers[i].styleCharacterName())    
                        # Read in player's choice of target
                        target = getPlayerInput(otherActivePlayers)
                    case 'Mantelesse the Far-Dreaming':
                        # Give player choice of weird target
                        print('Choose a player to weird:')
                        otherActivePlayers = list(filter(lambda p: p.isAbleToAct(), self.getOtherPlayers()))
                        for i in range(len(otherActivePlayers)):
                            print(str(i + 1) + '. ' + otherActivePlayers[i].styleCharacterName())    
                        # Read in player's choice of target
                        target = getPlayerInput(otherActivePlayers)
        return target

    def takeAction(self, action, target):
        # Load game
        global g_game
        match action:
            case '':
                pass
            case 'Attack':
                # Report action
                if self.isPlayer():
                    print('You attacked ' + target.styleCharacterName() + '.')
                elif target.isPlayer():
                    print(self.styleCharacterName() + ' attacked you.')
                else:
                    print(self.styleCharacterName() + ' attacked ' + target.styleCharacterName() + '.')
                # Add self to list of attack sources
                g_game.attackSources.append(self.id)
                # Add target to list of attack targets
                g_game.attackTargets.append(target.id)
                # Remove attack option for future turns in the room
                self.hasAttacked = True
            case 'Rest':
                # Report action
                if self.isPlayer():
                    print('You rested.')
                else:
                    print(self.styleCharacterName() + ' rested.')
                # Add self to list of rest targets
                g_game.restTargets.append(self.id)
                # Remove rest option for future turns in the room
                self.hasRested = True
            case 'Pass':
                # Add self to list of passing players
                g_game.passingPlayers.append(self)
                # Report intention to pass.
                if self.isPlayer():
                    print('You attempted to leave the room.')
                else:
                    print(self.styleCharacterName() + ' attempted to leave the room.')
            case 'Investigate':
                # Report action
                if self.isPlayer():
                    print('You chose to ' + g_game.location.room['actions'][0] + '.')
                else:
                    print(self.styleCharacterName() + ' chose to ' + g_game.location.room['actions'][0] + '.')
                # Mark as investigated
                self.hasInvestigated = True
                g_game.investigateTotal += self.character['ingenuity'] + self.timesCursed
            case 'Exert':
                # Report action
                if self.isPlayer():
                    print('You chose to ' + g_game.location.room['actions'][1] + '.')
                else:
                    print(self.styleCharacterName() + ' chose to ' + g_game.location.room['actions'][1] + '.')
                # Mark as investigated
                self.hasExerted = True
                g_game.exertTotal += self.character['resolve'] + self.timesCursed
            case 'Explore':
                # Report action
                if self.isPlayer():
                    print('You chose to ' + g_game.location.room['actions'][2] + '.')
                else:
                    print(self.styleCharacterName() + ' chose to ' + g_game.location.room['actions'][2] + '.')
                # Mark as explored
                self.hasExplored = True
                g_game.exploreTotal += self.character['finesse'] + self.timesCursed
            case 'Special Active':
                # Mark special active as used
                self.hasUsedActive = True
                # Determine what active the character has
                match self.character['name']:
                    case 'Reika of the Thousand Days':
                        # Player re-decides action and target
                        if self.isPlayer():
                            print('Choose an action to retake: ')
                            # Initialize options list
                            options = []
                            optionNum = 1
                            # Determine which options are available to the players and print
                            if g_game.player.hasAttacked and list(map(lambda p: p.isAbleToAct(), g_game.player.getOtherPlayers())) != [False, False, False]:
                                options.append('Attack')
                                print(str(optionNum) + '. Attack')
                                optionNum += 1
                            if g_game.player.hasRested and g_game.player.exhaustionLevel > 0:
                                options.append('Rest')
                                print(str(optionNum) + '. Rest')
                                optionNum += 1
                            if g_game.player.hasInvestigated and not g_game.location.hasBeenInvestigated:
                                options.append('Investigate')
                                # Calculate discount for if mirror was successfully interrogated
                                discount = 0
                                if g_game.isCluedIn:
                                    discount = 2
                                print(str(optionNum) + '. ' + room['actions'][0] + ' (' + str(room['requirements'][0] - discount) + ' Ingenuity)')
                                optionNum += 1
                            if g_game.player.hasExerted and not g_game.location.hasBeenExerted:
                                options.append('Exert')
                                print(str(optionNum) + '. ' + room['actions'][1] + ' (' + str(room['requirements'][1]) + ' Resolve)')
                                optionNum += 1
                            if g_game.player.hasExplored and not g_game.location.hasBeenExplored:
                                options.append('Explore')
                                print(str(optionNum) + '. ' + room['actions'][2] + ' (' + str(room['requirements'][2]) + ' Finesse)')
                                optionNum += 1
                            options.append('Pass')
                            print(str(optionNum) + '. Pass')
                            # Read in player's choice of action
                            action = getPlayerInput(options)
                            # Read in player's choice of target
                            target = self.getPlayerTarget(action)
                            # Handle chosen action with recursive call
                            self.takeAction(action, target)
                        else:
                            # Mark as anchored
                            self.isAnchored = True
                            # Get new AI action and target
                            action, target = self.decideAiAction()
                            # Report outcome
                            print(self.styleCharacterName() + ' anchored herself.')
                            # Handle chosen action with recursive call
                            self.takeAction(action, target)
                            # Mark as no longer anchored
                            self.isAnchored = False
                    case 'Endemene Silverblood':
                        # Add prototype to list of prototypes available to be used
                        self.prototypes.append(target)
                        # Add prototype to list of prototypes that cannot have inspiration gained for them again
                        self.hasPrototyped.append(target)
                        # remove prototype from inspiration list
                        self.inspiration.remove(target)
                        # Report outcome
                        if self.isPlayer():
                            print('You prototyped ' + target + '.')
                        else:
                            print(self.styleCharacterName() + ' prototyped ' + target + '.')
                    case 'Rainee Haraldsson':
                        # Ask player to guess
                        if self.isPlayer():
                            print('Enter your guess for ' + target.styleCharacterName() + '\'s role.')
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
                                    print(str(optionNum) + '. ' + role)
                                    optionNum += 1
                            # Read in player's choice of guess
                            guess = getPlayerInput(options)
                            # Inform player of the result of their guess
                            if guess == target.role['name']:
                                print('Your hunch proved correct. ' + target.styleCharacterName() + '\'s role is ' + target.styleRoleName() + '.')   
                                # Add target to list of guessed roles.
                                self.guessedPlayers.append(target.id)  
                            else:
                                print('Your hunch did not hold up. Still, you are closer now to unraveling the mystery that is ' + target.styleCharacterName() + '.')
                        else:
                            if target.isPlayer():
                                print(self.styleCharacterName() + ' interrogated you.')
                            else:
                                print(self.styleCharacterName() + ' interrogated ' + target.styleCharacterName() + '.')      
                    case 'Elvy, the Heart-Hammerer':
                        # If Elvy is still warded, remove ward
                        if self.isWarded:
                            self.loseWard()
                        # Report action
                        if self.isPlayer():
                            print('You guarded ' + target.styleCharacterName() + '.')
                        elif target.isPlayer():
                            print(self.styleCharacterName() + ' guarded you.')
                        else:
                            print(self.styleCharacterName() + ' guarded ' + target.styleCharacterName() + '.')
                        # Add target to list of guarded targets
                        g_game.guardTargets.append(target.id)
                        # Add source to list of guarding players
                        g_game.guardSources.append(self.id)
                    case 'Dredge':
                        if self.isPlayer():
                            # Print name of next room for player
                            try:
                                print('Through your scouting you learn that the next room the party will enter is ' + g_game.shuffledRooms[g_game.roomIndex]['name'] + '.')
                            # If there is no such room, report this
                            except IndexError:
                                print('Through your scouting, you learn that no rooms remain ahead of you. This is the end of the line.')
                        else:
                            print(self.styleCharacterName() + ' scouted ahead.')
                    case 'Mantelesse the Far-Dreaming':
                        # Report action
                        if self.isPlayer():
                            print('You weirded ' + target.styleCharacterName() + '.')
                        elif target.isPlayer():
                            print(self.styleCharacterName() + ' weirded you.')
                        else:
                            print(self.styleCharacterName() + ' weirded ' + target.styleCharacterName() + '.')
                        # Mark target as weirded
                        target.isWeirded = True
            case 'Reveal Active':
                # Trigger Marloe reveal
                self.triggerReveal('Marloe, Don of the Downtrodden')
    # END TAKEACTION

    def shouldAiEscape(self):
        # Load game
        global g_game
        match self.role['name']:
            case 'Mnanth, Whose Heart is Glass':
                if lookupPlayerByID(self.pactTargetID).isAlive == False:
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
                if len(list(filter(lambda p: p.timesCursed == 0 and p.isAlive and not p.hasEscaped, self.getOtherPlayers()))) == 0:
                    return True
                return False
            case 'Erstwhile, Collector Supreme':
                # Erstwhile will never try to escape
                return False
            case 'The Fisherwoman':
                # Escape if all other players are dead or escaped
                if len(list(filter(lambda p: p.isAlive and not p.hasEscaped, self.getOtherPlayers()))) == 0:
                    return True
                return False
    # END SHOULDAIESCAPE

    def shouldAiAggro(self):
        # Load Game
        global g_game
        # Never aggro if unable to attack
        if self.hasAttacked:
            return False
        # Never aggro if win condition has already been fulfilled
        if self.shouldAiEscape():
            return False
        otherActivePlayers = list(filter(lambda p: p.isAbleToAct(), self.getOtherPlayers()))
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

    def printCharacterInfo(self):
        character = self.character
        print(self.styleCharacterName() + '\nIngenuity: ' + str(character['ingenuity']) + '\nResolve: ' + str(character['resolve']) + '\nFinesse: ' + str(character['finesse']))
        print('Special Passive - ' + character['passive'] + ': ' + character['passiveDescription'] + '\nSpecial Active - ' + character['active'] + ': ' + character['activeDescription'])
    # END PRINTCHARACTERINFO

    def printRoleInfo(self):
        role = self.role
        print(self.styleRoleName() + '\nReveal Condition & Ability - ' + role['reveal'] + ': ' + role['revealDescription']+ '\nWin Condition - ' + role['winCondition'] + ': ' + role['winConDescription'])
        # Inform player of pact target's role if their role is Mnanth
        if role['id'] == 0:
            print('Your pact target is ' + lookupPlayerByID(self.pactTargetID).role['name'])
    # END PRINTROLEINFO

    def checkWinConditions(self):
        # Load game
        global g_game
        match self.role['name']:
            case 'Mnanth, Whose Heart is Glass':
                if not self.hasEscaped:
                    # Loss output 1 for player
                    if self.isPlayer():
                        print('You failed to escape. You lose the game.')
                        return
                    # Loss output 1 for AI
                    print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', failed to escape. They lose the game.')
                    return
                for p in g_game.allPlayers:
                    if lookupPlayerByID(self.pactTargetID).hasEscaped == True:
                        # Loss output 2 for player
                        if self.isPlayer():
                            print('You failed to prevent your sworn enemy from escaping the dungeon. You lose the game.')
                            return
                        # Loss output 2 for AI
                        print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', failed to eliminate their sworn enemy, ' + lookupPlayerByID(self.pactTargetID).character['name'] + '. They lose the game.')
                        return
                # Win output for player
                if self.isPlayer():
                    print('You managed to eliminate your sworn enemy and escape to tell the tale. You win the game.')
                    self.hasWon = True # for TEST mode only
                    return
                # Win output for AI
                print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', managed to eliminate their sworn enemy, ' + lookupPlayerByID(self.pactTargetID).character['name'] + ', and escape to tell the tale. They win the game.')
                self.hasWon = True # for TEST mode only
                return
            case 'Casglowve, the Captive Moon':
                if not self.hasEscaped:
                    # Loss output 1 for player
                    if self.isPlayer():
                        print('You failed to escape. You lose the game.')
                        return
                    # Loss output 1 for AI
                    print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', failed to escape. They lose the game.')
                    return
                for p in g_game.allPlayers:
                    if not g_game.isTowerBroken:
                        # Loss output 2 for player
                        if self.isPlayer():
                            print('You failed to break the Tower and free your love. You lose the game.')
                            return
                        # Loss output 2 for AI
                        print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', failed to break the tower and free their love. They lose the game.')
                        return
                # Win output for player
                if self.isPlayer():
                    print('You managed to break the tower, free your love, and escape. You win the game.')
                    self.hasWon = True # for TEST mode only
                    return
                # Win output for AI
                print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', managed to break the tower, free their love, and escape. They win the game.')
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
                                print('Half or more of the party managed to escape. You win the game.')
                                self.hasWon = True # for TEST mode only
                                return
                            # Win output for AI
                            print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', managed to see half or more of the party to freedom. They win the game.')
                            self.hasWon = True # for TEST mode only
                            return
                # Loss output for player
                if self.isPlayer():
                    print('Fewer than half of the party managed to escape. You lose the game.')
                    return
                # Loss output for AI
                print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', was not able to see half or more of the party to freedom. They lose the game.')
                return
            case 'Marloe, Don of the Downtrodden':
                if not self.hasEscaped:
                    # Loss output 1 for player
                    if self.isPlayer():
                        print('You failed to escape. You lose the game.')
                        return
                    # Loss output 1 for AI
                    print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', failed to escape. They lose the game.')
                    return
                for p in self.getOtherPlayers():
                    if p.hasEscaped and p.timesCursed == 0:
                        # Loss output 2 for player
                        if self.isPlayer():
                            print('You failed to prevent adventurers from escaping your grasp without being cursed. You lose the game.')
                            return
                        # Loss output 2 for AI
                        print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', failed to prevent adventurers from escaping their grasp without being cursed. They lose the game.')
                        return
                # Win output for player
                if self.isPlayer():
                    print('You managed to escape, which no others managed to do without being cursed. You win the game.')
                    self.hasWon = True # for TEST mode only
                    return
                # Win output for AI
                print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', escaped while preventing any adventurers from doing the same without being cursed. They win the game.')
                self.hasWon = True # for TEST mode only
                return
            case 'Erstwhile, Collector Supreme':
                if self.numRoomsVisited == 6:
                    # Win output for player
                    if self.isPlayer():
                        print('You visited every room in the dungeon. You win the game.')
                        self.hasWon = True # for TEST mode only
                        return
                    # Win output for AI
                    print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', visited every room in the dungeon. They win the game.')
                    self.hasWon = True # for TEST mode only
                    return
                # Loss output for player
                if self.isPlayer():
                    print('You did not visit every room in the dungeon before expiring. You lose the game.')
                    return
                # Loss output for AI
                print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', did not visit every room in the dungeon before expiring. They lose the game.')
                return
            case 'The Fisherwoman':
                if self.timesSeenHeart == 0:
                    # Loss output 1 for player
                    if self.isPlayer():
                        print('You failed to see the heart for yourself. You lose the game.')
                        return
                    # Loss output 1 for AI
                    print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', failed to see the heart for themself. They lose the game.')
                    return
                for p in self.getOtherPlayers():
                    if p.hasEscaped and p.timesSeenHeart > 0:
                        # Loss output 2 for player
                        if self.isPlayer():
                            print('You failed to prevent observers of the Wandering Heart from escaping. You lose the game.')
                            return
                        # Loss output 2 for AI
                        print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', failed to prevent observers of the Wandering Heart from escaping. They lose the game.')
                        return
                # Win output for player
                if self.isPlayer():
                    print('No observers of the Wandering Heart managed to escape, while you yourself did. You win the game.')
                    self.hasWon = True # for TEST mode only
                    return
                # Win output for AI
                print(self.styleCharacterName() + ', whose role was ' + self.styleRoleName() + ', escaped while preventing any observers of the Wandering Heart from doing the same. They win the game.')
                self.hasWon = True # for TEST mode only
                return
    # END CHECKWINCONDITIONS

    def triggerReveal(self, role):
        # Only trigger if self has the role that is being tested for and if self has not already been revealed
        if self.role['name'] == role and not self.isRevealed:
            # If player is warded, prevent reveal unless reveal is intentional or role is Cloudblessed
            if self.isWarded and role != 'Marloe, Don of the Downtrodden' and role != 'Cloudblessed':
                # Report succesful warding (if self is player)
                self.ward()
            else:
                # Report reveal
                if self.isPlayer():
                    print('Your role was revealed to be ' + self.styleRoleName() + '.')
                else:
                    print(self.styleCharacterName() + '\'s role was revealed to be ' + self.styleRoleName() + '.')
                # Mark as revealed
                self.isRevealed = True
                # Perform reveal effect
                self.reveal()
                # Quip
                self.quip()
    # END TRIGGERREVEAL

    def reveal(self):
        # Load game
        global g_game
        match self.role['name']:
            case 'Mnanth, Whose Heart is Glass':
                # Bar way
                g_game.isWayBarred = True
                # Report outcome
                print('Pillars of glass burst up from the ground to deny exit to all who remain in ' + g_game.location.room['name'] + '. They will not yield but for a lone player.')
            case 'Casglowve, the Captive Moon':
                # Pass immediately, ignoring all restrictions
                self.hasPassed = True
                # Report outcome if player has this role
                if self.isPlayer():
                    print('As you exit the room, born aloft on wings of moonlight, you feel a surge of wakefulness flow into you.')
                # Gain the benefit of a rest
                self.rest()
                # Each other active player gains exhaustion
                for p in self.getOtherPlayers():
                    if p.isAbleToAct():
                        # Report outcome if an ai has this role
                        if p.isPlayer():
                            print('As ' + self.styleCharacterName() + ' exits the room, born aloft on wings of moonlight, you feel a wave of exhaustion hit you. A part of you was taken to fuel their flight.')
                        # Gain exhaustion
                        p.gainExhaustion()
            case 'Cloudblessed':
                # Mark Cloudblessed as revealed in the current room
                g_game.location.cloudblessedRevealed = True
                # Report outcome
                if self.isPlayer():
                    print('A hallowed mist seeps into the room in the wake of your fall.')
                else:
                    print('A hallowed mist seeps into the room in the wake of ' + self.styleCharacterName() + '\'s fall.')
            case 'Marloe, Don of the Downtrodden':
                # Report outcome
                if self.isPlayer():
                    print('You call upon the power of the Fae House Marloethien, guarding all players from attack this turn.')
                else:
                    print(self.styleCharacterName() + ' calls upon the power of the Fae House Marloethien, guarding all players from attack this turn.')
                # Add other active players to guard targets and self to guard sources
                for p in g_game.allPlayers:
                    if p.isAbleToAct():
                        g_game.guardTargets.append(p.id)
                        g_game.guardSources.append(self.id)
                # Mark that Marloe was revealed this turn, so anyone successfully guarded can receive a curse
                g_game.marloeRevealedThisTurn = True
            case 'Erstwhile, Collector Supreme':
                # Report outcome
                print('Calming spores descend on the stricken party, granting everyone the strength to fight on a little longer.')
                # Each active player gains the benefit of a rest
                for p in self.getOtherPlayers():
                    if p.isAbleToAct():
                        p.rest()
            case 'The Fisherwoman':
                # Report outcome
                if self.isPlayer():
                    print('The brutality of your attack hits the other players like an avalanche, leaving them too stunned to act during their next turn.')
                elif g_game.player:
                    if g_game.player.isAbleToAct():
                        # Special print for when player is not self but is able to act
                        print('The brutality of ' + self.styleCharacterName() + '\'s attack hits you and the other players like an avalanche, leaving you too stunned to act during your next turn.')   
                    else:
                        print('The brutality of  ' + self.styleCharacterName() + '\'s attack hits the other players like an avalanche, leaving them too stunned to act during their next turn.')
                # Stun players
                for p in self.getOtherPlayers():
                    if p.isAbleToAct():
                        p.isStunned = True
                # Replenish attack action
                self.hasAttacked = False
    # END REVEAL

    def quip(self):
        # Quip only if self is an AI
        if not self.isPlayer():
            # Lookup character's reveal quip by id
            print(self.styleCharacterName() + ': "' + self.character['revealQuips'][self.role['id']] + '"')
    # END QUIP

    def undertow(self):
        # Return to play
        self.hasPassed = False
        # Report outcome
        if self.isPlayer():
            print('The undertow of the Piece of Time you wear drags you back to the moment before you left this room behind you. There is still more to do.')
        else:
            print('The undertow of the Piece of Time ' + self.styleCharacterName() + ' wears drags her back to the moment before she left this room behind her. There is still more to do.')
    # END UNDERTOW

    def inspire(self, inspiration):
        # Ignore if this inspiration has already been obtained
        if inspiration not in self.hasPrototyped and inspiration not in self.inspiration:
            # Add inspiration
            self.inspiration.append(inspiration)
            # Report outcome
            match inspiration:
                case 'Wings': # # Next time you would fail to pass, pass without instead
                    if self.isPlayer():
                        print('You are inspired in your isolation. You may now prototype wings.')
                    else:
                        print(self.styleCharacterName() + ' is inspired by her isolation.')
                case 'Shield': # Next time you would be attacked and are not guarded, prevent the attack 
                    if self.isPlayer():
                        print('You are inspired by the cruel workings of the deadly sword. You may now prototype a shield.')
                    else:
                        print(self.styleCharacterName() + ' is inspired by the cruel workings of the deadly sword.')
                case 'Lens': # Next time you rest, see the following for each player that rests at the same time: the role they have, the role another player has, and a role no player has. You will not know which is which
                    if self.isPlayer():
                        print('You are inspired by the sight of the heart in dreams. You may now prototype a lens.')
                    else:
                        print(self.styleCharacterName() + ' is inspired by something seen in her dreams.')
                case 'Net':
                    if self.isPlayer(): # The next time you attack a player, that player skips their next action
                        print('You are inspired by the imminent threat upon your life. You may now prototype a net.')
                    else:
                        print(self.styleCharacterName() + ' is inspired by the imminent threat upon her life.')
    # END INSPIRE

    def loseWard(self):
        # Remove ward
        self.isWarded = False
        # Report outcome
        if self.isPlayer():
            print('Your conspicuous action exposes you for what you really are. Your ward evaporates off your body.')
        else:
            print('Their conspicuous action exposes ' + self.styleCharacterName() + ' for what they really are. Their ward evaporates off their body.')
    # END LOSEWARD

    def ward(self):
        # Report outcome when player would be revealed
        if self.isPlayer():
            print('The ward you wear like a skin protects you from all scrutiny. Your role is not revealed.')
    # END WARD

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
                print('You discovered 1 supplies at your place of rest.')
            else:
                print(self.styleCharacterName() + ' discovered 1 supplies at his place of rest.')
        elif discoveryRoll >= 5 and discoveryRoll < 7:
            # Add 2 party supplies
            g_game.partySupplies += 2
            # Report outcome
            if self.isPlayer():
                print('You discovered 2 supplies at your place of rest.')
            else:
                print(self.styleCharacterName() + ' discovered 2 supplies at his place of rest.')
        elif discoveryRoll == 7:
            # Add 3 party supplies
            g_game.partySupplies += 3
            # Report outcome
            if self.isPlayer():
                print('You discovered 3 supplies at your place of rest.')
            else:
                print(self.styleCharacterName() + ' discovered 3 supplies at his place of rest.')
        else:
            # Add key
            g_game.isKeyFound = True
            # Report outcome
            if self.isPlayer():
                print('You discovered a mysterious key at your place of rest.')
            else:
                print(self.styleCharacterName() + ' discovered a mysterious key at his place of rest.')
    # END DISCOVER

    def unravel(self):
        # Load game
        global g_game
        # Load roles
        global g_roles
        # Create list of roles that have not already been unraveled and that are not currently in play
        rolesInPlay = list(map(lambda p: p.role, list(filter(lambda p: p.isAbleToAct(), g_game.allPlayers))))
        uniqueRolesNotInPlay = list(filter(lambda r: r not in rolesInPlay and r['id'] not in self.unraveledRoles, g_roles))
        # If no roles qualify, report this for player
        if len(uniqueRolesNotInPlay) == 0:
            if self.isPlayer():
                print('Every role either is in the room with you or has been seen by you before in dreams. You learn nothing from this dream.')
        # Otherwise select a role at random to unravel
        else:
            unraveledRole = rng.sample(uniqueRolesNotInPlay, 1)[0]
            # Report outcome if self is player
            if self.isPlayer():
                print('In dreams, you see the face of a role that is alien to you. With nothing to be said about the dungeon as a whole, you wake knowing ' + unraveledRole['name'] + ' was not in the room with you as you slept.')
            # Add role to list of unraveled roles
            self.unraveledRoles.append(unraveledRole['id'])
    # END UNRAVEL

    def unite(self, action):
        # Load game
        global g_game
        # Initialize room action tracker boolean
        isRoomAction = False
        match action:
            # If it's the attack action, each active player gains a level of exhaustion
            case 'Attack':
                # Report outcome
                if self.isPlayer():
                    print('Every player chose the attack action. Charged by your influence and by their common goal, all players gain a level of exhaustion from the intensity of the struggle.')
                else:
                    print('Every player chose the attack action. Charged by ' + self.styleCharacterName() + '\'s influence and by their common goal, all players gain a level of exhaustion from the intensity of the struggle.')
                for p in g_game.allPlayers:
                    if p.isAbleToAct():
                        # Gain exhaustion
                        p.gainExhaustion()
            # If it's the rest action, gain 2 party supplies
            case 'Rest':
                # Report outcome
                if self.isPlayer():
                    print('Every player chose the rest action. Charged by your influence and by their common goal, all find their party supplies can be stretched just a little bit more.')
                else:
                    print('Every player chose the rest action. Charged by ' + self.styleCharacterName() + '\'s influence and by their common goal, all find their party supplies can be stretched just a little bit more.')
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
                print('Every player chose to take the same room action. Charged by your influence and by their common goal, all find their efforts mean just that little bit more.')
            else:
                print('Every player chose to take the same room action. Charged by ' + self.styleCharacterName() + '\'s influence and by their common goal, all find their efforts mean just that little bit more.')
    # END UNITE
# END CLASS PLAYER

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

    def passPlayers(self, players):
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
                            print('You are turned away at the gate when you try to leave the arena. Blood must be drawn before anyone is allowed to proceed.')
                        else:
                            print(p.styleCharacterName() + ' is turned away at the gate when they try to leave the arena. Blood must be drawn before anyone is allowed to proceed.')
            case 1:
                # If fewer than two players are trying to pass, no one may pass
                if len(players) > 1:
                    validPass = False
                    # Report failure
                    for p in players:
                        if p.isPlayer():
                            print('The passageway by which one can squeeze down into the sublevels of the tower and onto the next room is narrow enough to only comfortably admit one person. Trying to leave at the same time another player does gets you nowhere.')
                        else:
                            print('The passageway by which one can squeeze down into the sublevels of the tower and onto the next room is narrow enough to only comfortably admit one person. Trying to leave at the same time another player does gets ' + p.styleCharacterName() + ' nowhere.')
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
                                print('In line with the decorum of the Mirthless Queen\'s court, you are among the first to leave the hall, and so you take with you a curse.')
                            else:
                                print('In line with the decorum of the Mirthless Queen\'s court, ' + p.styleCharacterName() + ' is among the first to leave the hall, and so they take with them a curse.')
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
                                print('In line with the decorum of the Mirthless Queen\'s court, you are among the last to leave the hall, and so you take with you a curse.')
                            else:
                                print('In line with the decorum of the Mirthless Queen\'s court, ' + p.styleCharacterName() + ' is among the last to leave the hall, and so they take with them a curse.')
            case 4:
                # Report outcome
                for p in players:
                    if p.isPlayer():
                        print('Although the cradle was idyllic, the process to extricate yourself from it is anything but. You must fight and strain every inch of the way through miles of foliage that clings to you and rot that makes your head swim.')
                    else:
                        print('Although the cradle was idyllic, the process to extricate yourself from it is anything but. ' + p.styleCharacterName() + ' must fight and strain every inch of the way through miles of foliage that clings to them and rot that makes their head swim.')
                # Each passing player gains exhaustion
                _ = [p.gainExhaustion() for p in players]

            case 5:
                # If fewer than two players are trying to pass, no one may pass
                if len(players) < 2:
                    validPass = False
                    # Report failure
                    for p in players:
                        if p.isPlayer():
                            print('The path along the cove is treacherous, and the storm makes it more so. Without at least one other player to help you on the way, you are forced to turn back.')
                        else:
                            print('The path along the cove is treacherous, and the storm makes it more so. Without at least one other player to help them on the way, ' + p.styleCharacterName() + ' is forced to turn back.')
        # Prevent passing if way is barred
        if g_game.isWayBarred:
            validPass = False
            # Report outcome
            for p in players:
                if p.isPlayer():
                    print('You strain and strain, but the glass blockade holds firm.')
                else:
                    print(p.styleCharacterName() + '  strains and strains, but the glass blockade holds firm.')        
        if not validPass:
            # If there is only player able to act and that player is Endemene, trigger inspiration
            actionablePlayers = list(filter(lambda p: p.isAbleToAct(), g_game.allPlayers))
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
                        print('For a glorious moment, your wings carry you over the room\'s dangers, allowing you o leave it behind you before smoke begins to billow from the mechanism and you are deposited unceremoniously on the ground.')
                    else:
                        print('For a glorious moment, ' + p.styleCharacterName() + '\'s wings carry her over the room\'s dangers, allowing her to leave it behind her before smoke begins to billow from the mechanism and she is deposited unceremoniously on the ground.')
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
                    if not p.hasAttacked and list(map(lambda q: q.isAbleToAct(), p.getOtherPlayers())) != [False, False, False]:
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
                                if list(map(lambda q: q.isAbleToAct() and not q.isRevealed, p.getOtherPlayers())) != [False, False, False]:
                                    #print('Found valid action: interrogate') # DEBUG PRINT
                                    isOptionOtherThanPass = True
                                    break
                            case 'Guard':
                                if list(map(lambda q: q.isAbleToAct(), p.getOtherPlayers())) != [False, False, False]:
                                    #print('Found valid action: guard') # DEBUG PRINT
                                    isOptionOtherThanPass = True
                                    break
                            case 'Scout':
                                    #print('Found valid action: scout') # DEBUG PRINT
                                    isOptionOtherThanPass = True
                                    break
                            case 'Weird':
                                if list(map(lambda q: q.isAbleToAct(), p.getOtherPlayers())) != [False, False, False]:
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
                            print('Unable to proceed to the next room and unable to take another action, you slowly waste away until eventually you succumb to the darkness of oblivion.')
                        else:
                            print('Unable to proceed to the next room and unable to take another action, ' + p.styleCharacterName() + ' slowly wastes away until eventually they succumb to the darkness of oblivion.')   
                        # Player dies
                        p.die()
        if validPass:
            # Pass players
            _ = [p.passAction() for p in players]
            # Carry out Cloudblessed delayed trigger if necessary
            attemptCloudblessedRevive()
    # END PASSPLAYERS

    def investigate(self, total):
        # Load game
        global g_game
        # Extract room for ease of access
        room = self.room
        # Calculate discount for Breaking the Magic if the mirror has been successfully interrogated
        discount = 0
        if g_game.isCluedIn and self.room['id'] == 1:
            discount = 2
        # Report failure
        if total < room['requirements'][0] - discount:
            # Calculate discount for if mirror was successfully interrogated
            print('The party failed to ' + room['actions'][0] + ' (' + str(total) + ' Ingenuity contributed, ' + str(room['requirements'][0] - discount) + ' needed).')
        # Report success and carry out outcome
        else:
            print('The party was able to ' + room['actions'][0] + ' (' + str(total) + ' Ingenuity contributed, ' + str(room['requirements'][0] - discount) + ' needed).')
            # Update room to disallow future attempts to investigate
            self.hasBeenInvestigated = True
            # Carry out result
            match room['actions'][0]:
                case 'Plumb the Wreckage':
                    printIfPlayerActive('Your careful search rewards you with 2 supplies found among the bodies and scrap.')
                    # Add supplies
                    g_game.partySupplies += 2
                case 'Break the Magic':
                    printIfPlayerActive('With the removal of a single brick, marked with a symbol pointed to by a long string of clues, the tower begins to crumble around you. Acting quickly, you all manage to escape in time.')
                    # Exhaust players that are in the room when the tower breaks
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.gainExhaustion()
                    # Separate exhaustion output with a line break
                    print('')
                    # Mark tower as broken
                    g_game.isTowerBroken = True
                    printIfPlayerActive('Left behind in the place where the Tower\'s highest reaches had stood is another vault, suspended still in midair. As the party looks on, the door to the vault turns, then opens. From within, pale moonlight spills forth, and the light is in the visage of a woman. She descends to you, identifying herself as the physical embodiment of Casglowve, the Captive Moon. She intends to leave this dungeon right now, and she will take the most exhausted player with her.')
                    # Select random player from among most exhausted players
                    randomPlayer = getMostExhaustedPlayer(list(filter(lambda p: p.isAbleToAct(), g_game.allPlayers)))
                    # Check if a player was found since exhaustion could have killed all remaning players
                    if randomPlayer:
                        # If random player is the player, give them the choice to escape
                        if randomPlayer.isPlayer():
                            print('You have been chosen from among the most exhausted players. Will you choose to escape? [y/n]')
                            validInput = False
                            while not validInput:
                                command = input()
                                try:
                                    command = command.lower()
                                except ValueError:
                                    pass
                                # Output result of choice
                                match command:
                                    case 'y':
                                        randomPlayer.escape()
                                        print('You escaped from the dungeon.')
                                        validInput = True
                                    case 'n':
                                        print('You decline the offer, carrying on in your exhaustion')
                                        validInput = True
                        else:
                            # Otherwise decide choice of AI
                            shouldEscape = randomPlayer.shouldAiEscape()
                            if shouldEscape:
                                print(randomPlayer.styleCharacterName() + ' was chosen from among the most exhausted players. They chose to accept the offer and escape.')
                                # AI escapes
                                randomPlayer.escape()
                            else:
                                print(randomPlayer.styleCharacterName() + ' was chosen from among the most exhausted players. They chose to decline the offer and remain in their exhaustion.')
                    else:
                        print('Unfortunately no players remain alive.')
                case 'Follow the Twine':
                    # Roll a D3. On a 1, a random player is cursed. On a 2, all players immediately enter a new room. On a 3, a random player escapes.
                    printIfPlayerActive('You expertly navigate the twists and turns of the twine and in following it, you come to understand the true nature of the alley as a fulcrum of potential. Chaos, in a word. ')
                    printIfPlayerActive('What you find at the end of the path is as unexpected for you as it no doubt was for the layer of the twine, if they even encountered the same fate:')
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
                                    print('A vision so densely packed with data as to be physically hazardous leaps from the well of darkness the twine drops into and plants itself inside your head. You become cursed.')
                                # Output result for AI:
                                else:
                                    print('A vision so densely packed with data as to be physically hazardous leaps from the well of darkness the twine drops into and plants itself inside ' + randomPlayer.styleCharacterName() + '\'s head. They become cursed.')
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
                                    print('A whip of cold energy lashes you, and suddenly you are in another place, the dungeon a distant memory. You have escaped.')
                                # Output result for AI:
                                else:
                                    print('A whip of cold energy lashes out to grab ' + randomPlayer.styleCharacterName() + ', and suddenly they are pulled through a tiny gap in the fabric of the road that closes behind them just as quickly as it opened. Have they escaped? It\'s impossible to say for sure.')
                case 'Answer the Riddle':
                    # Determine which answer is needed
                    if self.riddleAnswer == 1:
                        hint = 'Decorum demands that a price be paid by the first guest to leave.'
                    else:
                        hint = 'Decorum demands that a price be paid by the last guest to leave.'
                    printIfPlayerActive('The riddle asks the following question: \'what owes its likeness to the past, yet is most vibrant in the present? Is to some a prison, to others a stage? To some a mirror, others an open window, still others a blissful mystery? Is the greatest contest to have no prize but countless losers?\' Careful thought yields the answer to the riddle: decorum. When you speak the answer aloud, the writing on the wall changes before your very eyes. It now reads: ' + hint)
                    # Mark riddle as answered
                    self.isRiddleAnswered = True
                case 'Analyze the Music':
                    printIfPlayerActive('The rhythmic beat of the wind through the trees is almost like drums, peculiarly, and as you listen, you\'re struck with the bizarre notion that this sound is actually louder in some directions than others. You follow the sound until it brings to the very edge of the cradle, where you\'re faced with a wall of soil, detritus, and moving, breathing fungal shelf.')
                    # Output is different if the player has already seen the wandering heart
                    if g_game.player:
                        if g_game.player.timesSeenHeart > 0:
                            printIfPlayerActive('Peeling away dirt and snaking, tuberous fungal matter, you manage to poke a hole through the wall of the cradle, through which a warm red light shines. Looking through the hole, you see the source of the light is a great, pulsing hunk of red and pink tissue. It is the heart you saw before. What is it doing here?')
                        else:
                            printIfPlayerActive('Peeling away dirt and snaking, tuberous fungal matter, you manage to poke a hole through the wall of the cradle, through which a warm red light shines. Looking through the hole, you see the source of the light is a great, pulsing hunk of red and pink tissue. An enormous, beating heart.')
                    # Mark each active player as having seen the wandering heart and reset their exhaustion levels to 0
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.seeHeart()
                case 'Interpret the Sigils':
                    printIfPlayerActive('You piece together the remnants of a warning of what is to come. Two rooms from this one, you will encounter: ')
                    # Print name of the room two indices from the current one (at g_game.roomIndex - 1)
                    try:
                        futureRoom = g_game.shuffledRooms[g_game.roomIndex + 1]
                        printIfPlayerActive(futureRoom['name'] + '.')
                    # If there is no such room, report this
                    except IndexError:
                        print('nothing. One or fewer rooms remain to be explored.')
    # END INVESTIGATE

    def exert(self, total):
        # Load game
        global g_game
        # Extract room for ease of access
        room = self.room
        # Report failure
        if total < room['requirements'][1]:
            print('The party failed to ' + room['actions'][1] + ' (' + str(total) + ' Resolve contributed, ' + str(room['requirements'][1]) + ' needed).')
        # Report success and carry out outcome
        else:
            print('The party was able to ' + room['actions'][1] + ' (' + str(total) + ' Resolve contributed, ' + str(room['requirements'][1]) + ' needed).')
            # Update room to disallow future attempts to exert
            self.hasBeenExerted = True
            # Carry out result
            match room['actions'][1]:
                case 'Free the Blade':
                    printIfPlayerActive('A cold certainty fills you as the blade is wrested free of its resting place. With this blade drawn, it cannot be put back to rest until blood has been shed. All attacks will incur an extra level of exhaustion on their target until the next time a player dies.')
                    g_game.isSwordDrawn = True
                case 'Interrogate the Mirror':
                    printIfPlayerActive('The mirror is not cooperative, but through carefully worded questions and a healthy measure of psychology, you manage to trick it into revealing a critical detail about the nature of this tower: it is a prison for the mind as much as it is the body. With this knowledge, you will have an easier time breaking the tower should you choose to do so.')
                    g_game.isCluedIn = True
                case 'Confront the Beast':
                    printIfPlayerActive('You turn and wait for the beast that lumbers behind you to catch up. Your resolve holds strong as the sounds of its ragged breaths grows louder, and just when the sound is so loud you cannot hear yourself breathe over it, it begins to fade. Soon the breathing and footsteps both have faded to nothing. In their absence, your body swells with a newfound and deeply unnatural strength. You may be able to survive that which is not survivable, now ... though it may come at a cost.')
                    # Mark each active player as having conquered their fear
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.hasConqueredFear = True
                case 'Sit at the Table':
                    printIfPlayerActive('A tranquil calm settles over you as you seat yourself at the grand dining table and wait for the tides of fate to change. They do not, but after a while you have almost come to terms with this. Each party member gains the benefit of a rest.')
                    # all active players rest
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.rest()
                case 'Wish at the Well':
                    printIfPlayerActive('The surface of the well shimmers with a barely contained skin of magic. You experiment with all variety of items dropped into it, to no effect. Coins, flowers, trinkets are swallowed whole by the dark waters, giving nothing in return. Finally, you think to feed the well a drop of your blood. Immediately, you feel the price exacted as a curse takes hold of you. You may each make a single wish of the well, so choose wisely.')
                    printIfPlayerActive('You may secretly vote for one of the following: \n1. Wish for Wellness.\n2. Wish for Freedom. \n3. Wish for Knowledge. \n4. Wish for Resources. \n5. Wish for Doom.')
                    numVotes = [0, 0, 0, 0, 0]
                    playerVotes = [None, None, None, None]
                    # For each active player, collect vote
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            if p.id == 1:
                                # Read player choice
                                validInput = False
                                while not validInput:
                                    command = input()
                                    match command:
                                        case '1':
                                            numVotes[0] += 1
                                            validInput = True
                                            print('You voted for Wellness.')
                                            playerVotes[0] = 'Wellness'
                                        case '2':
                                            numVotes[1] += 1
                                            validInput = True
                                            print('You voted for Freedom.')
                                            playerVotes[0] = 'Freedom'
                                        case '3':
                                            numVotes[2] += 1
                                            validInput = True
                                            print('You voted for Knowledge.')
                                            playerVotes[0] = 'Knowledge'
                                        case '4':
                                            numVotes[3] += 1
                                            validInput = True
                                            print('You voted for Resources.')
                                            playerVotes[0] = 'Resources'
                                        case '5':
                                            numVotes[4] += 1
                                            validInput = True
                                            print('You voted for Doom.')
                                            playerVotes[0] = 'Doom'
                            else:
                                if p.shouldAiEscape():
                                    numVotes[1] += 1
                                    playerVotes[p.id - 1] = 'Wellness'
                                elif g_game.partySupplies < 4:
                                    numVotes[3] += 1
                                    playerVotes[p.id - 1] = 'Freedom'
                                elif p.exhaustionLevel > 1:
                                    numVotes[0] += 1
                                    playerVotes[p.id - 1] = 'Resources'
                                else:
                                    numVotes[2] += 1
                                    playerVotes[p.id - 1] = 'Knowledge'
                    # Report results of vote
                    if numVotes[0] > 0:
                        if numVotes[1] == 0 and numVotes[2] == 0 and numVotes[3] == 0 and numVotes[4] == 0:
                            print('A unanimous vote for Wellness was receved, so each player receives the benefit of a rest.')
                            # Rest
                            for p in g_game.allPlayers:
                                if p.isAbleToAct():
                                    p.rest
                        else:
                            print('A player voted for wellness, so a random player receives the benefit of a rest.')
                            # Choose a random player
                            playersAbleToAct = []
                            for p in g_game.allPlayers:
                                if p.isAbleToAct():
                                    playersAbleToAct.append(p)
                            randomPlayerIndex = rng.randint(0,len(playersAbleToAct)-1)
                            randomPlayer = playersAbleToAct[randomPlayerIndex]
                            # Player rests
                            randomPlayer.rest()
                    if numVotes[1] > 0:
                        if numVotes[0] == 0 and numVotes[2] == 0 and numVotes[3] == 0 and numVotes[4] == 0:
                            print('A unanimous vote for Freedom was receved, so each player may have their freedom from the dungeon.')
                            # Each active player escapes
                            for p in g_game.allPlayers:
                                if p.isAbleToAct():
                                    p.escape()
                                    # Report outcome
                                    if p.isPlayer():
                                        print('In a flash of shimmering lights accompanied by blustering winds, you are born somewhere far from here. You have escaped.')
                                    else:
                                        print('In a flash of shimmering lights accompanied by blustering winds, ' + p.styleCharacterName() + ' vanishes. They have escaped.')
                        else:
                            print('A player voted for Freedom, but a non-unanimous vote for Freedom is about as helpful as you might expect. Better luck next time.')
                    if numVotes[2] > 0:
                        if numVotes[0] == 0 and numVotes[1] == 0 and numVotes[3] == 0 and numVotes[4] == 0:
                            print('A unanimous vote for Knowledge was receved, so know this: there is no hope for you.')
                        else:
                            print('A player voted for Knowledge, but the vote was non-unanimous. Why don\'t I share with them what everyone else voted for?')
                            for i in range(len(playerVotes)):
                                vote = playerVotes[i]
                                if vote != None:
                                    print(g_game.allPlayers[i].styleCharacterName() + ' voted for ' + vote + '.')
                    if numVotes[3] > 0:
                        if numVotes[0] == 0 and numVotes[1] == 0 and numVotes[2] == 0 and numVotes[4] == 0:
                            print('A unanimous vote for Resources was receved, so the party gains 4 supplies.')
                            # Add 6 supplies
                            g_game.partySupplies += 4
                        else:
                            print('One or more players voted for Resources, so you gain 2 supplies.')
                            # Add x supplies
                            g_game.partySupplies += 2
                    if numVotes[4] > 0:
                        if numVotes[0] == 0 and numVotes[1] == 0 and numVotes[2] == 0 and numVotes[3] == 0:
                            print('A unanimous vote for Doom was received, so all players immediately die.')
                            # All active players die
                            for p in g_game.allPlayers:
                                if p.isAbleToAct():
                                    p.die()
                        else:
                            print('A vote for doom was received, so a random player will die. Such is the cost of such nonsense.')
                            # Choose a random player
                            playersAbleToAct = []
                            for p in g_game.allPlayers:
                                if p.isAbleToAct():
                                    playersAbleToAct.append(p)
                            randomPlayerIndex = rng.randint(0,len(playersAbleToAct)-1)
                            randomPlayer = playersAbleToAct[randomPlayerIndex]
                            # Player dies
                            randomPlayer.die()
                            print(randomPlayer.styleCharacterName() + ' dropped dead on the spot.')
                case 'Navigate the Ice':
                    # Output is different if the player has already seen the wandering heart
                    if g_game.player:
                        if g_game.player.timesSeenHeart > 0:
                            printIfPlayerActive('A gentle thrumming clues you into the fact that there is something large and very much alive buried beneath your feet. As you make your way to the center of the enormous shadow under the ice, your steps become more careful, as hair-thin cracks begin to spiral out from them. Yet you make it without a hitch, and are rewarded with a glimpse of what lies beneath. A faint red glow reveals the pulsing of an enormous heart underneath the ice. It is the same heart you saw before. What is it doing here?')
                        else:
                            printIfPlayerActive('A gentle thrumming clues you into the fact that there is something large and very much alive buried beneath your feet. As you make your way to the center of the enormous shadow under the ice, your steps become more careful, as hair-thin cracks begin to spiral out from them. Yet you make it without a hitch, and are rewarded with a glimpse of what lies beneath. A faint red glow reveals the pulsing of an enormous heart underneath the ice.')
                    # Mark each active player as having seen the wandering heart and reset their exhaustion levels to 0
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.seeHeart()
    # END EXERT

    def explore(self, total):
        # Load game
        global g_game
        # Extract room for ease of access
        room = self.room
        # Report failure
        if total < room['requirements'][2]:
            print('The party failed to ' + room['actions'][2] + ' (' + str(total) + ' Finesse contributed, ' + str(room['requirements'][2]) + ' needed).')
        # Report success and carry out outcome
        else:
            print('The party was able to ' + room['actions'][2] + ' (' + str(total) + ' Finesse contributed, ' + str(room['requirements'][2]) + ' needed).')
            # Update room to disallow future attempts to explore
            self.hasBeenExplored = True
            # Carry out result
            match room['actions'][2]:
                case 'Take the High Ground':
                    printIfPlayerActive('On the edge of the arena, you find a space where the piled junk reaches high enough that a player might be able to make it over the wall and into the next room if they get a boost up. Any number of players may take this opportunity as long as it least one chooses to stay behind.')
                    # For each active player, give the option to stay behind or leave
                    remainingPlayers = []
                    leavingPlayers = []
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            # Give player choice
                            if p.id == 1:
                                print('Will you choose to remain behind? [y/n]')
                                validInput = False
                                while not validInput:
                                    command = input()
                                    try:
                                        command = command.lower()
                                    except ValueError:
                                        pass
                                    # Output result of choice
                                    match command:
                                        case 'y':
                                            print('You elected to remain behind.')
                                            remainingPlayers.append(p)
                                            validInput = True
                                        case 'n':
                                            print('You elected to leave.')
                                            leavingPlayers.append(p)
                                            validInput = True
                            else:
                                if p.role['name'] == 'Cloudblessed':
                                    remainingPlayers.append(p)
                                else:
                                    leavingPlayers.append(p)
                    # Determine result
                    if len(remainingPlayers) > 0:
                        printIfPlayerActive('One or more players elected to stay behind. With their help, the following players were able to pass to the next room')
                        # Each leaving player passes
                        for p in leavingPlayers:
                            p.hasPassed = True
                            # Report passed player
                            print(p.styleCharacterName())
                    else:
                        # Report failure of anyone to pass
                        printIfPlayerActive('No players elected to stay behind, and so all have no choice but to do so.')
                case 'Spring the Vaults':
                    printIfPlayerActive('You deftly navigate the series of intricate traps and locks in place to wrest open the vaults in the Tower\'s basement. Inside the vast, dark space, you find only a single item, set neatly in the center of the floor. A key, to another door. You pocket the key, hoping that whatever it opens will be found in time.')
                    # Add key to party inventory
                    g_game.isKeyFound = True
                case 'Loot the Storefronts':
                    printIfPlayerActive('The storefronts have been largely picked over, but an extended search reveals 2 supplies hiding in cabinets and on shelves, in corners and behind locked doors.')
                    # Add supplies
                    g_game.partySupplies += 2
                case 'Raid the Kitchen':
                    printIfPlayerActive('You barge into the kitchen, interrupting a four-course meal being prepped by no one. All manner of foodstuffs sit out in a state of half or almost complete preparedness, just waiting to be served. You load your arms with all you can carry, walking away with 4 supplies.')
                    printIfPlayerActive('Each party member also walks away with a curse upon their name.')
                    # Add supplies
                    g_game.partySupplies += 4
                    # Add curse to each active player
                    for p in g_game.allPlayers:
                        if p.isAbleToAct():
                            p.timesCursed += 1 
                case 'Forage in the Marshland':
                    printIfPlayerActive('There is much to be found here worth eating, when you know what you are looking for. With a careful eye, you harvest 3 supplies from the wilds.')
                    # Add supplies
                    g_game.partySupplies += 3
                case 'Search for Shelter':
                    printIfPlayerActive('Through a slight gap the surface of the cove\'s rocky exterior, you find a place where the party can hunker down and weather the storm.')
                    g_game.isSheltered = True
    # END EXPLORE
# END CLASS LOCATION

def attemptCloudblessedRevive():
    # Load Game
    global g_game
    # Carry out effect only if Cloudblessed was revealed in the current room
    if g_game.location.cloudblessedRevealed:
        # Determine if all players have passed
        actionablePlayers = list(filter(lambda p: p.isAbleToAct(), g_game.allPlayers))
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
                        print('The cloud-blessed mists grant you another chance at life.')
                    else:
                        print('The cloud-blessed mists grant ' + p.styleCharacterName() + ' another chance at life.')
    # END ATTEMPTCLOUDBLESSEDREVEAL

def printIfPlayerActive(output):
    # Load game
    global g_game
    # Print if there is a player
    if g_game.player:
        # Print if player is active
        if g_game.player.isAbleToAct():
                print(output)
# END PRINTIFPLAYERACTIVE

def lookupPlayerByID(targetID):
    # Load game
    global g_game
    # Look up player from list of all players
    for p in g_game.allPlayers:
        if p.id == targetID:
            return p
# END LOOKUPPLAYERBYID

def lookupPlayerByRole(targetRole):
    # Load game
    global g_game
    # Look up player from list of all players
    for p in g_game.allPlayers:
        if p.role['name'] == targetRole:
            return p
    # Return error if no player has the role
    return None
# END LOOKUPPLAYERBYROLE

def lookupPlayerByCharacter(targetCharacter):
    # Load game
    global g_game
    # Look up player from list of all players
    for p in g_game.allPlayers:
        if p.character['name'] == targetCharacter:
            return p
    # Return error if no player has the role
    return None
# END LOOKUPPLAYERBYCHARACTER

def getMostExhaustedPlayer(players):
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

def getLeastExhaustedPlayer(players):
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

def getPlayerInput(options):
    # Load game
    global g_game
    # Initialize lock boolean
    validInput = False
    # Process input until valid input is received:
    while not validInput:
        # Request input
        print('> ', end=''),
        # Read input
        command = input()
        # Specifically reject the numbered command '0' as this will be read as valid when it is not
        if command != '0':
            # Validate input as a numbered command
            try: 
                index = int(command) - 1
                try:
                    # Determine player choice
                    choice = options[index]
                    # Mark valid input
                    validInput = True
                # Handle bad action number
                except IndexError:
                    pass
            # Handle bad command type
            except ValueError:
                if command == 'quit' or command == 'q':
                    # End program
                    quit()
                if command == 'view' or command == 'v':
                    print('Choose a player to view the stats of:')
                    for i in range(len(g_game.allPlayers)):
                        print(str(i + 1) + '. ' + g_game.allPlayers[i].styleCharacterName(), end=' ')
                        # Indicate which character the player is (first one in the list, always)
                        if i == 0:
                            print('(You)')
                        else:
                            print('') 
                    command = input()
                    # Output requested info
                    match command:
                        case '1':
                            g_game.allPlayers[0].printCharacterInfo()
                            # Print role as well for player
                            g_game.allPlayers[0].printRoleInfo()
                        case '2':
                            g_game.allPlayers[1].printCharacterInfo()
                        case '3':
                            g_game.allPlayers[2].printCharacterInfo()
                        case '4':
                            g_game.allPlayers[3].printCharacterInfo()
                        case _:
                            print('No such player found.')
                    print('\nUse the \'view\' command again to view another player\'s stats.')
    # Return player choice
    return choice
# END GETPLAYERINPUT

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
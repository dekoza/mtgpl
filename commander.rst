.. include:: symbols.rst

**************************
 Official Commander Rules
**************************

Last updated Oct 29th, 2013

Commander is the modern name for EDH, a Magic:The Gathering variant format which emphasises social interactions, interesting games, and creative deckbuilding. It can be played 1-on-1 but is usually multiplayer.

This page details the rules common to most play groups. Locally players often play with house rules, and are encouraged to, but this consensus version exists so that players know what to expect if they join a game outside their local play area.


==========
Philosophy
==========

Commander is designed to promote social games of magic.

It is played in a variety of ways, depending on player preference, but a common vision ties together the global community to help them enjoy a different kind of magic. That vision is predicated on a social contract: a gentleman's agreement which goes beyond these rules to includes a degree of interactivity between players. Players should aim to interact both during the game and before it begins, discussing with other players what they expect/want from the game.

House rules or "fair play" exceptions are always encouraged if they result in more fun for the local community.



=======================
Deck Construction Rules
=======================

#. Players must choose a legendary creature as the "Commander" for their deck.

   Players may choose any legendary creature as their Commander, although some choices may be met with disapproval by other players. Two players in the same game may choose the same Commander, and other players may include that card in their Deck even if it's not their Commander. Commanders are subject to the Legend rule just like any other legendary creature; multiple copies of the same creature (whether Commander and non-Commander) will all be put into the graveyard (or command zone) as a state based effect.

   The Commander is the principle around which the deck is built. It is more easily available than other cards in the deck, and decks will ususally want to leverage their Commander's strengths in their plans. It is not, however, guarenteed to be available at every point in the game so EDH decks should be able to function without it for a time.

   A deck's commander is also known as its "General" for historical reasons.

#. A card's *colour identity* is its colour plus the colour of any mana symbols in the card's rules text. A card's colour identity is established before the game begins, and cannot be changed by game effects.
   
   The Commander's colour identity restricts what cards may appear in the deck.

   * Cards in a deck may not have any colours in their identity which are not shared with the commander of the deck. (The identity of each card in the deck must be a subset of the General's)
   * Lands whose type includes swamp, island, plains, forest and/or mountain (e.g.: basic lands, shocklands, dual lands, Shadowmoor special-basics, etc) DO contain the corresponding mana symbol(s) as per CR 305.6. As such, while they are "colourless" they do have a colour identity and may not appear in a deck unless the Commander is of the appropriate identity.
   * While hybrid mana symbols may be played with either colour mana, they contribute both colours to the card's colour identity. Therefore they may only be played with a Commander whose identity includes ALL of the hybrid symbols' colours.
   * Basic land words (swamp, forest, etc) in the text box of a card do NOT represent a coloured mana symbol. They are not restricted to Commander of the same colour identity.
   * Reminder text is not included in the colour identity of a card.

   An Example of what cards are/aren't allowed in a three colour deck.

      A deck with :mtgtip:`Phelddagrif` (casting cost |mana_1| |mana_w| |mana_u| |mana_g|) as the Commander may not contain any cards whose colour identity includes red or black.

      * These cards would all be illegal in a Phelddagrif deck:
      
        * :mtgtip:`Goblin Piker` (Its mana cost contains a red mana symbol)
        * :mtgtip:`Elves of Deep Shadow` (Its ability contains a black mana symbol)
        * :mtgtip:`Talisman of Dominance` (All sorts of verbotten mana symbols)
        * :mtgtip:`Life // Death` (Three shall be the number of the colours)
        * :mtgtip:`Degavolver` (... right out)

      * Our Phelddagrif couldn't use any of these lands:
       
        * :mtgtip:`Underground River` (obvious, see above)
        * :mtgtip:`Godless Shrine`
        * :mtgtip:`Badlands`
        * :mtgtip:`Leechridden Swamp`, etc.

      * Phelddagrif may not call upon :mtgtip:`Boros Guildmage` for help
      * Phelddagrif IS allowed to use:
      
        * :mtgtip:`Esper Panorama`
        * :mtgtip:`Shard Convergence`

#. A deck may not generate mana outside its colours. If an effect would generate mana of an illegal colour, it generates colourless mana instead.
#. A Commander deck must contain exactly 100 cards, including the Commander.
#. With the exception of basic lands, no two cards in the deck may have the same english name.
#. Commander is played with vintage legal cards, with some exceptions:

   * cards are legal as of their set's prerelease
   * The following is the official :ref:`banned list for commander games<commander_banned>`. These cards (and others like them) should not be played without prior agreement from the other players in the game.
   * Additionally :ref:`the following legends may not be used as a Commander<banned_commanders>`.


==========
Play Rules
==========

#. The start of game procedure for Commander is as follows:
   
   #. Players announce their choice of Commander and move that card to the command zone.
   #. Players may then sideboard if the optional rules for sideboards are being used.
   #. Each player draws a hand of seven cards.
   #. Players may mulligan, using the modified :ref:`Partial Paris<partial-paris-mulligan>` method.

#. Being a Commander is not a characteristic [MTG CR109.3], it is a property of the card. As such, "Commander-ness" cannot be copied or overwritten by continuous effects, and does not change with control of the card.

   Examples: A :mtgtip:`Body Double` copying a Commander in a graveyard is not a Commander. A Commander which is affected by :mtgtip:`Cytoshape`, or is face down, is still a Commander.

#. If a player has been dealt 21 points of combat damage by a particular Commander during the game, that player loses a game. 

   * This is an additional state based effect.
   * Commander Damage is cumulative throughout the game; nothing can reduce the amount of damage a Commander has previously done to a player.
   * Because it is a property of the card and not a characteristic of the game object, a card is still the same Commander even if it leaves the field and returns.
   * While effects can raise a player's life total, it doesn't reduce the amount of damage previously taken from a Commander. (eg: :mtgtip:`Beacon of Immortality`)
   * Conversely, combat damage can be reduced, prevented, or replaced as it is taken, in which case it was never dealt and doesn't count towards the total taken from that Commander. (eg: :mtgtip:`Fog` or :mtgtip:`Captain's Maneuver`)
   * Commander Damage is specific to each Commander/Player pairing, not combined across all Commander.
   * A player can lose if he or she is dealt 21 points of combat damage by his or her own Commander (ie: under someone else's control).

#. While a Commander is in the command zone, it may be cast. As an additional cost to cast a Commander from the command zone, its owner must pay |mana_2| for each time it was previously cast from the command zone. (ie: Olivia Voldaren costs |mana_6| |mana_b| |mana_r| to cast for the third time.)

   A Commander is still subject to the normal timing restrictions for casting creatures (unless it has Flash or some other affect allows it to be played at another time, such as Vedalken Orrery)

#. If a Commander would be put into a graveyard or exile from anywhere, its owner may choose to move it to the command zone instead. Details

   * This is a replacement effect; the creature never goes to the graveyard and will not trigger such abilities.
   * Commanders will move to the library or hand as normal; only transitions to Exile or the Graveyard may be replaced.
   
   If a card is put into the exile zone face down from anywhere, and a player is allowed to look at that card in exile, the player must immediately do so. If it's a commander owned by another player, the player that looked at it turns it face up and puts it into the command zone.

#. Players begin the game with 40 life.
#. Commanders are subject to the Legend rule; a player cannot control more than one legend with the same name.
#. Abilities which refer to other cards owned outside the game (:mtgtip:`W<Burning Wish>`:mtgtip:`i<Cunning Wish>`:mtgtip:`s<Death Wish>`:mtgtip:`h<Glittering Wish>`:mtgtip:`e<Golden Wish>`:mtgtip:`s<Living Wish>`, :mtgtip:`Spawnsire`, :mtgtip:`Research<Research // Development>`, :mtgtip:`Ring of Ma'ruf`) do not function in Commander unless the optional sideboard rule is in use. If sideboards are used, wishes and similar cards may retrieve sideboard cards.

.. _partial-paris-mulligan:

Partial Paris Mulligan rule
===========================

Because Commander games are long and usually not played in multigame matches, the format uses a modified mulligan rule designed to alleviate mana-light hands without significantly increasing the odds of finding individual cards. This is also known as the "Brittany" mulligan rule.

#. In turn order, players may exile (face down) some or all of the cards in their hand.
#. Each player then draws one less card from their deck than the number they exiled.
#. Players who exiled at least one card may return to step 1 and repeat the process, drawing one less card each time.
#. Players shuffle all exiled cards into their deck.

It is worth noting that even with this form of mulligan, decks playing an insufficient number of mana sources will routinely draw poor hands or insufficient mana as the game progresses.

============================
Optional rules for Commander
============================

Commander is designed first and foremost for social players. It cannot be all things to all people.

Nevertheless, many people like to play for prizes or other non-social incentives. Those incentives can help build communities and playgroups, but they can also undermine the social contract which keeps the format balanced.

When running a competitive commander event, the recommended list of cards to avoid (under the primary deckbuilding rules) is one place to start. It is not however, nor is it intended to be, comprehensive. There are a great many uninteresting uses for the cards not listed there, and additional structure is required to keep degeneracy [#f1]_ in check. To that end, a selection of optional rules are provided here for prospective TOs or players who find their playgroup can't find a balance.


Sideboards
==========

Rather than filling every deck with banal responses, it is preferable to allow some flexibility in the composition of a deck.

* Players may bring a 10 card sideboard in addition to their 99 cards and 1 Commander.
* After Commanders are announced, players have 3 minutes to make 1-for-1 substitutions to their deck.
* Any cards not played as part of the deck may be retrieved by "wishes".

Reasoning
---------

Highly tuned threats piloted by skilled opponents mandate efficient answers. The minimum number of response cards required to ensure they are available in the early turns can easily overwhelm the majority of an EDH deck's building space.

Sideboards allow players to respond to the "best" strategies in a timely fashion . They should be strongly considered as a necessary defense against brokenness and degeneracy in an environment where no gentlemans agreement on style of play exists.

Victory Points
==============

Instead of a "last man standing" win condition, organizers are encouraged to use additional or alternate ways to win. Prizes can be awarded for things like:

* most combat damage dealt in a single turn
* biggest mana pool
* Commander Damage kills
* Most mana paid for a Commander
* etc

By encouraging players to play for disparate, interesting goals everyone has a more rewarding, social experience.

An extensive example can be found here

Democratic Victory
==================

An organizer who desires a tournament which better approximates normal commander games should reward players for some balance of winning and social play. One way to achieve this is

#. When the game is over, each player votes for an opponent whose play they enjoyed most.
#. Award two points for being the last player alive, and one point for each vote
#. Prizes can be given out by points awarded.


The League Rule
===============

A "League" consists of a regular group of players who frequently play together using the same decks. No two players in a league game may have the same Commander. Within a given league, Commander are allocated first-come, first-serve and are preserved between meetings/games. No player may have, in his or her deck, the Commander of any other player in the game; it should be replaced with some other card before the game begins.


=======
License
=======

#. All card names, artwork, and intrinsic Magic the Gathering game concepts are copyright Wizards of the Coast.
#. "Magic:The Gathering - Commander" is copyright Wizards of the Coast, 2010. Used with permission.
#.  All content not previously copyright by Wizards of the Coast were

    * created and copyright (2005-2013) by :email:`Gavin Duggan<edhforum@gmail.com>`
    * released under the terms of the `Academic Free License`_ (AFL) as of April 24th, 2007.
    * available for public reuse only with attribution, as per the terms of that license.


.. rubric:: Footnotes

.. [#f1] Degenerate: *adj* Having fallen below a normal or desireable state, especially functionally, morally, or socially. Having atrophied or declined to a state of sameness.

         Since one of the primary features of commander is the variety of games, and the variable nature of the problem each game presents, degenerate plays are those which take away from the variety and unpredictable nature of the games



.. _Academic Free License: http://www.opensource.org/licenses/academic.php

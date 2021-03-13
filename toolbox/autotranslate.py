import lark

grammar = r"""

start: ability
ability: static_ability
       | triggered_ability
       | activated_ability
       | keyword_ability

static_ability: effect

activated_ability: cost ":" effect

triggered_ability: condition "," effect

condition: ("When"|"Whenever") WORD+

effect: WORD+ "."

keyword_ability: KWD ("(" reminder_text ".)")?

cost: mana_cost ("," (TAP|UNTAP))? ("," other_cost)?
    | (TAP|UNTAP) ("," other_cost)?
    | other_cost

mana_cost: ("{" (MANA_SYMBOL|DIGIT ~ 1..2) "}")+

KWD: "Flying"
   | "First Strike"
   | "Double Strike"
   | "Trample"
   | "Menace"

other_cost: ("Pay"|"Sacrifice") WORD

reminder_text: WORD+

TAP: "{T}"
UNTAP: "{Q}"
ENERGY: "{E}"
MANA_SYMBOL: /(((2\/)|([WUBRG]\/))?[WUBRGP])|[XCS]/
WORD.-20: /\w+/

%import common.DIGIT
%import common.WS
%ignore WS
"""

parser = lark.Lark(grammar, parser="lalr")

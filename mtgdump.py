#!/usr/bin/env python3
import click
import mtgsdk

card_template = """
{card[name]}
   {card_text}

"""

symbols_map = {
#    '}{': '} {',
    '{C}': '|colorless|',
    '{T}': '|tap|',
    '{Q}': '|untap|',
    '{U}': '|mana_u|',
    '{W}': '|mana_w|',
    '{G}': '|mana_g|',
    '{B}': '|mana_b|',
    '{R}': '|mana_r|',
    '{P}': '|mana_p|',
    '{S}': '|mana_s|',
    '{2/U}': '|mana_2u|',
    '{2/W}': '|mana_2w|',
    '{2/B}': '|mana_2b|',
    '{2/G}': '|mana_2g|',
    '{2/R}': '|mana_2r|',
    '{U/P}': '|mana_up|',
    '{W/P}': '|mana_wp|',
    '{B/P}': '|mana_bp|',
    '{G/P}': '|mana_gp|',
    '{R/P}': '|mana_rp|',
    '{X}': '|mana_x|',
    '{0}': '|mana_0|',
    '{1}': '|mana_1|',
    '{2}': '|mana_2|',
    '{3}': '|mana_3|',
    '{4}': '|mana_4|',
    '{5}': '|mana_5|',
    '{6}': '|mana_6|',
    '{7}': '|mana_7|',
    '{8}': '|mana_8|',
    '{9}': '|mana_9|',
    '{10}': '|mana_10|',
    '{11}': '|mana_11|',
    '{12}': '|mana_12|',
    '{13}': '|mana_13|',
    '{14}': '|mana_14|',
    '{15}': '|mana_15|',
    '{R/G}': '|mana_rg|',
    '{R/W}': '|mana_rw|',
    '{U/B}': '|mana_ub|',
    '{U/R}': '|mana_ur|',
    '{W/B}': '|mana_wb|',
    '{W/U}': '|mana_wu|',
    '{B/G}': '|mana_bg|',
    '{B/R}': '|mana_br|',
    '{G/W}': '|mana_gw|',
    '{G/U}': '|mana_gu|',
    '\n': '\n\n   ',
    '||': '|\ |',

}


def reformat_card_text(text, card_name=None):
    for t, s in symbols_map.items():
        text = text.replace(t, s)
    # if card_name is not None:
    #     text = text.replace(card_name, 'this card')
    return text


@click.command()
@click.option('--expansion', '-e', help="Expansion symbol")
def import_rst(expansion):
    expansions = expansion.split(',')
    for expansion in expansions:
        page = 1
        with open(f"{expansion}.rst", 'w') as output:
            cardset = mtgsdk.Set.find(expansion)

            name = f""".. {cardset.name} (autogenerated)
.. include:: symbols.rst
        
{cardset.name}
{len(cardset.name) * '='}
        
"""
            output.write(name)
            while True:
                query = mtgsdk.Card.where(set=expansion).where(page=page)
                results = query.array()
                if not results:
                    break
                for card in results:
                    print(card['name'])
                    output.write(card_template.format(card=card, card_text=reformat_card_text(card.get('text', ''))))

                page += 1


if __name__ == '__main__':
    import_rst()

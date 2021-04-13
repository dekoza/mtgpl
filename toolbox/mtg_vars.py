expansions = [
    "10E",
    "2ED",
    "2XM",
    "3ED",
    "4ED",
    "5DN",
    "5ED",
    "6ED",
    "7ED",
    "8ED",
    "9ED",
    "A25",
    "AER",
    "AKH",
    "ALA",
    "ALL",
    "APC",
    "ARB",
    "ARN",
    "ATQ",
    "AVR",
    "BBD",
    "BFZ",
    "BNG",
    "BOK",
    "C13",
    "C14",
    "C15",
    "C16",
    "C17",
    "C18",
    "C19",
    "C20",
    "C21",
    "CHK",
    "CMR",
    "CN2",
    "CNS",
    "CON",
    "CSP",
    "DGM",
    "DIS",
    "DKA",
    "DOM",
    "DRK",
    "DST",
    "DTK",
    "E02",
    "ELD",
    "EMA",
    "EMN",
    "EVE",
    "EXO",
    "FEM",
    "FRF",
    "FUT",
    "GK1",
    "GK2",
    "GNT",
    "GPT",
    "GRN",
    "GTC",
    "HML",
    "HOU",
    "ICE",
    "IKO",
    "IMA",
    "INV",
    "ISD",
    "JMP",
    "JOU",
    "JUD",
    "KHC",
    "KHM",
    "KLD",
    "KTK",
    "LEA",
    "LEB",
    "LEG",
    "LGN",
    "LRW",
    "M10",
    "M11",
    "M12",
    "M13",
    "M14",
    "M15",
    "M19",
    "M20",
    "M21",
    "MBS",
    "MH1",
    "MIR",
    "MM2",
    "MM3",
    "MMA",
    "MMQ",
    "MOR",
    "MRD",
    "NEM",
    "NPH",
    "ODY",
    "OGW",
    "ONS",
    "ORI",
    "PCY",
    "PLC",
    "PLS",
    "RAV",
    "RIX",
    "RNA",
    "ROE",
    "RTR",
    "SCG",
    "SHM",
    "SOI",
    "SOK",
    "SOM",
    "STH",
    "STX",
    "THB",
    "THS",
    "TMP",
    "TOR",
    "TSP",
    "TSR",
    "UDS",
    "ULG",
    "UMA",
    "USG",
    "VIS",
    "WAR",
    "WTH",
    "WWK",
    "XLN",
    "ZEN",
    "ZNC",
    "ZNR",
]

card_template = """
:mtgtip:`{card[name]}<{image}|{card_uri}>`
   {card_text}

"""


symbols_map = {
    #    '}{': '} {',
    "{E}": "|energy|",
    "{C}": "|colorless|",
    "{T}": "|tap|",
    "{Q}": "|untap|",
    "{U}": "|mana_u|",
    "{W}": "|mana_w|",
    "{G}": "|mana_g|",
    "{B}": "|mana_b|",
    "{R}": "|mana_r|",
    "{P}": "|mana_p|",
    "{S}": "|mana_s|",
    "{2/U}": "|mana_2u|",
    "{2/W}": "|mana_2w|",
    "{2/B}": "|mana_2b|",
    "{2/G}": "|mana_2g|",
    "{2/R}": "|mana_2r|",
    "{U/P}": "|mana_up|",
    "{W/P}": "|mana_wp|",
    "{B/P}": "|mana_bp|",
    "{G/P}": "|mana_gp|",
    "{R/P}": "|mana_rp|",
    "{X}": "|mana_x|",
    "{0}": "|mana_0|",
    "{1}": "|mana_1|",
    "{2}": "|mana_2|",
    "{3}": "|mana_3|",
    "{4}": "|mana_4|",
    "{5}": "|mana_5|",
    "{6}": "|mana_6|",
    "{7}": "|mana_7|",
    "{8}": "|mana_8|",
    "{9}": "|mana_9|",
    "{10}": "|mana_10|",
    "{11}": "|mana_11|",
    "{12}": "|mana_12|",
    "{13}": "|mana_13|",
    "{14}": "|mana_14|",
    "{15}": "|mana_15|",
    "{16}": "|mana_16|",
    "{20}": "|mana_20|",
    "{R/G}": "|mana_rg|",
    "{R/W}": "|mana_rw|",
    "{U/B}": "|mana_ub|",
    "{U/R}": "|mana_ur|",
    "{W/B}": "|mana_wb|",
    "{W/U}": "|mana_wu|",
    "{B/G}": "|mana_bg|",
    "{B/R}": "|mana_br|",
    "{G/W}": "|mana_gw|",
    "{G/U}": "|mana_gu|",
    "\n": "\n\n   ",
    "||": "|\ |",
}
mtga_rev_map = {
    "|energy|": "E",
    "|colorless|": "C",
    "|tap|": "T",
    "|untap|": "Q",
    "|mana_u|": "U",
    "|mana_w|": "W",
    "|mana_g|": "G",
    "|mana_b|": "B",
    "|mana_r|": "R",
    "|mana_p|": "P",
    "|mana_s|": "Si",
    "|mana_2u|": "(2/U)",
    "|mana_2w|": "(2/W)",
    "|mana_2b|": "(2/B)",
    "|mana_2g|": "(2/G)",
    "|mana_2r|": "(2/R)",
    "|mana_up|": "(U/P)",
    "|mana_wp|": "(W/P)",
    "|mana_bp|": "(B/P)",
    "|mana_gp|": "(G/P)",
    "|mana_rp|": "(R/P)",
    "|mana_x|": "X",
    "|mana_0|": "0",
    "|mana_1|": "1",
    "|mana_2|": "2",
    "|mana_3|": "3",
    "|mana_4|": "4",
    "|mana_5|": "5",
    "|mana_6|": "6",
    "|mana_7|": "7",
    "|mana_8|": "8",
    "|mana_9|": "9",
    "|mana_10|": "10",
    "|mana_11|": "11",
    "|mana_12|": "12",
    "|mana_13|": "13",
    "|mana_14|": "14",
    "|mana_15|": "15",
    "|mana_rg|": "(R/G)",
    "|mana_rw|": "(R/W)",
    "|mana_ub|": "(U/B)",
    "|mana_ur|": "(U/R)",
    "|mana_wb|": "(W/B)",
    "|mana_wu|": "(W/U)",
    "|mana_bg|": "(B/G)",
    "|mana_br|": "(B/R)",
    "|mana_gw|": "(G/W)",
    "|mana_gu|": "(G/U)",
}
mtga_cost_map = {
    "C": "|colorless|",
    "T": "|tap|",
    "Q": "|untap|",
    "U": "|mana_u|",
    "W": "|mana_w|",
    "G": "|mana_g|",
    "B": "|mana_b|",
    "R": "|mana_r|",
    "P": "|mana_p|",
    "Si": "|mana_s|",
    "(2/U)": "|mana_2u|",
    "(2/W)": "|mana_2w|",
    "(2/B)": "|mana_2b|",
    "(2/G)": "|mana_2g|",
    "(2/R)": "|mana_2r|",
    "(U/P)": "|mana_up|",
    "(W/P)": "|mana_wp|",
    "(B/P)": "|mana_bp|",
    "(G/P)": "|mana_gp|",
    "(R/P)": "|mana_rp|",
    "X": "|mana_x|",
    "0": "|mana_0|",
    "1": "|mana_1|",
    "2": "|mana_2|",
    "3": "|mana_3|",
    "4": "|mana_4|",
    "5": "|mana_5|",
    "6": "|mana_6|",
    "7": "|mana_7|",
    "8": "|mana_8|",
    "9": "|mana_9|",
    "10": "|mana_10|",
    "11": "|mana_11|",
    "12": "|mana_12|",
    "13": "|mana_13|",
    "14": "|mana_14|",
    "15": "|mana_15|",
    "(R/G)": "|mana_rg|",
    "(R/W)": "|mana_rw|",
    "(U/B)": "|mana_ub|",
    "(U/R)": "|mana_ur|",
    "(W/B)": "|mana_wb|",
    "(W/U)": "|mana_wu|",
    "(B/G)": "|mana_bg|",
    "(B/R)": "|mana_br|",
    "(G/W)": "|mana_gw|",
    "(G/U)": "|mana_gu|",
}

cardtype_trans = [
    "0",  # 0
    "artifact",  # 1
    "creature",  # 2
    "enchantment",  # 3
    "instant",  # 4
    "land",  # 5
    "6",  # 6
    "7",  # 7
    "planeswalker",  # 8
    "9",  # 9
    "sorcery",  # 10
]

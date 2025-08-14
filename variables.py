import xml.etree.ElementTree as ET

# color pallettes for pitch classes

# Couleurs hex personnalisées converties en RGB
hex_to_rgb = lambda hex: tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))

# Couleurs des 7 notes naturelles
colors_1 = {
    0:  hex_to_rgb('#9656a2'),  # C
    2:  hex_to_rgb('#369acc'),  # D
    4:  hex_to_rgb('#95cf92'),  # E
    5:  hex_to_rgb('#f8e16f'),  # F
    7:  hex_to_rgb('#f4895f'),  # G
    9:  hex_to_rgb('#de324c'),  # A
    11: hex_to_rgb('#6c584c'),  # B
}

colors_2 = {
    0:  hex_to_rgb('#1f77b4'),  # C - Bleu
    2:  hex_to_rgb('#ff7f0e'),  # D - Orange doux
    4:  hex_to_rgb('#2ca02c'),  # E - Vert
    5:  hex_to_rgb('#d62728'),  # F - Rouge foncé
    7:  hex_to_rgb('#9467bd'),  # G - Violet moyen
    9:  hex_to_rgb('#8c564b'),  # A - Marron doux
    11: hex_to_rgb('#e377c2'),  # B - Rose moyen
}

colors_3 = {
    0:  hex_to_rgb('#1f77b4'),  # C - Bleu
    2:  hex_to_rgb('#ff7f0e'),  # D - Orange doux
    4:  hex_to_rgb('#2ca02c'),  # E - Vert
    5:  hex_to_rgb('#d62728'),  # F - Rouge foncé
    7:  hex_to_rgb('#9467bd'),  # G - Violet
    9:  hex_to_rgb('#8c564b'),  # A - Marron doux
    11: hex_to_rgb('#17becf'),  # B - Cyan clair (remplace rose)
}

colors_4 = {
    0:  hex_to_rgb('#FF6B6B'),  # C - Coral/Rouge (C comme Cherry)
    2:  hex_to_rgb('#4ECDC4'),  # D - Turquoise (D comme Deep sea)
    4:  hex_to_rgb('#45B7D1'),  # E - Bleu électrique (E comme Electric blue)
    5:  hex_to_rgb('#96CEB4'),  # F - Vert forêt (F comme Forest)
    7:  hex_to_rgb('#2ECC71'),  # G - Vert vif (G comme Green)
    9:  hex_to_rgb('#F39C12'),  # A - Ambre/Orange (A comme Amber)
    11: hex_to_rgb('#3498DB'),  # B - Bleu (B comme Blue)
}

colors_5 = {
    0:  hex_to_rgb('#DC143C'),  # C - Crimson
    2:  hex_to_rgb('#FCF55F'),  # D - Daffodil
    4:  hex_to_rgb('#5D3FD3'),  # E - Eggplant
    5:  hex_to_rgb('#FFA500'),  # F - Fox
    7:  hex_to_rgb('#009E60'),  # G - Green
    9:  hex_to_rgb('#00FFFF'),  # A - Aqua
    11: hex_to_rgb('#1F51FF'),  # B - Blue
}

colors_6 = {
    0:  hex_to_rgb('#DC143C'),   # C - Crimson        (r=220, g=20,  b=60)
    2:  hex_to_rgb('#6D4F37'),   # D - Dark Chocolate (r=109, g=79,  b=55)
    4:  hex_to_rgb('#6643db'),   # E - Eggplant       (r=102, g=67,  b=219)
    5:  hex_to_rgb('#FFA500'),   # F - Fox            (r=255, g=165, b=0)
    7:  hex_to_rgb('#009E60'),   # G - Green          (r=0,   g=158, b=96)
    9:  hex_to_rgb('#00CEF1'),   # A - Aqua           (r=0,   g=206, b=241)
    11: hex_to_rgb('#1F51FF'),   # B - Blue           (r=31,  g=81,  b=255)
}
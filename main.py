import xml.etree.ElementTree as ET

# Couleurs hex personnalisées converties en RGB
hex_to_rgb = lambda hex: tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))

pitch_mod12_colors = {
    0:  hex_to_rgb('#9656a2'),  # C
    2:  hex_to_rgb('#369acc'),  # D
    4:  hex_to_rgb('#95cf92'),  # E
    5:  hex_to_rgb('#f8e16f'),  # F
    7:  hex_to_rgb('#f4895f'),  # G
    9:  hex_to_rgb('#de324c'),  # A
    11: hex_to_rgb('#6c584c'),  # B
}

# Charge et parse le fichier XML
tree = ET.parse('note.mscx')
root = tree.getroot()

# Parcours tous les <Note> et applique la couleur selon pitch % 12
for note in root.findall('.//Note'):
    pitch_elem = note.find('pitch')
    if pitch_elem is not None:
        try:
            pitch = int(pitch_elem.text)
            mod12 = pitch % 12
            r, g, b = pitch_mod12_colors[mod12]
            color_elem = note.find('color')
            if color_elem is None:
                color_elem = ET.SubElement(note, 'color')
            color_elem.attrib = {
                'r': str(r),
                'g': str(g),
                'b': str(b),
                'a': '255'
            }
        except (ValueError, KeyError):
            continue

# Sauvegarde dans un nouveau fichier
tree.write('note_colored.mscx', encoding='utf-8', xml_declaration=True)

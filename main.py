import xml.etree.ElementTree as ET

# Couleurs hex personnalisées converties en RGB
hex_to_rgb = lambda hex: tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))

# Couleurs des 7 notes naturelles
pitch_mod12_colors = {
    0:  hex_to_rgb('#9656a2'),  # C
    2:  hex_to_rgb('#369acc'),  # D
    4:  hex_to_rgb('#95cf92'),  # E
    5:  hex_to_rgb('#f8e16f'),  # F
    7:  hex_to_rgb('#f4895f'),  # G
    9:  hex_to_rgb('#de324c'),  # A
    11: hex_to_rgb('#6c584c'),  # B
}

pitch_mod12_colors = {
    0:  hex_to_rgb('#1f77b4'),  # C - Bleu
    2:  hex_to_rgb('#ff7f0e'),  # D - Orange doux
    4:  hex_to_rgb('#2ca02c'),  # E - Vert
    5:  hex_to_rgb('#d62728'),  # F - Rouge foncé
    7:  hex_to_rgb('#9467bd'),  # G - Violet moyen
    9:  hex_to_rgb('#8c564b'),  # A - Marron doux
    11: hex_to_rgb('#e377c2'),  # B - Rose moyen
}

pitch_mod12_colors = {
    0:  hex_to_rgb('#1f77b4'),  # C - Bleu
    2:  hex_to_rgb('#ff7f0e'),  # D - Orange doux
    4:  hex_to_rgb('#2ca02c'),  # E - Vert
    5:  hex_to_rgb('#d62728'),  # F - Rouge foncé
    7:  hex_to_rgb('#9467bd'),  # G - Violet
    9:  hex_to_rgb('#8c564b'),  # A - Marron doux
    11: hex_to_rgb('#17becf'),  # B - Cyan clair (remplace rose)
}

# Dièses selon l'ordre standard
sharps_order = [6, 1, 8, 3, 10, 5, 0]  # F#, C#, G#, D#, A#, E#, B#
flats_order  = [10, 3, 8, 1, 6, 11, 4] # B♭, E♭, A♭, D♭, G♭, C♭, F♭

# Map dièse vers fondamentale (F♯ → F, C♯ → C, etc.)
sharp_to_natural = {x: (x - 1) % 12 for x in sharps_order}
flat_to_natural  = {x: (x + 1) % 12 for x in flats_order}

# Charge et parse le fichier XML
tree = ET.parse('note.mscx')
root = tree.getroot()

# Trouver le concertKey (signature de clé)
concert_key_elem = root.find('.//KeySig/concertKey')
concert_key = int(concert_key_elem.text) if concert_key_elem is not None else 0

# Détermination des altérations
altered_notes = {}
if concert_key > 0:
    for i in range(concert_key):
        sharp = sharps_order[i]
        base = sharp_to_natural[sharp]
        altered_notes[sharp] = base
elif concert_key < 0:
    for i in range(-concert_key):
        flat = flats_order[i]
        base = flat_to_natural[flat]
        altered_notes[flat] = base
# Si 0, aucune altération

# Application des couleurs
for note in root.findall('.//Note'):
    pitch_elem = note.find('pitch')
    if pitch_elem is not None:
        try:
            pitch = int(pitch_elem.text)
            mod12 = pitch % 12
            if mod12 in pitch_mod12_colors:
                color_source = mod12
            elif mod12 in altered_notes:
                color_source = altered_notes[mod12]
            else:
                continue  # Note altérée non définie dans la gamme
            r, g, b = pitch_mod12_colors[color_source]
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

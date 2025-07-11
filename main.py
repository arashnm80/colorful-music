from variables import *
import xml.etree.ElementTree as ET

# Couleurs des 7 notes naturelles
pitch_mod12_colors = {
    0:  hex_to_rgb('#DC143C'),  # C - Crimson
    2:  hex_to_rgb('#6D4F37'),  # D - Dark Chocolate
    4:  hex_to_rgb('#5D3FD3'),  # E - Eggplant
    5:  hex_to_rgb('#FFA500'),  # F - Fox
    7:  hex_to_rgb('#009E60'),  # G - Green
    9:  hex_to_rgb('#00CEF1'),  # A - Aqua
    11: hex_to_rgb('#1F51FF'),  # B - Blue
}

# Ordres standards
sharps_order = [6, 1, 8, 3, 10, 5, 0]  # F#, C#, G#, D#, A#, E#, B#
flats_order  = [10, 3, 8, 1, 6, 11, 4] # Bb, Eb, Ab, Db, Gb, Cb, Fb

# Mappings altérés → naturels
sharp_to_natural = {x: (x - 1) % 12 for x in sharps_order}
flat_to_natural  = {x: (x + 1) % 12 for x in flats_order}

# Parse le fichier
tree = ET.parse('note.mscx')
root = tree.getroot()

# Récupère la clé
concert_key_elem = root.find('.//KeySig/concertKey')
concert_key = int(concert_key_elem.text) if concert_key_elem is not None else 0

# Notes altérées par la clé
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

# Applique la couleur
for note in root.findall('.//Note'):
    pitch_elem = note.find('pitch')
    accidental_elem = note.find('Accidental')
    if pitch_elem is not None:
        try:
            pitch = int(pitch_elem.text)
            mod12 = pitch % 12
            color_source = None

            if concert_key != 0:
                # Si une altération est définie par la clé
                if mod12 in pitch_mod12_colors:
                    color_source = mod12
                elif mod12 in altered_notes:
                    color_source = altered_notes[mod12]
                elif mod12 in sharp_to_natural:
                    color_source = sharp_to_natural[mod12]
                elif mod12 in flat_to_natural:
                    color_source = flat_to_natural[mod12]
            else:
                # Pas d'armure : on se base uniquement sur l'accidental
                if accidental_elem is not None:
                    subtype = accidental_elem.find('subtype')
                    if subtype is not None:
                        subtype_text = subtype.text
                        if subtype_text == 'accidentalSharp':
                            color_source = sharp_to_natural.get(mod12, mod12)
                        elif subtype_text == 'accidentalFlat':
                            color_source = flat_to_natural.get(mod12, mod12)
                        else:
                            color_source = mod12  # pour les autres cas (bécarre etc.)
                    else:
                        color_source = mod12
                else:
                    color_source = mod12  # note naturelle sans altération

            if color_source in pitch_mod12_colors:
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

# Sauvegarde
tree.write('note_colored.mscx', encoding='utf-8', xml_declaration=True)

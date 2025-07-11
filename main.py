from variables import *

# Couleurs des 7 notes naturelles
pitch_mod12_colors = colors_6

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

# Applique la couleur par mesure
for measure in root.findall('.//Measure'):
    accidental_map = {}  # clé : pitch mod12, valeur : type ('sharp', 'flat')

    for note in measure.findall('.//Note'):
        pitch_elem = note.find('pitch')
        accidental_elem = note.find('Accidental')

        if pitch_elem is not None:
            try:
                pitch = int(pitch_elem.text)
                mod12 = pitch % 12
                color_source = None

                # Détecter une nouvelle altération dans cette note
                new_accidental = None
                if accidental_elem is not None:
                    subtype = accidental_elem.find('subtype')
                    if subtype is not None:
                        subtype_text = subtype.text
                        if subtype_text == 'accidentalSharp':
                            new_accidental = 'sharp'
                        elif subtype_text == 'accidentalFlat':
                            new_accidental = 'flat'
                        elif subtype_text == 'accidentalNatural':
                            new_accidental = 'natural'

                # Met à jour l'état d'altération temporaire pour cette note
                if new_accidental == 'sharp':
                    accidental_map[mod12] = 'sharp'
                    color_source = sharp_to_natural.get(mod12, mod12)
                elif new_accidental == 'flat':
                    accidental_map[mod12] = 'flat'
                    color_source = flat_to_natural.get(mod12, mod12)
                elif new_accidental == 'natural':
                    accidental_map.pop(mod12, None)
                    color_source = mod12
                else:
                    # Pas d'altération explicite → regarde l'état mémorisé
                    if mod12 in accidental_map:
                        kind = accidental_map[mod12]
                        if kind == 'sharp':
                            color_source = sharp_to_natural.get(mod12, mod12)
                        elif kind == 'flat':
                            color_source = flat_to_natural.get(mod12, mod12)
                    else:
                        color_source = mod12  # naturelle

                # Applique la couleur
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
                print("error")
                continue

# Sauvegarde
tree.write('note_colored.mscx', encoding='utf-8', xml_declaration=True)

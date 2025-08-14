from variables import *

# Colors of the 7 natural notes
pitch_mod12_colors = colors_6

# Standard orders
sharps_order = [6, 1, 8, 3, 10, 5, 0]  # F#, C#, G#, D#, A#, E#, B#
flats_order  = [10, 3, 8, 1, 6, 11, 4] # Bb, Eb, Ab, Db, Gb, Cb, Fb

# Mappings altered → natural
sharp_to_natural = {x: (x - 1) % 12 for x in sharps_order}
flat_to_natural  = {x: (x + 1) % 12 for x in flats_order}

# Parse the file
tree = ET.parse('note.mscx')
root = tree.getroot()

# Retrieve the key
concert_key_elem = root.find('.//KeySig/concertKey')
concert_key = int(concert_key_elem.text) if concert_key_elem is not None else 0

# Notes altered by the key
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

# Apply color per measure
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

                # Detect a new accidental in this note
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

                # Ensure sharp and flat notes are mapped to their base note
                if mod12 in altered_notes:
                    color_source = altered_notes[mod12]
                elif new_accidental == 'sharp':
                    accidental_map[mod12] = 'sharp'
                    color_source = sharp_to_natural.get(mod12, mod12)
                elif new_accidental == 'flat':
                    accidental_map[mod12] = 'flat'
                    color_source = flat_to_natural.get(mod12, mod12)
                elif new_accidental == 'natural':
                    accidental_map.pop(mod12, None)
                    color_source = mod12
                else:
                    # No explicit accidental → check the memorized state
                    if mod12 in accidental_map:
                        kind = accidental_map[mod12]
                        if kind == 'sharp':
                            color_source = sharp_to_natural.get(mod12, mod12)
                        elif kind == 'flat':
                            color_source = flat_to_natural.get(mod12, mod12)
                    else:
                        color_source = mod12  # natural

                # Apply the color
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

# Save
tree.write('note_colored.mscx', encoding='utf-8', xml_declaration=True)

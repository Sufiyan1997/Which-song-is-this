from fingerprint import fingerprint_song
from collections import Counter


def match(recording, rate, db):
    fp_recording = fingerprint_song(recording, rate)
    matched_couples = []
    for address in fp_recording.keys():
        if address in db:
            matched_couples.extend(db[address])

    matched_couple_count = Counter(
        couple[1] for couple in matched_couples
    ).most_common()

    if len(matched_couple_count) > 0:
        return matched_couple_count[0][0]
    else:
        return None

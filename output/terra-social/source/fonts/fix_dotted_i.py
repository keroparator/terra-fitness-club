#!/usr/bin/env python3
"""Lower the unusually high capital dotted-I accent in the bundled fonts.

The Open Sans outlines stay intact. Only the second composite component of
U+0130 moves vertically; the glyph width and every other glyph are unchanged.
This small, repeatable correction keeps Turkish uppercase headlines legible
when set on the original tight grid. The SIL OFL license is in OFL.txt.
"""

from pathlib import Path
import struct


TARGET_TOP = 1620  # Font units; normal cap height is 1462 of 2048.


def u16(data, offset):
    return struct.unpack_from(">H", data, offset)[0]


def s16(data, offset):
    return struct.unpack_from(">h", data, offset)[0]


def u32(data, offset):
    return struct.unpack_from(">I", data, offset)[0]


def checksum(data):
    padded = data + b"\0" * (-len(data) % 4)
    return sum(struct.unpack(">" + "I" * (len(padded) // 4), padded)) & 0xFFFFFFFF


def patch(path):
    data = bytearray(path.read_bytes())
    tables = {}
    for index in range(u16(data, 4)):
        entry = 12 + index * 16
        tag = data[entry : entry + 4].decode("ascii")
        tables[tag] = (entry, u32(data, entry + 8), u32(data, entry + 12))

    cmap = tables["cmap"][1]
    subtable = None
    for index in range(u16(data, cmap + 2)):
        record = cmap + 4 + index * 8
        candidate = cmap + u32(data, record + 4)
        if u16(data, candidate) == 4:
            subtable = candidate
            break
    if subtable is None:
        raise ValueError(f"{path}: Unicode cmap format 4 missing")

    count = u16(data, subtable + 6) // 2
    ends = subtable + 14
    starts = subtable + 16 + 2 * count
    deltas = subtable + 16 + 4 * count
    offsets = subtable + 16 + 6 * count
    codepoint = 0x0130
    for index in range(count):
        if u16(data, starts + index * 2) <= codepoint <= u16(data, ends + index * 2):
            delta = s16(data, deltas + index * 2)
            range_offset = u16(data, offsets + index * 2)
            glyph_id = (
                u16(data, offsets + index * 2 + range_offset + 2 * (codepoint - u16(data, starts + index * 2))) + delta
                if range_offset
                else codepoint + delta
            ) & 0xFFFF
            break
    else:
        raise ValueError(f"{path}: U+0130 missing")

    head = tables["head"][1]
    loca = tables["loca"][1]
    long_offsets = s16(data, head + 50) == 1
    glyph_index_offset = loca + glyph_id * (4 if long_offsets else 2)
    glyph_start = u32(data, glyph_index_offset) if long_offsets else u16(data, glyph_index_offset) * 2
    glyph = tables["glyf"][1] + glyph_start
    if s16(data, glyph) != -1:
        raise ValueError(f"{path}: U+0130 is not the expected composite")

    component = glyph + 10
    flags = u16(data, component)
    if not (not flags & 1 and flags & 2 and flags & 32):
        raise ValueError(f"{path}: unexpected first component layout")
    component += 6  # flags, glyph index, two signed 8-bit offsets
    flags = u16(data, component)
    if not (flags & 1 and flags & 2):
        raise ValueError(f"{path}: unexpected accent component layout")
    y_offset = component + 6
    previous_top = s16(data, glyph + 8)
    if previous_top <= TARGET_TOP:
        print(f"{path.name}: already at {previous_top} units")
        return
    old_y = s16(data, y_offset)
    struct.pack_into(">h", data, y_offset, old_y - (previous_top - TARGET_TOP))
    struct.pack_into(">h", data, glyph + 8, TARGET_TOP)

    glyf_entry, glyf_start, glyf_length = tables["glyf"]
    struct.pack_into(">I", data, glyf_entry + 4, checksum(data[glyf_start : glyf_start + glyf_length]))
    struct.pack_into(">I", data, head + 8, 0)
    struct.pack_into(">I", data, head + 8, (0xB1B0AFBA - checksum(data)) & 0xFFFFFFFF)
    path.write_bytes(data)
    print(f"{path.name}: U+0130 top {previous_top} -> {TARGET_TOP} units")


if __name__ == "__main__":
    directory = Path(__file__).resolve().parent
    for filename in ("Display.ttf", "Body.ttf", "Body-Semibold.ttf"):
        patch(directory / filename)

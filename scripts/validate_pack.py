import argparse
import json
from itertools import groupby
from pathlib import Path

from PIL import Image

PACK_DIR = Path(__file__).resolve().parents[1]
CELL_WIDTH, CELL_HEIGHT = 192, 208
COLUMNS = 8
EXPECTED_FRAMES = [6, 8, 8, 4, 5, 8, 6, 6, 6]
AGENTPET_ALPHA_THRESHOLD = 16


def load_alpha(pack_dir):
    manifest = json.loads((pack_dir / 'pet.json').read_text(encoding='utf-8'))
    if not isinstance(manifest, dict):
        raise ValueError('pet.json must contain an object')
    for key in ('id', 'displayName', 'spritesheetPath'):
        value = manifest.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'pet.json requires a non-empty {key}')

    path = pack_dir / manifest['spritesheetPath']
    with Image.open(path) as sheet:
        if sheet.format != 'WEBP' or sheet.mode != 'RGBA':
            raise ValueError('spritesheet must be an RGBA WebP')
        size = (COLUMNS * CELL_WIDTH, len(EXPECTED_FRAMES) * CELL_HEIGHT)
        if sheet.size != size:
            raise ValueError(f'expected spritesheet size {size}, got {sheet.size}')
        return sheet.getchannel('A')


def fixed_grid_frames(alpha):
    frames = []
    for row in range(len(EXPECTED_FRAMES)):
        occupied = []
        for col in range(COLUMNS):
            x, y = col * CELL_WIDTH, row * CELL_HEIGHT
            cell = alpha.crop((x, y, x + CELL_WIDTH, y + CELL_HEIGHT))
            occupied.append(cell.getbbox() is not None)
        count = sum(occupied)
        if occupied != [True] * count + [False] * (COLUMNS - count):
            raise ValueError(f'row {row + 1} has a transparent gap between frames')
        frames.append(count)
    return frames


def occupied_ranges(projection):
    start = 0
    for occupied, group in groupby(projection):
        end = start + sum(1 for _ in group)
        if occupied:
            yield start, end
        start = end


def agentpet_frames(alpha):
    visible = alpha.point(lambda value: 255 if value > AGENTPET_ALPHA_THRESHOLD else 0)
    _, rows = visible.getprojection()
    frames = []
    for top, bottom in occupied_ranges(rows):
        columns, _ = visible.crop((0, top, visible.width, bottom)).getprojection()
        frames.append(sum(1 for _ in occupied_ranges(columns)))
    return frames


def main():
    parser = argparse.ArgumentParser(description='Validate the Clawd Bot pet pack')
    parser.add_argument('--agentpet', action='store_true',
                        help='also require the AgentPet v1.17.5 slicer to find the expected frames')
    args = parser.parse_args()
    try:
        alpha = load_alpha(PACK_DIR)
        frames = fixed_grid_frames(alpha)
        if frames != EXPECTED_FRAMES:
            raise ValueError(f'expected fixed-grid frames {EXPECTED_FRAMES}, got {frames}')
        print(f'Fixed grid: {len(frames)} rows, frames {frames}')
        if args.agentpet:
            clips = agentpet_frames(alpha)
            print(f'AgentPet v1.17.5 slicing: {len(clips)} rows, frames {clips}')
            if clips != EXPECTED_FRAMES:
                raise ValueError(f'AgentPet slicing does not match the expected frames {EXPECTED_FRAMES}')
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()

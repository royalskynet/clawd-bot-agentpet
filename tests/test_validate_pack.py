from pathlib import Path
import tempfile
import unittest

from PIL import Image

from scripts.validate_pack import (
    CELL_WIDTH,
    COLUMNS,
    EXPECTED_FRAMES,
    PACK_DIR,
    agentpet_frames,
    fixed_grid_frames,
    load_alpha,
)


class PackTests(unittest.TestCase):
    def test_checked_in_pack_has_the_expected_fixed_grid(self):
        self.assertEqual(fixed_grid_frames(load_alpha(PACK_DIR)), EXPECTED_FRAMES)

    def test_fixed_grid_rejects_a_hole_between_frames(self):
        alpha = load_alpha(PACK_DIR)
        alpha.paste(0, (CELL_WIDTH, 0, 2 * CELL_WIDTH, alpha.height // len(EXPECTED_FRAMES)))
        self.assertEqual(alpha.width, COLUMNS * CELL_WIDTH)
        with self.assertRaisesRegex(ValueError, 'row 1 has a transparent gap'):
            fixed_grid_frames(alpha)

    def test_manifest_requires_a_spritesheet_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp)
            (pack / 'pet.json').write_text('{"id":"pet","displayName":"Pet"}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'spritesheetPath'):
                load_alpha(pack)

    def test_agentpet_splits_on_transparent_rows_and_columns(self):
        alpha = Image.new('L', (5, 4), 0)
        alpha.putdata([
            255, 16, 17, 0, 0,
            0, 16, 0, 0, 0,
            0, 0, 0, 17, 255,
            0, 0, 0, 255, 17,
        ])
        self.assertEqual(agentpet_frames(alpha), [2, 1])

import numpy as np

from xlsx_to_audio import CAST, match_loudness, presence_boost


def test_match_loudness_raises_quiet_signal():
    quiet = np.full(4000, 400.0, dtype=np.float32)
    out = match_loudness(quiet, 0.13)
    rms = float(np.sqrt(np.mean(out.astype(np.float64) ** 2)))
    assert rms > float(np.sqrt(np.mean(quiet**2)))
    assert rms > 0.10 * 32767 * 0.8


def test_narrateur_plus_fort_que_maman():
    assert CAST["narrateur"].volume > CAST["maman"].volume
    assert CAST["narrateur"].rms > CAST["maman"].rms


def test_presence_boost_changes_signal():
    rng = np.random.default_rng(0)
    x = rng.standard_normal(44100).astype(np.float32) * 1000
    y = presence_boost(x, 44100, db=4.0)
    assert y.shape == x.shape
    assert not np.allclose(x, y)

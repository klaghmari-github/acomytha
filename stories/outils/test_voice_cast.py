from voice_cast import parse_roster, split_script, spoken_text


def test_lina_sans_dit():
    roster = parse_roster("Lina, maman")
    text = (
        "C'est l'heure du déjeuner. Lina s'assoit à table, près de maman. "
        "Maman dit : tu peux goûter une petite bouchée. Juste une petite bouchée. "
        "Lina dit : c'est doux, maman. "
        "Maman dit : merci d'avoir goûté. Tu as su nommer le goût. "
        "Une petite portion, c'est déjà bien."
    )
    beats = split_script(text, roster)
    roles = [r for r, _ in beats]
    assert "maman" in roles
    assert "enfant-f" in roles
    assert "narrateur" in roles
    joined = spoken_text(beats).lower()
    assert "dit :" not in joined and "maman dit" not in joined
    maman_lines = " ".join(p.lower() for r, p in beats if r == "maman")
    assert "bouchée" in maman_lines or "bouchee" in maman_lines or "goûter" in maman_lines or "gouter" in maman_lines


def test_sami_papa():
    roster = parse_roster("Sami, papa, maman")
    text = "Sami s'arrête. Papa dit : je suis là. On attend l'adulte."
    beats = split_script(text, roster)
    assert beats[0][0] == "narrateur"
    assert any(r == "papa" for r, _ in beats)
    papa = [p for r, p in beats if r == "papa"][0]
    assert "dit" not in papa.lower()


def test_maitresse_pas_maman():
    roster = parse_roster("Léa, maman, maîtresse")
    text = (
        "Léa entre. La maîtresse dit : range ton manteau. "
        "Maman dit : je reviens à quatre heures."
    )
    beats = split_script(text, roster)
    roles = {r for r, _ in beats}
    assert "maitresse" in roles
    assert "maman" in roles


def test_hero_garcon():
    r = parse_roster("Sami, papa, maman")
    assert r.hero_role == "enfant-m"
    assert r.resolve("Sami") == "enfant-m"


def test_copine():
    r = parse_roster("Lina, Nora, maman")
    assert r.resolve("Lina") == "enfant-f"
    assert r.resolve("Nora") == "copine"

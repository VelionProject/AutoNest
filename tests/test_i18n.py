import importlib
import os


def test_translation_en():
    os.environ["AUTONEST_LANG"] = "en"
    import utils.i18n as i18n

    importlib.reload(i18n)
    assert i18n.t("Projektverzeichnis") == "Project directory"


def test_translation_de():
    os.environ["AUTONEST_LANG"] = "de"
    import utils.i18n as i18n

    importlib.reload(i18n)
    assert i18n.t("Projektverzeichnis") == "Projektverzeichnis"


def test_translation_fr():
    os.environ["AUTONEST_LANG"] = "fr"
    import utils.i18n as i18n

    importlib.reload(i18n)
    assert i18n.t("Projektverzeichnis") == "R\u00e9pertoire du projet"

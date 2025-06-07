import importlib
import os


def test_translation_en():
    os.environ["AUTONEST_LANG"] = "en"
    import utils.i18n as i18n

    importlib.reload(i18n)
    assert i18n.t("Projektverzeichnis") == "Project directory"

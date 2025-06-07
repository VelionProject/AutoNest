import pytest
import sys
import os

pytest.importorskip("tkinter")
pytest.importorskip("openai")

sys.path.insert(0, os.path.abspath("interface"))
sys.path.insert(0, os.path.abspath("core"))
from autonest_gui import AutoNestGUI
import tkinter as tk


def test_gui_launch():
    root = tk.Tk()
    gui = AutoNestGUI(root)
    root.update()
    root.destroy()

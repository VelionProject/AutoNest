import pytest
import sys
import os

pytest.importorskip("tkinter")
pytest.importorskip("openai")

# Add project root to PYTHONPATH so tests work when executed from the
# tests directory or via CI tools where the working directory may not be
# the repository root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from interface.autonest_gui import AutoNestGUI
import tkinter as tk


def test_gui_launch():
    root = tk.Tk()
    gui = AutoNestGUI(root)
    root.update()
    root.destroy()

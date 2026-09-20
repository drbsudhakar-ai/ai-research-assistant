from __future__ import annotations
from dataclasses import dataclass
import streamlit as st
@dataclass(slots=True)
class SettingsActionsState:
    save:bool=False; reset:bool=False; export:bool=False; import_:bool=False
class SettingsActions:
    def render(self)->SettingsActionsState:
        c=st.columns(4)
        return SettingsActionsState(
            c[0].button("Save",use_container_width=True),
            c[1].button("Reset",use_container_width=True),
            c[2].button("Export",use_container_width=True),
            c[3].button("Import",use_container_width=True))
__all__=["SettingsActions","SettingsActionsState"]
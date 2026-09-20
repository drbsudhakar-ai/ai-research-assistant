from __future__ import annotations
from dataclasses import dataclass
import streamlit as st
@dataclass(slots=True)
class AppearanceSettingsState:
    theme:str="System"; compact:bool=False
class AppearanceSettings:
    def render(self)->AppearanceSettingsState:
        return AppearanceSettingsState(
            st.selectbox("Theme",["System","Light","Dark"]),
            st.toggle("Compact Layout",False),
        )
__all__=["AppearanceSettings","AppearanceSettingsState"]
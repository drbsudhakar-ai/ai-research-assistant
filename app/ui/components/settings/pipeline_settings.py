from __future__ import annotations
from dataclasses import dataclass
import streamlit as st
@dataclass(slots=True)
class PipelineSettingsState:
    timeout:int=300; retries:int=1; parallel:bool=False
class PipelineSettings:
    def render(self)->PipelineSettingsState:
        return PipelineSettingsState(
            int(st.number_input("Timeout (sec)",1,3600,300)),
            int(st.number_input("Retries",0,10,1)),
            st.toggle("Enable Parallel Execution",False),
        )
__all__=["PipelineSettings","PipelineSettingsState"]
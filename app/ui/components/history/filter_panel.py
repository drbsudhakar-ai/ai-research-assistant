"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/history/filter_panel.py
Version      : 1.0.0
===============================================================================
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum
import streamlit as st

class SortField(str, Enum):
    ANALYSIS_DATE="Analysis Date"
    TITLE="Paper Title"
    EXECUTION_TIME="Execution Time"
    PROVIDER="Provider"
    MODEL="Model"

class SortDirection(str, Enum):
    ASC="Ascending"
    DESC="Descending"

@dataclass(slots=True)
class FilterState:
    provider:str="All"
    model:str="All"
    status:str="All"
    date_from:date|None=None
    date_to:date|None=None
    sort_field:SortField=SortField.ANALYSIS_DATE
    sort_direction:SortDirection=SortDirection.DESC
    apply_requested:bool=False
    reset_requested:bool=False

class FilterPanel:
    def render(self)->FilterState:
        with st.expander("Filters", expanded=False):
            c1,c2,c3=st.columns(3)
            provider=c1.selectbox("Provider",["All","Ollama","OpenAI","Gemini","DeepSeek"])
            model=c2.text_input("Model","All")
            status=c3.selectbox("Status",["All","Completed","Failed","Cancelled"])
            c4,c5=st.columns(2)
            df=c4.date_input("From",value=None)
            dt=c5.date_input("To",value=None)
            c6,c7=st.columns(2)
            sf=c6.selectbox("Sort By",[e.value for e in SortField])
            sd=c7.selectbox("Order",[e.value for e in SortDirection])
            a,b=st.columns(2)
            apply=a.button("Apply",use_container_width=True)
            reset=b.button("Reset",use_container_width=True)
        if reset:
            st.rerun()
        return FilterState(provider,model,status,df,dt,SortField(sf),SortDirection(sd),apply,reset)

__all__=["FilterPanel","FilterState","SortField","SortDirection"]

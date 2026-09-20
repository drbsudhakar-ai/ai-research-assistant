from __future__ import annotations
"""Production-ready Pagination."""
from dataclasses import dataclass
import math, streamlit as st
@dataclass(slots=True)
class PaginationState:
    page:int; page_size:int
class Pagination:
    def render(self,total:int,page:int,page_size:int=10)->PaginationState:
        pages=max(1,math.ceil(total/page_size))
        a,b,c=st.columns([1,2,1])
        if a.button("◀") and page>1: page-=1
        if c.button("▶") and page<pages: page+=1
        b.caption(f"Page {page}/{pages} • {total} records")
        page_size=st.selectbox("Page Size",[10,25,50,100],index=[10,25,50,100].index(page_size))
        return PaginationState(page,page_size)
__all__=["Pagination","PaginationState"]
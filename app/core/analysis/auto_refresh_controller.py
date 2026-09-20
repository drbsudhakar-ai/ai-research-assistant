"""
===============================================================================
Project      : AI Research Assistant
Module       : Auto Refresh Controller
File         : auto_refresh_controller.py
Version      : 5.0.0
Author       : Dr. B. Sudhakar

Description:
    Streamlit auto refresh controller for long running analysis.

Responsibilities:
    - Trigger Streamlit reruns while analysis executes.
    - Avoid refresh after completion.
    - Control refresh interval.
    - Prevent UI blocking.

===============================================================================
"""

from __future__ import annotations


from time import sleep
from threading import Thread, Event


import streamlit as st



class AutoRefreshController:
    """
    Controls periodic Streamlit refresh.
    """



    def __init__(
        self,
        interval: float = 1.0,
    ) -> None:

        self.interval = interval

        self.stop_event = Event()

        self.thread: Thread | None = None



    # ==================================================================
    # START
    # ==================================================================

    def start(self) -> None:
        """
        Start refresh loop.
        """


        if self.thread and self.thread.is_alive():

            return



        self.stop_event.clear()



        self.thread = Thread(

            target=self._loop,

            daemon=True,

        )


        self.thread.start()



    # ==================================================================
    # LOOP
    # ==================================================================

    def _loop(self) -> None:
        """
        Background refresh loop.
        """


        while not self.stop_event.is_set():


            sleep(
                self.interval
            )


            if self.stop_event.is_set():

                break



            self._request_refresh()



    # ==================================================================
    # REFRESH
    # ==================================================================

    def _request_refresh(self) -> None:
        """
        Request Streamlit rerun.

        Compatible with Streamlit versions
        supporting rerun.
        """


        try:

            st.rerun()


        except Exception:

            pass



    # ==================================================================
    # STOP
    # ==================================================================

    def stop(self) -> None:
        """
        Stop refresh.
        """

        self.stop_event.set()
"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Paper Information
File         : analyze_info.py

Description:
    Displays extracted research paper metadata.

Responsibilities:
    - Render paper information
    - Display extracted title
    - Display document statistics
    - Display detected sections

Version:
    5.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Any

import streamlit as st



# =============================================================================
# Section Utilities
# =============================================================================


def _get_section_count(
    sections: Any,
) -> int:
    """
    Safely calculate number of detected sections.

    PaperSections is a dataclass,
    therefore len() cannot be used directly.
    """

    if sections is None:

        return 0


    if isinstance(
        sections,
        dict,
    ):

        return len(sections)



    # Dataclass based PaperSections
    section_names = [

        "abstract",

        "introduction",

        "related_work",

        "methodology",

        "methods",

        "experiments",

        "results",

        "discussion",

        "conclusion",

        "references",

    ]


    count = 0


    for name in section_names:

        value = getattr(
            sections,
            name,
            None,
        )


        if value:

            count += 1



    return count



def _get_title(
    paper: Any,
) -> str:
    """
    Extract title safely.
    """

    title = getattr(
        paper,
        "title",
        None,
    )


    if title:

        return str(title)



    return "Untitled Research Paper"



# =============================================================================
# Main Renderer
# =============================================================================


def render_paper_information(
    prepared_paper: Any | None,
) -> None:
    """
    Render paper information panel.

    Args:
        prepared_paper:
            PreparedPaper instance.
    """

    if prepared_paper is None:

        st.info(
            "Paper information will appear after PDF preparation."
        )

        return



    st.subheader(
        "📄 Paper Information"
    )


    # -------------------------------------------------------------------------
    # Title
    # -------------------------------------------------------------------------

    title = _get_title(
        prepared_paper
    )


    st.markdown(
        f"""
        ### {title}
        """
    )


    st.divider()



    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    col1, col2, col3, col4 = st.columns(
        4
    )


    with col1:

        st.metric(

            "Pages",

            getattr(
                prepared_paper,
                "page_count",
                getattr(
                    prepared_paper,
                    "pages",
                    0,
                ),
            ),

        )



    with col2:

        st.metric(

            "Characters",

            getattr(
                prepared_paper,
                "character_count",
                getattr(
                    prepared_paper,
                    "characters",
                    0,
                ),
            ),

        )



    with col3:

        st.metric(

            "Sections",

            _get_section_count(

                getattr(
                    prepared_paper,
                    "sections",
                    None,
                )

            ),

        )



    with col4:

        st.metric(

            "Status",

            "Prepared",

        )



    st.divider()



    # -------------------------------------------------------------------------
    # Section Details
    # -------------------------------------------------------------------------

    sections = getattr(
        prepared_paper,
        "sections",
        None,
    )


    if sections:


        with st.expander(
            "📚 Detected Paper Sections",
            expanded=False,
        ):


            section_fields = [

                ("Abstract", "abstract"),

                ("Introduction", "introduction"),

                ("Related Work", "related_work"),

                ("Methodology", "methodology"),

                ("Methods", "methods"),

                ("Experiments", "experiments"),

                ("Results", "results"),

                ("Discussion", "discussion"),

                ("Conclusion", "conclusion"),

                ("References", "references"),

            ]


            displayed = False


            for label, field in section_fields:


                content = getattr(
                    sections,
                    field,
                    None,
                )


                if content:

                    displayed = True


                    st.markdown(
                        f"**{label}**"
                    )


                    preview = str(content)


                    if len(preview) > 500:

                        preview = (
                            preview[:500]
                            +
                            "..."
                        )


                    st.write(
                        preview
                    )



            if not displayed:

                st.caption(
                    "No structured sections detected."
                )
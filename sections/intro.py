# sections/intro.py
import streamlit as st


def render():
    st.title("🌳 Beneath the Same Sky — Paris’s Unequal Canopy")
    st.caption(
        "[Source: City of Paris — Tree Inventory (Open Data, ODbL License)]("
        "https://data.iledefrance.fr/explore/dataset/les-arbres/information/"
        "?disjunctive.espece&disjunctive.typeemplacement&disjunctive.arrondissement"
        "&disjunctive.genre&disjunctive.libellefrancais&disjunctive.varieteoucultivar"
        "&disjunctive.stadedeveloppement&disjunctive.remarquable)"
    )

    st.markdown(
        """
        <div style="text-align: justify; font-size: 1.05rem; line-height: 1.6; max-width: 900px; margin-top: 1rem;">
        I grew up in Paris, surrounded by trees I never truly noticed.<br>
        They were always there <b>quiet sentinels rooted in stone and history</b>, watching generations come and go.<br>

        Through the changing seasons, they’ve offered shade, oxygen, and beauty — a quiet form of care we rarely acknowledge.<br>
        Yet, despite their presence, I’ve come to realize how little I know about them, and about the <b>urban ecosystem</b> that sustains our lives.<br>

        To understand our environment is, in many ways, to understand ourselves.<br>
        And in Paris, this reflection raises an uncomfortable question:<br>
        <b>Do all Parisians breathe the same air — or does nature draw its borders too?</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

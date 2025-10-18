# sections/conclusion.py
import streamlit as st


def render():
    st.subheader("🌍 Conclusion — Do All Parisians Breathe the Same Air?")

    st.markdown(
        """
        <div style="text-align: justify; font-size: 1.05rem; line-height: 1.65; max-width: 1400px;">
        The data reveals that <b>nature, too, draws its borders in Paris</b>.<br>

        The outer districts — from the <b>12th to the 20th</b> — shelter most of the city’s trees,  
        while the dense central arrondissements remain largely <b>mineral and overheated</b>.<br>

        Even the <b>16th</b>, both green and privileged, reminds us that <b>access to nature often follows lines of wealth and space</b>.<br>

        Yet, abundance hides fragility.<br>
        Five species alone — <i>plane tree, linden, horse chestnut, maple,</i> and <i>Japanese pagoda tree</i> —  
        make up more than <b>70% of Paris’s canopy</b>, exposing the city to the risks of <b>monoculture, disease, and climate stress</b>.<br>

        Most trees are <b>adult</b>, offering shade today but signaling the need for <b>renewal tomorrow</b>.  
        And since the majority grow in <b>public domains</b> — from streets to cemeteries —  
        their distribution also reflects <b>how the city manages and shares its green space</b>.<br>

        So, across districts, species, and ages, the same pattern emerges — 
        nature in Paris is unevenly shared.<br>
        Because in the end, trees are not so different from people:<br>
        they grow where they’re allowed, they adapt, they endure — 
        and together, they shape the life of the city.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="margin-top: 2rem; font-size: 1.05rem; line-height: 1.65; max-width: 1400px;">

        <h4>🚀 Implications & Next Steps</h4>

        <ul style="margin-top: 0.8rem;">
        <li><b>Replant strategically</b> in under-canopied, central districts.</li>
        <li><b>Diversify species</b> to strengthen ecological resilience.</li>
        <li><b>Integrate green equity</b> into urban planning and housing policies.</li>
        <li><b>Monitor canopy age</b> to anticipate regeneration before decline.</li>
        </ul>

        <blockquote style="margin-top: 1.5rem; font-style: italic; color: #FFFFFF;">
        “If you can’t measure it, you can’t improve it.”
        </blockquote>

        By <b>measuring Paris’s living canopy</b>, we begin to see its inequalities —  
        and once seen, they can no longer be ignored.<br>

        Data, then, is not just a tool for analysis: it’s a <b>path toward change</b>,  
        toward a city where every Parisian might one day <b>breathe under the same shade</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

import streamlit as st
import pandas as pd
import numpy as np

def show_feature():
    st.subheader("Vet Locator")
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=["lat", "lon"],
    )
    st.map(df)
    st.write("Content.")
v
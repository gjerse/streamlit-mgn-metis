import streamlit as st
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from mgn import mgn_coronal
from utils import apply_solar_mask, save_to_fits_png

st.set_page_config(page_title="MGN METIS Enhancer", layout="wide")

# Header with logo
st.title("🛰️ MGN Coronal Enhancer (METIS)")

st.write("""
Upload a coronagraphic FITS image (e.g., METIS).  
Enhanced off‑limb

 structures using *Multiscale Gaussian Normalization* (MGN).
""")

uploaded = st.file_uploader("Upload FITS file", type=["fits"])
if uploaded:
    hdul = fits.open(uploaded)
    image = hdul[0].data.astype(float)
    hdul.close()

    st.subheader("Raw input image")
    st.image(image, clamp=True, use_column_width=True)

    # Sidebar params
    st.sidebar.header("MGN & Masking Options")
    gamma = st.sidebar.slider("Gamma (non-linear gain)", 1.0, 10.0, 3.0)
    apply_mask = st.sidebar.checkbox("Apply solar disc mask?", True)
    if apply_mask:
        cx = st.sidebar.number_input("Mask center X", min_value=0, max_value=image.shape[1], value=image.shape[1]//2)
        cy = st.sidebar.number_input("Mask center Y", min_value=0, max_value=image.shape[0], value=image.shape[0]//2)
        radius = st.sidebar.slider("Mask radius (px)", 100, max(image.shape)//2, int(min(image.shape)//2 * 0.9))

        image = apply_solar_mask(image, center=(cx, cy), radius=radius)

    st.sidebar.write("---")
    if st.sidebar.button("🔄 Run MGN"):
        with st.spinner("Processing MGN..."):
            mgn_img = mgn_coronal(image, gamma=gamma)

        st.subheader("🔍 MGN Output")
        st.image(mgn_img, clamp=True, use_column_width=True)

        st.download_button("💾 Download FITS + PNG", data=save_to_fits_png(mgn_img), file_name="mgn_output.zip", mime="application/zip")

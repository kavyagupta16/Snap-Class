import streamlit as st


def footer_home():
    st.markdown("""
        <div style="margin-top:2rem; display:flex; justify-content:center; align-items:center">
            <p style="font-weight:600; color:#FFFFFF; font-size:0.85rem; letter-spacing:0.02em;">
                SnapClass &middot; AI Attendance System
            </p>
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    st.markdown("""
        <div style="margin-top:2rem; display:flex; justify-content:center; align-items:center">
            <p style="font-weight:600; color:#475569; font-size:0.85rem; letter-spacing:0.02em;">
                SnapClass &middot; AI Attendance System
            </p>
        </div>
    """, unsafe_allow_html=True)
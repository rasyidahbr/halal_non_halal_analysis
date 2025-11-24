import streamlit as st

st.title("Hello World Test")
st.write("If you can see this, Streamlit deployment is working!")
st.success("✅ Success: Basic Streamlit functionality confirmed")

if st.button("Click me"):
    st.balloons()
    st.write("🎉 Button works too!")
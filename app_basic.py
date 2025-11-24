import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Halal Checker", page_icon="🥗")

# Simple ingredient database
INGREDIENTS = {
    'wheat flour': 'Halal',
    'sugar': 'Halal', 
    'salt': 'Halal',
    'gelatin': 'Non-Halal',
    'alcohol': 'Non-Halal',
    'vanilla extract': 'Doubtful',
    'lecithin': 'Halal',
    'water': 'Halal',
    'vegetable oil': 'Halal'
}

# App
st.title("🥗 Halal Ingredient Checker")
st.write("Check if ingredients are halal or non-halal")

# Input
ingredients_input = st.text_area("Enter ingredients (one per line):", 
                                placeholder="wheat flour\nsugar\ngelatin")

if st.button("Check Ingredients"):
    if ingredients_input:
        ingredients = [ing.strip().lower() for ing in ingredients_input.split('\n') if ing.strip()]
        
        if ingredients:
            st.write("### Results:")
            for ingredient in ingredients:
                # Check if ingredient is in our database
                status = "Unknown"
                for key, value in INGREDIENTS.items():
                    if key in ingredient or ingredient in key:
                        status = value
                        break
                
                # Display result
                if status == "Halal":
                    st.success(f"✅ {ingredient.title()}: {status}")
                elif status == "Non-Halal":
                    st.error(f"❌ {ingredient.title()}: {status}")
                elif status == "Doubtful":
                    st.warning(f"⚠️ {ingredient.title()}: {status}")
                else:
                    st.info(f"❓ {ingredient.title()}: {status}")
        else:
            st.error("Please enter at least one ingredient")
    else:
        st.error("Please enter some ingredients")

# Info
with st.expander("About"):
    st.write("""
    This tool checks common ingredients against Islamic dietary guidelines.
    - ✅ Halal: Permissible
    - ❌ Non-Halal: Forbidden  
    - ⚠️ Doubtful: Needs verification
    - ❓ Unknown: Not in database
    """)
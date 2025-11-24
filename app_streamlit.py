"""
Halal Ingredient Analysis - Streamlit App
Simple and deployment-ready version
"""
import streamlit as st
import pandas as pd
import re
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Halal Ingredient Analyzer",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hardcoded ingredient knowledge base
HALAL_INGREDIENTS = {
    'wheat flour': 'Halal - Plant-based',
    'sugar': 'Halal - Plant-based', 
    'salt': 'Halal - Mineral',
    'vegetable oil': 'Halal - Plant-based',
    'palm oil': 'Halal - Plant-based',
    'sunflower oil': 'Halal - Plant-based',
    'corn starch': 'Halal - Plant-based',
    'baking powder': 'Halal - Chemical leavening',
    'citric acid': 'Halal - Plant-derived',
    'ascorbic acid': 'Halal - Vitamin C',
    'lecithin': 'Halal - Usually plant-based emulsifier',
    'water': 'Halal - Pure'
}

NON_HALAL_INGREDIENTS = {
    'gelatin': 'Non-Halal - Usually from pork/non-halal beef',
    'lard': 'Non-Halal - Pork fat',
    'bacon': 'Non-Halal - Pork product',
    'ham': 'Non-Halal - Pork product', 
    'pepperoni': 'Non-Halal - Usually contains pork',
    'wine': 'Non-Halal - Contains alcohol',
    'beer': 'Non-Halal - Contains alcohol',
    'alcohol': 'Non-Halal - Intoxicant',
    'ethanol': 'Non-Halal - Alcohol',
    'cochineal': 'Non-Halal - Insect-derived coloring',
    'carmine': 'Non-Halal - Insect-derived coloring',
    'shellac': 'Non-Halal - Insect-derived coating'
}

DOUBTFUL_INGREDIENTS = {
    'vanilla extract': 'Doubtful - May contain alcohol',
    'natural flavors': 'Doubtful - Source unknown',
    'mono and diglycerides': 'Doubtful - May be from animal fat',
    'glycerin': 'Doubtful - May be from animal fat',
    'whey': 'Doubtful - Depends on rennet source',
    'enzymes': 'Doubtful - Source needs verification',
    'emulsifier': 'Doubtful - Source needs verification',
    'cheese': 'Doubtful - Depends on rennet used'
}

def load_ingredient_data():
    """Load ingredient data from CSV if available"""
    try:
        df = pd.read_csv('data/halal_non_halal_ingred.csv')
        return df
    except:
        return None

def analyze_ingredient(ingredient, df=None):
    """Analyze a single ingredient"""
    ingredient_lower = ingredient.lower().strip()
    
    # Check hardcoded lists first
    if any(key in ingredient_lower for key in HALAL_INGREDIENTS.keys()):
        for key in HALAL_INGREDIENTS.keys():
            if key in ingredient_lower:
                return 'Halal', HALAL_INGREDIENTS[key]
    
    if any(key in ingredient_lower for key in NON_HALAL_INGREDIENTS.keys()):
        for key in NON_HALAL_INGREDIENTS.keys():
            if key in ingredient_lower:
                return 'Non-Halal', NON_HALAL_INGREDIENTS[key]
    
    if any(key in ingredient_lower for key in DOUBTFUL_INGREDIENTS.keys()):
        for key in DOUBTFUL_INGREDIENTS.keys():
            if key in ingredient_lower:
                return 'Doubtful', DOUBTFUL_INGREDIENTS[key]
    
    # Check CSV data if available
    if df is not None:
        for _, row in df.iterrows():
            if (ingredient_lower in str(row.get('ingred_name', '')).lower() or 
                ingredient_lower in str(row.get('chem_name', '')).lower()):
                status_code = row.get('halal_non_halal_doubtful', 2)
                if status_code == 0:
                    return 'Halal', 'Database: Permissible'
                elif status_code == 1:
                    return 'Non-Halal', 'Database: Forbidden'
                else:
                    return 'Doubtful', 'Database: Needs verification'
    
    return 'Unknown', 'Not in database - consult Islamic scholar'

def main():
    # Title and header
    st.title("🥗 Halal Ingredient Analyzer")
    st.markdown("**Check if food ingredients comply with Islamic dietary laws**")
    
    # Load data
    df = load_ingredient_data()
    if df is not None:
        st.success(f"✅ Loaded {len(df)} ingredients from database")
    else:
        st.info("📚 Using built-in ingredient knowledge base")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Enter ingredients** in the text area
        2. **Separate** with commas or new lines
        3. **Click Analyze** to get results
        4. **Download** results as CSV
        """)
        
        st.header("🏷️ Status Legend")
        st.success("✅ **Halal** - Permissible")
        st.error("❌ **Non-Halal** - Forbidden") 
        st.warning("⚠️ **Doubtful** - Needs verification")
        st.info("❓ **Unknown** - Not in database")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Ingredient Input")
        
        # Input methods
        input_method = st.radio(
            "Choose input method:",
            ["Manual Entry", "File Upload", "Sample Analysis"]
        )
        
        ingredients_text = ""
        
        if input_method == "Manual Entry":
            ingredients_text = st.text_area(
                "Enter ingredients:",
                placeholder="Example: Wheat flour, Sugar, Gelatin, Lecithin, Natural flavors",
                height=150
            )
        
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader("Upload text file", type=['txt'])
            if uploaded_file:
                ingredients_text = str(uploaded_file.read(), "utf-8")
        
        else:  # Sample Analysis
            if st.button("📝 Load Sample Ingredients"):
                ingredients_text = "Wheat flour, Sugar, Salt, Gelatin, Lecithin, Vanilla extract, Natural flavors, Citric acid"
                st.rerun()
    
    with col2:
        st.header("📊 Quick Stats")
        
        # Show ingredient database size
        total_ingredients = len(HALAL_INGREDIENTS) + len(NON_HALAL_INGREDIENTS) + len(DOUBTFUL_INGREDIENTS)
        if df is not None:
            total_ingredients += len(df)
        
        st.metric("Database Size", f"{total_ingredients}+ ingredients")
        st.metric("Built-in Halal", len(HALAL_INGREDIENTS))
        st.metric("Built-in Non-Halal", len(NON_HALAL_INGREDIENTS))
        st.metric("Built-in Doubtful", len(DOUBTFUL_INGREDIENTS))
    
    # Analysis section
    if ingredients_text and st.button("🔍 Analyze Ingredients", type="primary"):
        # Parse ingredients
        if ',' in ingredients_text:
            ingredients_list = [ing.strip() for ing in ingredients_text.split(',')]
        else:
            ingredients_list = [ing.strip() for ing in ingredients_text.split('\n')]
        
        ingredients_list = [ing for ing in ingredients_list if ing]  # Remove empty
        
        if not ingredients_list:
            st.error("Please enter at least one ingredient")
            return
        
        # Analyze each ingredient
        results = []
        halal_count = 0
        non_halal_count = 0
        doubtful_count = 0
        unknown_count = 0
        
        for ingredient in ingredients_list:
            status, reason = analyze_ingredient(ingredient, df)
            results.append({
                'Ingredient': ingredient,
                'Status': status,
                'Reason': reason
            })
            
            if status == 'Halal':
                halal_count += 1
            elif status == 'Non-Halal':
                non_halal_count += 1
            elif status == 'Doubtful':
                doubtful_count += 1
            else:
                unknown_count += 1
        
        # Display summary
        st.markdown("### 📈 Analysis Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("✅ Halal", halal_count)
        with col2:
            st.metric("❌ Non-Halal", non_halal_count)
        with col3:
            st.metric("⚠️ Doubtful", doubtful_count)
        with col4:
            st.metric("❓ Unknown", unknown_count)
        
        # Detailed results
        st.markdown("### 📋 Detailed Analysis")
        
        for result in results:
            ingredient = result['Ingredient']
            status = result['Status']
            reason = result['Reason']
            
            if status == 'Halal':
                st.success(f"✅ **{ingredient}** - {status}")
            elif status == 'Non-Halal':
                st.error(f"❌ **{ingredient}** - {status}")
            elif status == 'Doubtful':
                st.warning(f"⚠️ **{ingredient}** - {status}")
            else:
                st.info(f"❓ **{ingredient}** - {status}")
            
            st.caption(f"📝 {reason}")
        
        # Overall verdict
        st.markdown("---")
        st.markdown("### 🎯 Overall Product Verdict")
        
        if non_halal_count > 0:
            st.error("🚫 **PRODUCT NOT HALAL** - Contains forbidden ingredients")
            st.markdown("❗ **Action**: Avoid this product")
        elif doubtful_count > 0 or unknown_count > 0:
            st.warning("⚠️ **PRODUCT QUESTIONABLE** - Contains doubtful/unknown ingredients")
            st.markdown("🔍 **Action**: Seek clarification from manufacturer or Islamic scholar")
        else:
            st.success("✅ **PRODUCT HALAL** - All ingredients are permissible")
            st.markdown("👍 **Action**: Safe to consume")
        
        # Export results
        if results:
            results_df = pd.DataFrame(results)
            csv_data = results_df.to_csv(index=False)
            
            st.download_button(
                label="📥 Download Analysis Results",
                data=csv_data,
                file_name=f"halal_analysis_{len(results)}_ingredients.csv",
                mime="text/csv",
                type="secondary"
            )
    
    # Footer information
    st.markdown("---")
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        ### 🎯 Purpose
        This tool helps Muslim consumers identify halal ingredients in food products based on Islamic dietary laws.
        
        ### 📚 Data Sources
        - MUIS (Majlis Ugama Islam Singapura) guidelines
        - Islamic food certification standards
        - Comprehensive ingredient databases
        
        ### ⚖️ Important Disclaimer
        This tool provides guidance based on available data. For definitive rulings on questionable ingredients, 
        please consult qualified Islamic scholars or certified halal authorities.
        
        ### 🔗 More Information
        - [GitHub Repository](https://github.com/rasyidahbr/halal_non_halal_analysis)
        - Made with ❤️ for the Muslim community
        """)

if __name__ == "__main__":
    main()
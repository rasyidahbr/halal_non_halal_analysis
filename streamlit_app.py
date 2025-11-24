"""
Halal Ingredient Analysis - Streamlit App
Simplified version combining features from app.py and app_improved.py
"""
import streamlit as st
import pandas as pd
import base64
import re
import os
from io import BytesIO
from PIL import Image

# Optional imports with error handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Halal Ingredient Analyzer",
    page_icon="🥗",
    layout="wide"
)

# Helper functions
def get_base64_of_bin_file(bin_file):
    """Convert image file to base64 for CSS background"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

def load_ingredient_data():
    """Load ingredient database from CSV"""
    try:
        df = pd.read_csv('data/halal_non_halal_ingred.csv')
        return df
    except FileNotFoundError:
        st.warning("Ingredient database not found. Using basic mode.")
        return None
    except Exception as e:
        st.error(f"Error loading ingredient data: {str(e)}")
        return None

def setup_custom_styling():
    """Setup custom CSS styling similar to original app"""
    img_base64 = get_base64_of_bin_file("snack.jpg")
    
    custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Aclonica&display=swap');

    body, [class*="st-"] {{
        font-family: 'Aclonica', sans-serif;
    }}

    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
    }}

    .main-header {{
        text-align: center;
        color: #2E8B57;
        font-weight: bold;
        margin-bottom: 20px;
    }}

    .ingredient-card {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def analyze_ingredients_basic(ingredient_text, df=None):
    """Basic ingredient analysis using the CSV database"""
    if not ingredient_text:
        return [], [], [], []
    
    # Parse ingredients
    ingredients = [ing.strip() for ing in re.split('[,\n]', ingredient_text) if ing.strip()]
    
    halal_ingredients = []
    non_halal_ingredients = []
    doubtful_ingredients = []
    unknown_ingredients = []
    
    if df is not None:
        for ingredient in ingredients:
            found = False
            ingredient_lower = ingredient.lower()
            
            for _, row in df.iterrows():
                ing_name = str(row.get('ingred_name', '')).lower()
                chem_name = str(row.get('chem_name', '')).lower()
                
                if ingredient_lower in ing_name or ing_name in ingredient_lower or \
                   ingredient_lower in chem_name or chem_name in ingredient_lower:
                    
                    status = row.get('halal_non_halal_doubtful', 2)
                    if status == 0:  # Halal
                        halal_ingredients.append(ingredient)
                    elif status == 1:  # Non-Halal
                        non_halal_ingredients.append(ingredient)
                    else:  # Doubtful
                        doubtful_ingredients.append(ingredient)
                    found = True
                    break
            
            if not found:
                unknown_ingredients.append(ingredient)
    else:
        # Fallback to basic hardcoded analysis
        basic_halal = ['wheat flour', 'sugar', 'salt', 'water', 'vegetable oil', 'palm oil']
        basic_non_halal = ['gelatin', 'lard', 'alcohol', 'wine', 'beer', 'bacon', 'ham']
        basic_doubtful = ['vanilla extract', 'natural flavors', 'mono and diglycerides']
        
        for ingredient in ingredients:
            ingredient_lower = ingredient.lower()
            if any(h in ingredient_lower for h in basic_halal):
                halal_ingredients.append(ingredient)
            elif any(nh in ingredient_lower for nh in basic_non_halal):
                non_halal_ingredients.append(ingredient)
            elif any(d in ingredient_lower for d in basic_doubtful):
                doubtful_ingredients.append(ingredient)
            else:
                unknown_ingredients.append(ingredient)
    
    return halal_ingredients, non_halal_ingredients, doubtful_ingredients, unknown_ingredients

def display_analysis_results(halal, non_halal, doubtful, unknown):
    """Display the analysis results in a clear format"""
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("✅ Halal", len(halal), help="Permissible ingredients")
    with col2:
        st.metric("❌ Non-Halal", len(non_halal), help="Forbidden ingredients")
    with col3:
        st.metric("⚠️ Doubtful", len(doubtful), help="Requires verification")
    with col4:
        st.metric("❓ Unknown", len(unknown), help="Not in database")
    
    st.markdown("---")
    
    # Detailed results
    col_left, col_right = st.columns(2)
    
    with col_left:
        if halal:
            st.success("✅ **Halal Ingredients**")
            for ingredient in halal:
                st.write(f"• {ingredient}")
        
        if non_halal:
            st.error("❌ **Non-Halal Ingredients**")
            for ingredient in non_halal:
                st.write(f"• {ingredient}")
    
    with col_right:
        if doubtful:
            st.warning("⚠️ **Doubtful Ingredients**")
            for ingredient in doubtful:
                st.write(f"• {ingredient}")
            st.caption("These ingredients require verification of their source.")
        
        if unknown:
            st.info("❓ **Unknown Ingredients**")
            for ingredient in unknown:
                st.write(f"• {ingredient}")
            st.caption("These ingredients are not in our database. Consult an Islamic scholar.")
    
    # Overall verdict
    st.markdown("---")
    if non_halal:
        st.error("🚫 **Overall Verdict: NOT HALAL** - Contains forbidden ingredients")
    elif doubtful or unknown:
        st.warning("⚠️ **Overall Verdict: REQUIRES VERIFICATION** - Contains questionable ingredients")
    else:
        st.success("✅ **Overall Verdict: HALAL** - All ingredients are permissible")

def main():
    """Main application function"""
    
    # Setup styling
    setup_custom_styling()
    
    # Header
    st.markdown('<h1 class="main-header">🥗 Halal Ingredient Analyzer 🍽️</h1>', unsafe_allow_html=True)
    st.markdown("**Analyze food ingredients to determine their Halal status according to Islamic dietary laws**")
    
    # Load ingredient database
    df = load_ingredient_data()
    if df is not None:
        st.success(f"✅ Loaded {len(df)} ingredients from database")
    else:
        st.info("📚 Using basic ingredient analysis mode")
    
    # Sidebar information
    with st.sidebar:
        st.header("📋 How to Use")
        st.markdown("""
        1. **Enter ingredients** in the text area below
        2. **Separate ingredients** with commas or new lines
        3. **Click 'Analyze'** to get the halal status
        4. **Review results** and overall verdict
        """)
        
        st.header("🏷️ Status Guide")
        st.success("✅ **Halal**: Permissible according to Islamic law")
        st.error("❌ **Non-Halal**: Forbidden in Islamic dietary laws")
        st.warning("⚠️ **Doubtful**: Source/processing needs verification")
        st.info("❓ **Unknown**: Not found in database")
        
        st.markdown("---")
        st.markdown("**Data Sources:**")
        st.markdown("• MUIS Singapore guidelines")
        st.markdown("• Islamic food certification standards")
        st.markdown("• Comprehensive ingredient databases")
    
    # Main interface
    st.header("🔍 Ingredient Analysis")
    
    # Input methods
    input_method = st.radio(
        "Choose input method:",
        ["Manual Text Input", "Sample Analysis"],
        horizontal=True
    )
    
    ingredients_text = ""
    
    if input_method == "Manual Text Input":
        ingredients_text = st.text_area(
            "Enter ingredients (separate with commas or new lines):",
            placeholder="Example: Wheat flour, Sugar, Salt, Gelatin, Natural flavors, Citric acid",
            height=150,
            help="List all ingredients from the product label"
        )
    
    else:  # Sample Analysis
        if st.button("📝 Load Sample Ingredients"):
            ingredients_text = """Wheat flour, Sugar, Salt, Vegetable oil, Lecithin (Soy), 
Natural vanilla flavoring, Baking powder, Citric acid, 
Mono and diglycerides, Artificial colors, Gelatin"""
            st.rerun()
    
    # Analysis button
    if ingredients_text and st.button("🔍 Analyze Ingredients", type="primary", use_container_width=True):
        with st.spinner("Analyzing ingredients..."):
            halal, non_halal, doubtful, unknown = analyze_ingredients_basic(ingredients_text, df)
        
        if halal or non_halal or doubtful or unknown:
            st.header("📊 Analysis Results")
            display_analysis_results(halal, non_halal, doubtful, unknown)
            
            # Export functionality
            if st.button("📥 Export Results as CSV"):
                results_data = []
                for ing in halal:
                    results_data.append({"Ingredient": ing, "Status": "Halal"})
                for ing in non_halal:
                    results_data.append({"Ingredient": ing, "Status": "Non-Halal"})
                for ing in doubtful:
                    results_data.append({"Ingredient": ing, "Status": "Doubtful"})
                for ing in unknown:
                    results_data.append({"Ingredient": ing, "Status": "Unknown"})
                
                results_df = pd.DataFrame(results_data)
                csv = results_df.to_csv(index=False)
                
                st.download_button(
                    label="💾 Download CSV Report",
                    data=csv,
                    file_name="halal_analysis_report.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No ingredients found. Please check your input.")
    
    # Information section
    st.markdown("---")
    with st.expander("ℹ️ About This Application"):
        st.markdown("""
        ### 🎯 Purpose
        This application helps Muslim consumers identify halal ingredients in food products 
        based on Islamic dietary laws and established halal certification guidelines.
        
        ### 📚 How It Works
        - **Database Analysis**: Ingredients are checked against a comprehensive database
        - **Islamic Guidelines**: Classifications follow established Islamic dietary laws
        - **MUIS Standards**: Based on Singapore's Islamic Religious Council guidelines
        
        ### ⚖️ Important Disclaimer
        This tool provides guidance based on available data and general Islamic principles. 
        For definitive rulings on questionable ingredients, please consult qualified Islamic 
        scholars or certified halal authorities.
        
        ### 🔗 Additional Resources
        - [MUIS Halal Guidelines](https://www.muis.gov.sg/halal)
        - [Project Repository](https://github.com/rasyidahbr/halal_non_halal_analysis)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("**Made with ❤️ for the Muslim community worldwide** 🌍")

if __name__ == "__main__":
    main()
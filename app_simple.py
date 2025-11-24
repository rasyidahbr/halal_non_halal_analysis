"""
Streamlit Deployment Ready - Halal Ingredient Analysis
"""
import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# Set up page config first
st.set_page_config(
    page_title="Halal Ingredient Analyzer",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add error handling for imports
def safe_import():
    """Safely import modules and handle missing dependencies"""
    try:
        # Add current directory to Python path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Try importing our modules
        from src.utils.data_handler import load_ingredients_data
        from src.utils.ingredient_parser import parse_ingredients, create_lookup_table, check_halal_status
        return True, None
    except Exception as e:
        st.error(f"Import error: {str(e)}")
        return False, str(e)

def load_data():
    """Load ingredients data with error handling"""
    try:
        # Try to load from multiple possible locations
        possible_paths = [
            "data/halal_non_halal_ingred.csv",
            "./data/halal_non_halal_ingred.csv",
            "halal_non_halal_ingred.csv"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                df = pd.read_csv(path)
                return df
        
        # If no file found, create sample data
        st.warning("Ingredients database not found. Using sample data.")
        return pd.DataFrame({
            'ingred_name': ['Lecithin', 'Gelatin', 'Vanilla Extract'],
            'chem_name': ['Lecithin', 'Gelatin', 'Vanilla Extract'],
            'description': ['Emulsifier', 'Gelling agent', 'Flavoring'],
            'halal_non_halal_doubtful': [0, 1, 2]  # 0=Halal, 1=Non-Halal, 2=Doubtful
        })
    except Exception as e:
        st.error(f"Data loading error: {str(e)}")
        return None

def simple_ingredient_checker(ingredients_text, df):
    """Simple ingredient checking logic"""
    if df is None:
        return [], [], []
    
    # Simple text parsing
    ingredients = [ing.strip().lower() for ing in ingredients_text.split(',')]
    
    halal_ingredients = []
    non_halal_ingredients = []
    doubtful_ingredients = []
    
    for ingredient in ingredients:
        found = False
        for _, row in df.iterrows():
            if ingredient in row['ingred_name'].lower() or ingredient in row['chem_name'].lower():
                if row['halal_non_halal_doubtful'] == 0:
                    halal_ingredients.append(ingredient)
                elif row['halal_non_halal_doubtful'] == 1:
                    non_halal_ingredients.append(ingredient)
                else:
                    doubtful_ingredients.append(ingredient)
                found = True
                break
        
        if not found:
            doubtful_ingredients.append(ingredient)
    
    return halal_ingredients, non_halal_ingredients, doubtful_ingredients

def main():
    """Main application"""
    st.title("🥗 Halal Ingredient Analyzer")
    st.caption("Analyze ingredients to determine their Halal status")
    
    # Check imports
    imports_ok, error = safe_import()
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Could not load ingredients data. Please check the data file.")
        return
    
    # Sidebar
    st.sidebar.header("📋 How to Use")
    st.sidebar.markdown("""
    1. **Enter Ingredients**: Type or paste ingredient list
    2. **Analyze**: Click the analyze button
    3. **Review Results**: See halal/non-halal classification
    4. **Export**: Download results as needed
    """)
    
    # Main interface
    st.header("🔍 Ingredient Analysis")
    
    # Input methods
    input_method = st.radio(
        "Choose input method:",
        ["Text Input", "File Upload", "Sample Analysis"],
        horizontal=True
    )
    
    ingredients_text = ""
    
    if input_method == "Text Input":
        ingredients_text = st.text_area(
            "Enter ingredients (separated by commas):",
            placeholder="Example: Wheat flour, Sugar, Salt, Lecithin, Natural flavors",
            height=100
        )
    
    elif input_method == "File Upload":
        uploaded_file = st.file_uploader(
            "Upload ingredient list (text file)",
            type=['txt', 'csv']
        )
        if uploaded_file:
            try:
                ingredients_text = str(uploaded_file.read(), "utf-8")
            except:
                st.error("Could not read file. Please upload a text file.")
    
    else:  # Sample Analysis
        if st.button("Use Sample Ingredients"):
            ingredients_text = "Wheat flour, Sugar, Salt, Lecithin, Gelatin, Natural vanilla extract, Citric acid"
    
    # Analysis
    if ingredients_text and st.button("🔍 Analyze Ingredients", type="primary"):
        with st.spinner("Analyzing ingredients..."):
            halal, non_halal, doubtful = simple_ingredient_checker(ingredients_text, df)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success(f"✅ **Halal Ingredients** ({len(halal)})")
            if halal:
                for ing in halal:
                    st.write(f"• {ing.title()}")
            else:
                st.write("None found")
        
        with col2:
            st.error(f"❌ **Non-Halal Ingredients** ({len(non_halal)})")
            if non_halal:
                for ing in non_halal:
                    st.write(f"• {ing.title()}")
            else:
                st.write("None found")
        
        with col3:
            st.warning(f"⚠️ **Doubtful/Unknown** ({len(doubtful)})")
            if doubtful:
                for ing in doubtful:
                    st.write(f"• {ing.title()}")
            else:
                st.write("None found")
        
        # Overall verdict
        st.markdown("---")
        if non_halal:
            st.error("🚫 **Overall Status: NOT HALAL** - Contains non-halal ingredients")
        elif doubtful:
            st.warning("⚠️ **Overall Status: DOUBTFUL** - Contains questionable ingredients")
        else:
            st.success("✅ **Overall Status: HALAL** - All ingredients are permissible")
        
        # Export option
        if st.button("📥 Download Results"):
            results_df = pd.DataFrame({
                'Ingredient': halal + non_halal + doubtful,
                'Status': ['Halal']*len(halal) + ['Non-Halal']*len(non_halal) + ['Doubtful']*len(doubtful)
            })
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="halal_analysis_results.csv",
                mime="text/csv"
            )
    
    # Information section
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        ### How it works:
        - **Database Lookup**: Compares ingredients against a comprehensive halal/non-halal database
        - **Classification**: Ingredients are classified as Halal (✅), Non-Halal (❌), or Doubtful (⚠️)
        - **Islamic Guidelines**: Based on Islamic dietary laws and MUIS guidelines
        
        ### Data Sources:
        - MUIS (Majlis Ugama Islam Singapura) guidelines
        - Islamic food certification standards
        - Comprehensive ingredient databases
        
        ### Note:
        This tool provides guidance based on available data. For definitive rulings, 
        consult with Islamic scholars or certified halal authorities.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("**Made with ❤️ for the Muslim community** | [GitHub Repository](https://github.com/rasyidahbr/halal_non_halal_analysis)")

if __name__ == "__main__":
    main()
"""
Ultra-Minimal Halal Ingredient Analyzer - Streamlit Cloud Ready
"""
import streamlit as st
import pandas as pd
import io

# Page configuration
st.set_page_config(
    page_title="Halal Ingredient Checker",
    page_icon="🥗",
    layout="centered"
)

# Hardcoded ingredient data (in case CSV loading fails)
INGREDIENT_DATA = {
    'gelatin': {'status': 'Non-Halal', 'reason': 'Usually derived from pork or non-halal beef'},
    'lecithin': {'status': 'Halal', 'reason': 'Plant-based emulsifier'},
    'vanilla extract': {'status': 'Doubtful', 'reason': 'May contain alcohol'},
    'cochineal': {'status': 'Non-Halal', 'reason': 'Insect-derived coloring'},
    'carmines': {'status': 'Non-Halal', 'reason': 'Insect-derived coloring'},
    'shellac': {'status': 'Non-Halal', 'reason': 'Insect-derived coating'},
    'whey': {'status': 'Doubtful', 'reason': 'Depends on rennet source'},
    'natural flavors': {'status': 'Doubtful', 'reason': 'Source unknown'},
    'mono and diglycerides': {'status': 'Doubtful', 'reason': 'May be from animal fat'},
    'glycerin': {'status': 'Doubtful', 'reason': 'May be from animal fat'},
    'lard': {'status': 'Non-Halal', 'reason': 'Pork fat'},
    'bacon': {'status': 'Non-Halal', 'reason': 'Pork product'},
    'ham': {'status': 'Non-Halal', 'reason': 'Pork product'},
    'wine': {'status': 'Non-Halal', 'reason': 'Contains alcohol'},
    'beer': {'status': 'Non-Halal', 'reason': 'Contains alcohol'},
    'alcohol': {'status': 'Non-Halal', 'reason': 'Intoxicant'},
    'ethanol': {'status': 'Non-Halal', 'reason': 'Alcohol'},
    'wheat flour': {'status': 'Halal', 'reason': 'Plant-based'},
    'sugar': {'status': 'Halal', 'reason': 'Plant-based'},
    'salt': {'status': 'Halal', 'reason': 'Mineral'},
    'water': {'status': 'Halal', 'reason': 'Pure'},
    'vegetable oil': {'status': 'Halal', 'reason': 'Plant-based'},
    'palm oil': {'status': 'Halal', 'reason': 'Plant-based'},
    'sunflower oil': {'status': 'Halal', 'reason': 'Plant-based'},
    'corn starch': {'status': 'Halal', 'reason': 'Plant-based'},
    'baking powder': {'status': 'Halal', 'reason': 'Chemical leavening agent'},
    'citric acid': {'status': 'Halal', 'reason': 'Plant-derived acid'},
    'sodium bicarbonate': {'status': 'Halal', 'reason': 'Chemical compound'},
    'ascorbic acid': {'status': 'Halal', 'reason': 'Vitamin C'},
}

def load_csv_data():
    """Try to load CSV data, fallback to hardcoded data"""
    try:
        # Try multiple possible CSV locations
        csv_paths = ['data/halal_non_halal_ingred.csv', 'halal_non_halal_ingred.csv']
        
        for path in csv_paths:
            try:
                df = pd.read_csv(path)
                if len(df) > 0 and 'ingred_name' in df.columns:
                    return df
            except:
                continue
        
        return None
    except:
        return None

def check_ingredient_status(ingredient, df=None):
    """Check if ingredient is halal, non-halal, or doubtful"""
    ingredient_lower = ingredient.lower().strip()
    
    # First check hardcoded data
    if ingredient_lower in INGREDIENT_DATA:
        return INGREDIENT_DATA[ingredient_lower]
    
    # Check CSV data if available
    if df is not None:
        try:
            for _, row in df.iterrows():
                if (ingredient_lower in str(row.get('ingred_name', '')).lower() or 
                    ingredient_lower in str(row.get('chem_name', '')).lower()):
                    
                    status_code = row.get('halal_non_halal_doubtful', 2)
                    if status_code == 0:
                        return {'status': 'Halal', 'reason': 'Listed as permissible'}
                    elif status_code == 1:
                        return {'status': 'Non-Halal', 'reason': 'Listed as forbidden'}
                    else:
                        return {'status': 'Doubtful', 'reason': 'Requires verification'}
        except:
            pass
    
    # Default for unknown ingredients
    return {'status': 'Unknown', 'reason': 'Not in database - consult Islamic scholar'}

def main():
    """Main application"""
    
    # Title and description
    st.title("🥗 Halal Ingredient Checker")
    st.markdown("**Check if food ingredients are Halal, Non-Halal, or Doubtful**")
    
    # Try loading CSV data
    df = load_csv_data()
    if df is not None:
        st.success(f"✅ Loaded {len(df)} ingredients from database")
    else:
        st.info("📚 Using built-in ingredient database")
    
    # Input section
    st.markdown("### 🔍 Enter Ingredients to Check")
    
    # Text input
    ingredients_input = st.text_area(
        "Type ingredients (one per line or separated by commas):",
        placeholder="Example:\nWheat flour\nSugar\nGelatin\nLecithin",
        height=120
    )
    
    # Sample ingredients button
    if st.button("📝 Use Sample Ingredients"):
        ingredients_input = "Wheat flour, Sugar, Gelatin, Lecithin, Vanilla extract, Natural flavors"
        st.rerun()
    
    # Analysis
    if ingredients_input and st.button("🔍 Analyze Ingredients", type="primary"):
        
        # Parse ingredients
        if ',' in ingredients_input:
            ingredients_list = [ing.strip() for ing in ingredients_input.split(',')]
        else:
            ingredients_list = [ing.strip() for ing in ingredients_input.split('\n') if ing.strip()]
        
        if not ingredients_list:
            st.error("Please enter at least one ingredient")
            return
        
        # Analyze each ingredient
        results = []
        halal_count = 0
        non_halal_count = 0
        doubtful_count = 0
        
        st.markdown("### 📊 Analysis Results")
        
        for ingredient in ingredients_list:
            if ingredient:
                result = check_ingredient_status(ingredient, df)
                results.append({
                    'Ingredient': ingredient,
                    'Status': result['status'],
                    'Reason': result['reason']
                })
                
                # Count statuses
                if result['status'] == 'Halal':
                    halal_count += 1
                elif result['status'] == 'Non-Halal':
                    non_halal_count += 1
                else:
                    doubtful_count += 1
        
        # Display results in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("✅ Halal", halal_count)
        with col2:
            st.metric("❌ Non-Halal", non_halal_count)
        with col3:
            st.metric("⚠️ Doubtful/Unknown", doubtful_count)
        
        # Detailed results
        st.markdown("### 📋 Detailed Results")
        
        for result in results:
            ingredient = result['Ingredient']
            status = result['Status']
            reason = result['Reason']
            
            if status == 'Halal':
                st.success(f"✅ **{ingredient}** - {status}")
                st.caption(reason)
            elif status == 'Non-Halal':
                st.error(f"❌ **{ingredient}** - {status}")
                st.caption(reason)
            else:
                st.warning(f"⚠️ **{ingredient}** - {status}")
                st.caption(reason)
        
        # Overall verdict
        st.markdown("---")
        st.markdown("### 🎯 Overall Product Status")
        
        if non_halal_count > 0:
            st.error("🚫 **NOT HALAL** - Contains non-halal ingredients")
        elif doubtful_count > 0:
            st.warning("⚠️ **DOUBTFUL** - Contains questionable ingredients that need verification")
        else:
            st.success("✅ **HALAL** - All ingredients are permissible")
        
        # Export option
        if st.button("📥 Download Results as CSV"):
            results_df = pd.DataFrame(results)
            csv_buffer = io.StringIO()
            results_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="💾 Download CSV File",
                data=csv_data,
                file_name="halal_ingredient_analysis.csv",
                mime="text/csv"
            )
    
    # Information section
    st.markdown("---")
    
    with st.expander("ℹ️ How This Tool Works"):
        st.markdown("""
        ### 🔍 Analysis Method:
        - **Database Lookup**: Ingredients are checked against a comprehensive database
        - **Islamic Guidelines**: Classifications based on Islamic dietary laws
        - **MUIS Standards**: Following Singapore's Islamic authority guidelines
        
        ### 📚 Classification System:
        - **✅ Halal**: Permissible according to Islamic law
        - **❌ Non-Halal**: Forbidden (contains pork, alcohol, etc.)
        - **⚠️ Doubtful**: Requires verification of source/processing method
        - **❓ Unknown**: Not in database - consult Islamic scholar
        
        ### ⚖️ Important Note:
        This tool provides guidance based on available data. For definitive rulings on 
        doubtful ingredients, please consult with qualified Islamic scholars or 
        certified halal authorities.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("**Made with ❤️ for the Muslim community** 🌍")
    st.markdown("📧 Questions? Check the [GitHub Repository](https://github.com/rasyidahbr/halal_non_halal_analysis)")

if __name__ == "__main__":
    main()
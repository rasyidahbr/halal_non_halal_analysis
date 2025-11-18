"""
UI components and styling for the Streamlit app        [data-testid="stAppViewContainer"] {
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        position: relative;
        }
        
        :root { --footer-gap: 160px; } /* adjust if your footer grows taller */

        [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        /* leave a gap at the bottom so footer is on raw background */
        inset: 0 0 var(--footer-gap) 0;
        background-color: rgba(255, 255, 255, 0.7);
        pointer-events: none;
        z-index: 1;
}
        
        /* Ensure content is above the overlay */
        [data-testid="stAppViewContainer"] > * {
        position: relative;
        z-index: 2;
        }
        
        [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
        }.
"""
import base64
import streamlit as st
from pathlib import Path
from typing import Optional


def get_base64_of_bin_file(bin_file_path: str) -> str:
    """
    Get base64 encoded string of a binary file.
    
    Args:
        bin_file_path (str): Path to the binary file
        
    Returns:
        str: Base64 encoded string
    """
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background_image(image_path: str) -> None:
    """
    Set a background image for the Streamlit app.
    
    Args:
        image_path (str): Path to the background image
    """
    if not Path(image_path).exists():
        return
        
    try:
        img = get_base64_of_bin_file(image_path)
        
        custom_css = f"""
        <style>
        
        @import url('https://fonts.googleapis.com/css2?family=Aclonica&display=swap');
        
        /* Apply the Aclonica font to general text elements */
        body, [class*="st-"], div, p, h1, h2, h3, h4, h5, h6, li, span, button, input, select, textarea {{
            font-family: 'Aclonica', sans-serif !important;
        }}
        
        /* Ensure all text elements use the font */
        .stButton > button, .stTextInput > div > div > input, .stSelectbox, .stMultiSelect {{
            font-family: 'Aclonica', sans-serif !important;
        }}
        
        [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        }}
        
        [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
        }}
        
        /* Add custom styling for the results display */
        .halal-status {{
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: 'Aclonica', sans-serif !important;
        }}
        
        .halal {{
            background-color: rgba(0, 255, 0, 0.2);
            border: 1px solid green;
            color: #006400;
        }}
        
        .non-halal {{
            background-color: rgba(255, 0, 0, 0.1);
            border: 1px solid #551606;
            color: #551606;
        }}
        
        .doubtful {{
            background-color: rgba(255, 255, 0, 0.2);
            border: 1px solid #B8860B;
            color: #8B4513;
        }}
        
        /* Custom warning and info boxes with standard font */
        .st-emotion-cache-16txtl3, .st-emotion-cache-r421ms {{
            font-family: 'Aclonica', sans-serif !important;
            color: #551606 !important;
        }}
        
        /* Style all error and warning messages with Blood Night color - maintain default transparency */
        .stException, .stError, .stWarning {{
            color: #551606 !important;
            font-family: 'Aclonica', sans-serif !important;
            /* Use default Streamlit error background transparency */
        }}
        
        </style>
        """
        
        st.markdown(custom_css, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background image: {e}")


def apply_global_font_style():
    """
    Apply the Aclonica font globally throughout the application.
    Set error and warning texts to Blood Night color (#551606).
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Aclonica&display=swap');
    
    /* Apply to all elements */
    html, body, [class*="st-"], div, p, h1, h2, h3, h4, h5, h6, li, span, button, input, select, textarea {
        font-family: 'Aclonica', sans-serif !important;
    }
    
    /* Custom title size for the app title */
    [data-testid="stAppViewContainer"] h1 {
        font-size: 2.5rem !important; /* Reduced font size */
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        white-space: nowrap; /* Prevent line breaks */
        overflow: visible; /* Allow content to extend beyond container if needed */
        text-align: center; /* Center the title */
        width: 100%; /* Ensure the title takes the full width */
    }
    
    /* Center the title container */
    [data-testid="stAppViewContainer"] [data-testid="stHeader"] {
        display: flex;
        justify-content: center;
    }
    
    /* Apply to specific Streamlit elements */
    .stButton > button, 
    .stTextInput > div > div > input, 
    .stSelectbox > div > div, 
    .stMultiSelect > div > div,
    .streamlit-expanderHeader,
    .streamlit-expanderContent {
        font-family: 'Aclonica', sans-serif !important;
    }
    
    /* Style for error and warning messages - maintain default transparency */
    .st-emotion-cache-16idsys p,
    .st-emotion-cache-r421ms p,
    .st-emotion-cache-1erivf3 p,
    .st-emotion-cache-16txtl3 p,
    .stAlert p {
        color: #551606 !important;
        font-family: 'Aclonica', sans-serif !important;
    }
    
    /* Blood Night color for error icons and borders - maintain default transparency */
    .st-emotion-cache-16idsys svg,
    .st-emotion-cache-r421ms svg,
    .st-emotion-cache-1erivf3 svg {
        fill: #551606 !important;
    }
    
    /* Maintain default Streamlit error/warning container background opacity */
    .st-emotion-cache-16idsys,
    .st-emotion-cache-r421ms,
    .st-emotion-cache-1erivf3,
    .st-emotion-cache-16txtl3,
    .stAlert {
        background-color: rgba(255, 224, 229, 0.4) !important; /* Restore default Streamlit error background with transparency */
    }
    </style>
    """, unsafe_allow_html=True)


def setup_page(title: str, caption: str, disclaimer: str, background_image: Optional[str] = None) -> None:
    """
    Set up the Streamlit page with title, caption, and background.
    
    Args:
        title (str): Page title
        caption (str): Page caption
        disclaimer (str): Page disclaimer
        background_image (Optional[str]): Path to background image
    """
    # Apply global font style first
    apply_global_font_style()
    
    st.title(title)
    
    if background_image:
        set_background_image(background_image)
    
    # Caption and disclaimer will be displayed in the footer instead


def display_halal_status(status: str, container=None) -> None:
    """
    Display the halal status with appropriate styling.
    
    Args:
        status (str): Halal status ('Halal', 'Non-Halal', or 'Doubtful')
        container: Optional Streamlit container to display in
    """
    target = container if container else st
    
    css_class = ""
    text_color = ""
    
    if status.lower() == 'halal':
        css_class = "halal"
        text_color = "#006400"  # Dark green
    elif status.lower() == 'non-halal':
        css_class = "non-halal"
        text_color = "#551606"  # Blood Night
    else:  # doubtful
        css_class = "doubtful"
        text_color = "#8B4513"  # SaddleBrown
        
    target.markdown(
        f"""<div class='halal-status {css_class}' style="font-family: 'Aclonica', sans-serif !important;">
            <h3 style="font-family: 'Aclonica', sans-serif !important; color: {text_color};">Product Status: {status}</h3>
        </div>""",
        unsafe_allow_html=True
    )


def display_unknown_ingredients(ingredients: list, container=None) -> None:
    """
    Display the list of unknown ingredients using Blood Night color.
    
    Args:
        ingredients (list): List of unknown ingredients
        container: Optional Streamlit container to display in
    """
    target = container if container else st
    
    if not ingredients:
        return
        
    target.markdown("""
    <h3 style="font-family: 'Aclonica', sans-serif !important; color: #551606;">Unknown Ingredients:</h3>
    """, unsafe_allow_html=True)
    
    # Join ingredients and display with Blood Night color
    ingredients_text = ", ".join(ingredients)
    target.markdown(f"""
    <div style="font-family: 'Aclonica', sans-serif !important; color: #551606; padding: 10px; 
    background-color: rgba(255, 243, 205, 0.3); border-radius: 5px; border-left: 3px solid #551606;">
    {ingredients_text}
    </div>
    """, unsafe_allow_html=True)


def display_ingredients_text(text: str, container=None) -> None:
    """
    Display the ingredients text with formatting.
    
    Args:
        text (str): Ingredients text
        container: Optional Streamlit container to display in
    """
    target = container if container else st
    target.markdown("### Extracted Ingredients:")
    target.write(text)


def display_ingredients_comparison(ingredients_list: list, lookup_table: dict, container=None) -> None:
    """
    Display ingredients with their halal status from the database for comparison.
    
    Args:
        ingredients_list (list): List of parsed ingredients
        lookup_table (dict): Dictionary mapping ingredients to their halal status
        container: Optional Streamlit container to display in
    """
    target = container if container else st
    
    target.markdown("### Ingredients Database Comparison:")
    
    # Create table with colored status
    table_rows = []
    for ingredient in ingredients_list:
        ingredient_lower = ingredient.lower()
        status = lookup_table.get(ingredient_lower, "Unknown")
        
        # Determine CSS class based on status
        if status == "Halal":
            status_html = '<span style="color: #006400; background-color: rgba(0, 255, 0, 0.2); padding: 3px 8px; border-radius: 3px;">Halal</span>'
        elif status == "Non-Halal":
            status_html = '<span style="color: #551606; background-color: rgba(255, 0, 0, 0.1); padding: 3px 8px; border-radius: 3px;">Non-Halal</span>'
        elif status == "Doubtful":
            status_html = '<span style="color: #8B4513; background-color: rgba(255, 255, 0, 0.2); padding: 3px 8px; border-radius: 3px;">Doubtful</span>'
        else:
            status_html = '<span style="color: #551606; background-color: rgba(211, 211, 211, 0.3); padding: 3px 8px; border-radius: 3px;">Not in Database</span>'
            
        table_rows.append(f"<tr><td>{ingredient}</td><td>{status_html}</td></tr>")
    
    # Create the HTML table
    table_html = f"""
    <div style="font-family: 'Aclonica', sans-serif !important; margin: 15px 0;">
    <table style="width: 100%; border-collapse: collapse; font-family: 'Aclonica', sans-serif !important;">
        <thead>
            <tr style="background-color: rgba(240, 240, 240, 0.5);">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Ingredient</th>
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Status in Database</th>
            </tr>
        </thead>
        <tbody>
            {''.join(table_rows)}
        </tbody>
    </table>
    </div>
    """
    target.markdown(table_html, unsafe_allow_html=True)
    
    
def display_custom_warning(message: str, title: str = "Warning", container=None) -> None:
    """
    Display a custom warning message with Blood Night color (#551606) text.
    
    Args:
        message (str): Warning message content
        title (str): Warning title
        container: Optional Streamlit container to display in
    """
    target = container if container else st
    target.markdown(f"""
    <div style="background-color: rgba(255, 243, 205, 0.4); padding: 20px; border-radius: 5px; border-left: 5px solid #FFD700; margin: 10px 0; color: #551606; font-family: 'Aclonica', sans-serif !important;">
    <h3 style="color: #551606; margin-top: 0; font-family: 'Aclonica', sans-serif !important;">⚠️ {title}</h3>
    <p style="color: #551606; font-family: 'Aclonica', sans-serif !important;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def display_footer(caption: str, disclaimer: str) -> None:
    """
    Display footer at the bottom of the page on the background (outside the main container).
    """
    st.markdown(
        """
        <style>
        .app-footer {
            margin-top: 1.25rem;
            text-align: center;
            z-index: 0; /* behind content layers */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="app-footer">
            <hr style="opacity: .3; margin: 0 0 8px 0;" />
            <div style="font-size: .9em; color: rgba(60,60,60,.85);">{caption}</div>
            <div style="font-size: .8em; color: rgba(60,60,60,.7);">{disclaimer}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def format_text_with_font(text: str) -> str:
    """
    Format text with the Aclonica font.
    
    Args:
        text (str): Text to format
        
    Returns:
        str: HTML-formatted text with Aclonica font
    """
    return f'<span style="font-family: \'Aclonica\', sans-serif !important;">{text}</span>'


def display_styled_text(text: str, container=None) -> None:
    """
    Display text with the Aclonica font.
    
    Args:
        text (str): Text to display
        container: Optional Streamlit container to display in
    """
    target = container if container else st
    target.markdown(format_text_with_font(text), unsafe_allow_html=True)


def create_export_button(data: dict, filename: str = "analysis_results.csv") -> None:
    """
    Create a button to export analysis results.
    
    Args:
        data (dict): Data to export
        filename (str): Name of the export file
    """
    import pandas as pd
    import io
    
    # Convert the data to a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index').reset_index()
    df.columns = ['Item', 'Value']
    
    # Convert to CSV
    csv = df.to_csv(index=False).encode()
    
    # Create a download button
    st.download_button(
        label="Export Results",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )
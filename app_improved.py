"""
Main application for Halal Ingredient Analysis using Streamlit.
"""
import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import toml
import os
from typing import Optional, Dict, Any, List

# Try to import openai, but make it optional
try:
    import openai
except ImportError:
    st.warning("OpenAI module not found. Image analysis and some API features will be disabled.")
    openai = None

# Import modules
from src.utils.ingredient_parser import parse_ingredients, create_lookup_table, check_halal_status
from src.utils.data_handler import load_ingredients_data
from src.api.openai_handler import extract_ingredients_from_image, query_openai_about_ingredients
from src.ui.components import (
    setup_page, display_halal_status, display_unknown_ingredients, 
    display_ingredients_text, create_export_button, display_custom_warning,
    display_footer, display_ingredients_comparison
)
from src.api.llama_index_handler import load_index_and_context, get_chat_engine
from config.settings import (
    APP_TITLE, APP_CAPTION, APP_DISCLAIMER, BACKGROUND_IMAGE,
    DEFAULT_MODEL, VISION_MODEL, CONTEXT_WINDOW, TEMPERATURE, MAX_TOKENS,
    OPENAI_API_ENDPOINT, INGREDIENTS_DATASET, SYSTEM_PROMPT,
    STORAGE_DIR, load_api_config
)


# Initialize OpenAI API key
def initialize_api_key() -> bool:
    """
    Initialize the OpenAI API key from config or environment.
    
    Returns:
        bool: True if API key is successfully initialized, False otherwise
    """
    if openai is None:
        display_custom_warning("OpenAI module not available. Some features will be disabled.", "Module Missing")
        return False
        
    try:
        config = load_api_config()
        openai.api_key = config['api'].get('openai_key', os.environ.get("OPENAI_API_KEY", ""))
        
        if not openai.api_key:
            display_custom_warning("OpenAI API key not found. Please set it in secrets.toml or as an environment variable.", "API Key Missing")
            return False
        return True
    except Exception as e:
        st.error(f"Error loading API key: {e}")
        return False


def process_image(image_bytes: bytes) -> Dict[str, Any]:
    """
    Process an uploaded image to extract and analyze ingredients.
    
    Args:
        image_bytes (bytes): Raw image bytes
        
    Returns:
        Dict[str, Any]: Results of the analysis
    """
    if openai is None:
        display_custom_warning("OpenAI module is required for image analysis.", "Module Required")
        return {}
        
    try:
        # Extract ingredients from image using GPT-4 Vision
        ingredients_text = extract_ingredients_from_image(
            image_bytes, 
            openai.api_key, 
            OPENAI_API_ENDPOINT, 
            VISION_MODEL, 
            MAX_TOKENS
        )
        
        # Parse the ingredients text
        ingredients_list = parse_ingredients(ingredients_text)
        
        # Load ingredients data
        df = load_ingredients_data(INGREDIENTS_DATASET)
        
        # Create lookup table
        lookup_table = create_lookup_table(df)
        
        # Check halal status
        product_status, unknown_ingredients = check_halal_status(ingredients_list, lookup_table)
        
        # If there are unknown ingredients, query OpenAI
        halal_status_response = None
        if unknown_ingredients and openai is not None:
            halal_status_response = query_openai_about_ingredients(
                unknown_ingredients, 
                openai.api_key, 
                OPENAI_API_ENDPOINT
            )
        
        return {
            "ingredients_text": ingredients_text,
            "ingredients_list": ingredients_list,
            "product_status": product_status,
            "unknown_ingredients": unknown_ingredients,
            "halal_status_response": halal_status_response,
            "lookup_table": lookup_table  # Include the lookup table for comparison
        }
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return {}


def main():
    """Main application function."""
    # Initialize API key and get status
    openai_available = initialize_api_key()
    
    # Setup the page (only title and background)
    setup_page(APP_TITLE, APP_CAPTION, APP_DISCLAIMER, BACKGROUND_IMAGE)

    st.markdown("""
    <style>
    :root { --footer-gap: 120px; }

    /* Use your existing page background; make the main 'card' transparent */
    :where(.stMain, main, section.main) > div.block-container {
    position: relative;
    padding: 2.0rem !important;
    margin-top: 1.25rem !important;
    margin-bottom: 2.0rem !important;

    /* No white background – let your current background show through */
    background: rgba(255, 255, 255, 0.9);

    /* Keep depth but subtle */
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    backdrop-filter: blur(2px); /* optional soft glass; remove if you prefer */
    }

    /* Optional gentle inner glow for structure (still transparent) */
    :where(.stMain, main, section.main) > div.block-container::before {
    content: "";
    position: absolute;
    inset: 0 0 var(--footer-gap) 0;
    border-radius: 16px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.04);
    pointer-events: none;
    }

    /* Ensure content stays above the pseudo background */
    :where(.stMain, main, section.main) > div.block-container > * {
    position: relative;
    z-index: 1;
    }

    /* Typography – keep your current fonts; apply Aclonica only to headings */
    h1, h2, h3, h4 {
    font-family: 'Aclonica', system-ui, -apple-system, Segoe UI, Roboto, sans-serif !important;
    letter-spacing: 0.2px;
    }
    body, p, label, .stMarkdown, .stTextInput, .stRadio, .stButton {
    font-family: inherit; /* keep whatever setup_page already applied */
    }

    /* Footer outside the card */
    .app-footer { margin-top: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)


    
    
    # Welcome message - directly below the title
    st.markdown("""
    <div style="margin-bottom: 20px;">
    <p style="font-size: 1.2em; font-family: 'Aclonica', sans-serif !important;">Welcome to Halal Ingredients Scanner! I can help you check the halal status of food ingredients.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show availability status
    if not openai_available:
        st.markdown("""
        <div style="background-color: rgba(255, 243, 205, 0.4); padding: 20px; border-radius: 5px; border-left: 5px solid #FFD700; margin: 10px 0; color: #551606;">
        <h3 style="color: #551606; margin-top: 0; font-family: 'Aclonica', sans-serif !important;">⚠️ OpenAI API key not configured correctly.</h3>
        
        <p style="color: #551606; font-family: 'Aclonica', sans-serif !important;">To use image analysis and chat features, please configure your OpenAI API key using one of these methods:</p>
        
        <ol style="color: #551606; font-family: 'Aclonica', sans-serif !important;">
            <li>Create a <code>.env</code> file with your API key (copy from .env.template)</li>
            <li>Set the OPENAI_API_KEY environment variable</li>
            <li>Create a <code>secrets.toml</code> file with your API key</li>
        </ol>
        
        <p style="color: #551606; font-family: 'Aclonica', sans-serif !important;">For detailed instructions, see the README_improved.md file.</p>
        </div>
        """, unsafe_allow_html=True)

    # Session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Remove welcome message from chat history as it's displayed separately
        
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    
    # User input section

    #Optional: thin divider after the setup_page title/caption
    st.divider()

    # --- STEP 1 ---
    st.markdown("### 🧭 Step 1 · Choose input method")
    input_method = st.radio(
        "Select one method",
        ["Upload Image", "Paste Ingredient List"],
        horizontal=True,
        index=0,
        help="Pick how you'd like to provide the ingredients"
    )

    # --- STEP 2 ---
    st.markdown("### 🧾 Step 2 · Provide your input")

    uploaded_image = None
    manual_ingredients = None

    col_left, col_right = st.columns([1,1], vertical_alignment="top")

    with col_left:
        if input_method == "Upload Image":
            uploaded_image = st.file_uploader(
                "Upload an image of product ingredients",
                type=["jpg", "jpeg", "png"],
                help="Clear, close-up photo of the full ingredients list"
            )
            st.caption("Limit 200MB • JPG, JPEG, PNG")
        else:
            manual_ingredients = st.text_area(
                "Enter ingredients (comma separated)",
                placeholder="e.g., water, sugar, E471, flavor enhancer (621), spices",
                height=120
            )
            st.caption("Example: *water, sugar, E471, flavor enhancer (621)*")

    with col_right:
        with st.expander("📸 Image tips (recommended)", expanded=False):
            st.markdown(
                "- Crop your image to focus directly on the ingredients list\n"
                "- Include both the **“Ingredients:”** label and the actual list\n"
                "- Ensure names are readable\n"
                "- Use good lighting and avoid glare\n"
                "- Higher resolution images work better"
            )
        with st.expander("🍶 Tips for cylindrical bottles", expanded=False):
            st.markdown(
                "- Take multiple photos if the list wraps around\n"
                "- Rotate the bottle to reduce curvature distortion\n"
                "- Keep the ingredients list centered\n"
                "- Place on a flat surface and rotate toward the camera\n"
                "- Use panorama mode for long wrapping lists"
            )

    # Optional: image enhancement toggle (only when uploading)
    enhance_image = False
    if input_method == "Upload Image" and uploaded_image is not None:
        enhance_image = st.checkbox("Enhance image for better text recognition", value=True)

    # --- STEP 3 ---
    st.markdown("### 🔍 Step 3 · Run analysis")
    run_analysis = st.button("Analyze", type="primary")

    results_container = st.container()

    # === ANALYSIS FLOW (unchanged logic, just gated by the button) ===
    analysis_results = None

    if run_analysis:
        if input_method == "Upload Image" and uploaded_image and openai_available:
            image_bytes = uploaded_image.read()
            image = Image.open(BytesIO(image_bytes))

            if enhance_image:
                from PIL import ImageEnhance, ImageFilter
                enhanced_image = image.copy().filter(ImageFilter.SHARPEN)
                enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(1.5)
                enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(1.2)
                buf = BytesIO(); enhanced_image.save(buf, format="JPEG"); image_bytes = buf.getvalue()

            with st.spinner("Analyzing image..."):
                analysis_results = process_image(image_bytes)
                st.session_state.analysis_results = analysis_results

        elif input_method == "Paste Ingredient List" and manual_ingredients and openai_available:
            with st.spinner("Analyzing ingredients..."):
                ingredients_list = parse_ingredients(manual_ingredients)
                df = load_ingredients_data(INGREDIENTS_DATASET)
                lookup_table = create_lookup_table(df)
                product_status, unknown_ingredients = check_halal_status(ingredients_list, lookup_table)

                halal_status_response = None
                if unknown_ingredients and openai is not None:
                    halal_status_response = query_openai_about_ingredients(
                        unknown_ingredients, openai.api_key, OPENAI_API_ENDPOINT
                    )

                analysis_results = {
                    "ingredients_text": manual_ingredients,
                    "ingredients_list": ingredients_list,
                    "product_status": product_status,
                    "unknown_ingredients": unknown_ingredients,
                    "halal_status_response": halal_status_response,
                    "lookup_table": lookup_table
                }
                st.session_state.analysis_results = analysis_results

        # --- RESULTS RENDERING (reuse your components) ---
        if analysis_results:
            with results_container:
                display_ingredients_text(analysis_results.get("ingredients_text", ""))

                ingredients_list = analysis_results.get("ingredients_list", [])
                lookup_table = analysis_results.get("lookup_table", {})
                if not lookup_table:
                    df = load_ingredients_data(INGREDIENTS_DATASET)
                    lookup_table = create_lookup_table(df)

                if ingredients_list:
                    display_ingredients_comparison(ingredients_list, lookup_table)

                display_halal_status(analysis_results.get("product_status", "Unknown"))

                unknown_ingredients = analysis_results.get("unknown_ingredients", [])
                if unknown_ingredients:
                    display_unknown_ingredients(unknown_ingredients)
                    halal_status_response = analysis_results.get("halal_status_response")
                    if halal_status_response:
                        st.write("Analysis of unknown ingredients:")
                        st.write(halal_status_response)
                    else:
                        display_custom_warning("Detailed analysis of unknown ingredients requires OpenAI API.", "API Required")

                if st.button("Export Results"):
                    export_data = {
                        "Product Status": analysis_results.get("product_status", "Unknown"),
                        "Ingredients": ", ".join(analysis_results.get("ingredients_list", [])),
                        "Unknown Ingredients": ", ".join(unknown_ingredients) if unknown_ingredients else "None",
                        "Analysis": analysis_results.get("halal_status_response", "No detailed analysis available")
                    }
                    create_export_button(export_data)

    # --- SEPARATE CHAT / Q&A SECTION ---
    st.divider()
    st.markdown("### 💬 Ask about ingredients (optional)")
    st.caption("Use this to ask about E-numbers, emulsifiers, or follow-ups after analysis.")
    text_prompt = st.text_input("Type your question…", key="text_input")

    if text_prompt:
        st.session_state.messages.append({"role": "user", "content": text_prompt})
        try:
            with st.spinner("Loading knowledge base..."):
                try:
                    index, gpt_context = load_index_and_context(
                        str(STORAGE_DIR), DEFAULT_MODEL, TEMPERATURE, CONTEXT_WINDOW, SYSTEM_PROMPT
                    )
                    chat_engine = get_chat_engine(index, gpt_context)
                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.write(message["content"])
                    if st.session_state.messages[-1]["role"] != "assistant":
                        with st.chat_message("assistant"):
                            with st.spinner("Thinking..."):
                                response = chat_engine.chat(text_prompt)
                                st.write(response.response)
                                st.session_state.messages.append({"role": "assistant", "content": response.response})
                except ImportError:
                    display_custom_warning("LlamaIndex is not installed. Please install it using: pip install llama-index", "Module Missing")
                    with st.chat_message("assistant"):
                        fallback_response = "I'm sorry, but I can't access the knowledge base right now. Please make sure LlamaIndex is installed."
                        st.write(fallback_response)
                        st.session_state.messages.append({"role": "assistant", "content": fallback_response})
        except Exception as e:
            display_custom_warning(f"Error in chat: {e}", "Error")
            with st.chat_message("assistant"):
                fallback_response = "I'm sorry, but I encountered an error. Please try again later."
                st.write(fallback_response)
                st.session_state.messages.append({"role": "assistant", "content": fallback_response})

        
    # --- FOOTER (outside main container) ---
    display_footer(APP_CAPTION, APP_DISCLAIMER)

    # (Optional) outside credits — remove entirely if you don’t want them
    # st.markdown("""
    # <div class="app-footer" style="
    #     text-align: center;
    #     font-size: 0.8em;
    #     color: rgba(60,60,60,0.6);
    #     margin-top: 0.5rem;
    #     line-height: 1.4;
    # ">
    #   <p>⚙️ <strong>Powered by</strong> LlamaIndex · GPT-3.5-Turbo · GPT-Vision Preview</p>
    #   <p style="font-style: italic; opacity: 0.7;">
    #     Disclaimer: I was created by a being who isn't from MUIS — for pure experimental use only.
    #   </p>
    # </div>
    # """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
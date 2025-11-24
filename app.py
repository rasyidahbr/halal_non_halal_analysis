# Import the required libraries
import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.chat_engine import CondenseQuestionChatEngine
from llama_index.llms import OpenAI
import openai
from llama_index import StorageContext, load_index_from_storage
from PIL import Image
from io import BytesIO
import toml
import requests
import pandas as pd
import base64
import re

################
# Streamlit app layout

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_base64_of_bin_file("snack.jpg")

custom_css = f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Aclonica&display=swap');

/* Apply the Aclonica font to general text elements */
body, [class*="st-"] {{
    font-family: 'Aclonica', sans-serif;
}}

[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
}}

[data-testid="stHeader"] {{
background-color: rgba(0, 0, 0, 0);
}}

</style>
"""

st.title('Halal Ingredient Analysis :fries: :icecream: :pretzel: :popcorn: :cookie:')
st.markdown(custom_css, unsafe_allow_html=True)
st.caption("Halal ingredient analysis powered by comprehensive database and AI")
st.caption("Disclaimer: For educational and experimental use. Consult Islamic scholars for definitive rulings.")
    
#####################

with open('secrets.toml', 'r') as f:
    config = toml.load(f)

# Set OpenAI API key through the streamlit app's secrets
openai.api_key = config['api']['openai_key']#= st.secrets["openai_key"]

# Load the dataset for halal ingredients
df = pd.read_csv('./data/halal_non_halal_ingred.csv')

# Convert all string columns to lowercase and remove spaces
for col in df.columns:
    if df[col].dtype == 'object':  # Check if the column is of string type
        df[col] = df[col].str.lower()

# Function to create a lookup table from the pre-processed DataFrame
def create_lookup_table(df):
    # Use only required columns and create a dictionary for lookup
    lookup_table = df.set_index('ingred_name')['halal_non_halal_doubtful'].to_dict()
    return lookup_table


def parse_ingredients(ingredients_text):
    # Normalize the text
    ingredients_text = ingredients_text.lower().replace("[", "(").replace("]", ")")
    
    # Remove newline characters
    ingredients_text = ingredients_text.replace("\n", ",")

    # Remove the portion starting from "allergen information:"
    ingredients_text = re.sub(r'allergen information:.*|allergen information.*', '', ingredients_text)
    
    # Regular expression to remove everything after "Contains" up to a period or the end of the string
    ingredients_text = re.sub(r'(contains|may contain:).*?(\.|$)', '', ingredients_text)

    # Replace specific phrases
    phrases_to_remove = ["the ingredients listed in the image are:\n\n", "ingredients:", 'the ingredients listed on the image', 
                         "here are the ingredients as listed on the image:\n\n ", "here are the ingredients as listed on the image: ", "are as follows:  -",
                        "the ingredients listed on the image are as follows:\n\n ", "are as follows:", "are:", "the ingredients listed", 
                         "the image shows a list of ingredients", "which includes items like", 
                         "the list is a typical example of ingredients you might find on the packaging of a processed food product",
                         "and it provides important information for consumers about what is in the product as well as potential allergens they should be aware of",
                        "the text also mentions","here are the ingredients exactly as they appear in the image:", "sure", 
                        "here is the list of ingredients exactly as they appear in the image:", "in the image", "the ingredients  are listed as follows:", "on the packaging",
                        "the ingredients exactly as they appear"]
    
    for phrase in phrases_to_remove:
        ingredients_text = ingredients_text.replace(phrase, "")

    # Replace remaining "\n" with ", "
    ingredients_text = ingredients_text.replace("\n", "")
        
    # Replace semicolons with commas
    ingredients_text = ingredients_text.replace(';', ',')
    
    # Remove a full stop at the end if it exists
    ingredients_text = ingredients_text.rstrip('.')
    
    # Replace remaining "-" with ", "
    ingredients_text = ingredients_text.replace("-", "")
    
    # Remove any periods ('.')
    ingredients_text = ingredients_text.replace('.', '')
    
    # Split based on commas not within parentheses
    ingredients = re.split(r',\s*(?![^()]*\))', ingredients_text)
    
    # Strip whitespace from each ingredient
    parsed_ingredients = [ingredient.strip() for ingredient in ingredients if ingredient.strip()]
    return parsed_ingredients


def check_halal_status(ingredients, lookup_table):
    product_halal_status = 'Halal'  # Default status
    unknown_ingredients = []

    for ingredient in ingredients:
        ingredient_lower = ingredient.lower()

        # Check the Halal status from the lookup table
        status = lookup_table.get(ingredient_lower, "Unknown")

        if status == 'Non-Halal' or status == 'Doubtful':  # Non-halal or doubtful
            product_halal_status = 'Non-Halal'
        elif status == "Unknown":
            product_halal_status = 'Doubtful'
            unknown_ingredients.append(ingredient)

    # Return a tuple: product status and list of unknown ingredients
    return product_halal_status, unknown_ingredients

def is_halal(ingredient_list, headers):
    payload = {
        "model": "gpt-3.5-turbo",  # You can choose your preferred model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides information."},
            {"role": "user", "content": f"Determine if the ingredients in '{ingredient_list}' are halal."}
        ]
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        return f"An error occurred: {e}"




# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help?"}]

# User input section
st.write("Please enter your question or upload an image for ingredient analysis.")

# Text input with a unique key
text_prompt = st.text_input("Enter your question", key="text_input")


# Function to encode the image to base64
def encode_image(image_bytes):
    # Directly encode the bytes-like object to base64
    base64_image = base64.b64encode(image_bytes).decode()
    return base64_image

# Initialize user_input
user_input = None

# Image upload
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Process input
if uploaded_image:
    # Read bytes from the uploaded file
    image_bytes = uploaded_image.read()

    # Display the uploaded image
    image = Image.open(BytesIO(image_bytes))
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    st.session_state.messages.append({"role": "user", "content": "Image uploaded"})
    
    # Encode the image to base64
    base64_image = encode_image(image_bytes)

    # ... [Make the API request with base64_image]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"  # Replace with your actual API key
    }

    # Payload for the request
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please provide a list of the ingredients exactly as they appear in the image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 800
    }


    try:
        # Make the API request to OpenAI
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        # Main logic
        if response.status_code == 200:
            response_data = response.json()

            # Extracting the content from the response
            ingredients_text = response_data['choices'][0]['message']['content']

            # Parse the ingredients_text to get the ingredients_list with main and sub-ingredients
            ingredients_list = parse_ingredients(ingredients_text)

            # Creating the lookup table from the pre-processed DataFrame
            lookup_table = create_lookup_table(df)

            # Checking the status of each ingredient
            product_status, unknown_ingredients = check_halal_status(ingredients_list, lookup_table)

            # Print the results
            st.write(ingredients_text)
            st.write("Product Halal Status:", product_status)
            if unknown_ingredients:
                st.write("Unknown Ingredients:", unknown_ingredients)
                halal_status_response = is_halal(unknown_ingredients, headers)
                st.write(f"""Status of {unknown_ingredients}: 
                          {halal_status_response}""")    
        else:
            st.error("Error occurred: " + response.json().get('error', {}).get('message', ''))
        
    except requests.exceptions.RequestException as e:
        if e.response.status_code == 429:
            st.error("Rate limit exceeded. Please try again later.")
            # Log the request ID for further investigation
            st.info("Request ID for support: " + response.headers.get('X-Request-ID', 'Not available'))

            
        else:
            st.error("An error occurred: " + str(e))
            
elif text_prompt:
    user_input = text_prompt
    st.session_state.messages.append({"role": "user", "content": text_prompt})
       
        

# Load and index data
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading – hang tight! This should take 1-2 minutes."):
        # Rebuild the storage context
        storage_context = StorageContext.from_defaults(persist_dir="./storage")

        # Load the index
        index = load_index_from_storage(storage_context)

        # Load the model 
        gpt_context = ServiceContext.from_defaults(llm=OpenAI(model="ft:gpt-3.5-turbo-1106:personal::8TJn8Zjj", temperature=0), context_window=2048, system_prompt="As an expert in halal food certification, your task is to meticulously analyze the ingredients of food products. "
    "A user is looking to determine if a specific food product is halal. "
    "For each ingredient listed in a product, provide a detailed assessment based on the information available in the uploaded documents. "
    "Some ingredients may have different halal statuses depending on their sources or processing methods. "
    "Evaluate each ingredient to determine if it is halal, non-halal, or doubtful. "
    "Consider the source and processing of each ingredient, as this can influence its halal status. "
    "Your goal is to ensure that each ingredient in the product is halal. If any ingredient is non-halal, doubtful, not identifiable, or lacks sufficient information to ascertain its halal status, then the entire food product should be considered non-halal. "
    "Provide a conclusive assessment for each ingredient, thereby determining the overall halal status of the food product.")
        return index, gpt_context

index, gpt_context= load_data()


# Create chat engine
query_engine = index.as_query_engine(service_context=gpt_context)
chat_engine = CondenseQuestionChatEngine.from_defaults(query_engine, verbose=True)

# Display and process chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate response
if user_input and st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(user_input)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)

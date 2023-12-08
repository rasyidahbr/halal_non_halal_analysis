
# Automated Halal Product Identification through Ingredient Analysis


## Background

In an increasingly diverse and globalized food market, ensuring that individuals with specific dietary requirements, such as those adhering to Halal principles, can confidently identify suitable food products remains a significant challenge. The lack of accessible, accurate, and real-time information on the Halal status of various food items poses a barrier to millions of Muslim consumers, especially in non-Muslim countries. This challenge is exacerbated by the complexity of ingredient lists, varying interpretations of Halal standards, and the presence of doubtful or unfamiliar ingredients.
## Problem Statement

Accessing accurate Halal product information is challenging, hindering Muslim consumers' dietary choices. This project aims to develop an automated system that analyzes ingredient lists from product images to determine their Halal status, providing a convenient solution for Halal-conscious consumers in a global food market.
## Objective

- Create a model that can classify food products as halal, not halal, or of uncertain status based on their ingredient lists.
    - Uncertain ingredients will then be checked through OpenAI to determine if the ingredients are halal.

- Enhancing the ability of consumers, especially Muslims, to make informed choices when purchasing food items abroad.
## Success Metrics

- Answer Relevancy
    - Measures how relevant the generated answer is to the question

- Faithfulness
    - Measures how accurate the generated answer, hallucinated or factuality
## Data

- The halal food data utilized is sourced from the MUIS website, and this information is also employed in the backend processing of GPT 3.5 Turbo.
    - [MUIS: Food and Drinks Categories](https://www.muis.gov.sg/halal/Religious-Guidelines/Food-and-Drinks-Categories)
    - [MUIS: Food Selection](https://www.muis.gov.sg/halal/Religious-Guidelines/Food-Selection)
    - [MUIS: Food Preparation](https://www.muis.gov.sg/halal/Religious-Guidelines/Food-Preparation)    


- the `halal_non_halal_ingred.csv` ingredient list is consolidated from:-
    - [MUIS: Food Additive List](https://www.muis.gov.sg/-/media/Files/Halal/Documents/FOOD-ADDITIVE-LISTING-5.ashx)
    - [World of Islam Food Numbers](https://special.worldofislam.info/Food/numbers.html)
    - [Islamcan.com](https://islamcan.com/blog/2020/01/halal-and-haram-ingredient-database/)

## Project Workflow

1. **Gathering Ingredient Data**
- **Goal**: Collect comprehensive data on ingredients, categorized into halal, non-halal, and uncertain groups.

2. **Capturing Label Images**
- **Approach**: Photograph labels of products to capture detailed ingredient information.

3. **Extracting Text from Images**
- **Technique**: Use image text recognition technology to identify and document ingredients from images.

4. **Verifying Ingredient's Halal Status**
- **Method**:
  - Cross-reference ingredients with an established list.
  - Determine and report halal status:
    - Label as "Halal" if ingredients match the halal category.
    - Note as doubtful or non-halal based on list categorization.

5. **Handling Ingredients Not in List**
- **Tactic**:
  - Utilize the OpenAI model for assessing the halal status of unlisted ingredients.
  - Announce the determined status for these ingredients.

6. **System Backend Enhancement**
- **Actions**:
  - Improve the system's precision and functionality through backend development.

7. **Chat Model Refinement**
  - Tailor the chat model for enhanced handling of halal ingredient-related queries.
## Conclusion

**Effective in Simple Ingredient Detection:** 
- performs efficiently in identifying basic ingredients, 
- Effective in simpler scenarios of ingredient analysis.

**Optimal Model Performance:**
- Gpt-3.5-turbo-1106
- Formulation of prompts, a pivotal role in influencing model performance

### Future Developments

**Streamlining Phrase Recognition:** 
- Opting for an efficient module to eliminate unwanted phrases streamlines ingredient extraction

**Detailed Analysis of Sub-Ingredients:** 
- Enhancing halal status determination requires analyzing both main and sub-ingredients for a comprehensive understanding of ingredient lists

** Refining Halal Status Determination**

**Ongoing Model Improvement:**

**Incorporating User Feedback:**




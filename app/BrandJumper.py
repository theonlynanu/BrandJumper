import os
import openai
import argparse
import re
from typing import List

openai.api_key = os.getenv("OPENAI_API_KEY")

#Checks if input is short enough
max_input_length = 14

# Gathers user input using 'python ###.py -i "{input}"' 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type = str, required=True)
    args = parser.parse_args()
    user_input = args.input
    
    #Validates length of input and throws error if too long
    if validate_length(user_input):
        generate_brand_name(user_input)
        generate_tagline(user_input)
    else:
        raise ValueError(f"Input length must be under {max_input_length} characters. Submitted input is '{user_input}'")

def validate_length(prompt: str) -> bool:
    return len(prompt) <= max_input_length

# Generates branding snippet using user input defined in main()
def generate_brand_name(prompt:str) -> List[str]:
    # Specifies request for OpenAI completion, informed by fake brand names
    enriched_prompt = f"""Generate five novel brand names for a web product.
    
    Product: product roadmap
    Names: Visboard, Roadahead, MyChart, PlanIt, ProductMapper
    
    Product: video editing
    Names: SceneSetter, Archimedes, Filmagic, EditTime, FrameFix
    
    Product: spell checking
    Names: Hemingway, WordFixer, Syntactics, Perfect Essay, EZ Spell
    
    Product: domain hosting
    Names: .yes, DomainSqueeze, BigURL, Web Booker, SiteFinder
    
    Product:{prompt}
    Names: """

    # Creates response variable based on davinci engine.
    response = openai.Completion.create(
        engine="text-davinci-002", prompt = enriched_prompt, max_tokens = 32, temperature = 1
    )
    
    # Extracts text from OpenAI response and strips two lines of whitespace
    brand_names: str = response["choices"][0]["text"].strip()
    
    # Uses regex to split names into list
    dirty_array = re.split(",|\n|-|;", brand_names) #The prompt method should restrict delimiters to commas, but temp of 1 occasionally throws dashes or line breaks
    
    # Cleans whitespace and removes empty entries from array.
    names_array = [name.strip() for name in dirty_array]
    names_array = [name for name in names_array if len(name) > 0]
    
    print(f"Names: {names_array}")
    return names_array

#Generates tagline for product using same user input as brand name
def generate_tagline(prompt:str):
    # Specifies prompt for OpenAI Completion
    enriched_prompt = f"Generate a tagline for a {prompt} brand: "
    # Creates response variable based on davinci engine
    response = openai.Completion.create(
        engine="text-davinci-002", prompt = enriched_prompt, max_tokens = 32, temperature = .6
    )
    
    # Extracts text output and strips whitespace
    tagline = response["choices"][0]["text"].strip()

    # Appends ellipses if prompt is truncated due to token limit
    if tagline[-1] not in [".", "!", "?"]:
        tagline += "..."
        
    print(f"Tagline: {tagline}")    
    return tagline

if __name__ == "__main__":
    main()
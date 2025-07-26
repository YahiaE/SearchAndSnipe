import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv("D:/Projects/SearchAndSnipe/backend/gemini-deal-agent/.env")

genai.configure(api_key=os.getenv("GEMINI_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

user_input = input("Enter a description of what product you would like to search for (type, price, features): ")

prompt = f'''From the following request, extract:
- `product`: the main item the user wants
- `max_price`: the upper limit of what they’re willing to spend (number only, optional)
- `features`: list of any features, brands, styles, or priorities mentioned

Return only valid JSON in this format:
{{
  "product": "string",
  "max_price": "number or null",
  "features": ["string"]
}}

Example:
Input: "I want a comfortable office chair under 200 dollars, preferably mesh with lumbar support."

Output:
{{
  "product": "office chair",
  "max_price": 200,
  "features": ["mesh", "lumbar support", "comfortable"]
}}

Now process this input:
"{user_input}"
'''

response = model.generate_content(prompt)

print(response.text)

from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import time
import os
# client = OpenAI(api_key = "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")

# Load API key from the environment file, if available



app = Flask(__name__)

prompt_v2 = '''## Recipe Creation

As an expert in recipe development, your task is to guide users in creating delicious recipes. Your objective is to craft a straightforward recipe, detailing precise ingredient quantities and offering clear, step-by-step cooking instructions. Your guidance should include specific frying or boiling times to ensure users can easily follow along. Keep your instructions simple and clear for optimal understanding.

**Output Format:** To ensure consistency across all recipes, format your instructions using Markdown. Make sure to start by naming the dish. This format will help maintain uniformity in each recipe's presentation.'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            response = generate_response(user_input)
            return render_template('index.html', user_input=user_input, response=response)
        
        # Handle API key submission from the popup
        submitted_api_key = request.form.get('api_key')
        if submitted_api_key:
            save_api_key(submitted_api_key)
            return render_template('index.html', user_input='', response=None)

    return render_template('index.html', user_input='', response=None)

def save_api_key(api_key):
    # Save the API key to the environment file (e.g., .env)
    print('save', api_key)
    with open('.env', 'w') as env_file:
        env_file.write(f'OPENAI_API_KEY={api_key}')

def generate_response(input_text):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    print('api key', api_key)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": prompt_v2
        },
        {
        "role": "user",
        "content": f"You will focus on utilizing the following ingredients: {input_text}"
        },
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    print(response)
    return response.choices[0].message.content
    # time.sleep(5)
    # return '''# Perfectly Peppered Steak\n\n## Ingredients:\n- 2 8-ounce beef steaks \n- 2 teaspoons black pepper \n- 1 teaspoon salt \n- 1 tablespoon olive oil \n- 2 cloves garlic, minced \n- 2 tablespoons butter \n\n## Instructions:\n\n1. **Prepare the Steaks:**\n   - Take the beef steaks out of the refrigerator and let them come to room temperature for about 30 minutes.\n   - Pat the steaks dry with paper towels and season both sides with salt and black pepper.\n\n2. **Sear the Steaks:**\n   - Heat the olive oil in a skillet over medium-high heat.\n   - Once the oil is hot, add the steaks to the skillet and sear for 4-5 minutes on each side for medium-rare doneness. Adjust the time based on your preferred level of doneness.\n\n3. **Add Flavor:**\n   - In the last minute of cooking, add the minced garlic and butter to the skillet.\n   - Baste the steaks with the garlic butter sauce for added flavor.\n\n4. **Rest and Serve:**\n   - Remove the steaks from the skillet and let them rest for about 5 minutes.\n   - Slice the steaks'''


if __name__ == '__main__':
    app.run(debug=True)

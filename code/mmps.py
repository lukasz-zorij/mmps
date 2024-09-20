# Author: Lukasz Zorij
# Date: 09/20/2024
# 
# This code is free to use, but please include the source and copyright information.
# Copyright (c) 2024 Lukasz Zorij. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.


import logging
import re
import hashlib
import datetime
from openai import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain_core.prompts import PromptTemplate
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

API_KEY = "sk-"   # Replace with your actual API key

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=API_KEY)

# Define the system message
SYSTEM = "You are an expert in solving problems and analysis. Use pseudo code to describe functionality and logic to developer working in any computer languge."

# Variable to control DEBUG logging
DEBUG = True

def setup_logging(user_prompt):
    # Generate a unique log file name based on the SHA256 hash of the user prompt and current time and date
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hash_object = hashlib.sha256((user_prompt + current_time).encode())
    log_filename = f"job_{hash_object.hexdigest()}.log"
    
    # Set up logging to the unique log file
    logging.basicConfig(
        filename=log_filename, 
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging setup complete.")
    logging.info(f"User prompt: {user_prompt}")

class Memory:
    def __init__(self):
        self.layers = {1: [], 2: [], 3: [], 4: [], 5: []}
    
    def store(self, layer, data):
        self.layers[layer].append(data)
        logging.debug(f"Storing data in layer {layer}: {data}")
    
    def retrieve(self, layer):
        data = self.layers[layer]
        logging.debug(f"Retrieving data from layer {layer}: {data}")
        return data

def call_openai_model(messages, model="gpt-4o-mini", max_tokens=100, temperature=0.5):
    logging.info(f"Calling model '{model}' with parameters: max_tokens={max_tokens}, temperature={temperature}")
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    result = completion.choices[0].message.content.strip()
    logging.info(f"Received response: {result}")
    return result

def extract_keywords(user_prompt, temperature, max_tokens):
    task_prompt = f"Given the user's input: '{user_prompt}', extract 5 keywords or phrases and provide a one-sentence description for each."
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": task_prompt}
    ]
    return call_openai_model(messages, model="gpt-4o-mini", max_tokens=max_tokens, temperature=temperature)

def analyze_keywords(user_prompt, keywords, temperature, max_tokens):
    task_prompt = f"User's input: '{user_prompt}'. Analyze each keyword: {keywords}. Explain how it relates to solving the problem."
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": task_prompt}
    ]
    return call_openai_model(messages, model="gpt-4o-mini", max_tokens=max_tokens, temperature=temperature)

def generate_keyword_pairs_correlation(user_prompt, analyses, temperature, max_tokens):
    task_prompt = f"Based on user's input: '{user_prompt}', create pairs of keywords from the analyses: {analyses}. Explain how each pair relates to the problem."
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": task_prompt}
    ]
    return call_openai_model(messages, model="gpt-4o-mini", max_tokens=max_tokens, temperature=temperature)

def synthesize_pair_relations(user_prompt, correlations, temperature, max_tokens):
    task_prompt = f"Taking into account the user's input: '{user_prompt}', synthesize and mix the following correlations into a unified explanation: {correlations}. Do not include any code just information how to solve problem."
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": task_prompt}
    ]
    return call_openai_model(messages, model="gpt-4o-mini", max_tokens=max_tokens, temperature=temperature)

def summarize_all(user_prompt, memory, temperature, max_tokens):
    layer_3_answers = memory.retrieve(3)
    layer_4_answers = memory.retrieve(4)
    combined = ' '.join(layer_3_answers + layer_4_answers)
    task_prompt = f"With the user's input in mind: '{user_prompt}', summarize the following information into a final, comprehensive response: {combined}. Do not include any code just information how to solve problem, remove duplicates."
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": task_prompt}
    ]
    return call_openai_model(messages, model="gpt-4o", max_tokens=max_tokens, temperature=temperature)

def gpt4o_score(user_prompt, responses):
    combined_responses = "\n".join([f"Response {i+1}: {response}" for i, response in enumerate(responses)])
    scoring_prompt = (f"Use scoring technique from 1-10 (Output only score nothing more just numeric value without any comments and additional information - use csv to show rate of response in order like in this prompt) to get best answer related (best value to solve the user's problem in proposed way) with user's prompt. "
                      f"Evaluate the following responses:\n\nUser's input: '{user_prompt}'\n\n{combined_responses}")
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": scoring_prompt}
    ]
    logging.info(f"Scoring prompt: {scoring_prompt}")
    score_response = call_openai_model(messages, model="gpt-4o", max_tokens=20, temperature=0.0)
    logging.info(f"Model output (scoring): {score_response}")
    try:
        scores = [float(score) for score in re.findall(r'\b\d+\b', score_response)]
        if any(score < 1 or score > 10 for score in scores):
            raise ValueError("Score out of range")
    except (ValueError, IndexError):
        scores = [0] * len(responses)
    scores_csv = ','.join(str(score) for score in scores)
    logging.info(f"Scores in CSV format: {scores_csv}")
    best_response, best_score = sorted(zip(responses, scores), key=lambda x: x[1], reverse=True)[0]
    logging.debug(f"Best scored response: {best_response} with score: {best_score}")
    return best_response, best_score

def main():
    user_prompt = input("Enter your main prompt: ")
    setup_logging(user_prompt)
    logging.debug(f"Received user prompt: {user_prompt}")
    memory = Memory()

    with ThreadPoolExecutor() as executor:
        futures = []
        for i in tqdm(range(3), desc="Processing", disable=not DEBUG):  # Perform the loop 3 times
            temperature = 0.3 + i * 0.2
            max_tokens = 100 + i * 200
            final_tokens = 2000
            logging.info(f"Step {i+1}: Extracting keywords with temperature {temperature} and max_tokens {max_tokens}")
            futures.append(executor.submit(extract_keywords, user_prompt, temperature, max_tokens))
            logging.info(f"Step {i+1}: Analyzing keywords")
            futures.append(executor.submit(analyze_keywords, user_prompt, futures[-1].result(), temperature, max_tokens))
            logging.info(f"Step {i+1}: Generating keyword pairs correlation")
            futures.append(executor.submit(generate_keyword_pairs_correlation, user_prompt, futures[-1].result(), temperature, max_tokens))
            logging.info(f"Step {i+1}: Synthesizing pair relations")
            futures.append(executor.submit(synthesize_pair_relations, user_prompt, futures[-1].result(), temperature, max_tokens))
            logging.info(f"Step {i+1}: Summarizing all information")
            futures.append(executor.submit(summarize_all, user_prompt, memory, temperature, final_tokens))

        for future in futures:
            result = future.result()
            memory.store(futures.index(future) % 5 + 1, result)

    # Use GPT-4o to score the final responses
    final_answers = memory.retrieve(5)
    logging.info("Scoring final responses")
    best_answer, best_score = gpt4o_score(user_prompt, final_answers)
    # Print the best score before the best answer
    print(f'Best Score: {best_score}\n')
    # Print the best scored answer
    print(f'Do not simplify anything it is waste of time.\nCompare with original functionality.\nDo not explain, just generate full code in one shot. \nUse exactly how and what is in that instructions and requirements to implement it in best way, fully working solution.\n"""{best_answer}"""')
    logging.debug(f"Final best answer: {best_answer} with score: {best_score}")

if __name__ == "__main__":
    main()
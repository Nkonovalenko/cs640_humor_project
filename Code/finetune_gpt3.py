'''
This file is part of the semester project for CS 640 at Boston University.
It is for experiments to further investigate claims in the paper "Do Androids Laugh at Electric Sheep",
through several experiments:
    1) Fine Tuning GPT-3 on a set of New Yorker Caption Contest Captions, to have it describe the setting/joke where those captions would be a punchline
        Status: Manually creating dataset for the fine-tuning
    2) Running idioms through GPT-3 to see whether it can explain what those idioms mean
        Status: Completed
    3) Feeding the output of the GPT-3 explanations of idioms, into DALL-E 2, to see whether generative models could understand deeper topics in humor (such as idioms)


Idioms from: https://github.com/jbrew/idiomash/blob/master/text/idioms.txt
New Yorker Captions from: https://github.com/nextml/caption-contest-data/blob/gh-pages/nyccwinners/nyc_winners.json
'''
import json

import os
import openai

import secret


# Load your API key from an environment variable or secret management service
openai.api_key = secret.SECRET_API_KEY
model = None

FINETUNED = ""

# Function to parse the captions JSON
caption_pairs = {}
def parse_captions():
    with open('./Data/nycwinners.json') as caption_file:
        caption_winners = json.load(caption_file)

    for contest in caption_winners:
        contest = contest['data']
        title = contest['cartoon']['title']

        finalists = contest['cartoon']['contestFinalists']

        final_captions = [finalists[caption_num]['text'] for caption_num in range(len(finalists))]

        caption_pairs[title] = final_captions

# Dictionary tracking prompt keys to GPT-output values
prompt_response = {}
def request(prompt, FINETUNED):

    if (FINETUNED):
        model = FINETUNED
    else:
        model = "text-davinci-002"

    # Make the request to GPT-3 given a prompt
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    # Extract the text
    response_text = response['choices'][0]['text']

    # Add to dictionary
    prompt_response[prompt] = response_text


idioms = []
def parse_idioms():
    idioms_file = open('Data/idioms.txt', 'r')

    for line in idioms_file.readlines():
        line = line.replace('\n', "")

        if line:
            idioms.append(line)

def save_meanings(start_index, end_index, idiom_meanins):
    filename = 'idiom_meanings_' + str(start_index) + '_' + str(end_index) + '.txt'

    with open(filename, 'w') as output_file:
        output_file.write(json.dumps(idiom_meanings))

parse_idioms()

idiom_meanings = {}
def gpt_idioms(start_index, end_index):
    for index in range(start_index, end_index):
        # Create the prompt
        prompt = "What does it mean to be " + idioms[index]

        # Make request to GPT-3 API
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1,
        )

        response_text = response['choices'][0]['text']

        # Store the text response in dictionary
        idiom_meanings[prompt] = response_text

        # Write the dictionary to text file
        save_meanings(start_index, end_index, idiom_meanings)

        # Output for debugging
        print("Prompt: ", prompt)
        print("Response: ", response_text)
        print('--------')

'''
#################################################################################
#################################################################################
|                                                                               |
|                             Task 1: Captions                                  |
|                                                                               |
#################################################################################
#################################################################################
'''

'''
    This section is still in progress. Manually creating a dataset that GPT can be fine tuned with.

    Tried to get GPT to tell jokes with the captions being punch lines, however this fails:

    Prompt:  Tell a joke about Yeah, I hate the throwback uniforms, too.
    Response:

    Why did the chicken cross the road?

    To get to the other side.
'''


captions = True

if captions:
    parse_captions()

    start_index = 10
    end_index = 12


    for index in range(start_index, end_index):
        contest = list(caption_pairs)[index]
        for caption in caption_pairs[contest]:
            prompt = "Give a funny scenario for " + caption[1:-1]

            response = openai.Completion.create(
                model="text-davinci-002",
                prompt="""Give a funny scenario for. 
                prompt: Give a funny scenario for First you must gain their trust.
                completion: A man wearing a full body mouse costume and writing on a clipboard is standing next to another man in a lab coat. The men are surrounded by cages that are full of rats.Two scientists are talking in a lab, with a cage full of mice off to the left. One of the scientists is dressed like a rat.A man dressed as a giant rat is checking the mice in the cages. A scientist looks on.
                ###
                prompt: Give a funny scenario for Frank called to say he'll be late, he's stuck at the office.
                completion: An office meeting is taking place inside a subway cart. Everyone at the meeting is acting like this is normal.Men are sitting around a table. But the table is in the subway.A group of businesspeople are having a meeting in a subway car. They are talking to a CEO.
                ###
                prompt: Give a funny scenario for This better be good. That floor was waxed last night!"
                completion: A dirty man crawls on the ground towards a group of people sitting down. They are looking at him in astonishment with a sign above them that says \"Emergency Hotline\".A dirty exhausted man is crawling toward an emergency hotline booth. One of the operators is yelling at him.A man is on the floor and he is very dirty. An emergency hotline sign is up on the wall. A woman is yelling at the man on the floor."
                ###
                prompt: Give a funny scenario for Remember that time you made me laugh and people came out of my nose?
                completion":Two large reptile monsters are destroying a whole city. One of them looks happily at the other as it eats.Two monsters are rampaging through a city. They're eating the buildings.Two dinosaurs are devouring a city. One is gobbling up a building
                """+prompt,
                temperature=0.6,
                max_tokens=150,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1,
                )
            response_text = response['choices'][0]['text']
            print("Prompt: ", prompt)
            print("Response: ", response_text)
            print('-------')

    # response = openai.Image.create(
    #     prompt="a white siamese cat",
    #     n=1,
    #     size="1024x1024"
    # )
    # image_url = response['data'][0]['url']

'''
#################################################################################
#################################################################################
|                                                                               |
|                              Task 2: IDIOMS                                   |
|                                                                               |
#################################################################################
#################################################################################
'''
run_idioms = False
if (run_idioms):
    # First we need to parse the idioms
    parse_idioms()

    start_index = 100
    end_index = 200

    # Make requests to GPT
    gpt_idioms(start_index, end_index)



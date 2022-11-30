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

captions = False  
make_text = True ## generate gpt3 outputs
length = 35      ## how many shots learning
start = 50
end = 70
## declare test range, from 50 to ~


if captions:
    ############################### generate text ######################
    if make_text:
        f=open('./Data/cleaned2.json')
        cleaned = json.load(f)
        fewshots =""""""
        for i in range(length): 
            fewshots+="""prompt: """;
            fewshots+=cleaned['info'][i]['prompt']
            fewshots+=""" completion: """
            fewshots+=cleaned['info'][i]['completion']
            if(i<length-1) : fewshots+=""" ### """

        res = []
        for index in range(start, end):
            prompt = "Give a funny scenario for " + cleaned['info'][index]['prompt']
            # print("""Give a funny scenario. ### """+fewshots+prompt)
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt= prompt if length==0 else """Give a funny scenario. ### """+fewshots+prompt,
                temperature=0.6,
                max_tokens=150,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1,
                )
            response_text = response['choices'][0]['text']
            content = {"prompt":prompt, "completion":response_text}
            res.append(content)

        if length == 0:   
            with open('./Results/gpt_results_0shots.json', "w") as file:
                file.write('{'+'"'+"info" +'"'+':'+ '[')
                for i in range(len(res)):
                    file.write(json.dumps(dict(res[i])))
                    if i<len(res)-1: file.write(","+"\n")
                file.write(']'+'}')
        elif length == 5:
            with open('./Results/gpt_results_5shots.json', "w") as file:
                file.write('{'+'"'+"info" +'"'+':'+ '[')
                for i in range(len(res)):
                    file.write(json.dumps(dict(res[i])))
                    if i<len(res)-1: file.write(","+"\n")
                file.write(']'+'}')
        else:
            with open('./Results/gpt_results_50shots.json', "w") as file:
                file.write('{'+'"'+"info" +'"'+':'+ '[')
                for i in range(len(res)):
                    file.write(json.dumps(dict(res[i])))
                    if i<len(res)-1: file.write(","+"\n")
                file.write(']'+'}')

    ############################### text to image ######################
    if length ==0:
        f=open('./Results/gpt_results_0shots.json')
    elif length==5:
        f=open('./Results/gpt_results_5shots.json')
    else: 
        f=open('./Results/gpt_results_50shots.json')
    gptres = json.load(f)
    dalle_res = []
    for key in gptres['info']: 
        # print("key: "+key['completion'])
        response = openai.Image.create(
            prompt=key['completion'],
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        content = {"prompt":key['prompt'],"url":image_url}
        dalle_res.append(content)
    if length == 0: 
        with open('./Results/dalle_results_0shot.json', "w") as file:
            for elem in dalle_res:
                file.write(json.dumps(dict(elem)))
                file.write(","+'\n')
    elif length==5:
        with open('./Results/dalle_results_5shot.json', "w") as file:
            for elem in dalle_res:
                file.write(json.dumps(dict(elem)))
                file.write(","+'\n')
    else:
        with open('./Results/dalle_results_50shot.json', "w") as file:
            for elem in dalle_res:
                file.write(json.dumps(dict(elem)))
                file.write(","+'\n')

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



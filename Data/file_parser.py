import json

# Generate file for finetuning. Match caption to their descriptions
def file_generator1():
    f=open('./Data/all_newyorker_contest_annotations.json')
    data = json.load(f)
    cleaned =[]
    for key in data:   
        if(data[key]['official_newyorker_finalists']==[]):
            continue  
        contest = {
            "prompt":"Tell a joke about "+str(data[key]['official_newyorker_finalists'][0]).encode('ascii', 'ignore').decode('unicode_escape').strip('"\"'),
            "completion": data[key]['mturk_annotations']['description_hit'][0]['image_description']+data[key]['mturk_annotations']['description_hit'][1]['image_description']+data[key]['mturk_annotations']['description_hit'][2]['image_description']
        }
        cleaned.append(contest)
    with open('./Data/cleaned.json', "w") as file:
        for elem in cleaned:
            file.write(json.dumps(dict(elem)))
            file.write('\n')

# Generate file for human evaluation. Match contest number to caption and descriptions.
def file_generator2():
    f=open('./Data/all_newyorker_contest_annotations.json')
    data = json.load(f)
    cleaned =[]
    for key in data:   
        if(data[key]['official_newyorker_finalists']==[]):
            continue  
        contest = {
            "contest_number": data[key]['contest_number'],
            "prompt":"Tell a joke about "+str(data[key]['official_newyorker_finalists'][0]).encode('ascii', 'ignore').decode('unicode_escape').strip('"\"'),
            "completion": data[key]['mturk_annotations']['description_hit'][0]['image_description']+data[key]['mturk_annotations']['description_hit'][1]['image_description']+data[key]['mturk_annotations']['description_hit'][2]['image_description']
        }
        cleaned.append(contest)
    with open('./Data/cleaned2.json', "w") as file:
        for elem in cleaned:
            file.write(json.dumps(dict(elem)))
            file.write('\n')

file_generator1()
file_generator2()

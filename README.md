# cs640_humor_project
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

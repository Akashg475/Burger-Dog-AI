# Burger-Dog-AI
This project implements an AI Player using Deep Reinforcement Learning for the game Burger Dog

***

## Instructions

### Step 1:
    Clone/Download the respository in your system

### Step 2:
Run the command in terminal

    pip install -r requiremets.txt

### Step 3:
To play the game: run the following command

    python human.py
To train a new agent: edit the agent name you want to train in train.py (line 2)

The new agent is saved in *trained_models/*

    Possible_Agents = ["A2C", "DQN", "PPO", "ARS", "MaskablePPO", "QRDQN", "TRPO"]
    AGENT_NAME = "A2C"


Run the following command in terminal

    python train.py




To watch your trained agent play the game: 

Change the agent name in enjoy.py (line 2)

    Possible_Agents = ["A2C", "DQN", "PPO", "ARS", "MaskablePPO", "QRDQN", "TRPO"]
    AGENT_NAME = "A2C"

Change "trained_models" to "final_trained_models" in line 26 to enjoy pre-trained agents

run the following command

    python enjoy.py

#
## Benchmarks
These agents were trained for same number of episodes. The score is the average over 100 games.
<table>
    <tr>
        <th> Name </th>
        <th> Score </th>
    </tr>
    <tr>
        <td> A2C </td>
        <td> 3492.78 </td>
    </tr>
    <tr>
        <td> ARS </td>
        <td> 4172.58 </td>
    </tr>
</table>
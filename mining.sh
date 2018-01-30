#!/bin/bash

python recursive.py past/ q_past.csv ori_past.csv technology

python recursive.py present/ q_present.csv ori_present.csv technology

python cosine_sim.py q_past.csv q_present.csv 

python random_walk.py out_past.txt out_present.txt out_layer.txt

python result.py Score_layer_1.txt ori_past.csv
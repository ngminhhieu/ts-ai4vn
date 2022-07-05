#!/bin/bash

rm competition.zip

zip -j scoring_program.zip ./scoring_program/*.py
zip -j scoring_program.zip ./scoring_program/metadata

zip -j public_ground_truth.zip ./data/public/gt.csv
zip -j private_ground_truth.zip ./data/private/gt.csv

zip -j competition.zip html/award.html html/data.html html/evaluation.html html/overview.html html/submission.html html/terms.html
zip -j competition.zip competition.yaml scoring_program.zip public_ground_truth.zip private_ground_truth.zip
zip -j competition.zip logo/logo.svg

rm public_ground_truth.zip
rm private_ground_truth.zip
rm scoring_program.zip
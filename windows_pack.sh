rm competition.zip

7z a scoring_program.zip ./scoring_program/*.py
7z a scoring_program.zip ./scoring_program/metadata

7z a public_ground_truth.zip -i!./data/public/*/*.csv
7z a private_ground_truth.zip -i!./data/private/*/*csv

7z a competition.zip ./html/award.html ./html/data.html ./html/evaluation.html ./html/overview.html ./html/submission.html ./html/terms.html
7z a competition.zip competition.yaml scoring_program.zip public_ground_truth.zip private_ground_truth.zip
7z a competition.zip ./logo/logo.png

rm public_ground_truth.zip
rm private_ground_truth.zip
rm scoring_program.zip
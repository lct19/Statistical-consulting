# Statistical consulting project

I developed the analysis program for the statistical consulting course Leiden university 2022-2023. 

This study aims to explore the relationship between disinformation tweets with some linguistic features: negations, conjunctions, first-person pronouns, and some words related to sense, causal and cognitive. Also, we investigate the potential differences of these relationships in 4 different languages of Twitter communities. To achieve this goal, we present nine hypotheses based on the findings stated in previous literature. First, it assumes that the proportion of tweets that contain Negations (H1), Refs to self (H2), Conjunctions (H3), Other conjunctions (H4), Initial conjunction (H5), Levelers (H6), Sense words (H7), Causal words (H8), and Cognitive words (H9) are different between disinformation and information groups. Then, we compare the rejected hypotheses for the tweets in four languages: English, Italian, French, and Dutch. Due to the number of observations and subjectivity of fact-checking, the biggest challenge we face is measuring the inaccurate feature indicators in our argument.

## umc module

The umc module is the module I developed for statistical data analysis. The main methods used here are the group comparison method(https://doi.org/10.1007/s11336-021-09794-x) and holm's sequential procedure (https://www.jstor.org/stable/4615733). It works as a self-defined module in Python.

## simulation

Several simulations are performed to illustrate when the negative estimates of variance occur, and the corrected uncertain-t-test works well for this study. The basic idea is that we first generate a dataset containing two columns: feature indicator and group indicator. The feature indicator measures whether an observation includes a feature (1) or not (0), and the group indicator stands for its group membership. This 'correct' dataset is given to the t-test as a control. Then, given the accuracy vector (acc 1, acc 2) (acc 1 for feature indicators, and acc 2 for group indicators), We can generate an 'inaccurate' dataset with some misclassifications. This 'inaccurate' dataset and the corresponding accuracy are given to the corrected uncertain-t-test. At last, the accuracy vector added by noise and the 'inaccurate' dataset is given to the corrected uncertain-t-test. This one is labeled as an "estimate" uncertain-t-test, which simulates that we only have an estimate of the probabilities of a group membership.

## real data analysis

This Jupiter notebook shows results after applying the umc module to the actual dataset. The original dataset is provided by Prof. Matthijs Westera (https://mwestera.humanities.uva.nl/index.shtml). Note that the data is not included for privacy reasons.

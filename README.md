# Statistical-consulting

Here is the analysis program that I developed for statistical consulting course, Leiden university 2022-2023. 

In this project, I would like to use a group comparison test proposed by Bauer, T.A. et al. to test the difference of a certain feature between fake and non-fake tweets. Then, The Holm method was used to counteract the problem of multiple comparisons. To be specific, I first want to know if there are different linguistic characteristics between disinformation and information in tweets related to COVID-19. Second, I will compare the results for four languages, including English, French, Italian and Dutch. Due to the number of observations and subjectivity of fact-checking, the biggest challenge is how to take into account the inaccuracy of the label truth or liars and the inaccuracy of linguistic features in our argument.

## umc module
The umc module is the module I developed for real data analysis. Main methods used here are group comparison method(https://doi.org/10.1007/s11336-021-09794-x) and holm's squential procedure (https://www.jstor.org/stable/4615733).

## simulation
Power test of the group comparison method.

## real data analysis
Applied the module to the our project.

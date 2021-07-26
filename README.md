# so-analysis
StackOverflow Survey 2020 - Job Satisfaction Analysis

### Table of contents
1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

This should run by default with Anaconda installation with python 3.x. Requires Jupyter Lab/Notebook. 

The StackOverflow survey data is not pushed in this repository. To run the notebooks these steps.

1. Download StackOverflow survey ([https://insights.stackoverflow.com/survey/](https://insights.stackoverflow.com/survey/))
2. Unzip and place the raw data under the folder `data/raw`. Extracted files are `survey_results_public.csv` and `survey_results_schema.csv`.
3. Run `notebook/01-so-clean.ipynb` to generate processed clean data.

You are ready to explore `notebook/02-so-eda.ipynb` or read `docs/satisfaction.md` for my analysis.

## Project Motivation<a name="motivation"></a>

This project aims to explore the things a company could do to satisfy IT employees. With this, I'm interested with the StackOverflow Survey 2020 dataset to better understand:

1. What do the respondents think as the perfect IT company?
2. Is salary or languages/technologies/frameworks effective enough to solve job satisfaction issues?
3. What other hidden factors that affects job satisfaction?


## File Descriptions <a name="files"></a>

There 2 notebooks in this project. The `01-so-clean.ipynb` contains basic cleaning and column renaming while `02-so-eda.ipynb` contains the analysis needed to answer the questions. Utility python codes are located at `src`.


## Results<a name="results"></a>

Main findings are located at `docs`.

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

MIT License.
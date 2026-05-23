# Text Authorship Classifier

A Python text-analysis project for comparing writing styles and classifying unknown texts by likely source author.

## Overview

This project builds simple statistical models of texts using several writing-style features, then compares an unknown text against two known source models.

The classifier uses log similarity scores to determine which source text the unknown text more closely resembles.

## Features

- Counts word frequencies
- Counts word-length frequencies
- Applies a simple custom stemming function
- Counts sentence-length patterns
- Counts coordinating/subordinating conjunctions
- Compares unknown texts against source texts
- Reports which source is the closer stylistic match

## Text Features

The model tracks:

- Words
- Word lengths
- Word stems
- Sentence lengths
- Conjunction usage

## How to Run

```bash
python text_authorship_classifier.py
```
To use your own files, place `.txt` files in the same folder and update the filenames in the `run_tests()` function.

## Skills Demonstrated
* Python scripting
* Text pre-processing
* Dictionary-based frequency modeling
* Similitary scoring
* Authorship attribution
* Basic computational linguistics

## Limitations
This is a lightweight educational authorship classifier. It uses simple frequency dictionaries and a custom stemmer rather than a full NLP pipeline, so results should be treated as exploratory rather than definitive.

## Future Improvements
* Replace `eval()` with JSON-based model saving/loading
* Add command-line arguments for source and mystery files
* Export comparison scores as CSV
* Add more stylistic features
* Add visualizations of feature distributions
* Support more than two source authors

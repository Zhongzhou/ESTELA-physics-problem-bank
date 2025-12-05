# Sharable Isomorphic Problem Banks for Introductory Physics
This repository contains isomorphic problem banks for introductory level physics that are created with the assistance of Generative AI. 
This work is sponsored by the NSF-IUSE-HSI ESTELA project (add award link and details here...). 

## What are isomorphic problem banks and how to use them.
### Isomorphic problems
The working definition of "isomorphic problems" are problems that have variations that are:
* More substantial than simply changing numbers or trivial replacement of nouns. 
* Involve at least one modification in the problem solution, such as changing a negative sign.
* Are considered to test the same set of learning objectives for the course, while not significantly changing difficulty (currently this is still a subjective call.)

### Isomorphic problem banks
An isomorphic problem bank is a collection of problems that any two problems in the bank can be considered as isomorphs according to the above definition. These problem banks are dynamic and can be extended.

### Recommended use isomorphic problems banks
* Upload problem banks to your LMS (currently supports Canvas)
* Use as both exam practice and exam item by randomly draw one problem from the bank.

## Problem Bank Creation Workflow
Follow this workflow to create an isomorphic problem bank that can be imported into Canvas. If you wish to directly use any of the problem banks, skip to step 5.

1. Setup the problem folder

2. Create the yaml file with the assistant of GPT

3. (Optional) Create a zip file for images

4. Upload the yaml to the yaml to QTI converter

5. upload the QTI package 


## Structure of Repository
(Coming soon)

### Templates
The [Templates](./Templates/) folder contains templates for problem YAML files and formatting guidance. 
* [Problem-bank-template.yaml](./Templates/Problem-bank-template.yaml) is the template to use for new problem banks. To create a new problem bank, copy this file to the bank folder.

* [YAML_formatting_prompt.md](./Templates/YAML_formatting_prompt.md) contains useful examples and prompt templates to instruct the AI to format the generated problems in the correct yaml format.


### Course Folders

### Index files

## YAML to QTI converter
https://canvas-lti.cdl.ucf.edu/yaml-to-qti/

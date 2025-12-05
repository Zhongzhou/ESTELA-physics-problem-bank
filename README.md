# Sharable Isomorphic Problem Banks for Introductory Physics
This repository contains isomorphic problem banks for introductory level physics that are created with the assistance of Generative AI. 
The bank structure is currently designed so that it can be reliably converted into QTI file compatible with CANVAS new Quiz item bank.
This work is sponsored by the NSF-IUSE-HSI ESTELA project (add award link and details here...). 

## What are isomorphic problem banks and how to use them.
### Isomorphic problems
The working definition of "isomorphic problems" are problems that have variations that are:
* More substantial than simply changing numbers or trivial replacement of nouns. 
* Involve at least one modification in the problem solution, such as changing a negative sign.
* Are considered to test the same set of learning objectives for the course, while not significantly changing difficulty (currently this is still a subjective call.)

### Isomorphic problem banks
An isomorphic problem bank is a collection of problems so that any two problems in one bank can be considered as isomorphs according to the above definition. These problem banks are dynamic and can be updated and extended.

### Recommended use of isomorphic problems banks
* Upload problem banks to your LMS (currently supports Canvas New Quiz)
* Use as both exam practice and exam item by randomly draw one problem from the bank.

## Structure of Repository

### Templates
The [Templates](./Templates/) folder contains templates for problem YAML files and formatting guidance:

* [Problem-bank-template.yaml](./Templates/Problem-bank-template.yaml) is the template to use for new problem banks. To create a new problem bank, copy this file to the bank folder. This file contains explanation to all components of the problem bank yaml file.

* [YAML_formatting_prompt.md](./Templates/YAML_formatting_prompt.md) contains useful examples and prompt templates to instruct the AI to format the generated problems in the correct yaml format.

* [YAML_problem_types.md](./Templates/YAML_problem_types.md): Detailed explanation for each problem type supported by CANVAS new quiz.

### Problem banks by course
Currently there is [PHY I Mechanics](./PHY%20I%20Mechanics/)
* [Topics.csv](./PHY%20I%20Mechanics/Topics.csv) is a list of topics typically included for PHY I Mechanics
* Each unit folder roughly corresponds to one unit of typical PHY I instruction. Each unit folder contains multiple problem bank folders.
    * Each problem bank folder contains the following components
        * A YAML file (.yml or .yaml). This is contains the problem bank and problem bank meta-data, and is human-readable.
        * A QTI file (.zip). This is the file that can be imported into CANVAS New Quiz Item Bank. 
        * (Optional) Either a Figure.zip or Image.zip file. This contains all the images used for each problem. This doesn't need to be uploaded to CANVAS
        * (Optional) Folders that contain other related meta-data or backup, older version yaml files.
    * The yaml and zip file, as well as the problem folder, are named according to the following naming convention:

            Subject-Unit-Abbreviation_of_title_-mmddyy.yaml
            
            For example: PHY1-F-1DKINT-091525 corresponds to: Physics 1, Force, 1D Kinematics with Non-Constant Acceleration, created on 09-15-2025

## Problem Bank Creation Workflow
Follow this workflow to create an isomorphic problem bank that can be imported into Canvas. If you wish to directly use any of the problem banks, skip to step 5.

1. *Setup the problem folder*: 
    * Create a folder under the intended course and unit. You can give it a temporary name such as "Newton's Laws Problem Draft".
    * Copy the [Problem-bank-template.yaml](./Templates/Problem-bank-template.yaml) file into your new folder

2. Complete the yaml file with the assistant of GenAI
    * Plan and start your problem creation process with GenAI assistance. (for reference see: https://arxiv.org/abs/2508.14755, and also see the existing folders as examples) 
    * Format the generated problems in the format specified in [YAML_problem_types.md](./Templates/YAML_problem_types.md) and [YAML_formatting_prompt.md](./Templates/YAML_formatting_prompt.md)
    * Make sure to record each generation prompt. This metadata is critical for understanding the structure of the bank and any future expansion.
    * Name your problem bank following the comments in the template document.
    * Save AI-generated data tables or code snippets in a sub-folder for more consistent future expansion of the problem bank.

3. (Optional) Create a zip file for images
    * If your problem involves one or more images, you need to store your images in a zip file that doesn't contain sub-folders
    * The file names of image files should match the names used in the yaml file. 

4. Upload the yaml to the yaml to QTI converter: https://canvas-lti.cdl.ucf.edu/yaml-to-qti/ 
    * The QTI converter is developed by UCF center for distributed learning. Currently it is available to UCF faculty only, but we are in the process of code reviews and making it open-source.
    * The converter will return the QTI package in the form of a zip file for download.

5. Upload the QTI package to CANVAS as item banks.
    * Recommended to only use the problem banks with New Quiz, since traditional quiz do not handle question banks very well and can create many independent copies.
    1. In CANVAS, go to any course that has item banks enabled (this is the default)
    2. Go to item banks from the side menu, create a new item bank (with a placeholder name)
    2. Open the problem bank, click the vertical ... menu in upper-right corner, and select "Import Content"
    3. Either select the QTI zip file or drag the zip file into the upload dialogue box on the screen. 
    




# Formatting prompt
Copy the following prompts into chatGPT for creation of standard format. For problems with longer solution, do 2-3 problems at a time.

**Note: For more problem types and more controls, refer to "./YAML_problem_types.md"**

# Numerical problem formatting prompt
Now please help me transform the first 5 problems into a YAML format, according to the example problem format below. 

* The answer: value: field should contain the actual answer number from the data table above, 
* The feedback: general field should contain the full solution generated above.  
* Math equations and expressions should be written in LaTex and enclosed in `<latex></latex>` tags:

``` yaml
- numerical: # The problem type is a numerical input problem
    id: q1
    title: Title of Question 
    points: 3
    text: | 
      This is example question text which contains an inline equation: <latex>x^2 + 2x + 1 = 0</latex>.
      We can also write equation in new line using:
      Degree ° Theta θ Delta Δ Pi π and other special characters can be inserted literally or using the character's corresponding HTML hex code.  
      <latex>
      x^2 + 2x + 1 = 0
      </latex>

    answer:
        value: 42.2 # The answer to the problem
        margin_type: percent # ... any answer within a certain absolute range will also be counted as 'correct'
        tolerance: 3 # The tolerance value
    feedback:
        general: The solution of the problem
        on_correct: Good job!
        on_incorrect: Try again!
```

# Multiple choice problem formatting prompt
Now please help me transform the first 5 problems into a YAML format, according to the example problem format below. 

* The answer: value: field should contain the actual answer number from the data table above, 
* The feedback: general field should contain the full solution generated above. 
* Math equations should be enclosed in `<latex></latex>` tags:

``` yaml
questions:
- multiple_choice:
    id: q-1 
    title: Title of Question
    points: 1
    text: |
      Question body goes here
    figure: figure_folder/figure-name.png
    answers:
        - answer:
            text: First answer choice
            correct: true
        - answer:
            text: Second answer
            correct: false
        - answer:
            text: Third answer
            correct: false
        - answer:
            text: Forth answer
            correct: false
    feedback:
        general: The solution of the problem
        on_correct:  
        on_incorrect: 
```
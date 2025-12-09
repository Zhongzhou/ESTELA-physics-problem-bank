# User Prompts

## Prompt 1
I want to write an isomorphic problem-set for my students about motion with constant acceleration on a straight-line segment. 

There are five relevant kinematic variables (displacement, instantaneous initial velocity, instantaneous final velocity, constant acceleration, and time interval) associated with each such segment. These physical quantities are related to each other via the kinematic equations. In a typical problem, three of the five variables are given either explicitly or implicitly, and the kinematic equations are used to find the other two. 

Now, generate 5 "real-life" instances of objects in motion with constant acceleration along a straight segment that can be used in this problem set. Do not write full problems yet--just state the objects and a brief description of their motion.

## Prompt 2
For each of the instances, identify one or two kinematic variables that are central to the story -- either because the variable is naturally implied by the description or can be directly measured by an observer (note that acceleration is not something that is known or can be measured directly unless the object is in free fall.) Identify the implicit value or otherwise ascribe a realistic value. Make a table.

## Prompt 3
For each instance, come up with two sets of kinematic variables that a) include the variables in the table above, b) are somewhat realistic, and c) satisfy the kinematic equations. Make a table.

## Prompt 4
Before we turn each set into a word problem, make a version of this table where the two central variables plus one other variable are given (implicitly or explicitly), and pick one of the last two variables as the one to solve for.

## Prompt 5
For the ball thrown upwards: set 1 provide vf implicitly at max height, and ask for t; for set 2, provide vf implicitly at max height and ask for displacement.

## Prompt 6
Turn each set into a word problem with rich context. Provide the given variables (implicitly or explicitly) and ask about the variable to solve for. Make the instructions in regular language and try to use keywords to communicate the variables as opposed to explicitly naming them by the physics jargon (like initial velocity and final velocity.) Do not separate the question from the problem head.

## Prompt 7
For the first problem, write a solution in the following format:
1. Acknowledge that the physics involved is about motion with constant acceleration along a straight segment, and thus the kinematic equations can be used. Make a brief statement about what's given and what variable is to be found. If the question is about a physical quantity that is the magnitude of another physical quantity, amke that explicit.
2. Make a table of the kinematic variables: displacement, initial instantaneous velocity, final instantaneous velocity, acceleration, and time interval. For each variable indicate whether it is implicitly or explicitly given or put a question mark if it is to be solved for.
3. Next identify the kinematic equation to be used based on the knowns and unknowns. 
4. Start from the common form of the kinematic equation and algebraically manipulate the equation to find the variable to be solved for. 
5. Substitute for the variables with their numerical; values and units and solve.

## Prompt 8
beautiful. do the same for all sets. take your time.

## Prompt 9
for the ball thrown vertically upward, set 1: make initial speed 6.0 m/s and for set 2, make it 8.0 m/s

## Prompt 10
help me transform all the problems and corresponding solutions into a YAML format, following the template example below. All fields from the template should be replicated in the generated YAML file, and should have the same value as the template, with the following exceptions: The id and title fields: generate an appropriate ID and title without giving away any of the physics. The problem statement should go in the text field. The answer: value: field should contain only the numerical value extracted from the corresponding answer in the solution. The feedback: general field should contain the full solution generated above. In all fields, math equations and expressions should be written in LaTex and enclosed in <latex></latex> tags. Here's the example template: 
- numerical: # The problem type is a numerical input problem. do not change.
    id: q1 #generate an id 
    title: Title of Question #generate a title that does not give away any part of the physics
    points: 1 #keep it 1 for now
    text: |
        ... 
    answer:
        value: 42.2 # The numerical answer to the problem. ONLY the number, with no units or mark down.
        margin_type: percent #the allowed variance is the tolerance percent of the value.
        tolerance: 5 # The tolerance. 
    feedback:
        general: ... #This is where the solution goes.
        on_correct: Good job! #do not change
        on_incorrect: Try again! #do not change

## Prompt 11
output all my prompts in  a markdown file


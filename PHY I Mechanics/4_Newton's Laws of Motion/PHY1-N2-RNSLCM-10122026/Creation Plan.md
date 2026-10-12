# Circular Motion Generation Plan
This document is a plan to create isomorphic versions of circular motion problems under different scenarios

## Scenario descriptions

### 1. vertical circular motion tied to a string ()
A small object being swung in a vertical circle, subjected to gravity, stays on track
### 2. vertical circular motion on a track.
An object (a toy car or a real car or an experimental device) moves on a circular track fast without leaving the track, subjected to gravity
### 3. horizontal circular motion tied to a string with wind or current from the left/right
An object (a model airplane, a model boat, a model car etc.) travels on circle while tied to a string or wire, with either wind or current coming from the left or right.
### 4. horizontal circular motion on a circular track with friction and wind from the right
An object (a car or a truck etc.) travels on a circular path/road, there is friction between the object and the ground, with either wind coming from the left or right.

## item:
### variations:
2 types of constraint: tension, normal force
3 force orientations: left/right/top(gravity)
2 scenarios each type
3 locations on track: top/bottom/side or left/center/right 
### tally:
2 types of contraint \times 3 locations \times 3 force orientations \times 2 scenarios = 32 isomorphic versions. (the actual creation maybe a little less)

## Question structure:
Asks students to choose the correct form of Newton's second law equation *along the radial direction (direction along the radius of the track)* and one of three positions.
The three possible positions are:
    * For gravity case: 1: top of circle 2: horizontal (either left or right), 3: bottom of circle
    * For wind/current cases: 1: left of circle horizontal (west) 2: top (north) or bottom (south) of circle 3: right of circle (east)
   
For example, in the vertical loop with tension case, the choice items are as follows (a_c stands for centripetal acceleration, F_c stands for centripetal force in the distractors):

1. T + mg = m a_c (correct for the top position)
2. T - mg = m a_c (correct for the bottom position)
3. T = m a_c (correct for the side position)
4. T + mg + F_c = m a_c (distractor 1)
5. T - mg + F_c = m a_c (distractor 2)
6. T + F_c = m a_c (distractor 3)

Other variations are similar.

## creation process

1. Generate 4 candidate scenarios for each scenario description for me to choose, save the result in a file and wait for my comment before proceeding.

2. Use python to generate a diagram for each selected scenario. Each diagram should:
   1. Label the object
   2. Use one arrow to indicate the direction of gravity, or an array of arrows to indicate the direction of wind or current.
   3. In the tension cases, use dashed line for the circular trajectory and solid line for rope/cable. In the normal force/friction cases, use solid line/lines to depict the track/road, and used dashed line to indicate the radius.
   4. Each image should label and contain the three locations specified above.
   
3. For each scenario, write the problem body, the choice items and indicate the correct response. The problem body should clearly state the definition of each variable used in all the choice items. Write one problem for each of the four scenario categories for me to review before proceeding to generate all of the variations.
   
4. Call on a new agent to evaluate each generated item, make small fixes automatically, and list major updates for me to consider.

5. Convert markdown to yaml when everything is finalized.
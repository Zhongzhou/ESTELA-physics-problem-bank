# General rules

## YAML hierarchy

Any given set of questions defined in the resulting YAML document should be contained under a single `questions` property, as follows:

```yaml
questions:
# note that 'question' is not one of the supported question types, it is used here as an example
- question:
    # first question's definition here
- question:
    # second question's definition here
# etc.
```

## Required properties

All question types (unless otherwise indicated) require at minimum the `id`, `title` and `text` properties to be defined and have values. Optionally, a `points` property may be defined. For example:
```yaml
questions:
- question:
    # this is a plain text string value and must be unique across all questions in the bank
    id: q1
    # this is a plain text string value
    title: Title of Question
    # this value isn't strictly necessary when creating an item bank
    # it will specify how many points the question is worth if used to build a quiz item
    points: 5
    # this is a string value that, unless otherwise indicated, may contain Markdown HTML (with some exceptions) or plain text
    text: |
        Question stem text goes here.
        Standard text following Markdown formatting rules.  
        For best results, include blank lines between blocks of text or two blank spaces at the end of each line to insert line breaks.  
        **Bold text.**  
        *Italicized text.*  
        <sup>Superscript text must use standard HTML tags.</sup>  
        <sub>Subscript text must use standard HTML tags.</sub>  
        Degree ° Theta θ Delta Δ Pi π and other special characters can be inserted literally or using the character's corresponding HTML hex code.  
        Mathematical equations can be written using LaTeX and contained within nonstandard 'latex' HTML-like tags.  
        The tags and corresponding LaTeX may be written inline:<latex>\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}</latex>  
        The tags and corresponding LaTeX may also be written on separate lines:
        <latex>
        a^2 + b^2 = c^2
        </latex>
    # feedback and any other question type-specific properties are typically defined after the basic requirements
```

## Optional properties

### Calculator

Any question of any question type may optionally define a `calculator` property, which may have a value of either `basic` or `scientific` which will enable the basic or scientific on-screen calculator, respectively.

```yaml
questions:
- question:
    # assume additional question properties i.e. id, title, text, etc. are defined first
    
    calculator: basic # or 'scientific'
```

### Feedback

Any question of any type may optionally define a `feedback` property which may contain up to three types of feedback:
* `general`: Will always appear.
* `on_correct`: Will appear when a question is answered correctly.
* `on_incorrect`: Will appear when a question is **not** answered correctly.

Any type of feedback may be either a plain text string, or a Markdown HTML string. For example:
```yaml
questions:
- question:
    # assume additional question properties i.e. id, title, text, etc. are defined first
    feedback:
        general: General feedback, or the solution to the problem.
        on_correct: Good job!
        on_incorrect: |
            For more detailed feedback, full Markdown HTML is an option.  
            Keep in mind that while Markdown is fully supported, certain strings such as subscripts, superscripts, and mathematical formulas may require using non-Markdown HTML or HTML-like tags.

```

Each question type will have its own particular properties and rules, as explained below.

# Numerical questions

Numerical questions accept answers in the form of a number, and may be configured to require varying degrees and types of specificity. Below are examples of each kind.

Note that all numerical questions require an `answer` property, which itself is an object that requires a `value` property given a numeric value regardless of answer type (unless otherwise indicated). Depending on the specific type of answer, additional properties of `answer` may be required.

## Percentage margin of tolerance

In addition to `value`, the `answer` object requires a `margin_type` property with a value of `percent`, and a `tolerance` property with a numeric value indicating the percentage of error within which a given number is considered 'correct'.

```yaml
- numerical:
    id: question_numerical_1
    title: Numerical - Percentage Margin
    text: |    
        This is a numerical question for which any answer within a percentage value of the target number is correct.

    answer:
        value: 150 # for example in this case, the 'correct' value is 150, but...
        margin_type: percent # ... any answer within a certain percentage will also be counted as 'correct'
        tolerance: 0.05 # in this case, any answer within .05% of 150 is 'correct'
```

## Absolute margin of tolerance

In addition to `value`, the `answer` object requires a `margin_type` property with a value of `absolute`, and a `tolerance` property with a numeric value indicating the amount of error within which a given number is considered 'correct'.

```yaml
- numerical:
    id: question_numerical_2
    title: Numerical - Absolute Margin
    points: 100
    text: This is a numerical question for which any answer within an absolute value of the target number is correct.

    answer:
        value: 42 # for example in this case, the 'correct' value is 42, but...
        margin_type: absolute # ... any answer within a certain absolute range will also be counted as 'correct'
        tolerance: 3 # in this case, any answer between 39 (42 - 3) or 45 (42 + 3) (both inclusive) is 'correct'
```

## Exact

The `answer` object should not have any additional properties defined, the correct answer must be the numeric value of the `value` property.

```yaml
- numerical:
    id: question_numerical_3
    title: Numerical - Exact
    points: 100
    text: This is a numerical question for which only one number is correct.

    answer:
        # only the value given below will be accepted
        value: 28.5
```

## Range

Instead of a `value` property, the `answer` object must instead define two numeric values:
* `range_start`: the lowest number for which an answer is correct.
* `range_end`: the highest number for which an answer is correct.

Any number between `range_start` and `range_end` will be considered correct.

```yaml
- numerical:
    id: question_numerical_4
    title: Numerical - Range
    points: 100
    text: This is a numerical question for which any number between two numbers is correct.

    answer:
        # any answer including or between the numbers specified below will be accepted
        range_start: 4
        range_end: 8
```

## Significant figure precision

In addition to `value`, the `answer` object requires a `precision_type` property with a value of `significant_digits`, and a `precision` property with a numeric value indicating the number of significant figures of precision within which a number is considered 'correct'.

```yaml
- numerical:
    id: question_numerical_5
    title: Numerical - Significant Figure Precision
    points: 100
    text: This is a numerical question for which any number within a range of significant figure precision of the target number is correct.

    answer:
        # any answer within the range of the given value +- the specified significant digit value will be accepted
        value: 42.123 # in this case, the 'correct' value is 42.123
        precision_type: significant_digits
        # technically, counting significant figures, the 'correct' value is actually 42.12300
        # this means that any value between 42.122995 and 42.123005 is 'correct'
        precision: 7
```

## Decimal place precision

In addition to `value`, the `answer` object requires a `precision_type` property with a value of `decimals`, and a `precision` property with a numeric value indicating the number of decimal places of precision within which a number is considered 'correct'.

```yaml
- numerical:
    id: question_numerical_6
    title: Numerical - Decimal Place Precision
    points: 100
    text: This is a numerical question for which any number within a range of decimal point precision of the target number is correct.

    answer:
        # any answer within the range of the given value +- the specified decimal places value will be accepted
        value: 42.123 # in this case, the 'correct' value is 42.123
        precision_type: decimals
        # this means that any value between 42.1225 and 42.1235 is 'correct'
        precision: 3
```

# Multiple choice questions

Multiple choice questions present multiple answers, only one of which is correct.

Note that all multiple choice questions require an `answers` property, which itself is a list that contains multiple `answer` objects. Each `answer` object must contain an `answer` property with a plain text string value. 

## Locking positions

Multiple choice questions may optionally have their answers shuffled into a different order than the one defined in the YAML document. However, it is possible to set a `lock` property on an individual answer to lock it into its defined position.

For example:
```yaml
- multiple_choice:
    id: question_multiple_choice_1
    title: Multiple Choice - Locked Answer
    points: 1
    text: |
        This is a standard multiple choice question, in which only one answer is correct and all other choices grant no points.  
        Note: the third answer option is locked into position.
    answers:
    - answer:
        text: A
        # in standard multiple choice questions, each anser option must have
        #  a 'correct' property
        # this property should have a value of 'false' for every answer except
        #  the single correct one, which should have a value of 'true'
        correct: false
    - answer:
        text: B
        correct: true
    - answer:
        text: C
        # set the 'lock' property to the boolean value 'true' on an answer to
        #  keep it in that location when shuffling
        # note that setting 'lock' to 'false' is not necessary, as omitting
        #  the property entirely assumes a value of 'false'
        lock: true
        correct: false
    - answer:
        text: D
        correct: false
    - answer:
        text: E
        correct: false
```

## Variable points

Instead of a standard multiple choice question in which only a single answer is worth any points, multiple choice questions may also allow for each answer to have a different point value.

In this case, rather than a `correct` property, each `answer` object must instead have a `points` property indicating how many points that answer is worth. The corresponding `points` property on the question object itself (if set) must match the value of the answer option worth the most points.

```yaml
- multiple_choice:
    id: question_multiple_choice_2
    title: Multiple Choice - Variable Points
    # when allowing a different number of points per answer, make sure the
    #  question's 'points' property has the same value as the highest-value answer
    points: 8
    text: A multiple choice question in which points are awarded based on the selected answer.
    answers:
    - answer:
        text: Six
        points: 6
    - answer:
        text: Eight
        points: 8
    - answer:
        text: Four
        points: 4
    - answer:
        text: Five
        points: 5
```

# True or false questions

True or false questions only allow for a single answer: true, or false.

Questions will have a single `answer` property with a value of either `true` or `false`. Points are only awarded for selecting whichever value is correct.

```yaml
- true_false:
    id: question_true_false_1
    title: True or False
    points: 1
    text:  A question in which the correct answer is either 'true' or 'false'.
    # use the boolean literal values `true` or `false` 
    answer: false
```

# Categorization questions

Categorization questions require numerous options to be correctly sorted into categories. The question object must have a `categories` property, which contains a list of `category` objects. Each `category` object must have a `description`, which is a plain text string value, and an `answers` property which contains a list of plain text string values corresponding to that category's items. Each category's `answers` property must contain at least one item.

Optionally, a `distractors` property may be defined in the question object as a list of plain text string values.

```yaml
- categorization:
    id: question_categorization_1
    title: Categorization
    points: 100
    text: A categorization question for which answer options must be correctly sorted into categories, with some optionally defined distractors.

    categories:
    # each category requires the 'description' and 'answers' properties
    - category:
        description: Category 1
        # the 'answers' property needs to be an array containing at least
        #  one string element
        answers:
        - Category 1 Item 1
        - Category 1 Item 2
        - Category 1 Item 3
    - category:
        description: Category 2
        answers:
        - Category 2 Item 1
    - category:
        description: Category 3
        answers:
        - Category 3 Item 1
        - Category 3 Item 2
    # distractors are optional, but if set will be a list of string elements as seen below
    distractors:
    - Distractor 1
    - Distractor 2
```

# Essay questions

Essay questions don't evaluate answers immediately, rather they allow for certain input tools to be enabled optionally.

## No options

The following is an example of an essay question without any features enabled. Answers may be plain text only, a word counter will not be displayed, the spell checker will not be enabled, and there will be no minimum or maximum word count.

```yaml
- essay:
    id: question_essay_1
    title: An essay question that does not specify any answer requirements or tools.
    points: 3
    text: |
        Essay questions may enable the rich content editor, spelling checker, and word counter for answers.
        They may also enable word limits, which additionally require a defined minimum and maximum word count.
```

## All options

The following is an example of an essay question with all possible features enabled. Answers may be authored using a rich content editor, a word counter will be displayed, a spell checker will be enabled and both minimum and maximum word counts will be required.

The following properties govern the above features:
* `rce`: Whether the rich content editor is enabled.
* `spell_check`: Whether the spell checker is enabled.
* `word_count`: Whether the current word count will be displayed.
* `word_limit`: If set, will be an object requiring both `min` and `max` properties.
    * `min`: The minimum requird word count.
    * `max`: The maximum allowable word count.

```yaml
- essay:
    id: question_essay_2
    title: An essay question that does specifies all possible options.
    points: 15
    text: |
        Essay questions may enable the rich content editor, spelling checker, and word counter for answers.
        They may also enable word limits, which additionally require a defined minimum and maximum word count.
    rce: true # this may be true or false - if not set, will default to false
    spell_check: true # this may be true or false - if not set, will default to false
    word_count: true # this may be true or false - if not set, will default to false
    # if word_limit is set, it must also contain 'min' and 'max' properties
    # if it is not set, there will be no word limit by default
    word_limit:
        min: 50
        max: 100
```

# File upload questions

File upload questions may require any number of files and specify any number of file types. The optional `allowed_extensions` property may be set to a comma-separated plain text string value indicating which file extensions may be uploaded. The optional `number_files` property may be set to an integer to determine how many files may (or must?) be uploaded.

For example, this is a question which requires two files, allowing either the .jpg or .jpeg extensions:

```yaml
- file_upload:
    id: question_file_upload_1
    title: File Upload - Two Files, .jpg or .jpeg
    points: 2
    text: A file upload question that restricts file extensions to 'jpg' and 'jpeg' and requires two files.
    # any number of file extensions can be used here, separated by commas
    allowed_extensions: .jpg, .jpeg
    number_files: 2
```

Likewise, this is a question with requires only a single file, only allowing the .gif extension:

```yaml
- file_upload:
    id: question_file_upload_2
    title: File Upload - Single file, .gif
    points: 2
    text: A file upload question that restricts file extensions to 'gif' and 'jpeg' and requires one file.
    # any number of file extensions can be used here, separated by commas
    allowed_extensions: .gif
    number_files: 1
```

# Ordering questions

Ordering questions define a list of items which must be placed in the given order in order to be counted as 'correct'. The question must have an `answers` property defined, containing a list of `answer` elements which may be plain text or HTML strings.

Optionally, a `labels` property may be defined as an object containing plain text `top` and `bottom` properties, which will bookend the ordered items with the given text labels. Additionally, a `paragraph` property may be set to `true` to modify the presentation of the ordered items from a vertical list to an inline paragraph.

## Basic

The following is an example of an ordering question without bookend labels and no additional configuration, meaning the items will be ordered in a vertical list:

```yaml
- ordering:
    id: question_ordering_1
    title: Ordering - No Paragraph, No Labels
    points: 2
    text: An ordering question without labels and not presenting answers in a paragraph.
    answers:
    - answer: Item 1.
    - answer: |
        Item 2.
        When not presenting answers in a paragraph, they should appear in a vertical list.
    - answer: |
        Item 3.
    - answer: Item 4
```

## Paragraph and labels

The following is an example of an ordering question with labels bookending the ordered items, configured to present the items in a paragraph rather than a vertical list:

```yaml
- ordering:
    id: question_ordering_2
    title: Ordering - Paragraph, Labels
    points: 4
    text: An ordering question that presents answers in a paragraph and includes labels.
    # an 'answers' property containing a list of 'answer' objects is required
    answers:
    - answer: |
        Item 1.
        <strong>These items can contain HTML.</strong>
    - answer: Item 2. Or they can be simple strings.
    - answer: |
        Item 3.
        <span style="background-color: #e03e2d; color; #fbeeb8;">The usual HTML rules should still work.</span>
    - answer: |
        Item 4.
        The presentation method should handle rendering.

    # this may be true or false - if not set, will default to false
    paragraph: true
    # if 'labels' is set, it must also contain 'top' and 'bottom' properties
    # if it is not set, there will be no labels by default
    labels:
        top: Top label text.
        bottom: Bottom label text.
```

# Fill in the blank questions

Fill in the blank questions allow for blanks to be specified within an HTML string, each blank allowing one of multiple possible answer methods.

Note that fill in the blank questions are defined as `fill_in_multiple_blanks` objects in the YAML document.

Fill in the blank questions must define a `blanks` property, which contains a list of `blank` objects. All `blank` objects must define two plain text string properties:
* `id`: The unique identifier for that blank within that question.
* `type`: The type of answer allowed for the blank, either `open`, `dropdown` or `bank`.

`blank` objects with a `type` value of `open` must also define a plain text string `subtype` property indicating which variety of open entry 

Blanks are indicated in the question text by containing the blank's identifier within square bracket `[]` characters, for example `[blank1]`, etc.

Additional configuration of how provided answers are graded per blank may be available depending on the selected answer type. Each blank's possible answer types may be chosen from three main categories: open entry, dropdown, and word bank. 

## Open entry

Open entry blanks generally allow users to freely type their response for a given blank. However, open entry blanks allow for significant customization by specifying a 'subtype' from the following options:
* `contains`: Any answer containing the given text is counted as 'correct'.
    * The `blank` object must also contain a plain text string `answer` property denoting the specific text that an answer must contain for the blank to be counted as 'correct'.
* `close`: Any answer within a separately defined Levenshtein distance of the given phrase is counted as 'correct'.
    * The `blank` object must also contain a plain text string `answer` property denoting the specific text to compare against a given answer.
    * The `blank` object must also contain a `settings` property, which should be an object containing the `levenshtein` and `ignore_case` properties:
        * `levenshtein`: An integer indicating the acceptable Levenshtein distance from the value of `answer` that still counts as a correct answer.
        * `ignore_case`: A boolean `true` or `false` indicating whether case should be counted towards the Levenshtein distance for determining correctness.
* `multiple`: Any answer matching one of several specific provided phrases is counted as 'correct'.
    * The `blank` object must also contain an `answers` property **instead of** the usual `answer` property.
        * `answers`: A list of plain text strings denoting all possible correct phrases for the blank.
* `regex`: Any provided answer that matches a given regular expression is counted as 'correct'. The value of `answer` should be a plain text string which will be interpreted as a regular expression.

The following is an example of a single fill in the blank question using all possible open entry blank subtypes:

```yaml
- fill_in_multiple_blanks:
    id: question_fill_in_multiple_blanks_1
    title: Fill in the Blank - Open Entry
    points: 15
    text: |
        A fill-in-the-blank question with multiple blanks covering various answer options.  
        Keep in mind that in the XML, blanks are denoted with square brackets '[' and ']' enclosing the blank's response ID.  
        Generated YAML should track blanks with square brackets containing IDs corresponding with the blanks defined in the question's 'blanks' property.  
        [blank_1] open entry option 1 - contains the text "open entry".  
        [blank_2] open entry option 2 - 'close enough' text match with a variable Levenshtein distance that can also ignore case if desired - in this case, a distance of '3' and ignoring case with the target text of "Close Enough 1".  
        [blank_3] open entry option 3 - 'close enough' text match, same as above with a Levenshtein distance of 2 that <strong>does not</strong> ignore case with the target text of "Close Enough 2".  
        [blank_4] open entry option 4 - must exactly match the target text, in this case "Exact match".  
        [blank_5] open entry option 5 - specifying correct answers. Authors may specify any number of phrases that count as 'correct', test-takers must provide one of them. In this case "One", "Two", or "Four".  
        [blank_6] open entry option 6 - regular expression matching. Authors may provide a regular expression that responses are compared to. In this case, "^Regular( )+Expression$".

    # an 'answers' property containing a list of 'answer' objects is required
    blanks:
    - blank:
        # ideally these IDs should be UUIDs to avoid collisions
        # so long as they're unique within the question text anything should work
        id: blank_1
        # 'type' defines the answer type: 'open', 'dropdown' or 'bank'
        type: open
        # 'subtype' defines the text match option for 'open' responses:
        # 'contains', 'close', 'match', 'multiple', or 'regex'
        subtype: contains
        # for all but the 'multiple' subtype, a single (plain text) string is
        #  considered to be the 'correct' answer, with the specific
        #  rules of the text matching type determining correct-ness
        answer: contains text
    - blank:
        id: blank_2
        type: open
        subtype: close
        # 'close' matching specifies levenshtein distance and
        #  whether or not to ignore case when calculating closeness
        settings:
            levenshtein: 3
            ignore_case: true
        answer: Close Enough 1
    - blank:
        id: blank_3
        type: open
        subtype: close
        settings:
            levenshtein: 2
            ignore_case: false
        answer: Close Enough 2
    - blank:
        id: blank_4
        type: open
        subtype: match
        answer: Exact match
    - blank:
        id: blank_5
        type: open
        subtype: multiple
        # 'multiple' matching replaces a single 'answer' with an 'answers' array
        # the 'answers' array must contain at least one string
        answers:
            - One
            - Two
            - Four
    - blank:
        id: blank_6
        type: open
        subtype: regex
        # 'regex' matching uses the provided 'answer' string as a regular expression
        # responses fitting the regular expression count as correct
        answer: ^Regular( )+Expression$
```

## Dropdown

Dropdown blanks define a specific set of options that users may select from, replacing the `answer` property with an `answers` property that contains a list of plain text strings.

```yaml
- fill_in_multiple_blanks:
    id: question_fill_in_multiple_blanks_2
    title: Fill in the Blank - Dropdown
    points: 15
    text: |
        A fill-in-the-blank question with multiple blanks covering various answer options.  
        Keep in mind that in the XML, blanks are denoted with square brackets '[' and ']' enclosing the blank's response ID.  
        Generated YAML should track blanks with square brackets containing IDs corresponding with the blanks defined in the question's 'blanks' property.  
        [blank_1] dropdown option - authors specify the correct answer as the first option and may define as many distractors as they like.
    
    blanks:
    - blank:
        id: blank_1
        # 'dropdown' answer types have no subtype
        type: dropdown
        # 'answers' is a list that must contain at least one string
        # the first item in 'answers' is the correct answer, all others are incorrect
        answers:
            - Correct Answer
            - Incorrect Answer
            - A Distractor
            - Another Distractor
```

## Word banks

Word bank blanks may define valid phrases, separated by commas, as a plain text string in the `answer` property. If there are multiple blanks with a `type` value of `bank`, their answers are collated and made available across all blanks alongside any defined distractors.

```yaml
- fill_in_multiple_blanks:
    id: question_fill_in_multiple_blanks_3
    title: Fill in the Blank - Word Bank
    points: 15
    text: |
        A fill-in-the-blank question with multiple blanks covering various answer options.  
        Keep in mind that in the XML, blanks are denoted with square brackets '[' and ']' enclosing the blank's response ID.    
        Generated YAML should track blanks with square brackets containing IDs corresponding with the blanks defined in the question's 'blanks' property.  
        [blank_1] word bank option 1. Authors may define a single correct answer per blank, and all options will be usable for all blanks.  
        [blank_2] word bank option 2. Authors may also optionally allow word bank choices to be reused. If enabled, this will allow multiple word bank blanks to use the same word from the question's word bank.  
        Distractors can be defined individually, and will likewise be available alongside the correct word bank options for all blanks.
    
    # distractors for a fill-in-the-blank question are defined on the question
    # they are only used in word bank responses, but are shared between all
    #  word bank responses in the question
    # 'distractors' contains a list of strings
    distractors:
        - A distractor
        - Another distractor
        - A third distractor

    # allow word bank choices to be selected for more than one blank
    allow_reuse: true

    blanks:
    - blank:
        id: blank_1
        # 'bank' answer types have no subtype
        type: bank
        # for 'bank' blanks, each blank's correct answer is added to
        #  a bank that any other 'bank' blank may use
        answer: Phrase 1
    - blank:
        id: blank_2
        type: bank
        answer: Phrase 2
```

# Formula questions

Formula questions allow for the definition of numeric variables in a question's text and the definition of a corresponding formula with which those variables are calculated into a number of potential answers.

There are several considerations to be made for formula questions in the YAML input documents. Variables are declared in a question's text via backtick `` ` `` characters. Since generated YAML documents are expected to format question text in a Markdown format which automatically converts backticks, these characters must be properly escaped with backslashes.

All formula questions require a `variables` property, containing a list of `variable` objects corresponding to the variables declared in the question text, with the following properties:
* `name`: Must match the name of the variable as it is declared in the question text.
* `min`: The minimum numeric value of the variable.
* `max`: The maximum numeric value of the variable.
* `decimals`: The number of decimal places to which a variable's value may be specific.

For example, in a question where `x` and `y` are the declared variables, a `variables` list may look like this:
```yaml
variables:
- variable:
    name: x
    min: 1.0
    max: 5.0
    decimals: 1
- variable:
    name: y
    min: 1.0
    max: 5.0
    decimals: 1
```
The above example would define the variables `x` and `y` as numbers between 1 and 5 specific to a single decimal point.

While the value of the `formula` property is (at this time) somewhat unused by these tools, it should correspond to the values of the answers generated for each formula question.

All formula questions also require an `answers` property, containing a list of `answer` objects containing a `result` property indicating the correct value for that answer, and additional properties corresponding to each declared variable for the question, assigned the values for those variables in the context of that answer. For example, using the variables as described above with a `function` value of `2x + y`, an `answers` list may look like this:
```yaml
answers:
- answer:
    x: 1.5
    y: 2
    result: 5 # note - this is 2(1.5) + (2)
- answer:
    x: 3.7
    y: 5
    result: 12.4 # note - this is 2(3.7) + (5)
```
The `answers` list must contain at least one `answer`, but may contain any number desired.

Formula questions require numeric answers in either decimal or scientific notation, and may optionally allow for a margin of error. These configurations are managed in a `settings` property, which is an object that contains properties as follows:
* `decimals`: The number of decimal places to which given answers must be specific.
* `scientific`: The boolean value `true` or `false`, whether answers must be given in scientific notation.
* `margin_type`: If `scientific` is given a value of `false`, this must be present to indicate the type of margin of error.
    * `percent`: Values within a given percentage of the target number will be counted as 'correct'.
    * `absolute`: Values within a given absolute amount of the target number will be counted as 'correct'.
* `margin`: The percentage or absolute number within which a given answer is 'correct', depending on the margin type.

Note that the `margin_type` and `margin` properties of the `settings` object must be absent if `scientific` has a value of `true`, and must be present if `scientific` has a value of `false`.

## Scientific notation

By setting the `scientific` property of the `settings` object to `true`, in combination with the value of the adjacent `decimals` property, answers will be expected in scientific notation (e.g. `4.22*10^1` instead of `42.247`).

For example:
```yaml
- formula:
    id: question_formula_1
    title: Formula - Scientific Notation
    points: 15
    text: |
        A formula question where answers are expected in scientific notation.  
        Formula questions require variables in the question text, indicated by backticks.  
        Keep in mind also that backticks are parsed in Markdown to format text as code blocks, so they will have to be escaped.  
        For example: \`x\` and \`y\`.  
        The formula (defined elsewhere) will use these variables. Any number of solutions to any number of decimal places may be defined.  
        Optionally, an on-screen calculator can also be made available (basic or scientific).
    
    # specific value ranges for the variables defined in the question text can be set here
    #  these values must be defined for all variables
    variables:
    - variable:
        # must match one of the variables defined in the question text
        name: x
        min: 5.0
        max: 10.0
        decimals: 1
    - variable:
        name: y
        min: 2.000
        max: 10.000
        decimals: 3

    settings:
        # how many decimal places to which answers must be precise
        decimals: 2
        # whether or not answers should be given in scientific notation
        # note: if this is 'true', margin of error does not need to be set
        #  (and it'll be ignored if it is)
        scientific: true

    # not sure what kind of notation is allowed/used for this formula
    # the formula may only be used to auto-generate answers on the assessment builder side
    formula: 5x + y

    # each answer must define values for all available variables indicated in the question text
    #  as well as a valid 'result' based on the values chosen for those variables
    # further, the value of 'result' must match the expected format i.e. decimal or scientific notation
    answers:
    - answer:
        x: 7.6
        y: 4.247
        result: "4.22*10^1"
    - answer:
        x: 7.4
        y: 3.868
        result: "4.09*10^1"
    - answer:
        x: 7.4
        y: 4.730
        result: "4.17*10^1"
    - answer:
        x: 6.6
        y: 8.127
        result: "4.11*10^1"
    - answer:
        x: 9.6
        y: 3.848
        result: "5.18*10^1"
```

## Percentage margin of tolerance

By setting the `scientific` property of the `settings` object to `false`, in combination with the value of the adjacent `decimals` property, answers will be expected in decimal format within a defined margin of tolerance of the target number.

By setting the value of the adjacent `margin_type` property to `percent`, any answer within a given percentage of the target number (as determined by the adjacent `margin` property) will be considered 'correct'.

Unlike with numeric questions, these margins do not need to be manually defined - only the target number.

```yaml
- formula:
    id: question_formula_2
    title: Formula - Margin of Error - Percent
    points: 15
    text: |
        A formula question where answers are expected in scientific notation.  
        Formula questions require variables in the question text, indicated by backticks.  
        Keep in mind also that backticks are parsed in Markdown to format text as code blocks, so they will have to be escaped.  
        For example: \`x\` and \`y\`.  
        The formula (defined elsewhere) will use these variables. Any number of solutions to any number of decimal places may be defined.  
        Optionally, an on-screen calculator can also be made available (basic or scientific).
    
    # specific value ranges for the variables defined in the question text can be set here
    #  these values must be defined for all variables
    variables:
    - variable:
        # must match one of the variables defined in the question text
        name: x
        min: 0.0
        max: 10.0
        decimals: 1
    - variable:
        name: y
        min: 0.000
        max: 10.000
        decimals: 3

    settings:
        # how many decimal places to which answers must be precise
        decimals: 2
        # whether or not answers should be given in scientific notation
        # note: if this is 'false', margin of error must be set
        scientific: false
        # margin of error settings must exist when not using scientific notation
        margin_type: percent
        margin: 5

    # not sure what kind of notation is allowed/used for this formula
    # the formula may only be used to auto-generate answers on the assessment builder side
    formula: 2x + y

    # each answer must define values for all available variables indicated in the question text
    #  as well as a valid 'result' based on the values chosen for those variables
    # further, the value of 'result' must match the expected format i.e. decimal or scientific notation
    answers:
    - answer:
        x: 6.0
        y: 7.557
        result: 19.557
    - answer:
        x: 2.8
        y: 9.943
        result: 15.543
    - answer:
        x: 7.9
        y: 7.031
        result: 22.831
    - answer:
        x: 4.0
        y: 3.474
        result: 11.474
    - answer:
        x: 4.4
        y: 1.650
        result: 10.450
```

## Absolute margin of tolerance

By setting the `scientific` property of the `settings` object to `false`, in combination with the value of the adjacent `decimals` property, answers will be expected in decimal format within a defined margin of tolerance of the target number.

By setting the value of the adjacent `margin_type` property to `absolute`, any answer within a given numeric value of the target number (as determined by the adjacent `margin` property) will be considered 'correct'.

Unlike with numeric questions, these margins do not need to be manually defined - only the target number.

```yaml
- formula:
    id: question_formula_3
    title: Formula - Margin of Error - Absolute
    points: 15
    text: |
        A formula question where answers are expected in scientific notation.  
        Formula questions require variables in the question text, indicated by backticks.  
        Keep in mind also that backticks are parsed in Markdown to format text as code blocks, so they will have to be escaped.  
        For example: \`x\` and \`y\`.  
        The formula (defined elsewhere) will use these variables. Any number of solutions to any number of decimal places may be defined.  
        Optionally, an on-screen calculator can also be made available (basic or scientific).
    
    # specific value ranges for the variables defined in the question text can be set here
    #  these values must be defined for all variables
    variables:
    - variable:
        # must match one of the variables defined in the question text
        name: x
        min: 5.0
        max: 10.0
        decimals: 1
    - variable:
        name: y
        min: 2.000
        max: 10.000
        decimals: 3

    settings:
        # how many decimal places to which answers must be precise
        decimals: 2
        # whether or not answers should be given in scientific notation
        # note: if this is 'false', margin of error must be set
        scientific: false
        margin_type: absolute
        margin: 0.3

    # not sure what kind of notation is allowed/used for this formula
    # the formula may only be used to auto-generate answers on the assessment builder side
    formula: 2x + y

    # each answer must define values for all available variables indicated in the question text
    #  as well as a valid 'result' based on the values chosen for those variables
    # further, the value of 'result' must match the expected format i.e. decimal or scientific notation
    answers:
    - answer:
        x: 6.0
        y: 7.557
        result: 19.557
    - answer:
        x: 2.8
        y: 9.943
        result: 15.543
    - answer:
        x: 7.9
        y: 7.031
        result: 22.831
    - answer:
        x: 4.0
        y: 3.474
        result: 11.474
    - answer:
        x: 4.4
        y: 1.650
        result: 10.450
```

# Multiple answer questions

Multiple choice questions present multiple answers, of which any number may be correct.

Note that all multiple answer questions require an `answers` property, which itself is a list that contains multiple `answer` objects. Each `answer` object must contain a `text` property with a plain text or HTML string value. Each `answer` object may also indicate whether or not it is one of the correct options via a `correct` property with a value of `true`. 

Multiple answer questions may optionally have their answers shuffled into a different order than the one defined in the YAML document. However, it is possible to set a `lock` property on an individual answer to lock it into its defined position.

Multiple answer questions may be scored partially, or by requiring a full exact match.

## Partial credit

To enable partial credit on a muliple answer question, the question must have a `partial` property defined with a value of `true`.

This will grant partial credit depending on how many correct answers are chosen, minus a penalty if any incorrect answers are chosen.

For example:
```yaml
- multiple_answers:
    id: question_multiple_answer_1
    title: Multiple Answer - Partial Credit
    points: 5
    text: |
        This is a multiple answer question that awards partial credit with a penalty based on chosen answers.  
        Partial credit is awarded for correct answers selected and a penalty is applied for incorrect answers selected.  
        Any option may be locked, preserving that option's position if shuffling is enabled.

    # to enable partial credit and penalties, set the 'partial' property of the question object to 'true'
    # this will give partial credit if some correct answers are selected, but
    #  will also apply score penalties if incorrect answers are selected
    partial: true

    answers:
    - answer:
        text: |
            Correct. Option 1.  
            Answer text can be HTML.
        # if an answer is one of the correct options, the 'correct' property must be set to 'true'
        correct: true
        # any answer option may be optionally locked into its position by setting the value of the 'lock' property to 'true'
        # if this value is set to 'false' or is not set at all, then the answer may be positioned differently if shuffling is enabled
        lock: true
    - answer:
        text: Correct. Option 2. Answer text can also be plain text.
        correct: true
    - answer:
        text: Incorrect. Option 3.
        # incorrect answers may set this value to false or omit it entirely
        correct: false
    # incorrect answers may optionally leave 'correct' undefined - if it is absent, a value of 'false' is assumed
    - answer:
        text: Incorrect. Option 4.
    - answer:
        text: |
            Incorrect.
            <strong>Option 5.</strong>
        lock: true
```

## Exact match

If a multiple answer question's `partial` property is set with a value of `false` or omitted entirely, the question will be scored according to an exact match.

In this mode, all correct answers must be selected in order to receive credit for the question.

```yaml
- multiple_answers:
    id: question_multiple_answer_2
    title: Multiple Answer - Exact Match
    points: 25
    text: This is a multiple answer question that only awards credit if all correct answers are selected.

    # multiple answer questions requiring an exact match (all correct answers selected) do not require a 'partial' property
    # it can be set to false, or omitted entirely - if not present, 'false' will be assumed

    answers:
    - answer:
        text: |
            Correct. Option 1.  
            Answer text can be HTML.
        # if an answer is one of the correct options, the 'correct' property must be set to 'true'
        correct: true
        # any answer option may be optionally locked into its position by setting the value of the 'lock' property to 'true'
        # if this value is set to 'false' or is not set at all, then the answer may be positioned differently if shuffling is enabled
        lock: true
    - answer:
        text: Correct. Option 2. Answer text can also be plain text.
        correct: true
    - answer:
        text: Incorrect. Option 3.
        # incorrect answers may set this value to false or omit it entirely
        correct: false
    # incorrect answers may optionally leave 'correct' undefined - if it is absent, a value of 'false' is assumed
    - answer:
        text: Incorrect. Option 4.
    - answer:
        text: |
            Incorrect.
            <strong>Option 5.</strong>
        lock: true
```

# Hot spot questions

Hot spot questions present an image, and define at least one (but potentially multiple) areas in which credit is awarded if clicked.

All hot spot questions require the `figure` and `areas` properties:
* `figure`: Plain text string value matching the name of the image file to be used.
* `areas`: A list of `area` objects defining clickable areas within the given image. All `area` objects require the `type` and `locations` properties.
    * `type`: A plain text string indicating area type, one of three values:
        * `bounded`: Polygonal area.
        * `ellipse`: Elliptical area.
        * `rectangle`: Rectangular area.
    * `location`: A list of floating point numbers corresponding to the limits of the clickable area.
    > NOTE: While all of the numbers listed in `location` appear to be floating point numbers, I have no idea how they are determined or what they correspond to. My assumption is that they occur in pairs and correspond to X and Y coordinates somehow, but I have no way of knowing for sure.

There are three clickable area options: polygonal, rectangular, and elliptical.

Examples of hot spot questions using each area type are as follows:
```yaml
- hot_spot:
    id: question_hot_spot_1
    title: Hot Spot - Polygon
    points: 5
    text: |
        This is a hot spot question using a polygonal click area.  
        Any hot spot question may have any number of valid clickable areas.  

    # a hot spot question must have a single figure to identify the relative path
    #  to the media file used as the clickable image for this question
    # note: currently this property is used to indicate figures for use in question text
    # at some point in the future that may have to change, for now it's overloaded    
    figure: triangle.png

    # a hot spot question may have any number of valid areas, but must have at least one
    areas:
    - area:
        # there are three valid values for the 'type' property of an 'area' object:
        # polygonal: "bounded"
        # rectangular: "rectangle"
        # elliptical: "ellipse"
        type: bounded
        # each of the locations constraining this clickable area
        # elliptical and rectangular areas will have four, polygons may have many more
        # DISCLAIMER: I have no idea how these numbers are generated, so the tool will
        #  currently assume that all of the values given here are valid and logically
        #  consistent with each other, and it's up to the prompt to do that properly
        # these locations will be individual floating-point numbers
        locations:
            - 0.2071821124745916
            - 0.7516374313031695
            - 0.5035007151998796
            - 0.2336821501166905
            - 0.8022284122562674
            - 0.7540465256342693
            - 0.2071821124745916
            - 0.7516374313031695
    - area:
        type: bounded
        locations:
            - 0.11804562222389521
            - 0.17827298050139276
            - 0.30836407438078745
            - 0.17345479183919296
            - 0.2192275841300911
            - 0.3372732063539863
            - 0.11804562222389521
            - 0.17827298050139276

- hot_spot:
    id: question_hot_spot_2
    title: Hot Spot - Ellipse
    points: 5
    text: |
        This is a hot spot question using an elliptical click area.  
        Any hot spot question may have any number of valid clickable areas.  

    figure: ellipse.png

    areas:
    - area:
        type: ellipse
        locations:
            - 0.838364827222766
            - 0.7251373936610706
            - 0.16381841451479334
            - 0.26740947075208915

- hot_spot:
    id: question_hot_spot_3
    title: Hot Spot - Rectangle
    points: 5
    text: |
        This is a hot spot question using a rectangular click area.  
        Any hot spot question may have any number of valid clickable areas.  

    figure: rectangle.png

    areas:
    - area:
        type: rectangle
        locations:
            - 0.21440939546789128
            - 0.2529549047654897
            - 0.787773846269668
            - 0.7444101483098697
```

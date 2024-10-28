import spacy
from z3 import *

# Initialize spaCy model
nlp = spacy.load('en_core_web_sm')

# Initialize Z3 solver and character variables
solver = Solver()
characters = {}
constraints = [] 

# Helper function to get or create Z3 boolean variables for characters
def get_character_var(name):
    if name not in characters:
        characters[name] = Bool(f'{name}_knight')
    return characters[name]

# Function to parse and create Z3 constraints automatically
def parse_and_create_constraints(sentence):
    doc = nlp(sentence)

    # Initialize variables for speaker, subjects, and role
    speaker = None
    subjects = []
    role = None

    # Extract speaker, subjects, and role using dependency parsing
    for token in doc:
        # Identify the speaker (subject of "says")
        if token.dep_ == "nsubj" and token.head.text == "says":
            speaker = get_character_var(token.text)

        # Handle multiple subjects (e.g., "both A and B are knights")
        if token.dep_ == "nsubj" and token.head.pos_ == "AUX":
            subjects.append(get_character_var(token.text))
        if token.dep_ == "conj" and token.head.dep_ == "nsubj":
            subjects.append(get_character_var(token.text))

        # Identify the role (knight or knave)
        if token.dep_ == "attr" and token.head.pos_ == "AUX":
            role = token.text

    # Generate Z3 constraints based on parsed structure
    if role == "knave":
        
        # Speaker claims subject(s) are knaves
        for subject in subjects:
            solver.add(Implies(speaker, Not(subject)))
            constraints.append(Implies(speaker, Not(subject))) 
            
    elif role == "knight":
        
        # Speaker claims subject(s) are knights
        for subject in subjects:
            solver.add(Implies(speaker, subject))
            constraints.append(Implies(speaker, subject)) 

# Example statements
statements = [
    "A says B is a knave",
    "B says both A and B are knights"
]

# Process each statement and create constraints
for statement in statements:
    parse_and_create_constraints(statement)

# Add constraint: At least one character must be a knight
# solver.add(Or(*characters.values()))

# Check the solution
if solver.check() == sat:
    print("Solution found:")
    print(solver.model())
else:
    print("No valid solution.")


print(constraints)
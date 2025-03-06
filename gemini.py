import google.generativeai as genai
import os
import sys
from plantuml import run_plantuml_jar
 

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    sys.exit(1)
 
genai.configure(api_key=GOOGLE_API_KEY)

# If the input is paraphrase add the following line in the prompt

# Example Input Format :
#     1. Component A calls Method X in Component B with parameter P1.
#     2. Component B processes P1 and calls Method Y in Component C.
#     3. Component C interacts with External API D to fetch data.
#     4. Component C returns the fetched data to Component B.
#     5. Component B processes the data and returns the result to Component A.
 
def generate_sequence_diagram(prompt_or_code):
  
    model = genai.GenerativeModel('gemini-2.0-flash')
 
    prompt = f"""
    Instructions:
    You are tasked with analyzing the provided step-by-step interaction descriptions and converting them into a sequence diagram. The goal is to extract meaningful interactions between components (e.g., method calls, external API interactions) and represent them visually in a structured format.

    Input Details :
    -> You will be provided with a step-by-step narrative of interactions between components.
    -> Each step describes who initiates the interaction, what is being called, and any parameters or return values involved.
    -> Pay special attention to:
    -> Internal method calls between components.
    -> External dependencies (e.g., API calls, database interactions).
    -> The flow of data between components.
    
    Output Requirements :
    -> Generate a sequence diagram in a text-based format (e.g., PlantUML, Mermaid) that can be directly rendered using tools like PlantText or Mermaid Live Editor.
    -> Ensure the sequence diagram includes:
    -> All participants (components, external APIs, etc.).
    -> Arrows representing interactions (e.g., method calls, data flow).
    -> Make sure each arrow has been correctly numbered.
    -> Parameters passed and return values (if relevant).
    -> Clearly label each interaction to reflect the provided narrative.
    
    Dependencies :
    -> Highlight all external dependencies (e.g., "External API D").
    -> If a component depends on another component or external system, explicitly show the relationship in the sequence diagram.
    
    Example Output Format :
    @startuml
    actor User
    participant "Component A" as A
    participant "Component B" as B
    participant "Component C" as C
    participant "External API D" as D

    User -> A: Initiate process
    A -> B: Call Method X with P1
    B -> C: Call Method Y
    C -> D: Fetch data
    D --> C: Return fetched data
    C --> B: Return fetched data
    B --> A: Return processed result
    A --> User: Display result
    @enduml
    
    Here I am providing the code description,

 
    {prompt_or_code}
 
    Use PlantUML syntax for the sequence diagram.
    """
 
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating sequence diagram: {e}")
        return None
 
def call_bot(user_input):

    diagram = generate_sequence_diagram(user_input)
 
    if diagram:
        print(diagram)
        #Optionally save the diagram to a file
        filename = "sequence_diagram.puml"
        with open(filename, "w") as f:
            f.write(diagram)
        print(f"\nSequence diagram saved to {filename}")
        puml_file = "sequence_diagram.puml"
        jar_file = "plantuml.1.2023.7.jar"
        run_plantuml_jar(puml_file, jar_file)
    else:
        print("Failed to generate sequence diagram.")
 
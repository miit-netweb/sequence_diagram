import google.generativeai as genai
import os
import sys
from plantuml import run_plantuml_jar
 
# Configure your API key
GOOGLE_API_KEY = "AIzaSyDrJI0ewPGZzsPRW8Dcy9qBMO_gMxLfIVc"
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
 
    # prompt = f"""
    # Instructions:
    # You are tasked with analyzing the provided step-by-step interaction descriptions and converting them into a sequence diagram. The goal is to extract meaningful interactions between components (e.g., method calls, external API interactions) and represent them visually in a structured format.
 
    # Input Details :
    # -> You will be provided with a step-by-step narrative of interactions between components.
    # -> Each step describes who initiates the interaction, what is being called, and any parameters or return values involved.
    # -> Pay special attention to:
    # -> Internal method calls between components.
    # -> External dependencies (e.g., API calls, database interactions).
    # -> The flow of data between components.
   
    # Output Requirements :
    # -> Generate a sequence diagram in a text-based format (e.g., PlantUML, Mermaid) that can be directly rendered using tools like PlantText or Mermaid Live Editor.
    # -> Ensure the sequence diagram includes:
    # -> All participants (components, external APIs, etc.).
    # -> Arrows representing interactions (e.g., method calls, data flow).
    # -> Make sure each arrow has been correctly numbered.
    # -> Parameters passed and return values (if relevant).
    # -> Clearly label each interaction to reflect the provided narrative.
   
    # Dependencies :
    # -> Highlight all external dependencies (e.g., "External API D").
    # -> If a component depends on another component or external system, explicitly show the relationship in the sequence diagram.
   
   
    # Here I am providing the code,
 
 
    # {prompt_or_code}
 
    # Use PlantUML syntax for the sequence diagram.
    # """
   
    prompt = f"""
    Objective
    Analyze a provided codebase to identify components, their interactions, and dependencies, then generate a PlantUML diagram that visually represents the system's architecture and workflow.
 
    Step 1: Code Analysis Instructions
    1.1 Understand the System Purpose
 
    Identify the core functionality of the codebase (e.g., file upload system, API service, data processor).
    Note the primary actors (e.g., users, external systems, cron jobs).
    1.2 Identify Components
 
    Structural Components :
    Classes, modules, services, or functions (e.g., UserController, DatabaseService).
    backend boundaries (e.g. REST APIs).
    Infrastructure (e.g., message queues, caching layers).
    External Dependencies :
    Libraries (e.g., flask, react).
    APIs (e.g., payment gateways, third-party services).
    Databases (e.g., MySQL, Redis).
    Cloud services (e.g., AWS S3, Firebase).
   
    1.3 Map Interactions
 
    Internal Interactions :
    Method calls between classes/modules (e.g., UserService.createUser() → Database.save()).
    Event-driven flows (e.g., message brokers like Kafka/RabbitMQ).
    External Interactions :
    API requests/responses (e.g., POST /api/login → AuthAPI.authenticate()).
    Database operations (e.g., SELECT * FROM users).
    1.4 Track Data Flow
 
    Parameters passed between components (e.g., formData in HTTP requests).
    Return values (e.g., API responses, database query results).
    Data transformations (e.g., JSON parsing, data normalization).
   
    == Workflow Example ==
    User -> FE: Initiates action (e.g., file upload)
    FE -> BE: Sends HTTP request\n(method: POST, data: FormData)
    BE -> DB: Validates data\n(queries existing records)
    DB --> BE: Returns validation result
    alt Validation Success
        BE -> API: Calls external service\n(e.g., image processing)
        API --> BE: Returns processed data
        BE -> DB: Persists result
        DB --> BE: Confirms storage
        BE --> FE: Returns 200 OK\n(response: JSON)
    else Validation Failure
        BE --> FE: Returns 400 Error\n(error: "Invalid data")
    end
    @enduml
    2.2 Rules for Representation
 
    Actors : Represent users or external systems initiating interactions.
    Participants : Use descriptive names for components (e.g., AuthService, PaymentGateway).
    Arrows :
    -> for synchronous calls.
    --> for return values.
    --> with alt/else for conditional flows.
    Annotations : Label interactions with method names, parameters, and return types.
    2.3 Validate the Diagram
 
    Cross-check with code to ensure all critical interactions are included.
    Verify dependencies (e.g., if Database is used, ensure all CRUD operations are mapped).
    Add notes for edge cases (e.g., error handling, retries).
    Step 3: Output Requirements
    Provide:
 
    A PlantUML script that:
    Includes all components and dependencies identified in Step 1.
    Uses proper syntax for sequence diagrams or component diagrams.
    Labels interactions clearly (e.g., POST /api/data, Database.save()).
    A brief explanation of the diagram’s structure and key flows.
    Example Use Case
    If analyzing a file upload system:
 
    Components: Frontend, Flask Backend, FileStorage API, Database.
    Interactions:
    User → Frontend: Selects files.
    Frontend → Backend: POST /upload.
    Backend → FileStorage: save(file).
    FileStorage → Database: record(file_metadata).
   
    Here I am providing the code for the project analyse it generate plantUML for the same
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
import openai



def get_sequence_diagram(user_input):
    """Generates a sequence diagram in PlantUML format using OpenAI API."""

    prompt = f"""
    You are an expert in software architecture and UML diagrams.
    Convert the following description or code into a valid PlantUML sequence diagram.

    {user_input}

    Return only the PlantUML code, starting with @startuml and ending with @enduml.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to gpt-3.5-turbo if needed
            messages=[{"role": "system", "content": "Generate UML sequence diagrams in PlantUML."},
                      {"role": "user", "content": prompt}],
            temperature=0.5
        )

        plantuml_code = response["choices"][0]["message"]["content"]
        return plantuml_code.strip()
    
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return None

if __name__ == "__main__":
    user_input = input("Enter code snippet or prompt for sequence diagram: \n")
    
    plantuml_code = get_sequence_diagram(user_input)
    
    if plantuml_code:
        print("\nGenerated PlantUML Code:\n")
        print(plantuml_code)
        
        # Save to file (optional)
        with open("diagram.puml", "w") as f:
            f.write(plantuml_code)
        print("\n✅ PlantUML diagram saved as diagram.puml")
    else:
        print("❌ Could not generate sequence diagram.")

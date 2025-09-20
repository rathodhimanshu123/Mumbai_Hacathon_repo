def process_symptoms(symptoms):
    """
    Process user symptoms and determine urgency level.
    
    Args:
        symptoms (list): A list of symptom strings provided by the user.
    
    Returns:
        dict: A dictionary containing processed symptoms and urgency level.
    """
    # Placeholder for urgency determination logic
    urgency_level = "low"  # Default urgency level
    processed_symptoms = []

    for symptom in symptoms:
        # Here you would add logic to analyze each symptom
        processed_symptoms.append(symptom)

        # Example logic to determine urgency level
        if "severe" in symptom.lower():
            urgency_level = "high"
        elif "moderate" in symptom.lower():
            urgency_level = "medium"

    return {
        "processed_symptoms": processed_symptoms,
        "urgency_level": urgency_level
    }

def ask_clarifying_questions(symptom):
    """
    Ask clarifying questions based on the user's symptom input.
    
    Args:
        symptom (str): The symptom provided by the user.
    
    Returns:
        str: A clarifying question related to the symptom.
    """
    # Example clarifying questions
    questions = {
        "headache": "How long have you been experiencing the headache?",
        "fever": "What is your current temperature?",
        "cough": "Is the cough dry or productive?"
    }
    
    return questions.get(symptom.lower(), "Can you provide more details about your symptom?")
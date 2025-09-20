def test_preliminary_analysis():
    # Sample input for testing
    symptoms = {
        'name': 'Headache',
        'severity': 5,
        'duration': '2 hours'
    }
    
    # Expected output
    expected_analysis = {
        'analysis': 'You may be experiencing a tension headache.',
        'lifestyle_suggestions': [
            'Stay hydrated.',
            'Take a break from screens.',
            'Consider relaxation techniques.'
        ]
    }
    
    # Call the analysis function (to be implemented in src/core/analysis.py)
    result = analyze_symptoms(symptoms)
    
    # Assert the expected output matches the result
    assert result == expected_analysis, f"Expected {expected_analysis}, but got {result}"

def test_lifestyle_suggestions():
    # Sample input for testing
    symptoms = {
        'name': 'Fatigue',
        'severity': 3,
        'duration': '1 week'
    }
    
    # Expected output
    expected_suggestions = [
        'Ensure you are getting enough sleep.',
        'Consider a balanced diet.',
        'Engage in regular physical activity.'
    ]
    
    # Call the lifestyle suggestions function (to be implemented in src/core/analysis.py)
    result = get_lifestyle_suggestions(symptoms)
    
    # Assert the expected output matches the result
    assert result == expected_suggestions, f"Expected {expected_suggestions}, but got {result}"
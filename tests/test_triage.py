import unittest
from src.core.triage import process_symptoms, determine_urgency

class TestTriageLogic(unittest.TestCase):

    def test_process_symptoms_valid(self):
        symptoms = ["fever", "cough"]
        result = process_symptoms(symptoms)
        self.assertIsInstance(result, dict)
        self.assertIn("clarifying_questions", result)
        self.assertIn("urgency_level", result)

    def test_determine_urgency_high(self):
        severity = "high"
        urgency = determine_urgency(severity)
        self.assertEqual(urgency, "Immediate attention required")

    def test_determine_urgency_low(self):
        severity = "low"
        urgency = determine_urgency(severity)
        self.assertEqual(urgency, "Monitor and consult if symptoms persist")

if __name__ == '__main__':
    unittest.main()
class Symptom:
    def __init__(self, name: str, severity: int, duration: int):
        self.name = name
        self.severity = severity
        self.duration = duration

    def __repr__(self):
        return f"Symptom(name={self.name}, severity={self.severity}, duration={self.duration})"
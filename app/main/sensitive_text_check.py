from presidio_analyzer import AnalyzerEngine

# The AnalyzerEngine loads a spaCy NER model, so it is expensive to build.
# Construct it once at import time and reuse it for every request.
_analyzer = AnalyzerEngine()


def supported_entities():
    """Return the list of PII entity types Presidio can analyze for English."""
    return _analyzer.get_supported_entities(language="en")


class SensitiveText:

    # constructor
    def __init__(self, text_to_check):
        self.text_to_check = text_to_check
        self.emails = self.detect(["EMAIL_ADDRESS"])
        self.names = self.detect(["PERSON"])

    def detect(self, entities):
        """Yield each occurrence of the requested Presidio entities, in document order."""
        for line in self.text_to_check:
            results = _analyzer.analyze(text=line, entities=entities, language="en")
            for result in sorted(results, key=lambda r: r.start):
                yield line[result.start:result.end]

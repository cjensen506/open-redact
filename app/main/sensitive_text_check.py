from presidio_analyzer import AnalyzerEngine

# The AnalyzerEngine loads a spaCy NER model, so it is expensive to build.
# Construct it once at import time and reuse it for every request.
_analyzer = AnalyzerEngine()


class SensitiveText:

    # constructor
    def __init__(self, text_to_check):
        self.text_to_check = text_to_check
        self.emails = self._detect("EMAIL_ADDRESS")
        self.names = self._detect("PERSON")

    def _detect(self, entity):
        """Yield each occurrence of the given Presidio entity, in document order."""
        for line in self.text_to_check:
            results = _analyzer.analyze(text=line, entities=[entity], language="en")
            for result in sorted(results, key=lambda r: r.start):
                yield line[result.start:result.end]

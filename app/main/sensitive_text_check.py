import re
import spacy

class SensitiveText:

    # constructor
    def __init__(self, text_to_check):
        self.text_to_check = text_to_check

        # static methods work independent of class object
    @staticmethod
    def email_check(lines):

        """ Function to recognize email address """

        # email regex
        EMAIL_REG = r"([\w\.\d]+\@[\w\d]+\.[\w\d]+)"
        for line in lines:
            # matching the regex to each line
            if re.search(EMAIL_REG, line, re.IGNORECASE):
                search = re.search(EMAIL_REG, line, re.IGNORECASE)

                # yields creates a generator
                # generator is used to return
                # values in between function iterations
                yield search.group(1)

    @staticmethod
    def name_check(lines):
        nlp = spacy.load("en_core_web_sm")
        for line in lines:
            doc = nlp(line)
            for X in doc.ents:
                if X.label_ == 'PERSON':
                    yield X.text

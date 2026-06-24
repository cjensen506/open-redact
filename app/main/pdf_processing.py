# imports
import fitz
from app.main.sensitive_text_check import SensitiveText


class Redactor:

    # constructor
    def __init__(self, mem_area, entities):
        self.mem_area = mem_area
        self.entities = entities

    def redaction(self):

        """ main redactor code """

        # opening the pdf
        doc = fitz.open(stream=self.mem_area, filetype="pdf")

        # iterating through pages
        for page in doc:

            # getting the rect boxes which consist of the matching sensitive text
            my_sensitive_text = SensitiveText(page.get_text("text").split('\n'))

            for data in my_sensitive_text.detect(self.entities):
                areas = page.search_for(data)

                # drawing outline over sensitive datas
                [page.add_redact_annot(area, fill=(0, 0, 0)) for area in areas]

            # applying the redaction
            page.apply_redactions()

        # returning the new pdf
        return doc.write()


# driver code for testing
if __name__ == "__main__":
    pass

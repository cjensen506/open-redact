import unittest
from app.main.sensitive_text_check import SensitiveText


class EmailTests(unittest.TestCase):
    def test_find_email(self):
        email = "fake_email@fake.com"
        string_with_email = "The quick brown fox fake_email@fake.com the lazy dog"
        my_sensitive_text = SensitiveText([string_with_email])
        for found_email in my_sensitive_text.emails:
            self.assertEqual(found_email, email)  # Should find the email address in string

    def test_no_email(self):
        string_with_email = "The quick brown fox jumped over the lazy dog"
        my_sensitive_text = SensitiveText([string_with_email])
        for found_email in my_sensitive_text.emails:
            self.assertTrue(False)  # Shouldn't find an email

class NameTests(unittest.TestCase):
    def test_find_one_name(self):
        name = "Lindsey Horan"
        string_with_name = "off the cross Lindsey Horan scores again"
        my_sensitive_text = SensitiveText([string_with_name])
        for found_name in my_sensitive_text.names:
            self.assertEqual(found_name, name)  # Should find the name

    def test_find_names(self):
        names = ["Lindsey Horan", "Christine Sinclair"]
        string_with_name = "Lindsey Horan with a great cross to Christine Sinclair"
        my_sensitive_text = SensitiveText([string_with_name])
        for count, found_name in enumerate(my_sensitive_text.names):
            self.assertEqual(found_name, names[count])  # Should find each name

    def test_find_no_name(self):
        string_with_name = "off the cross nobody scores again"
        my_sensitive_text = SensitiveText([string_with_name])
        for found_name in my_sensitive_text.names:
            self.assertTrue(False)  # Should find the name


if __name__ == '__main__':
    unittest.main()

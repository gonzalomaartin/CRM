from django.test import TestCase
from django.shortcuts import reverse

class LandingPageTest(TestCase): 
    def __init__(self): 
        self.response = self.client.get(reverse("landing-page"))

    def test_status_code(self): 
        self.assertEqual(self.response.status_code, 200)
    
    def test_template_name(self):
        self.assertTemplateUsed(self.response, "landing.html")

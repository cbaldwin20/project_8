from django.test import TestCase
from django.urls import reverse

from minerals.models import Minerals

quick_instance = {
        "name": "Abramovite",
        "image_filename": "240px-Abramovite.jpg",
        "image_caption": "",
        "category": "Sulfides and Sulfosalts",
        "formula": "<sub>1</sub>,<sub>066</sub>.<sub>44</sub> g/mol",
        "strunz_classification": "02.HF.25a (8th edition)",
        "crystal_system": "Triclinic - Pinacoidal; Space group = P1",
        "unit_cell": "a = 23.4 Å, b = 5.77 Å, c = 5.83 Å; α = 89.1°, β = 89.9°,"
        " γ = 91.5°",
        "color": "Silver gray",
        "cleavage": "Perfect on {100}",
        "luster": "Metallic",
        "streak": "Black",
        "diaphaneity": "Opaque",
        "crystal_habit": "Encrustations - Forms crust-like aggregates on matrix",
        "group": "Sulfides"
    }

quick_instance2 = {
        "name": "Laurionite",
        "image_filename": "240px-Laurionite-154998.jpg",
        "image_caption": "Laurionite crystals in a vug from the Laurium "
        "district of Greece",
        "category": "Halide",
        "formula": "PbCl(OH)",
        "strunz_classification": "3.DC.05",
        "crystal_system": "Orthorhombic",
        "unit_cell": "a = 7.111 Å, b = 9.6987 Å, c = 4.0203 Å; Z=4",
        "color": "Colorless",
        "crystal_symmetry": "Orthorhombic dipyramidalH-M symbol: "
        "(2/m 2/m 2/m)Space group: Pnam",
        "cleavage": "Distinct on {101}",
        "mohs_scale_hardness": "3 - 3.5",
        "luster": "Adamantine, pearly",
        "streak": "White",
        "diaphaneity": "Transparent",
        "optical_properties": "Biaxial (-)",
        "refractive_index": "nα = 2.077 nβ = 2.116 nγ = 2.158",
        "crystal_habit": "Elongated tabular prismatic crystals",
        "specific_gravity": "6.241",
        "group": "Halides"
    }

class MineralsModelTest(TestCase):
    """test that the Mineral model is working"""
    def test_saving_and_retrieving_items(self):
        """tests that the Mineral model saves instances properly"""
        Minerals.objects.create(**quick_instance)
        Minerals.objects.create(**quick_instance2)
        all_instances = Minerals.objects.all()
        minerals1 = all_instances[0]
        minerals2 = all_instances[1]
        self.assertEqual(minerals1.name, "Abramovite")
        self.assertEqual(minerals2.streak, "White")
        self.assertNotEqual(minerals1, minerals2)
        self.assertEqual(str(minerals1), 'Minerals - {}'.format(minerals1.name))

class HomePageTest(TestCase):
    """tests that the home page works"""
    def setUp(self):
        """creates an instance in our database"""
        Minerals.objects.create(**quick_instance)
            
    def test_uses_home_template(self):
        """Makes sure that the home page is using the correct template """
        response = self.client.get(reverse('minerals:home'))
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, "Abramovite")

class DetailViewTest(TestCase):
    """tests the detail page """
    def test_detail_view_to_detail_html_page(self):
        """checks to see the detail view uses the correct template
        with the correct info being sent """
        #response = self.client.get('minerals:detail', id=1)
        mineral_one = Minerals.objects.create(**quick_instance)
        response = self.client.get(reverse(
            'minerals:detail', args=[mineral_one.id]))
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual(response.context['mineral'], mineral_one)

class SearchViewTest(TestCase):
    """tests the search field """
    def test_search_view_to_correct_html_page(self):
        """checks that the search field goes to the correct template """
        Minerals.objects.create(**quick_instance)
        response = self.client.get('%s?q=Abra' % reverse('minerals:search'))
        self.assertTemplateUsed(response, 'index.html')

class LetterViewTest(TestCase):
    """tests the clickable letter anchors """
    def test_letter_view_to_correct_html_page(self):
        """tests that the clickable letter anchors go to the correct template """
        Minerals.objects.create(**quick_instance)
        response = self.client.get(reverse('minerals:letter', args=["A"]))
        self.assertTemplateUsed(response, 'index.html')

class GroupViewTest(TestCase):
    """ tests the clickable group anchors"""
    def test_group_view_to_correct_html_page(self):
        """ tests the clickable group anchors use the correct template"""
        Minerals.objects.create(**quick_instance)
        response = self.client.get(reverse('minerals:group', args=["Sulfides"]))
        self.assertTemplateUsed(response, 'index.html') 

class ColorViewTest(TestCase):
    """tests the clickable color anchors """
    def test_color_view_to_correct_html_page(self):
        """tests the clickable color anchors use the correct template
        and gets the correct info """
        mineral_one = Minerals.objects.create(**quick_instance)
        mineral_two = Minerals.objects.create(**quick_instance2)
        response = self.client.get(reverse('minerals:color', args=["Silver"]))
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['all_minerals'][0], mineral_one) 
        self.assertNotEqual(response.context['all_minerals'][0], mineral_two)

    def test_color_view_to_correct_html_page_for_other(self):
        """tests that the 'other' clickable anchor works under the colors """
        mineral_one = Minerals.objects.create(**quick_instance)
        mineral_two = Minerals.objects.create(**quick_instance2)
        response = self.client.get(reverse('minerals:color', args=["other"]))
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['all_minerals'][0], mineral_two)
        self.assertNotEqual(response.context['all_minerals'][0], mineral_one)













       
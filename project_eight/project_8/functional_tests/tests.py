from django.test import LiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import WebDriverException
import time

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
        "color": "blue",
        "cleavage": "Perfect on {100}",
        "luster": "Metallic",
        "streak": "White",
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

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
	"""one class for all my functional tests"""
	def setUp(self):
		"""create some instances in the database"""
		Minerals.objects.create(**quick_instance)
		Minerals.objects.create(**quick_instance2)
		self.browser = webdriver.Firefox()
	def tearDown(self):
		self.browser.quit()

	def solve_loading_interference(
		self, specific_text, specific_text_not="cheese"):
		"""is a method instead of doing 'time.sleep()'"""
		#we set this up so not only do we not have to use a 'time.sleep()'
		#to let the browser load, we catch the browser when it loads
		#within a half second which cuts down on wait time to finish the testing.
		#you have to do a time.wait type of maneuver after whenever you do
		#input.send_keys.(Keys.ENTER) or click()
		start_time = time.time()
		while True:
			try:
				page_text = self.browser.find_element_by_tag_name('body').text 
				self.assertIn(specific_text, page_text)
				self.assertNotIn(specific_text_not, page_text)
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e 
				time.sleep(0.5)

	def test_home_page_appears(self):
		"""test if homepage comes up"""
		self.browser.get(self.live_server_url)
		self.assertIn("Macky's Minerals: A magnificant catalog of minerals", 
			self.browser.title)

		header_text = self.browser.find_element_by_tag_name('h1').text 
		self.assertIn("Macky's Minerals", header_text)

	def test_search_bar(self):
		"""testing if the search field works"""
		self.browser.get(self.live_server_url)
		#testing the search field
		inputbox = self.browser.find_element_by_id('searchbox')
		self.assertEqual(inputbox.get_attribute('name'), 'q')

		inputbox.send_keys('Abramovite')
		inputbox.send_keys(Keys.ENTER)
		#this will test that if we enter 'Abramovite' into the 
		#search bar, that 'Abramovite' will show up but 'Laurionite'
		#will not. 
		self.solve_loading_interference("Abramovite", "Laurionite")

	def test_search_bar_part_2(self):
		"""testing that the search field correctly excludes objects"""
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('searchbox')
		inputbox.send_keys('white')
		# this is testing that if I put in white, that both of these
		# will show up because they both have white color. 
		self.solve_loading_interference("Laurionite")
		self.solve_loading_interference("Abramovite")
  
	def test_clicking_letter_for_mineral(self):
		"""testing if clicking the letter anchor link will bring object"""
		self.browser.get(self.live_server_url)
		letters = self.browser.find_elements_by_class_name('selectorL')
		for letter in letters:
			if letter.text == "L":
				letterL = letter 
				break 
		letterL.click()
		self.solve_loading_interference("Laurionite", "Abramovite")

	# francis_list_url = self.browser.current_url
	# self.assertRegex(francis_list_url, '/lists/.+')
	# self.assertNotEqual(francis_list_url, edith_list_url)

	def test_clicking_group_for_mineral(self):
		"""click mineral group anchor will get objects"""
		self.browser.get(self.live_server_url)
		groups = self.browser.find_elements_by_class_name('selectorG')
		for group in groups:
			if group.text == "Halides":
				groupG = group 
				break 
		groupG.click()
		self.solve_loading_interference("Laurionite", "Abramovite")

	def test_clicking_color_for_mineral(self):
		"""click color anchor tag will get objects"""
		self.browser.get(self.live_server_url)
		colors = self.browser.find_elements_by_class_name('selectorC')
		for color in colors:
			if color.text == "blue":
				colorC = color 
				break 
		colorC.click()
		self.solve_loading_interference("Abramovite", "Laurionite")

	def test_clicking_for_detail(self):
		"""click a mineral name anchor tag and get object"""
		self.browser.get(self.live_server_url)
		detail_minerals = self.browser.find_elements_by_class_name(
			"minerals__anchor")
		for mineral in detail_minerals:
			if mineral.text == "Laurionite":
				mineralM = mineral 
				break 
		mineralM.click()
		self.solve_loading_interference("Laurionite", "Abramovite")

	"""
	def test_clicking_random_for_mineral(self):
		self.browser.get(self.live_server_url)
		random_min = self.browser.find_element_by_id('selectorR')
		random_min.click()
		
		start_time = time.time()
		while True:
			try:
				detail_min = self.browser.find_element_by_id('ran_min').text  
				self.assertIn(detail_min, ["Abramovite", "Laurionite"])
				break
				#AssertionError means 'row_text' was not in 'row.text'
				#WebDriverException means the page didn't finish loading (?)
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e 
				time.sleep(0.5)
	"""
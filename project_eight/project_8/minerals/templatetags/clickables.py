from django import template
import random

from minerals.models import Minerals

register = template.Library()

@register.inclusion_tag('groups_clickables.html')
def groups_list(clickable=None):
    """a list of groups to be clicked on in html"""
    groups = ['Silicates', 'Oxides', 'Sulfates',
     'Sulfides', 'Carbonates', 'Halides']
    groups += ['Sulfosalts', 'Phosphates',
     'Borates', 'Organic Minerals', 'Arsenates']
    groups +=  ['Native Elements', 'Other']
    return {'groups': groups, 'clickable':clickable }

@register.inclusion_tag('colors_clickables.html')
def colors_list(clickable_C=None):
    """a list of colors to be click on in html"""
    colors = ["yellow", 'tan', 'white', 'gray', 'black', 'blue', 'violet']
    colors += ['brown', 'red', 'green', 'orange', 'other']
    return {'colors': colors, 'clickable_C': clickable_C }

@register.inclusion_tag('letters_clickables.html')
def letters_list(clickable_L=None):
    """a list of letters to be clicked on in html"""
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return {'letters': letters, 'clickable_L': clickable_L }

@register.inclusion_tag('random_num.html')
def random_number():
    """click on this and it will give you a random mineral object
    and will go to its detail html page"""
    all_minerals = Minerals.objects.all()
    random_total = len(all_minerals)
    random_num = random.randint(1, random_total)
    return {'random_num': random_num} 
















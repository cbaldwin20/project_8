
from django import template
import random

from minerals.models import Minerals

register = template.Library()

@register.inclusion_tag('groups_clickables.html')
def groups_list(clickable=None):
    groups = ['Silicates', 'Oxides', 'Sulfates', 'Sulfides', 'Carbonates', 'Halides']
    groups += ['Sulfosalts', 'Phosphates', 'Borates', 'Organic Minerals', 'Arsenates']
    groups +=  ['Native Elements', 'Other']
    return {'groups': groups, 'clickable':clickable }


@register.inclusion_tag('colors_clickables.html')
def colors_list(clickable_C=None):
    colors = ["yellow", 'tan', 'white', 'gray', 'black', 'blue', 'violet']
    colors += ['brown', 'red', 'green', 'orange', 'other']
    return {'colors': colors, 'clickable_C': clickable_C }


@register.inclusion_tag('letters_clickables.html')
def letters_list(clickable_L=None):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return {'letters': letters, 'clickable_L': clickable_L }


@register.inclusion_tag('random_num.html')
def random_number():
    all_minerals = Minerals.objects.all()
    random_total = len(all_minerals)
    random_num = random.randint(1, random_total)
    return {'random_num': random_num} 

   















from django.shortcuts import render
from .models import Minerals 
from django.db.models import Q
 
def home(request):
    """the home page of the site. The 'A' anchor letter is 
    automatically selected """
    all_minerals = Minerals.objects.filter(name__startswith="A")
    clickable_L = "A"
    return render(request, 'index.html', {'all_minerals': all_minerals,
        'clickable_L': clickable_L})

def detail(request, id):
    """displays one single mineral """
    mineral = Minerals.objects.get(id=id)
    print("This is the mineral- {}".format(mineral))
    return render(request, 'detail.html', {'mineral': mineral})

def search(request):
    """activates when search field is used """
    term = request.GET.get('q')
    all_minerals = Minerals.objects.filter(
        Q(name__icontains=term)|Q(category__icontains=term)|
        Q(formula__icontains=term)|
        Q(strunz_classification__icontains=term)|
        Q(crystal_system__icontains=term)|Q(unit_cell__icontains=term)|
        Q(color__icontains=term)|Q(crystal_symmetry__icontains=term)|
        Q(cleavage__icontains=term)|
        Q(mohs_scale_hardness__icontains=term)|Q(luster__icontains=term)|
        Q(streak__icontains=term)|
        Q(diaphaneity__icontains=term)|Q(optical_properties__icontains=term)|
        Q(group__icontains=term)|
        Q(group__icontains=term)|Q(refractive_index__icontains=term)|
        Q(crystal_habit__icontains=term)|
        Q(specific_gravity__icontains=term))
    return render(request, 'index.html', {'all_minerals': all_minerals})

def letter(request, letter):
    """activates when a letter anchor is clicked """
    all_minerals = Minerals.objects.filter(name__startswith=letter)
    return render(request, 'index.html', {'all_minerals': all_minerals,
                                        'clickable_L': letter})

def group(request, group):
    """activates when a 'group' anchor is clicked"""
    all_minerals = Minerals.objects.filter(group=group)
    return render(request, 'index.html', {'all_minerals': all_minerals, 
                                    'clickable':group})

def color(request, color):
    """activates when a 'color' anchor is clicked """
    if color == 'other':
        colors = ["yellow", 'tan', 'white', 'gray', 'black', 'blue', 'violet']
        colors += ['brown', 'red', 'green', 'orange', 'other']
        all_minerals = Minerals.objects
        for i in colors:
            all_minerals = all_minerals.exclude(color__icontains=i)
    else:
        all_minerals = Minerals.objects.filter(color__icontains=color)
    return render(request, 'index.html', {'all_minerals': all_minerals,
                                        'clickable_C':color})
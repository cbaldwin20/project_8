from django.shortcuts import render
from .models import Minerals 
from django.db.models import Q


# Create your views here.
def home(request):
    all_minerals = Minerals.objects.all()
    return render(request, 'index.html', {'all_minerals': all_minerals})


def detail(request, id):
    mineral = Minerals.objects.get(id=id)
    print("This is the mineral- {}".format(mineral))
    return render(request, 'detail.html', {'mineral': mineral})


def search(request):
    term = request.GET.get('q')
    all_minerals = Minerals.objects.filter(
        Q(name__icontains=term)|Q(category__icontains=term)|Q(formula__icontains=term)|
        Q(strunz_classification__icontains=term)|Q(crystal_system__icontains=term)|Q(unit_cell__icontains=term)|
        Q(color__icontains=term)|Q(crystal_symmetry__icontains=term)|Q(cleavage__icontains=term)|
        Q(mohs_scale_hardness__icontains=term)|Q(luster__icontains=term)|Q(streak__icontains=term)|
        Q(diaphaneity__icontains=term)|Q(optical_properties__icontains=term)|Q(group__icontains=term)|
        Q(group__icontains=term)|Q(refractive_index__icontains=term)|Q(crystal_habit__icontains=term)|
        Q(specific_gravity__icontains=term))
    return render(request, 'index.html', {'all_minerals': all_minerals})


def letter(request, letter):
    all_minerals = Minerals.objects.filter(name__startswith=letter)
    return render(request, 'index.html', {'all_minerals': all_minerals,
                                        'clickable_L': letter})


def group(request, group):
    all_minerals = Minerals.objects.filter(group=group)
    return render(request, 'index.html', {'all_minerals': all_minerals, 
                                    'clickable':group})


def color(request, color):
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
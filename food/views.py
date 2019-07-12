from django.shortcuts import render,HttpResponse,get_object_or_404,HttpResponseRedirect,Http404
from .models import*
from .forms import RecipeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify

def index_view(request):

    recipe_list = Recipe.objects.all()
    query=request.GET.get("q")
    if query:
        recipe_list=recipe_list.filter(name__icontains=query)

    recipes=Recipe.objects.all()
    paginator = Paginator(recipe_list, 3)

    page = request.GET.get('sayfa')
    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:

        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    return render(request,'food/index.html',{'recipes':recipes})

def detail_view(request,slug):
    recipe=get_object_or_404(Recipe,slug=slug)
    is_liked = False
    if recipe.likes.filter(id=request.user.id).exists():
        is_liked=True
    context={
        'recipe':recipe,
        'is_liked':is_liked,
        'total_likes': recipe.total_likes(),
    }
    return render(request,'food/detail.html',context)

def like_recipe(request):
    recipe=get_object_or_404(Recipe,id=request.POST.get('recipe_id'))
    is_liked=False
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
        is_liked=False
    else:
        recipe.likes.add(request.user)
        is_liked=True

    return HttpResponseRedirect(recipe.get_absolute_url())


def create_view(request):
    if not request.user.is_authenticated:#Kullanıcı üye mi değil mi kontrolü
        return Http404()

    form=RecipeForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        recipe=form.save(commit=False)
        recipe.user = request.user
        recipe = form.save()
        return HttpResponseRedirect(recipe.get_absolute_url())
    context={
        'form':form,
    }
    return render(request,'food/form.html',context)

def update_view(request,slug):

    recipe=get_object_or_404(Recipe,slug=slug)
    form = RecipeForm(request.POST or None,request.FILES or None,instance=recipe)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(recipe.get_absolute_url())
    context = {

        'form': form,
    }
    return render(request, 'food/form.html', context)

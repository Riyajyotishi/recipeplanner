from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Recipe
from django.contrib.auth.decorators import login_required



@login_required
def profile_page(request):
    user = request.user
    recipe_count = Recipe.objects.filter().count()

    return render(request, 'recipes/profile.html', {
        'user': user,
        'recipe_count': recipe_count
    })

def recipe_list(request):
     category = request.GET.get('category')

     if category:
        recipes = Recipe.objects.filter(category=category)
     else:
         recipes = Recipe.objects.all()

     search = request.GET.get('search')
     category = request.GET.get('category')

     recipes = Recipe.objects.all()
 
     if search:
        recipes = recipes.filter(title__icontains=search)

     if category:
        recipes = recipes.filter(category=category)    
     return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def add_recipe(request):
    if request.method == 'POST':
        Recipe.objects.create(
            title=request.POST.get('title'),
            ingredients=request.POST.get('ingredients'),
            description=request.POST.get('description'),
            category=request.POST.get('category')
        )
        return redirect('recipe_list')

    return render(request, 'recipes/add_recipe.html')

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.method == 'POST':
        recipe.title = request.POST.get('title')
        recipe.ingredients = request.POST.get('ingredients')
        recipe.instructions = request.POST.get('instructions')
        recipe.description = request.POST.get('description')
        recipe.category = request.POST.get('category')
        recipe.save()
        return redirect('recipe_list')

    return render(request, 'recipes/edit_recipe.html', {'recipe': recipe})

def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.delete()
    return redirect('recipe_list')



# ---------- SIGNUP ----------
def signup_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username:
            messages.error(request, "Username is required")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'recipes/signup.html')


# ---------- LOGIN ----------
def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'recipes/login.html')


# ---------- LOGOUT ----------
def logout_page(request):
    logout(request)
    return redirect('login')

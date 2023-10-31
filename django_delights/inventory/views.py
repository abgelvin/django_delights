from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

# Create your views here.

class HomeView(TemplateView):
    template_name = 'inventory/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context


class IngredientListView(ListView):
    template_name = 'inventory/ingredient_list.html'
    model = Ingredient
    queryset = Ingredient.objects.all()


class MenuItemListView(ListView):
    template_name = 'inventory/menuitem_list.html'
    model = MenuItem
    queryset = MenuItem.objects.all()


# class RecipeRequirementListView(ListView):
#     template_name = 'inventory/recipe_requirement_list.html'
#     model = RecipeRequirement
#     queryset = RecipeRequirement.objects.all()


class PurchaseListView(ListView):
    template_name = 'inventory/purchase_list.html'
    model = Purchase
    queryset = Purchase.objects.all()


class IngredientCreateView(CreateView):
    template_name = 'inventory/ingredient_form.html'
    model = Ingredient
    fields = ['name', 'quantity', 'unit', 'price_per_unit']
    success_url = '/ingredients/new'


class MenuItemCreateView(CreateView):
    template_name = 'inventory/menuitem_form.html'
    model = MenuItem
    fields = ['name', 'price']
    success_url = '/menu/new'


class RecipeRequirementCreateView(CreateView):
    template_name = 'inventory/recipe_requirement_form.html'
    model = RecipeRequirement
    fields = ['menu_item', 'ingredient', 'quantity']
    success_url = '/recipe/new'


class PurchaseCreateView(CreateView):
    template_name = 'inventory/purchase_list.html'
    model = Purchase
    fields = ['menu_item', 'timestamp']
    queryset = Purchase.objects.all()


class IngredientUpdateView(UpdateView):
    template_name = 'inventory/ingredient_update_form.html'
    model = Ingredient
    fields = ['name', 'quantity', 'unit', 'price_per_unit']
    success_url = '/ingredients'

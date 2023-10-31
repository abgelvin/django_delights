from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm


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
    form_class = IngredientForm


class MenuItemCreateView(CreateView):
    template_name = 'inventory/menuitem_form.html'
    model = MenuItem
    form_class = MenuItemForm


class RecipeRequirementCreateView(CreateView):
    template_name = 'inventory/recipe_requirement_form.html'
    model = RecipeRequirement
    form_class = RecipeRequirementForm


class PurchaseCreateView(TemplateView):
    template_name = 'inventory/purchase_form.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['menu_items'] = [i for i in MenuItem.objects.all() if i.available()]
        return context
    
    def post(self, request):
        menu_item_id = request.POST['menu_item']
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect('/purchases')
    
    
class IngredientUpdateView(UpdateView):
    template_name = 'inventory/ingredient_update_form.html'
    model = Ingredient
    form_class = IngredientForm
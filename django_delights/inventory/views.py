from typing import Any
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context


class IngredientListView(LoginRequiredMixin, ListView):
    template_name = 'inventory/ingredient_list.html'
    model = Ingredient
    queryset = Ingredient.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for ingredient in Ingredient.objects.all():
            quantity = ingredient.quantity
            price = ingredient.price_per_unit
            total = quantity * price
            context["total"] = total
        
        return context


class MenuItemListView(LoginRequiredMixin, ListView):
    template_name = 'inventory/menuitem_list.html'
    model = MenuItem
    queryset = MenuItem.objects.all()


# class RecipeRequirementListView(ListView):
#     template_name = 'inventory/recipe_requirement_list.html'
#     model = RecipeRequirement
#     queryset = RecipeRequirement.objects.all()


class PurchaseListView(LoginRequiredMixin, ListView):
    template_name = 'inventory/purchase_list.html'
    model = Purchase
    queryset = Purchase.objects.all()


class IngredientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'inventory/ingredient_form.html'
    model = Ingredient
    form_class = IngredientForm


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'inventory/menuitem_form.html'
    model = MenuItem
    form_class = MenuItemForm


class RecipeRequirementCreateView(LoginRequiredMixin, CreateView):
    template_name = 'inventory/recipe_requirement_form.html'
    model = RecipeRequirement
    form_class = RecipeRequirementForm


class PurchaseCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/purchase_form.html'

    def get_context_data(self, **kwargs):
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
    
    
class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/ingredient_update_form.html'
    model = Ingredient
    form_class = IngredientForm


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(
            revenue=Sum('menu_item__price'))['revenue']
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.price_per_unit * recipe_requirement.quantity

        context['revenue'] = revenue
        context['total_cost'] = total_cost
        context['profit'] = revenue - total_cost

        return context


# class LoginView(LoginView):
#     redirect_authenticated_user = True
    
#     def get_success_url(self) -> str:
#         return redirect('/home')


def log_out(request):
    logout(request)
    return redirect('/')
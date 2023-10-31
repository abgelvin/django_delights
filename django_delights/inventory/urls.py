from django.urls import path
from .views import (
    HomeView,
    IngredientListView, 
    MenuItemListView, 
    PurchaseListView, 
    # RecipeRequirementListView, 
    IngredientCreateView,
    MenuItemCreateView,
    PurchaseCreateView,
    RecipeRequirementCreateView,
    IngredientUpdateView,
    ReportView
    )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ingredients/', IngredientListView.as_view(), name='ingredients'),
    path('menu/', MenuItemListView.as_view(), name='menu'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    # path('recipes/', RecipeRequirementListView.as_view(), name='recipes'),
    path('ingredients/new', IngredientCreateView.as_view(), name='add_ingredient'),
    path('ingredients/<pk>/update', IngredientUpdateView.as_view(), name='ingredient_update'),
    path('menu/new', MenuItemCreateView.as_view(), name='add_menuitem'),
    path('purchases/new', PurchaseCreateView.as_view(), name='add_purchase'),
    path('recipe/new', RecipeRequirementCreateView.as_view(), name='update_recipe'),
    path('reports/', ReportView.as_view(), name = 'reports')
]
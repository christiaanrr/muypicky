from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item
from .forms import ItemForm

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            object_list = Item.objects.filter(public=True).order_by('-timestamp')
            return render(request, "home.html", {"object_list": object_list})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = Item.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-updated")[:5]
        return render(request, "menus/home_feed.html", {'object_list': qs})

class AllUserRecentItemListView(ListView):
    template_name = 'home.html'
    def get_queryset(self):
        return Item.objects.filter(user__is_active=True)

class ItemListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user) #checks if user is authenticated


class ItemDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)  # checks if user is authenticated


class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'menus/form.html'
    form_class = ItemForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)  # checks if user is authenticated

    def get_context_data(self, *args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args, *kwargs)
        context['title'] = 'Create Item'
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'menus/detail-update.html'
    form_class = ItemForm

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)  # checks if user is authenticated

    def get_context_data(self, *args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args, *kwargs)
        context['title'] = 'Update Item'
        return context

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
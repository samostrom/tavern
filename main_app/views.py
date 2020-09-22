
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Group, Profile, System
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from random import choice
from .forms import ExtendedUserCreationForm, GroupForm


def landing(request):
    return render(request, 'landing.html')


@login_required
def groups_index(request):
    groups = Group.objects.filter(players=request.user.profile).order_by('date')
    return render(request, 'groups/index.html', {'groups': groups})

@login_required
def groups_detail(request, group_id):
    return redirect('groups_index') # TODO

@login_required
def lfg(request):
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        groups = Group.objects.filter(
            looking=True, system__in=profile.systems.all())
        groups = groups.exclude(players=profile).exclude(contenders=profile)
        group = choice(groups)
        return render(request, 'groups/lfg.html', {'group': group})
    else:
        # TODO: make this a redirect to profile setup, OR always initialize a profile in signup
        return redirect('landing')


@login_required
def add_contender(request):
    group = Group.objects.get(id=request.POST['group_id'])
    group.contenders.add(request.user.profile)
    return redirect('lfg')


class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['group_name', 'system', 'date', 'location', 'details']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = GroupForm(request.POST)
        if form.is_valid():
            new_group = form.save()
            new_group.players.add(request.user.id)
        # TODO: un-stub when we have single group view
        return redirect('groups_index')


def profile_create(request):
    profile = Profile.objects.all()
    return render(request, 'main_app/profile/profile.html', {'profile': profile})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('groups_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = ExtendedUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

from .models import Album,Song


from django.views import generic

#views already avaolabale with django
from django.views.generic.edit import CreateView, UpdateView, DeleteView

#redirect to url
from django.shortcuts import render,redirect

#for authentication
from django.contrib.auth import authenticate,login

#whenever an album is deleted it redirects it to some url reverse_lazy(url)
from django.core.urlresolvers import reverse_lazy

from django.views.generic import View

from .forms import UserForm

#generic view


class IndexView(generic.ListView):
	template_name = 'music/index.html'
	context_object_name = 'albums'
	def get_queryset(self):
		return Album.objects.all()

class DetailView(generic.DetailView):
	model = Album
	context_object_name = 'album'
	template_name = 'music/detail.html'


class AlbumCreate(CreateView):
	model = Album
	fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
	model = Album
	success_url = reverse_lazy('music:index')

class UserFormView(View):
	form_class = UserForm
	template_name = 'music/registration_form.html'

	#handle get request on this url i.e. user registration
	#None means we dont pass in any context
	def get(self,req):
		form = self.form_class(None)
		return render(req,self.template_name,{'form':form})

	#handle post request. submission of new user form
	def post(self,req):
		form = self.form_class(req.POST)
		if form.is_valid():
			#creates a form object but doesent save it to database
			user = form.save(commit = False)
			#clean and normalize data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			#use to encrypt the password to save in database
			user.set_password(password)
			user.save()

			#return User objects if credentils are correct
			#for logging in after checking in database
			user = authenticate(username=username,password=password)

			#check if present in datm
			if user is not None:
				if user.is_active:
					login(req,user)
					return redirect('music:index')

		
		return render(req,self.template_name,{'form':form})




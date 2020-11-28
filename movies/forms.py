from django import forms


from .models import Reviews

class ReviewForm(forms.ModelForm):
	"""Review form"""
	class Meta:
		model = Reviews
		fields = ('name','email','text')




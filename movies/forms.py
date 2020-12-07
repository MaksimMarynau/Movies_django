from django import forms


from .models import Reviews, Rating, RatingStar

class ReviewForm(forms.ModelForm):
	"""Review form"""
	
	class Meta:
		model = Reviews
		fields = ('name','email','text')


class RatingForm(forms.ModelForm):
	""" Form to add rating """
	star = forms.ModelChoiceField(
			queryset = RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
		)

	class Meta:
		model = Rating
		fields = ("star",)


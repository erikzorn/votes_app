from django import forms

#from django.core.validators import

#def validate_zip(value):
#	zip_validator = 

class SubmitZipForm(forms.Form):
	zip = forms.IntegerField(label="", widget=forms.TextInput({ "placeholder": "enter zipcode here" }))

	def clean(self):	# entire form
		cleaned_data = super(SubmitZipForm, self).clean()
		zip = cleaned_data['zip']

	def clean_zip(self):	# individual field
		zip = self.cleaned_data['zip']
		return zip

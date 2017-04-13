from django import forms

#from django.core.validators import

#def validate_zip(value):
#	zip_validator = 

class SubmitZipForm(forms.Form):
	zip = forms.IntegerField(label="Submit Zip")

	def clean(self):	# entire form
		cleaned_data = super(SubmitZipForm, self).clean()
		#print(cleaned_data)
		zip = cleaned_data['zip']
		#print zip

	def clean_zip(self):	# individual field
		zip = self.cleaned_data['zip']
		#print(zip)
		return zip

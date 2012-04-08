from django import forms

""" forms.py: defines forms used in homework7 project- DocumentForm & QueryForm """

class DocumentForm(forms.Form):
      """ DocumentForm(forms.Form): form for file upload """
      title=forms.CharField(label='Collection:')
      docfile=forms.FileField(label='Select a file:')

class QueryForm(forms.Form):
      """ QueryForm(forms.Form): form for text search query """
      title=forms.CharField(label='Query string:',widget=forms.TextInput(attrs={'size': '70'}))


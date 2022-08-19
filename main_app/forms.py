from django import forms


class AddContentForm(forms.Form):
    title = forms.CharField(max_length=30)
    is_private = forms.BooleanField()
    categoryID = forms.IntegerField()
    file = forms.FileField()
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
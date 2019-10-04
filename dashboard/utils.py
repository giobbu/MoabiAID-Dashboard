from django import forms

from bootstrap_datepicker_plus import DatePickerInput

from crispy_forms.helper import FormHelper

class BadRequestError(Exception):
    pass

class MapControls(forms.Form):
    """
    Controls that are used to select a data and a time for the map
    
    :param Form: [description]
    :type Form: [type]
    """
    date = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y')) #TODO: make date picker and add hour of the day slider

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_media = False
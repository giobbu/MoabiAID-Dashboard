from django import forms
from django.forms.widgets import ChoiceWidget

from bootstrap_datepicker_plus import DatePickerInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field

class BadRequestError(Exception):
    pass

class SliderWidget(ChoiceWidget):
    input_type = 'range'
    template_name = 'dashboard/widgets/rangeslider.html'
    option_template_name = 'dashboard/widgets/slideroption.html'

    def __init__(self, attrs=None, min_range=0, max_range=100, step=1):

        if max_range <= min_range:
            raise ValueError('The minimal value can not be larger than the maximal value')

        slider_attrs = {
            'class': 'custom-range',
            'min': min_range,
            'max': max_range,
            'step': step
        }

        choices = [(c,c) for c in range(min_range, max_range + step, step)] #We add to max_range to also include the max bound

        if attrs is not None:
            slider_attrs.update(attrs)
        super().__init__(attrs=slider_attrs, choices=choices)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context


class SliderField(forms.ChoiceField):
    
    def __init__(self, min_range=0, max_range=100, step=1):
        widget = SliderWidget(min_range=min_range, max_range=max_range, step=step)
        super().__init__(choices=widget.choices, widget=widget)


class MapControls(forms.Form):
    """
    Controls that are used to select a data and a time for the map
    
    :param Form: [description]
    :type Form: [type]
    """
    date = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y')) #TODO: make date picker and add hour of the day slider
    day_of_week = SliderField(min_range=1, max_range=7)
    time_of_day = SliderField(max_range=24) #Hours start at 0, the default

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_media = False
        self.helper.layout = Layout(
            Field('date'),
            Field('day_of_week', data_valuedisplay='#day_of_week_val'),
            HTML('<p id="day_of_week_val"></p>'),
            Field('time_of_day', data_valuedisplay='#time_of_day_val'),
            HTML('<p id="time_of_day_val"></p>')
        )
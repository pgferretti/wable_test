from django.forms.widgets import ClearableFileInput
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Currently'
    input_text = 'Change'
    clear_checkbox_label = 'Clear'

    template_with_initial = '%(input)s'

    template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    url_markup_template = '<a href="{0}">{1}</a>'

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = format_html(self.url_markup_template,
                                                   value.url,
                                                   force_text(value))

        return mark_safe(template % substitutions)

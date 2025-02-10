from django import forms

class FormContactos(forms.Form):
    asunto = forms.CharField(max_length=100)
    mensaje = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(required=False, label='Tu correo electronico')

    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        num_palabras = len(mensaje.split())
        if num_palabras < 4:
            raise forms.ValidationError("Se requiere minimo 4 palabras")

        return mensaje
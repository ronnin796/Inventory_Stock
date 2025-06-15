from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label="Select Excel File (.xls or .xlsx)",
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if file:
            if not file.name.endswith(('.xls', '.xlsx')):
                raise forms.ValidationError("Only .xls or .xlsx files are supported.")
            if file.size > 5 * 1024 * 1024:  # 5MB limit (optional)
                raise forms.ValidationError("File too large (max 5MB).")
        return file

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

def validate_even(value):
    if value % 2 !=0:
        raise ValidationError('%(value)s ไม่ใช่เลขคู่', params={'value': value})
class PollForm(forms.Form):
    title = forms.CharField(label="ชื่อโพล", max_length=100, required=True)
    email = forms.CharField()
    no_questions = forms.IntegerField(label="จำนวนคำถาม", min_value=0, max_value=10, validators=[validate_even])
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def clean_title(self):
        data = self.cleaned_data['title']
        if "ไอทีหมีแพนด้า" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")
        return data

    def clean(self):
        """validate แบบ form สังเกตว่ามันจะเป็นค่าของ 2 field"""
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and not end:
            #raise forms.ValidationError('โปรดเลือกวันที่สิ้นสุด')
            self.add_error('end_date', 'โปรดเลือกวันที่สิ้นสุด') #แสดงในฟิลด์
        elif end and not start:
            #raise forms.ValidationError('โปรดเลือดวันที่เริ่มต้น')
            self.add_error('start_date', 'โปรดเลือกวันที่เริ่มต้น')

class CommentForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(max_length=500, widget=forms.Textarea)
    email = forms.EmailField(required=False)
    tel = forms.CharField(max_length=10, required=False)

    def  clean_tel(self):
        data = self.cleaned_data['tel']
        if data.isdigit():
            pass
        else:
            self.add_error('tel', "หมายเลขโทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
        if len(str(data)) == 10:
            pass
        else:
            self.add_error('tel', "หมายเลขโทรศัพท์ต้องมี 10 หลัก")
        return data

    def clean(self):
        cleaned_data = super().clean()
        tel = cleaned_data.get('tel')
        email = cleaned_data.get('email')
        print(tel)
        print(email)
        if tel and not email:
            raise forms.ValidationError("ต้องกรอก Email หรือ Mobile Number")
        elif email and not tel:
            raise forms.ValidationError("ต้องกรอก Email หรือ Mobile Number")
        elif not tel and not email:
            raise forms.ValidationError("ต้องกรอก Email หรือ Mobile Number")
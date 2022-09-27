from django import forms

from .models import Reserve

class ReserveForm(forms.ModelForm):
    """
    予約フォームの自作
    """

    class Meta:
        """
        モデルReserveの各フィールドウィジェットを
        Bootstrap使用にカスタマイズ
        """
        model = Reserve
        fields = ('reserve_date', 'reserve_num', 'reserve_time', 'name', 'email', 'tel', 'comment')
        widgets = {
                'reserve_date': forms.Select(attrs={
                    'class': 'form-select',
                    'name': 'reserve_date',
                    'placeholder': '予約日',
                }),
                'reserve_num': forms.Select(attrs={
                    'class': 'form-select',
                    'name': 'reserve_num',
                    'placeholder': '人数',
                }),
                'reserve_time': forms.Select(attrs={
                    'class': 'form-select',
                    'name': 'reserve_time',
                    'placeholder': '時間',
                }),
                'name': forms.TextInput(attrs={
                    'class': 'form-control',
                    'name': 'name',
                    'placeholder': '氏名',
                }),
                'email': forms.EmailInput(attrs={
                    'class': 'form-control',
                    'name': 'email',
                    'placeholder': 'メールアドレス',
                }),
                'tel': forms.TextInput(attrs={
                    'type': 'tel',
                    'class': 'form-control',
                    'name': 'tel',
                    'placeholder': '電話番号',
                    }),
                'comment': forms.Textarea(attrs={
                    'class': 'form-control',
                    'name': 'reserve_time',
                    'placeholder': '備考欄',
                }),
        }

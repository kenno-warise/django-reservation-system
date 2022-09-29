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
        labels = { # 各フィールドのラベルを設定
                'reserve_date': '【1】 予約日を選択',
                'reserve_num': '【2】 予約人数を選択',
                'reserve_time': '【3】 予約時間を選択',
                'name': '【4】 予約情報を選択',
                'comment': '【5】 備考欄',
        }
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
                    'placeholder': 'お名前（山田　太郎（ヤマダ　タロウ）',
                }),
                'email': forms.EmailInput(attrs={
                    'class': 'form-control',
                    'name': 'email',
                    'placeholder': 'メールアドレス（sample@example.com',
                }),
                'tel': forms.TextInput(attrs={
                    'type': 'tel',
                    'class': 'form-control',
                    'name': 'tel',
                    'placeholder': '電話番号（xxx-xxxx-xxxx',
                    }),
                'comment': forms.Textarea(attrs={
                    'class': 'form-control',
                    'name': 'reserve_time',
                    'placeholder': '備考欄',
                }),
        }

        # バリデーションエラーメッセージ
        error_messages = {
                "reserve_date": {
                    "required": "予約日を選択してください！",
                },
                "reserve_num": {
                    "required": "人数を選択してください！",
                },
                "reserve_time": {
                    "required": "時間を選択してください！",
                },
                "name": {
                    "required": "お名前を入力してください！",
                },
                "email": {
                    "required": "Emailを入力してください！",
                },
                "tel": {
                    "required": "電話番号を入力してください！",
                },
        }

    """
    # カスタムクリーンメソッド    
    def clean_tel(self):
        import re
        number = self.cleaned_data.get("tel")
        if number: # 正規表現を使用して正しい電話番号が入力されているかテスト
            raise forms.ValidationError("0000-0000-0000のように正しく入力してください。")
        return None
    """

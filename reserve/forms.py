from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Reserve, Shop

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ID'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'PASSWORD'
        """
        イテレーションで各css属性を取得
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        """


# 予約日
"""
設定機能で設定された予約可能日考慮

reserve_date_tup = ('', '予約日')
reservable_range_list = []

if Shop.objects.exists():
    # ここで「〇日前」というデータを取得
    shop_query = Shop.objects.select_related('reservable_date')[0].reservable_date.reservable_date
    print('↓↓')
    print(shop_query)
    # 余計な文字列を取り除き、int型に変換
    shop_query_int = int(shop_query.replace('日前', ''))
    # 現在から「〇日後」のdatetimeを取得
    one_day_later = timezone.now().date() + timezone.timedelta(days=shop_query_int)
    # 予約可能範囲として〇日後から約１ヵ月先の予約が可能
    for r in range(32):
        date = one_day_later + timezone.timedelta(days=r)
        reservable_range_list.append((date, date))
else: # Shopテーブルにデータが存在しない場合
    now_date = timezone.now().date()
    for i in range(1, 31):
        date = now_date + timezone.timedelta(days=i)
        reservable_range_list.append((date, date))
reservable_range_list.insert(0, reserve_date_tup)
choices_date = tuple(reservable_range_list)

# 予約人数
reserve_num_tup = ('', '予約人数')
if Shop.objects.exists():
    # ForignKey先のデータを取得し予約画面で表示
    shop_querys = Shop.objects.select_related('max_reserve_num')[0].max_reserve_num.max_reserve_num
    shop_querys = range(1, shop_querys+1)
    num_data_list = [(query, query) for query in shop_querys]
else:
    num_data_list = []
    for i in range(1, 5):
        num_data_list.append((i, i))
num_data_list.insert(0, reserve_num_tup)
choices_num = tuple(num_data_list)

# 予約時間

1時間当たりの予約時間考慮する

reserve_time_tup = ('', '予約時間')
try:
    if Shop.objects.all():
        shop_querys = Shop.objects.values_list('start_time')
        time_data_list = [(query[0], query[0]) for query in shop_querys]
    else:
        time_data_list = []
except:
    time_data_list = []
if not time_data_list:
    timenow = timezone.datetime(2022, 10, 1, 17, 00)
    for i in range(5):
        time = timenow + timezone.timedelta(hours=i)
        time_data_list.append((time.time(), time.time()))
time_data_list.insert(0, reserve_time_tup)
choices_time = tuple(time_data_list)
"""
class ReserveForm_2(forms.ModelForm):
    print('Hello')
    """
    models.pyでchoicesの定義をしていたが、forms.pyで処理することにしたので、
    ReserveFormの仮クラスとしてReserveForm_2を定義しChoiceFieldをそれぞれ作成。
    よって今後はこちらのクラスを本格的に使用していく。
    """
    # 予約日
    """
    設定機能で設定された予約可能日考慮
    """
    reserve_date_tup = ('', '予約日')
    reservable_range_list = []

    if Shop.objects.exists():
        # ここで「〇日前」というデータを取得
        shop_query = Shop.objects.select_related('reservable_date')[0].reservable_date.reservable_date
        print('↓↓')
        print(shop_query)
        # 余計な文字列を取り除き、int型に変換
        shop_query_int = int(shop_query.replace('日前', ''))
        # 現在から「〇日後」のdatetimeを取得
        one_day_later = timezone.now().date() + timezone.timedelta(days=shop_query_int)
        # 予約可能範囲として〇日後から約１ヵ月先の予約が可能
        for r in range(32):
            date = one_day_later + timezone.timedelta(days=r)
            reservable_range_list.append((date, date))
    else: # Shopテーブルにデータが存在しない場合
        now_date = timezone.now().date()
        for i in range(1, 31):
            date = now_date + timezone.timedelta(days=i)
            reservable_range_list.append((date, date))
    reservable_range_list.insert(0, reserve_date_tup)
    choices_date = tuple(reservable_range_list)

    # 予約人数
    reserve_num_tup = ('', '予約人数')
    if Shop.objects.exists():
        # ForignKey先のデータを取得し予約画面で表示
        shop_querys = Shop.objects.select_related('max_reserve_num')[0].max_reserve_num.max_reserve_num
        shop_querys = range(1, shop_querys+1)
        num_data_list = [(query, query) for query in shop_querys]
    else:
        num_data_list = []
        for i in range(1, 5):
            num_data_list.append((i, i))
    num_data_list.insert(0, reserve_num_tup)
    choices_num = tuple(num_data_list)
    
    # 予約時間
    """
    1時間当たりの予約時間考慮する
    """
    reserve_time_tup = ('', '予約時間')
    try:
        if Shop.objects.all():
            shop_querys = Shop.objects.values_list('start_time')
            time_data_list = [(query[0], query[0]) for query in shop_querys]
        else:
            time_data_list = []
    except:
        time_data_list = []
    if not time_data_list:
        timenow = timezone.datetime(2022, 10, 1, 17, 00)
        for i in range(5):
            time = timenow + timezone.timedelta(hours=i)
            time_data_list.append((time.time(), time.time()))
    time_data_list.insert(0, reserve_time_tup)
    choices_time = tuple(time_data_list)
    
    reserve_date = forms.fields.ChoiceField(
            choices=choices_date,
            label='【1】 予約日を選択',
            widget=forms.Select(attrs={
                'class': 'form-select',
                'name': 'reserve_date',
                'placeholder': '予約日',
                }),
            error_messages={
                "required": "予約日を選択してください！",
                },
            )
    reserve_num = forms.fields.ChoiceField(
            choices=choices_num,
            label='【2】 予約人数を選択',
            widget=forms.Select(attrs={
                'class': 'form-select',
                'name': 'reserve_num',
                'placeholder': '予約人数',
                }),
            error_messages={
                "required": "人数を選択してください！",
                },
            )
    reserve_time = forms.fields.ChoiceField(
            choices=choices_time,
            label='【2】 予約時間を選択',
            widget=forms.Select(attrs={
                'class': 'form-select',
                'name': 'reserve_time',
                'placeholder': '予約時間',
                }),
            error_messages={
                "required": "時間を選択してください！",
                },
            )

    class Meta:
        """
        モデルReserveの各フィールドウィジェットを
        Bootstrap使用にカスタマイズ
        """
        model = Reserve
        fields = ('reserve_date', 'reserve_num', 'reserve_time', 'name', 'email', 'tel', 'comment')
        labels = { # 各フィールドのラベルを設定
                'name': '【4】 予約情報を選択',
                'comment': '【5】 備考欄',
                }
        widgets = {
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


class ReserveForm(forms.ModelForm):
    """
    予約フォームの自作（注）
    注：ReserveForm_2を使用するように修正する
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


class ShopForm(forms.ModelForm):
    """設定フォームの自作"""

    class Meta:
        model = Shop
        fields = ('reservable_date', 'start_time', 'end_time', 'max_reserve_num')
        widgets = {
                'reservable_date': forms.Select(attrs={
                    'class': 'form-select',
                    'name': 'reservable_date',
                    'placeholder': '予約可能日',
                }),
                'start_time': forms.Select(attrs={
                    'class': 'form-select',
                    'name': 'start_time',
                    'placeholder': '開始時間',
                }),
                'end_time': forms.Select(attrs={
                    'class': 'form-select',
                    'name': 'end_time',
                    'placeholder': '終了時間',
                }),
                'max_reserve_num': forms.Select(attrs={
                    'class': 'form-select',
                    'name': 'max_reserve_num',
                    'placeholder': '上限人数',
                }),
        }
        # バリデーションエラーメッセージ
        error_messages = {
                "reserve_date": {
                    "required": "予約日を選択してください！",
                },
                "start_time": {
                    "required": "選択してください",
                },
                "end_time": {
                    "required": "選択してください",
                },
                "max_reserve_num": {
                    "required": "選択してください",
                },
        }

class EveryYearForm(forms.Form):
    """
    予約リスト画面のプルダウンで使うデータを取得
    """
    year_and_month = Reserve.objects.values_list('reserve_date')

    # choiece用の年を取得
    year_list = [t[0].year for t in year_and_month]
    year_unique = list(set(year_list))
    year_list_tuple = [(str(y), str(y)+'年') for y in year_unique]
    # year_list_tuple = [('2022', '2022年'), ('2023', '2023年')]
    
    # choiece用の月を取得
    month_list = [t[0].month for t in year_and_month]
    # ↓setのみだと並びがランダムになってしまうので、sortedで並びを保持する
    month_unique = list(sorted(set(month_list), key=month_list.index))
    month_list_tuple = [(str(y), str(y)+'月') for y in month_unique]
    # month_list_tuple = [('9', '9月'), ('10', '10月')]

    years = tuple(year_list_tuple)
    months = tuple(month_list_tuple)

    year_pulldown = forms.ChoiceField(
            choices=years,
            widget=forms.widgets.Select(attrs={'class': 'form-select'}),
    )
    month_pulldown = forms.ChoiceField(
            choices=months,
            widget=forms.widgets.Select(attrs={'class': 'form-select'}),
    )

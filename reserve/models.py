from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

class Shop(models.Model):
    """
    [店舗情報テーブル]
    予約可能日:reservable_date
    営業開始:start_time
    営業終了:end_time
    予約上限人数:max_reserve_num
    """
    reservable_date = models.DateField(verbose_name='予約可能日')
    start_time = models.TimeField(verbose_name='開店時間')
    end_time = models.TimeField(verbose_name='閉店時間')
    max_reserve_num = models.IntegerField(verbose_name='１時間当たりの予約上限人数')

    def __str__(self):
        return str(self.reservable_date)

class Reserve(models.Model):
    """
    [予約情報テーブル]
    予約日:reserve_date
    予約時間:reserve_time
    予約人数:reserve_num
    氏名:name
    メールアドレス:email
    電話番号:tel
    備考:comment
    """

    """
    各フィールド引数のchoicesに指定するためのタプル変数作成
    Shopモデルがまだ未完成なので、その場しのぎの実装
    """
    # 予約日
    reserve_date_tup = ('', '予約日')
    try: # djangoDBのテーブルエラー回避のためのtry文
        if Shop.objects.all():
            shop_querys = Shop.objects.values_list('reservable_date')
            shop_data_list = [(query[0], query[0]) for query in shop_querys]
        else:
            shop_data_list = []
    except:
        shop_data_list = []
    if not shop_data_list:
        datenow = timezone.now().date()
        for i in range(7):
            date = datenow + timezone.timedelta(days=i)
            shop_data_list.append((date, date))
    shop_data_list.insert(0, reserve_date_tup)
    choices_date = tuple(shop_data_list)

    # 予約人数
    reserve_num_tup = ('', '予約人数')
    try:
        if Shop.objects.all():
            shop_querys = Shop.objects.values_list('max_reserve_num')
            shop_querys = range(1, shop_querys[0][0]+1)
            num_data_list = [(query, query) for query in shop_querys]
        else:
            num_data_list = []
    except:
        num_data_list = []
    if not num_data_list:
        for i in range(1, 6):
            num_data_list.append((i, i))
    num_data_list.insert(0, reserve_num_tup)
    choices_num = tuple(num_data_list)

    # 予約時間
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

    reserve_date = models.DateField(
            verbose_name='予約日',
            max_length=20,
            choices=choices_date,
            unique=True,
    )
    # reserve_date = models.ForeignKey(Shop, on_delete=models.PROTECT, verbose_name='予約日')

    reserve_time = models.TimeField(
            verbose_name='予約時間',
            max_length=10,
            choices=choices_time,
            unique=True,
    )
    
    # reserve_time = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='予約時間')
    reserve_num = models.IntegerField(
            verbose_name='予約人数',
            # max_length=10,
            choices=choices_num,
            unique=True,
    )
    name = models.CharField(verbose_name='氏名', max_length=20)
    email = models.EmailField(verbose_name='メールアドレス', max_length=100, unique=True)
    # RegexValidatorを使用すると正規表現でバリデーションをかけることができる
    num_regex = RegexValidator(
            regex=r'^0[789]0-\d{4}-\d{4}',
            message=("「例：080-1234-5678」のように入力してください。")
    )
    tel = models.CharField(
            verbose_name='電話番号',
            max_length=20,
            validators=[num_regex],
            unique=True,
    )
    comment = models.TextField(
            null=True, # DB内にNULLとして空の値を保持する
            blank=True, # フィールドがブランク（空白）になることが許容される
            verbose_name='備考欄',
            max_length=1000,
    )
    """
    def __str__(self):
        return str(self.reserve_date)
    """

# Create your models here.

from django.db import models

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
    reserve_date = models.DateField(verbose_name='予約日')
    reserve_time = models.TimeField(verbose_name='予約時間')
    reserve_num = models.IntegerField(verbose_name='予約人数', default=1)
    name = models.CharField(verbose_name='氏名', max_length=100)
    email = models.EmailField(verbose_name='メールアドレス', max_length=254)
    tel = models.CharField(verbose_name='電話番号', max_length=20)
    comment = models.TextField(verbose_name='備考欄')

    def __str__(self):
        return str(self.reserve_date)

class Shop(models.Model):
    """
    [店舗情報テーブル]
    予約可能日:reservable_date
    営業開始:start_time
    営業終了:end_time
    予約上限人数:max_reserve_num
    """
    reservable_date = models.IntegerField(verbose_name='予約可能日')
    start_time = models.TimeField(verbose_name='開店時間')
    end_time = models.TimeField(verbose_name='閉店時間')
    max_reserve_num = models.IntegerField(verbose_name='１時間当たりの予約上限人数')




# Create your models here.

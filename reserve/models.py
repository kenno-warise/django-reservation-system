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
    reserve_date = models.DateField()
    reserve_time = models.TimeField()
    reserve_num = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    tel = models.CharField(max_length=20)
    comment = models.TextField()

    def __str__(self):
        return self.reserve_date

class Shop(models.Model):
    """
    [店舗情報テーブル]
    予約可能日:reservable_date
    営業開始:start_time
    営業終了:end_time
    予約上限人数:max_reserve_num
    """
    reservable_date = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_reserve_num = models.IntegerField()

    def __str__(self):
        return self.reservable_date

# Create your models here.

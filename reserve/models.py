from django.core.validators import RegexValidator
from django.db import models


class SetIntegration(models.Model):
    set_name = models.CharField(max_length=20, verbose_name="設定ネーム")

    def __str__(self):
        return self.set_name


class ReservableDate(models.Model):
    name = models.ForeignKey(
        SetIntegration, verbose_name="設定ネーム", on_delete=models.CASCADE
    )
    reservable_date = models.CharField(max_length=10, verbose_name="予約可能時間")

    def __str__(self):
        return self.reservable_date


class StartTime(models.Model):
    name = models.ForeignKey(
        SetIntegration, verbose_name="設定ネーム", on_delete=models.CASCADE
    )
    start_time = models.TimeField(verbose_name="開始時間")

    def __str__(self):
        return str(self.start_time)


class EndTime(models.Model):
    name = models.ForeignKey(
        SetIntegration, verbose_name="設定ネーム", on_delete=models.CASCADE
    )
    end_time = models.TimeField(verbose_name="終了時間")

    def __str__(self):
        return str(self.end_time)


class MaxReserveNum(models.Model):
    name = models.ForeignKey(
        SetIntegration, verbose_name="設定ネーム", on_delete=models.CASCADE
    )
    max_reserve_num = models.IntegerField(verbose_name="予約上限人数")

    def __str__(self):
        return str(self.max_reserve_num)


class Shop(models.Model):
    """
    [店舗情報テーブル]
    予約可能日:reservable_date
    営業開始:start_time
    営業終了:end_time
    予約上限人数:max_reserve_num

    メモ：
    ForeignKeyを使っている理由は、データを保存する際にプルダウンで取得できるようにする必要があったため
    他の方法は、CharFieldでchoicesを設定しようと思ったが、ソースを変更する必要があるため辞めた
    """

    reservable_date = models.ForeignKey(
        ReservableDate, verbose_name="予約可能日", on_delete=models.CASCADE
    )
    start_time = models.ForeignKey(
        StartTime, verbose_name="開店時間", on_delete=models.CASCADE
    )
    end_time = models.ForeignKey(EndTime, verbose_name="閉店時間", on_delete=models.CASCADE)
    max_reserve_num = models.ForeignKey(
        MaxReserveNum, verbose_name="１時間当たりの予約上限人数", on_delete=models.CASCADE
    )

    def __str__(self):
        return "Shopの編集"


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

    reserve_date = models.DateField(
        verbose_name="予約日",
        max_length=20,
    )
    reserve_time = models.TimeField(
        verbose_name="予約時間",
        max_length=10,
        # unique=True,
        # error_messages={
        #    'unique':'この時間帯はご予約できません。',
        # }
    )
    reserve_num = models.IntegerField(
        verbose_name="予約人数",
    )
    name = models.CharField(verbose_name="氏名", max_length=20)
    email = models.EmailField(
        verbose_name="メールアドレス",
        max_length=100,
        # unique=True,
        # error_messages={
        #    'unique':'こちらのメールアドレスで既にご予約がされています。',
        # }
    )
    # RegexValidatorを使用すると正規表現でバリデーションをかけることができる
    num_regex = RegexValidator(
        regex=r"^0[789]0-\d{4}-\d{4}", message=("「例：080-1234-5678」のように入力してください。")
    )
    tel = models.CharField(
        verbose_name="電話番号",
        max_length=20,
        validators=[num_regex],
        unique=True,
        error_messages={
            "unique": "こちらの電話番号で既にご予約がされています。",
        },
    )
    comment = models.TextField(
        null=True,  # DB内にNULLとして空の値を保持する
        blank=True,  # フィールドがブランク（空白）になることが許容される
        verbose_name="備考欄",
        max_length=1000,
    )

    def __str__(self):
        return "Reserveの編集"


# Create your models here.

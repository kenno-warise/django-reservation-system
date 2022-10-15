from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import ReserveForm
from .models import (EndTime, MaxReserveNum, ReservableDate, SetIntegration,
                     Shop, StartTime)


def create_models_and_choicedata():
    SetIntegration.objects.create(set_name='name')
    name = SetIntegration.objects.get(id=1)

    ReservableDate.objects.create(name=name, reservable_date='1日前')
    StartTime.objects.create(name=name, start_time='9:00')
    EndTime.objects.create(name=name, end_time='12:00')
    MaxReserveNum.objects.create(name=name, max_reserve_num=1)

    reservable_date = ReservableDate.objects.get(id=1)
    starttime = StartTime.objects.get(id=1)
    endtime = EndTime.objects.get(id=1)
    max_reserve_num = MaxReserveNum.objects.get(id=1)

    Shop.objects.create(
            reservable_date=reservable_date,
            start_time=starttime,
            end_time=endtime,
            max_reserve_num=max_reserve_num,
    )

    # 予約日
    reserve_date_tup = ("", "予約日")
    reservable_range_list = []
    # 予約人数
    reserve_num_tup = ("", "予約人数")
    num_data_list = []
    # 予約時間
    reserve_time_tup = ("", "予約時間")
    time_data_list = []
    
    if Shop.objects.exists():
        # 予約時間
        # ここで「〇日前」というデータを取得
        shop_query = Shop.objects.select_related("reservable_date")[
            0
        ].reservable_date.reservable_date
        # 余計な文字列を取り除き、int型に変換
        shop_query_int = int(shop_query.replace("日前", ""))
        # timedeltaオブジェクトの生成
        timedelta = timezone.timedelta(days=shop_query_int)
        # 現在から「〇日後」のdatetimeを取得
        one_day_later = timezone.now().date() + timedelta
        # 予約可能範囲として〇日後から約１ヵ月先の予約が可能
        for r in range(32):
            date = one_day_later + timezone.timedelta(days=r)
            reservable_range_list.append((str(date), date))
    
        # 予約人数
        # ForignKey先のデータを取得し予約画面で表示
        shop_querys = Shop.objects.select_related("max_reserve_num")[
            0
        ].max_reserve_num.max_reserve_num
        shop_querys = range(1, shop_querys + 1)
        num_data_list = [(query, query) for query in shop_querys]
        
        # 予約時間
        start_time_query = Shop.objects.select_related("start_time")[
                0
        ].start_time.start_time
        end_time_query = Shop.objects.select_related("end_time")[0].end_time.end_time
        # 0時間のdatetimeオブジェクトを作成、後にリスト内包表記で使用
        date_obj = start_time_query.replace(0)
        # 各種datetimeオブジェクトからint型ｎ変換
        start_time_int = start_time_query.hour
        end_time_int = end_time_query.hour
        # int型にした変数をrangeに挿入
        time_range = range(start_time_int, end_time_int)
        # リスト内包表記でchoices用のリスト内タプルを作成
        time_data_list = [
            (date_obj.replace(t), date_obj.replace(t)) for t in time_range
        ]
    
    # 予約日
    reservable_range_list.insert(0, reserve_date_tup)
    choices_date = tuple(reservable_range_list)
    # 予約人数
    num_data_list.insert(0, reserve_num_tup)
    choices_num = tuple(num_data_list)
    # 予約時間
    time_data_list.insert(0, reserve_time_tup)
    choices_time = tuple(time_data_list)

    return choices_date, choices_num, choices_time

class IndexTests(TestCase):
    def test_no_shopdata(self):
        """
        予約画面
        """
        response = self.client.get(reverse("reserve:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIs(Shop.objects.exists(), False)
        self.assertContains(response, "現在ご予約は受け付けておりません")

    def test_post_no_field_is_invalid(self):
        """
        必須項目が何も選択されずにPOSTされた場合のテスト
        """
        SetIntegration.objects.create(set_name='name')
        name = SetIntegration.objects.get(id=1)

        ReservableDate.objects.create(name=name, reservable_date='1日前')
        StartTime.objects.create(name=name, start_time='9:00')
        EndTime.objects.create(name=name, end_time='12:00')
        MaxReserveNum.objects.create(name=name, max_reserve_num=1)

        reservable_date = ReservableDate.objects.get(id=1)
        starttime = StartTime.objects.get(id=1)
        endtime = EndTime.objects.get(id=1)
        max_reserve_num = MaxReserveNum.objects.get(id=1)

        Shop.objects.create(
                reservable_date=reservable_date,
                start_time=starttime,
                end_time=endtime,
                max_reserve_num=max_reserve_num,
        )
        response = self.client.post("/index/", {
            'reserve_date':'',
            'reserve_num':1,
            'reserve_time':'9:00',
            'name':'name',
            'email':'example@ex.com',
            'tel':'080-1111-1111',
            'comment': '',
        })
        self.assertIs(Shop.objects.exists(), True)
        self.assertFormError(response, 'form', 'reserve_date', '予約日を選択してください！')

    def test_post_is_valid_session_redirect(self):
        """
        POSTされて全て有効であった場合、sessionに保存されてconfirmにリダイレクトされる
        """
        # choiceデータを代入
        choices_date, choices_num, choices_time = create_models_and_choicedata()
        
        field_data = {
            'reserve_date':'2022-10-16',
            'reserve_num':1,
            'reserve_time':'10:00:00',
            'name':'name',
            'email':'example@ex.com',
            'tel':'080-1111-1111',
            'comment': '',
        }
        response = self.client.post("/index/", field_data)
        form = ReserveForm(field_data)
        form.fields["reserve_date"].choices = choices_date
        form.fields["reserve_num"].choices = choices_num
        form.fields["reserve_time"].choices = choices_time
        session = self.client.session
        session['form-data'] = field_data
        self.assertIs(Shop.objects.exists(), True)
        self.assertRedirects(response, reverse('reserve:confirm'))


class ConfirmTest(TestCase):
    """予約確認画面"""
    def test_no_sessionfield_index_redirect(self):
        response = self.client.get(reverse('reserve:confirm'))
        session_data = self.client.session.get('form_data')
        self.assertRedirects(response, reverse('reserve:index'))

# Create your tests here.

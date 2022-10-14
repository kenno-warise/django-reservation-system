from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mass_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from config import settings

from .forms import EveryYearForm, LoginForm, ReserveForm, ShopForm
from .models import Reserve, Shop


def index(request):
    """予約画面"""
    """
    以下は機能設定で考慮された各種プルダウンで表示するためのchoices変数の作成
    """
    # 予約日
    reserve_date_tup = ("", "予約日")
    reservable_range_list = []

    if Shop.objects.exists():
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
    else:  # Shopテーブルにデータが存在しない場合
        now_date = timezone.now().date()
        for i in range(1, 31):
            date = now_date + timezone.timedelta(days=i)
            reservable_range_list.append((date, date))
    reservable_range_list.insert(0, reserve_date_tup)
    choices_date = tuple(reservable_range_list)

    # 予約人数
    reserve_num_tup = ("", "予約人数")
    if Shop.objects.exists():
        # ForignKey先のデータを取得し予約画面で表示
        shop_querys = Shop.objects.select_related("max_reserve_num")[
            0
        ].max_reserve_num.max_reserve_num
        shop_querys = range(1, shop_querys + 1)
        num_data_list = [(query, query) for query in shop_querys]
    else:
        num_data_list = []
        for i in range(1, 5):
            num_data_list.append((str(i), i))
    num_data_list.insert(0, reserve_num_tup)
    choices_num = tuple(num_data_list)

    # 予約時間
    reserve_time_tup = ("", "予約時間")
    if Shop.objects.exists():
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
    else:
        time_data_list = []
        timenow = timezone.datetime(2022, 10, 1, 17, 00)
        for i in range(5):
            time = timenow + timezone.timedelta(hours=i)
            time_data_list.append((time.time(), time.time()))
    time_data_list.insert(0, reserve_time_tup)
    choices_time = tuple(time_data_list)

    if request.method == "POST":
        form = ReserveForm(request.POST)

        form.fields["reserve_date"].choices = choices_date
        form.fields["reserve_num"].choices = choices_num
        form.fields["reserve_time"].choices = choices_time
        if form.is_valid():
            # 検証を通過したらPOSTされたデータをsession用のDBに保持し、confirmへリダイレクト
            request.session["form_data"] = request.POST
            return redirect("reserve:confirm")
        else:  # 検証に失敗したら
            # commentフィールド以外で１つでも未記入のフィールドが存在していたら
            # 各フィールドのclass属性にis-invalid（失敗）もしくわis-valid（クリア）を追記する
            for field in form:
                if field.errors:
                    # フォームが未入力のフィールド
                    # comment以外で入力されていないフィールドはclass属性にis-invalidを追記する
                    form[field.name].field.widget.attrs["class"] += " is-invalid"
                else:
                    if (
                        field.name != "comment"
                    ):  # commentフィールドはnull, blank共にTrueなので空でもOK
                        # フォームに入力されているフィールド
                        # comment以外で入力されたフィールドはclass属性にis-validを追記する
                        form[field.name].field.widget.attrs["class"] += " is-valid"
    else:
        # セッションに入力途中のデータがあればそれを使う
        form = ReserveForm(request.session.get("form_data"))

        form.fields["reserve_date"].choices = choices_date
        form.fields["reserve_num"].choices = choices_num
        form.fields["reserve_time"].choices = choices_time

    return render(request, "reserve/index.html", {"form": form})


def confirm(request):
    """予約確認画面"""
    # sessionに保持されているデータを取得
    session_form_data = request.session.get("form_data")

    if session_form_data is None:  # sessionデータが空であれば入力ページにリダイレクトされる
        return redirect("reserve:index")

    """
    以下は機能設定で考慮された各種プルダウンで表示するためのchoices変数の作成
    """
    # 予約日
    reserve_date_tup = ("", "予約日")
    reservable_range_list = []

    if Shop.objects.exists():
        # ここで「〇日前」というデータを取得
        shop_query = Shop.objects.select_related("reservable_date")[
            0
        ].reservable_date.reservable_date
        # 余計な文字列を取り除き、int型に変換
        shop_query_int = int(shop_query.replace("日前", ""))
        # 現在から「〇日後」のdatetimeを取得
        one_day_later = timezone.now().date() + timezone.timedelta(days=shop_query_int)
        # 予約可能範囲として〇日後から約１ヵ月先の予約が可能
        for r in range(32):
            date = one_day_later + timezone.timedelta(days=r)
            reservable_range_list.append((str(date), date))
    else:  # Shopテーブルにデータが存在しない場合
        now_date = timezone.now().date()
        for i in range(1, 31):
            date = now_date + timezone.timedelta(days=i)
            reservable_range_list.append((date, date))
    reservable_range_list.insert(0, reserve_date_tup)
    choices_date = tuple(reservable_range_list)

    # 予約人数
    reserve_num_tup = ("", "予約人数")
    if Shop.objects.exists():
        # ForignKey先のデータを取得し予約画面で表示
        shop_querys = Shop.objects.select_related("max_reserve_num")[
            0
        ].max_reserve_num.max_reserve_num
        shop_querys = range(1, shop_querys + 1)
        num_data_list = [(query, query) for query in shop_querys]
    else:
        num_data_list = []
        for i in range(1, 5):
            num_data_list.append((str(i), i))
    num_data_list.insert(0, reserve_num_tup)
    choices_num = tuple(num_data_list)

    # 予約時間
    reserve_time_tup = ("", "予約時間")
    if Shop.objects.exists():
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
    else:
        time_data_list = []
        timenow = timezone.datetime(2022, 10, 1, 17, 00)
        for i in range(5):
            time = timenow + timezone.timedelta(hours=i)
            time_data_list.append((time.time(), time.time()))
    time_data_list.insert(0, reserve_time_tup)
    choices_time = tuple(time_data_list)
    # sessionから予約日と予約時間を使用してDBに同じ日時のデータが保存されていないかフィルタリングする
    reserve_query = Reserve.objects.filter(
        reserve_date=session_form_data["reserve_date"],
        reserve_time=session_form_data["reserve_time"],
    )
    # Shopテーブルから現在の1時間当たりの予約上限数を取得する
    shop_max_num = Shop.objects.select_related("max_reserve_num")[
        0
    ].max_reserve_num.max_reserve_num
    # Reserveテーブルから取得した日時データの予約人数を合計する
    reserve_max_num_sum = sum([query.reserve_num for query in reserve_query])
    # 予約上限数と合計値を引き算する
    remaining_limit = abs(shop_max_num - reserve_max_num_sum)
    # 残りの予約上限人数以下であればresultはNone値を代入する
    if remaining_limit >= int(session_form_data["reserve_num"]):
        result = None
    else:  # 予約上限人数以上であればエラー処理のための要素をresultに代入する
        result = remaining_limit

    if request.method == "POST":

        if remaining_limit >= int(session_form_data["reserve_num"]):  # 残り数以下であれば予約を保存する
            form = ReserveForm(session_form_data)
            # 以下の代入がなければ各フォームがエラーとなってしまう
            form.fields["reserve_date"].choices = choices_date
            form.fields["reserve_num"].choices = choices_num
            form.fields["reserve_time"].choices = choices_time

            if form.is_valid():
                form.save()

                # 予約が保存されたらメールの送信処理に入る
                subject_reserve = "ご予約ありがとうございます"
                subject_admin = "予約を至りました"
                message = "予約日: {}\n予約時間: {}\n予約人数: {}\n予約者: {}\nEmail: {}\nTEL: {}\nComment: {}".format(
                    form.data["reserve_date"],
                    form.data["reserve_time"],
                    form.data["reserve_num"],
                    form.data["name"],
                    form.data["email"],
                    form.data["tel"],
                    form.data["comment"],
                )
                from_email = ""  # 送信者（送信者のアドレスはsettingsに設定された値
                recipient_list = [form.data["email"]]  # 受信者
                recipient_admin = [settings.EMAIL_HOST_USER]

                # 予約者送信設定
                message_reserve = (subject_reserve, message, from_email, recipient_list)
                # 管理人送信設定
                message_admin = (subject_admin, message, from_email, recipient_admin)
                # 予約者と管理人にそれぞれメールを送信
                send_mass_mail((message_reserve, message_admin))

                return redirect("reserve:complete")

    """
    reserve_dateとreserve_timeのsession変数はstr型となって格納されるため
    ここではdatetimeモジュールを使用してdatetime型へ変換する。
    よってテンプレートフィルタで「date」フィルタが使えるようになる
    """
    session_form_data["reserve_date"] = timezone.datetime.strptime(
        session_form_data["reserve_date"], "%Y-%m-%d"
    ).date()
    session_form_data["reserve_time"] = timezone.datetime.strptime(
        session_form_data["reserve_time"], "%H:%M:%S"
    ).time()

    context = {
        "session_form_data": session_form_data,
        "result": result,
    }
    return render(request, "reserve/confirm.html", context)


def complete(request):
    """予約完了画面"""
    """
    session変数に保持されている予約データを空にする
    """
    request.session.pop("form_data", None)
    return render(request, "reserve/complete.html")


class Login(LoginView):
    """ログイン画面"""

    form_class = LoginForm
    template_name = "reserve/login.html"


class Logout(LogoutView):
    """ログアウト"""


@login_required
def reserve_list(request):
    """予約リスト画面"""
    """
    プルダウンの初期値は絞り込みで表示する
    """
    if Shop.objects.exists():  # クエリセットの存在チェック
        shop_id = Shop.objects.values("id").get()["id"]
    else:
        shop_id = None
    form = EveryYearForm()
    # 予約日と予約時間で絞り込んだ日付順に当日以降のデータを取得して表示する
    reserves = Reserve.objects.order_by(
        "reserve_date", "reserve_time"
    ).filter(  # 予約リストでデフォルト表示されるデータをフィルタリング
        reserve_date__gte=timezone.now(),
        reserve_date__year=form.years[0][0],
        reserve_date__month=form.months[0][0],
    )
    context = {
        "reserves": reserves,
        "shop_id": shop_id,
        "form": form,
    }
    return render(request, "reserve/reserve_list.html", context)


def pulldown_access(request):
    """予約リスト画面のプルダウンによる非同期処理"""
    # javascriptから送られてきた要素を取得
    select_value = request.POST.get("year_val")
    if not select_value:  # 値が存在しなければデフォルトの予約リスト画面を表示
        return redirect("reserve:reserve_list")
    # 「,」に合わせてsplitする
    select_value = select_value.split(",")
    result_query = Reserve.objects.order_by("reserve_date", "reserve_time").filter(
        reserve_date__gte=timezone.now(),
        reserve_date__year=int(select_value[0]),
        reserve_date__month=int(select_value[1]),
    )
    # javascriptでイテレーションするためにリスト内辞書に変換
    query_list = list(result_query.values())
    # 表記を日本人向け（デフォルトのフォーマット）にするため、曜日を設定
    weeks = {
        "Monday": "（月）",
        "Tuesday": "（火）",
        "Wednesday": "（水）",
        "Thursday": "（木）",
        "Friday": "（金）",
        "Saturday": "（土）",
        "Sunday": "（日）",
    }
    # デフォルトのフォーマットに合わせるため、各辞書のキーに代入
    for query in query_list:
        query["reserve_date"] = (
            query["reserve_date"].strftime("%m/%d")
            + weeks[query["reserve_date"].strftime("%A")]
        )
        query["reserve_time"] = query["reserve_time"].strftime("%H:%M")

    return JsonResponse({"query_list": query_list})


@login_required
def setting(request, id):
    """設定画面"""

    shop_404 = get_object_or_404(Shop, id=id)
    if request.method == "POST":
        form = ShopForm(request.POST, instance=shop_404)
        if form.is_valid():
            form.save()
            return redirect("reserve:index")
        else:  # 検証に失敗したら
            # １つでも未記入のフィールドが存在していたら
            # 各フィールドのclass属性にis-invalid（失敗）もしくわis-valid（クリア）を追記する
            for field in form:
                if field.errors:
                    # フォームが未入力のフィールド
                    # 入力されていないフィールドはclass属性にis-invalidを追記する
                    form[field.name].field.widget.attrs["class"] += " is-invalid"
                else:
                    # フォームに入力されているフィールド
                    # 入力されたフィールドはclass属性にis-validを追記する
                    form[field.name].field.widget.attrs["class"] += " is-valid"
    else:
        form = ShopForm(instance=shop_404)

    context = {
        "form": form,
        "shop_404": shop_404,
    }
    return render(request, "reserve/setting.html", context)


# Create your views here.

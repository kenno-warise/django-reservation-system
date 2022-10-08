from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ReserveForm, ReserveForm_2, LoginForm, ShopForm, EveryYearForm
from .models import Reserve, Shop

def index(request):
    """予約画面"""
    if request.method == "GET":
        if request.session.get('form_data') is None:
            form = ReserveForm_2()
            """
            以下は機能設定で考慮された各種プルダウンで表示するためのchoices変数の作成
            """

            # 予約日
            reserve_date_tup = ('', '予約日')
            reservable_range_list = []
        
            if Shop.objects.exists():
                # ここで「〇日前」というデータを取得
                shop_query = Shop.objects.select_related('reservable_date')[0].reservable_date.reservable_date
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
            reserve_time_tup = ('', '予約時間')
            if Shop.objects.exists():
                start_time_query = Shop.objects.select_related('start_time')[0].start_time.start_time
                end_time_query = Shop.objects.select_related('end_time')[0].end_time.end_time
                # 0時間のdatetimeオブジェクトを作成、後にリスト内包表記で使用
                date_obj = start_time_query.replace(0)
                # 各種datetimeオブジェクトからint型ｎ変換
                start_time_int = start_time_query.hour
                end_time_int = end_time_query.hour
                # int型にした変数をrangeに挿入
                time_range = range(start_time_int, end_time_int)
                # リスト内包表記でchoices用のリスト内タプルを作成
                time_data_list = [(date_obj.replace(t), date_obj.replace(t)) for t in time_range]
            else:
                time_data_list = []
                timenow = timezone.datetime(2022, 10, 1, 17, 00)
                for i in range(5):
                    time = timenow + timezone.timedelta(hours=i)
                    time_data_list.append((time.time(), time.time()))
            time_data_list.insert(0, reserve_time_tup)
            choices_time = tuple(time_data_list)
            
            form.fields['reserve_date'].choices = choices_date
            form.fields['reserve_num'].choices = choices_num
            form.fields['reserve_time'].choices = choices_time

        else:
            # セッションに入力途中のデータがあればそれを使う
            form = ReserveForm_2(request.session.get('form_data'))
    elif request.method == "POST":
        form = ReserveForm_2(request.POST)
        if form.is_valid():
            # 検証を通過したらPOSTされたデータをsession用のDBに保持し、confirmへリダイレクト
            request.session['form_data'] = request.POST
            return redirect('reserve:confirm')
        else: # 検証に失敗したら
            # commentフィールド以外で１つでも未記入のフィールドが存在していたら
            # 各フィールドのclass属性にis-invalid（失敗）もしくわis-valid（クリア）を追記する
            for field in form:
                if field.errors:
                    # フォームが未入力のフィールド
                    # comment以外で入力されていないフィールドはclass属性にis-invalidを追記する
                    form[field.name].field.widget.attrs['class'] += ' is-invalid'
                else:
                    if field.name != 'comment': # commentフィールドはnull, blank共にTrueなので空でもOK
                        # フォームに入力されているフィールド
                        # comment以外で入力されたフィールドはclass属性にis-validを追記する
                        form[field.name].field.widget.attrs['class'] += ' is-valid'
    return render(request, 'reserve/index.html', {'form':form})

def confirm(request):
    """予約確認画面"""
    from django.utils import timezone
    # sessionに保持されているデータを取得
    session_form_data = request.session.get('form_data')

    if session_form_data is None: # sessionデータが空であれば入力ページにリダイレクトされる
        return redirect('reserve:index')
    """
    reserve_dateとreserve_timeのsession変数はstr型となって格納されるため
    ここではdatetimeモジュールを使用してdatetime型へ変換する。
    よってテンプレートフィルタで「date」フィルタが使えるようになる
    """
    session_form_data['reserve_date'] = timezone.datetime.strptime(
            session_form_data['reserve_date'],
            '%Y-%m-%d'
    ).date()
    session_form_data['reserve_time'] = timezone.datetime.strptime(
            session_form_data['reserve_time'],
            '%H:%M:%S'
    ).time()

    if request.method == "POST":
        form = ReserveForm(session_form_data)
        if form.is_valid():
            form.save()
            return redirect('reserve:complete')
        print(form.errors)
    return render(request, 'reserve/confirm.html', {'session_form_data': session_form_data })

def complete(request):
    """予約完了画面"""
    """
    session変数に保持されている予約データを空にする
    """
    request.session.pop('form_data', None)
    return render(request, 'reserve/complete.html')

class Login(LoginView):
    """ログイン画面"""
    form_class = LoginForm
    template_name = 'reserve/login.html'

class Logout(LogoutView):
    """ログアウト"""

@login_required
def reserve_list(request):
    """予約リスト画面"""
    """
    プルダウンの初期値は絞り込みで表示する
    """
    if Shop.objects.exists(): # クエリセットの存在チェック
        shop_id = Shop.objects.values('id').get()['id']
    else:
        shop_id = None
    form = EveryYearForm()
    reserves = Reserve.objects.filter( # 予約リストでデフォルト表示されるデータをフィルタリング
            reserve_date__year=form.years[0][0],
            reserve_date__month=form.months[0][0],
    )
    context = {
            'reserves': reserves,
            'shop_id': shop_id,
            'form': form,
    }
    return render(request, 'reserve/reserve_list.html', context)

@login_required
def setting(request, id):
    """設定画面"""

    shop_404 = get_object_or_404(Shop, id=id)
    if request.method == "POST":
        form = ShopForm(request.POST, instance=shop_404)
        if form.is_valid():
            form.save()
            return redirect('reserve:index')
        else: # 検証に失敗したら
            # １つでも未記入のフィールドが存在していたら
            # 各フィールドのclass属性にis-invalid（失敗）もしくわis-valid（クリア）を追記する
            for field in form:
                if field.errors:
                    # フォームが未入力のフィールド
                    # 入力されていないフィールドはclass属性にis-invalidを追記する
                    form[field.name].field.widget.attrs['class'] += ' is-invalid'
                else:
                    # フォームに入力されているフィールド
                    # 入力されたフィールドはclass属性にis-validを追記する
                    form[field.name].field.widget.attrs['class'] += ' is-valid'
    else:
        form = ShopForm(instance=shop_404)

    context = {
            'form': form,
            'shop_404': shop_404,
    }
    return render(request, 'reserve/setting.html', context)


# Create your views here.

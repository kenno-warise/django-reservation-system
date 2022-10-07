from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ReserveForm, LoginForm, ShopForm, EveryYearForm
from .models import Reserve, Shop

def index(request):
    """予約画面"""
    if request.method == "GET":
        # セッションに入力途中のデータがあればそれを使う
        form = ReserveForm(request.session.get('form_data'))
    elif request.method == "POST":
        form = ReserveForm(request.POST)
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
    print(form.years)
    print(form.months)
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

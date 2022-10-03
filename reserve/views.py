from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import ReserveForm, LoginForm

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
    return render(request, 'reserve/complete.html')

class Login(LoginView):
    """ログイン画面"""
    form_class = LoginForm
    # template_name = 'reserve/login.html'

def reserve_list(request):
    """予約リスト画面"""
    return render(request, 'reserve/reserve_list.html')

def setting(request):
    """設定画面"""
    return render(request, 'reserve/setting.html')

# Create your views here.

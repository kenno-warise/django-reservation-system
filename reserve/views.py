from django.shortcuts import render, redirect

from .forms import ReserveForm

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
    # sessionに保持されているデータを取得
    session_form_data = request.session.get('form_data')
    if session_form_data is None: # sessionデータが空であれば入力ページにリダイレクトされる
        return redirect('reserve:index')
    form = ReserveForm(session_form_data)
    if request.method == "POST":
        form.save()
        return redirect('reserve:complete')
    return render(request, 'reserve/confirm.html', {'form': form})

def complete(request):
    """予約完了画面"""
    return render(request, 'reserve/complete.html')

# Create your views here.

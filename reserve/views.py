from django.shortcuts import render, redirect

from .forms import ReserveForm

def index(request):
    if request.method == "GET":
        # セッションに入力途中のデータがあればそれを使う
        form = ReserveForm(request.session.get('form_data'))
    else:
        form = ReserveForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = request.POST
            # form.save()
            return redirect('reserve:confirm')
        else:
            # commentフィールド以外で１つでも未記入のフィールドが存在していたら
            # 各フィールドのclass属性にis-invalid（失敗）もしくわis-valid（クリア）を追記する
            for field in form:
                if field.errors:
                    # フォームが未入力のフィールド
                    # comment以外で入力されていないフィールドはclass属性にis-invalidを追記する
                    form[field.name].field.widget.attrs['class'] += ' is-invalid'
                else:
                    if field.name != 'comment':
                        # フォームに入力されているフィールド
                        # comment以外で入力されたフィールドはclass属性にis-validを追記する
                        form[field.name].field.widget.attrs['class'] += ' is-valid'
    #else:
        #form = ReserveForm()

    return render(request, 'reserve/index.html', {'form':form})

def confirm(request):
    return render(request, 'reserve/confirm.html')

def complete(request):
    return render(request, 'reserve/complete.html')

# Create your views here.

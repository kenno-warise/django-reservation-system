from django.contrib import admin

from .models import Reserve, Shop, ReservableDate


class ReserveAdmin(admin.ModelAdmin):
    """
    [チェンジリストのカスタマイズ]
    list_display
    list_filter
    search_fields
    """
    list_display = ('reserve_date', 'reserve_time', 'name', 'reserve_num', 'email', 'tel', 'comment') # チェンジリストに表示するフィールド
    # list_filter = ['reserve_date'] # 日付に対してフィルター（絞り込む）を掛けられる
    search_fields = ['reserve_date'] # 日付を指定して検索（検索ボックスの追加）

class ReservableInline(admin.TabularInline):
    model = ReservableDate
    extra = 7

class ShopAdmin(admin.ModelAdmin):
    """
    [チェンジフォームのカスタマイズ]
    list_display
    fieldsets
    """
    inlines = [ReservableInline]
    list_display = ('start_time', 'end_time', 'max_reserve_num')
    fieldsets = [
            (None, {
                'fields': (
                    ('start_time', 'end_time'),
                    'max_reserve_num',
                )
            }),
    ]

admin.site.register(Shop, ShopAdmin)
admin.site.register(Reserve, ReserveAdmin)

# Register your models here.

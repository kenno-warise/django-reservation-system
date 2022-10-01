from django.contrib import admin

from .models import Reserve, Shop


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

class ShopAdmin(admin.ModelAdmin):
    """
    [チェンジフォームのカスタマイズ]
    fieldsets
    """
    fieldsets = [
            (None, {'fields': ('reservable_date',
                ('start_time', 'end_time'),
                'max_reserve_num',
            )}),
    ]

admin.site.register(Shop, ShopAdmin)
admin.site.register(Reserve, ReserveAdmin)

# Register your models here.

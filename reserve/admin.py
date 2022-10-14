from django.contrib import admin

from .models import (EndTime, MaxReserveNum, ReservableDate, Reserve,
                     SetIntegration, Shop, StartTime)


class ReservableInline(admin.TabularInline):
    model = ReservableDate
    extra = 1


class StartInline(admin.TabularInline):
    model = StartTime
    extra = 1


class EndInline(admin.TabularInline):
    model = EndTime
    extra = 1


class MaxReserveInline(admin.TabularInline):
    model = MaxReserveNum
    extra = 1


class SetIntegrationAdmin(admin.ModelAdmin):

    inlines = [
        ReservableInline,
        StartInline,
        EndInline,
        MaxReserveInline,
    ]


class ReserveAdmin(admin.ModelAdmin):
    """
    [チェンジリストのカスタマイズ]
    list_display
    list_filter
    search_fields
    """

    list_display = (
        "reserve_date",
        "reserve_time",
        "name",
        "reserve_num",
        "email",
        "tel",
        "comment",
    )  # チェンジリストに表示するフィールド
    # list_filter = ['reserve_date'] # 日付に対してフィルター（絞り込む）を掛けられる
    search_fields = ["reserve_date"]  # 日付を指定して検索（検索ボックスの追加）


class ShopAdmin(admin.ModelAdmin):
    """
    [チェンジフォームのカスタマイズ]
    list_display
    fieldsets
    """

    # inlines = [ReservableInline]
    list_display = ("reservable_date", "start_time", "end_time", "max_reserve_num")
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "reservable_date",
                    ("start_time", "end_time"),
                    "max_reserve_num",
                )
            },
        ),
    ]


# forginmodel = [ReservableDate, StartTime, EndTime, MaxReserveNum]
admin.site.register(Shop, ShopAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(SetIntegration, SetIntegrationAdmin)

# Register your models here.

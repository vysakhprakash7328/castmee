from django.contrib import admin
from .models import *


class StateAdmin(admin.ModelAdmin):
    search_fields = ['name']


class DistrictAdmin(admin.ModelAdmin):
    search_fields = ['name','state']


class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ['name']


class SkillsAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ConsiderMeAdmin(admin.ModelAdmin):
    search_fields = ['name']


class AvailableForAdmin(admin.ModelAdmin):
    search_fields = ['name']


class PreferredGeneAdmin(admin.ModelAdmin):
    search_fields = ['name']


class InterestAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ProjectTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


class HairTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


class HairColorAdmin(admin.ModelAdmin):
    search_fields = ['name']


class BodyTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


class EyeColorAdmin(admin.ModelAdmin):
    search_fields = ['name']


class SkinColorAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ArtistExtendedAdmin(admin.StackedInline):
    model = ArtistExtended


class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistExtendedAdmin]


class ProducerExtendedAdmin(admin.StackedInline):
    model = ProducerExtended


class ProducerAdmin(admin.ModelAdmin):
    inlines = [ProducerExtendedAdmin]


class WishListAdmin(admin.ModelAdmin):
    pass


class PreferredFormatAdmin(admin.ModelAdmin):
    pass


# class Wishlis

admin.site.register(State,StateAdmin)
admin.site.register(District,DistrictAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Language,LanguageAdmin)
admin.site.register(Skills,SkillsAdmin)
admin.site.register(ConsiderMe,ConsiderMeAdmin)
admin.site.register(AvailableFor,AvailableForAdmin)
admin.site.register(PreferredGene,PreferredGeneAdmin)
admin.site.register(Interest,InterestAdmin)
admin.site.register(ProjectType,ProjectTypeAdmin)
admin.site.register(HairType,HairTypeAdmin)
admin.site.register(HairColor,HairColorAdmin)
admin.site.register(BodyType,BodyTypeAdmin)
admin.site.register(EyeColor,EyeColorAdmin)
admin.site.register(SkinColor,SkinColorAdmin)
admin.site.register(Artist,ArtistAdmin)
admin.site.register(Producer,ProducerAdmin)
admin.site.register(WishList,WishListAdmin)
admin.site.register(PreferredFormat,PreferredFormatAdmin)
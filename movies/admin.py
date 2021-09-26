from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url',)
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 0
    readonly_fields = ('name', 'email',)


class MShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 0
    readonly_fields = ('get_shots',)

    def get_shots(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_shots.short_description = 'Image'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'country', 'draft',)
    list_display_links = ('title',)
    list_filter = ('category', 'year',)
    list_per_page = 10
    list_editable = ('draft',)
    search_fields = ('title', 'category__name',)
    readonly_fields = ('get_poster',)
    ordering = ('id',)
    inlines = [MShotsInline, ReviewInline, ]
    save_on_top = True
    save_as = True
    actions = ('publish', 'unpublish')
    prepopulated_fields = {'url': ('title', 'world_premier')}
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description',)
        }),
        (None, {
            'fields': (('poster', 'get_poster'),)
        }),
        (None, {
            'fields': (('year', 'country', 'world_premier'),)
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('directors', 'actors', 'genres'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        (None, {
            'fields': (('category', 'url', 'draft'),)
        }),
    )

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="auto">')

    get_poster.short_description = 'Poster'

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 set was changed.'
        else:
            message_bit = f'{row_update} sets were changed.'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 set was changed.'
        else:
            message_bit = f'{row_update} sets were changed.'
        self.message_user(request, f'{message_bit}')

    unpublish.short_description = "UnPublish"
    unpublish.allowed_permissions = ('change',)
    publish.short_description = "Publish"
    publish.allowed_permissions = ('change',)


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'description', 'get_image', 'id')
    readonly_fields = ('get_image',)
    prepopulated_fields = {'url': ('name',)}


    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Image'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url', 'id')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'star', 'ip',)


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'get_image', 'movie')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Image'  # Підпис поля


admin.site.register(RatingStar)

admin.site.site_header = "Django Movies"

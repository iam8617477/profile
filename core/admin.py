from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import AR, Command, File, Note, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


def truncate_and_format(text, max_lines=3):
    if text:
        lines = text.split('\n')
        truncated_lines = lines[:max_lines]
        if len(lines) > max_lines:
            truncated_lines.append('...')
        truncated_text = '\n'.join(truncated_lines)
        return format_html('<pre style="margin: 0;padding: 0;">{}</pre>', truncated_text)
    return ''


def display_tags(obj):
    return ', '.join([tag.name for tag in obj.tags.all()])


display_tags.short_description = 'Tags'


def short_text(text):
    if text:
        return text[:75] + ('...' if len(text) > 75 else '')
    return '-'


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = (
        display_tags,
        'display_code',
        'title',
        'short_description',
    )
    search_fields = ('title', 'code')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)

    def display_code(self, obj):
        return truncate_and_format(obj.code)

    display_code.short_description = 'Code'

    def short_description(self, obj):
        return short_text(obj.description)

    short_description.short_description = 'Description'


class NoteForm(forms.ModelForm):
    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        instance = kwargs.get('instance')
        if instance:
            kwargs['initial'].update({'description': instance.get_decrypted_description()})
        super().__init__(*args, **kwargs)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    form = NoteForm
    list_display = (
        display_tags,
        'title',
        'short_description',
        'short_link',
    )
    search_fields = ('title', 'code')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)

    def short_description(self, obj):
        return short_text(obj.get_decrypted_description())

    short_description.short_description = 'Description'

    def short_link(self, obj):
        return short_text(obj.link)

    short_link.short_description = 'Link'


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'file', 'uuid', 'download_link')
    search_fields = ('title', 'uuid')

    def download_link(self, obj):
        url = reverse('download_file', args=[obj.uuid])
        return format_html('<a href="{}" target="_blank">Download</a>', url)

    download_link.short_description = 'Download Link'


@admin.register(AR)
class ARAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'data', 'created_at', 'updated_at')
    search_fields = ('uuid',)

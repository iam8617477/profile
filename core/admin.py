from django.contrib import admin
from django.utils.html import format_html
from .models import Tag, Command, Note


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


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = (display_tags, 'display_code', 'title', 'short_description', )
    search_fields = ('title', 'code')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)

    def display_code(self, obj):
        return truncate_and_format(obj.code)

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    def short_description(self, obj):
        if obj.description:
            return obj.description[:75] + ('...' if len(obj.description) > 75 else '')
        return '-'

    short_description.short_description = 'Description'

    display_tags.short_description = 'Tags'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (display_tags, 'title', 'description', 'link', )
    search_fields = ('title', 'code')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)

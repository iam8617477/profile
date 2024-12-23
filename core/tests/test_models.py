import pytest
from core.models import Tag, Command, Note


@pytest.mark.django_db
def test_tag():
    created_tag = Tag.objects.create(name='Test Tag')
    retrieved_tag = Tag.objects.get(id=created_tag.id)

    assert retrieved_tag.name == 'Test Tag'
    assert str(retrieved_tag) == 'Test Tag'


@pytest.mark.django_db
def test_command():
    tag = Tag.objects.create(name='Command Tag')
    created_command = Command.objects.create(
        code='Some code for command',
        title='Test Command',
        description='This is a test command description'
    )
    created_command.tags.add(tag)
    retrieved_command = Command.objects.get(id=created_command.id)

    assert retrieved_command.title == 'Test Command'
    assert str(retrieved_command) == 'Test Command'
    assert retrieved_command.code == 'Some code for command'
    assert retrieved_command.tags.count() == 1
    assert tag in retrieved_command.tags.all()


@pytest.mark.django_db
def test_note():
    tag = Tag.objects.create(name='Note Tag')
    created_note = Note.objects.create(
        title='Test Note',
        description='This is a test note description',
        link='http://example.com'
    )
    created_note.tags.add(tag)
    retrieved_note = Note.objects.get(id=created_note.id)

    assert retrieved_note.title == 'Test Note'
    assert str(retrieved_note) == 'Test Note'
    assert retrieved_note.link == 'http://example.com'
    assert retrieved_note.tags.count() == 1
    assert tag in retrieved_note.tags.all()

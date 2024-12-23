import pytest
from core.models import Tag


@pytest.mark.django_db
def test_tag_creation_and_retrieval():
    created_tag = Tag.objects.create(name='Test Tag')
    retrieved_tag = Tag.objects.get(id=created_tag.id)

    assert retrieved_tag.name == 'Test Tag'
    assert str(retrieved_tag) == 'Test Tag'

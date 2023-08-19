import pytest

from bookmarks.models import Bookmark, LinkType
from user_auth.tests.conftest import user_client, api_client, user, email, password

@pytest.fixture
def bookmark_payload():
    return {
        "target_url": "https://lenta.ru/news/2023/08/11/pitt_jolie_divorce/"
    }


@pytest.fixture
def valid_bookmark_answer():
    return {
        "id": 1,
        "title": "Почему распался брак Джоли и Питта: актеры развелись спустя 7 лет судов",
        "description": "Брэд Питт и Анджелина Джоли развелись спустя семь лет судебных разбирательств. Сообщается, "
                       "что пара пришла к соглашению и урегулировала беспокоящие их вопросы: по предварительным "
                       "данным, артистка получит опеку над их тремя несовершеннолетними детьми, а актер — полный "
                       "контроль над их общей винодельней во Франции.",
        "link": "https://lenta.ru/news/2023/08/11/pitt_jolie_divorce/",
        "image": "https://icdn.lenta.ru/images/2023/08/11/16/20230811162921817/share_c9945c4721c04b6ad7e7cd59d40ba9b5"
                 ".jpg",
        "created_at": "2023-08-19T20:08:09.722368Z",
        "modified_at": "2023-08-19T20:08:09.722368Z",
        "owner": 1,
        "link_type": "article"
    }


@pytest.fixture
def bookmark(user):
    return Bookmark.objects.create(
        owner=user,
        title="Почему распался брак Джоли и Питта: актеры развелись спустя 7 лет судов",
        description="Брэд Питт и Анджелина Джоли развелись спустя семь лет судебных разбирательств. Сообщается, "
                       "что пара пришла к соглашению и урегулировала беспокоящие их вопросы: по предварительным "
                       "данным, артистка получит опеку над их тремя несовершеннолетними детьми, а актер — полный "
                       "контроль над их общей винодельней во Франции.",
        link="https://lenta.ru/news/2023/08/11/pitt_jolie_divorce/",
        image="https://icdn.lenta.ru/images/2023/08/11/16/20230811162921817/share_c9945c4721c04b6ad7e7cd59d40ba9b5"
                 ".jpg",
        link_type=LinkType.objects.get(pk="article")
    )
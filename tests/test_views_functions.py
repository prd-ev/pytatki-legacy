import pytest
from pytatki.views import get_usergroups_of_user

def test_get_usergroups_of_user(insert_usergroup):
    if get_usergroups_of_user(1) != [{'idusergroup': 1, 'name': 'test', 'color': '#ffffff', 'description': 'test', 'image_path': 'img/default.jpg'}]:
        print(get_usergroups_of_user(1))
        raise AssertionError()


def test_index(s):
    s.go('/')
    assert 'Kozea' in s.title
    assert s('h1')


def test_index_2(s):
    s.go('/')
    assert 'Kozea' in s.title
    assert s('ol')

from zipper import Cursor

tree = (
    (1, 2),
    ('x', 'y', (3, 4)),
    'x',
    'y'
)
cursor = Cursor.makecursor(tree)


def test_make_cursor():
    assert cursor.node == tree


def test_movements():
    c = cursor
    c = c.movedown()
    assert c.node == (1, 2)
    c = c.moveright().moveright()
    assert c.node == 'x'
    c = c.moveleft().moveleft()
    assert c.node == (1, 2)
    c = c.moveup()
    assert c.node == tree


def test_top():
    c = cursor
    while c.can_down():
        c = c.movedown()

    assert c.top().node == cursor.node


def test_inserts():
    c = cursor
    c = c.insert_right(1)
    assert c.moveright().node == 1
    c = c.insert_left((1, 2))
    assert c.moveleft().node == (1, 2)
    c = c.insert_down('x')
    assert c.node[-1] == 'x'


if __name__ == "__main__":
    test_make_cursor()
    test_movements()
    test_top()
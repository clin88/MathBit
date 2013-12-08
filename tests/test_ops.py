from ops import OpCursor

def test_moveup():
    tree = (
        (1, 2),
        ('x', 'y', (3, 4)),
        'x',
        'y'
    )
    cursor = OpCursor.makecursor(tree)
    cursor = cursor.movedown()
    assert cursor.moveup().node == tree


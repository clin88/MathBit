MathBit
=======

Mathbit is a computer algebra system for elementary algebra, geometry,
and statistics that yields the steps it takes to solve problems. It's intended
as a tool to help students grasp symbolic math.

Well, that's what I'm shooting for anyway. It currently only simplifies
elementary algebraic expressions.

Roadmap
=======

1. Additional functionality, including solving linear and quadratic equations.
2. A more robust parser capable of handling conventional math syntax, including
implicit multiplication and negatives.
3. Latex formatter.
4. REST API.

If you think this project is cool, please contribute :). 

Behind the Scenes
=================

Expressions are represented using a syntax tree. For example,
multiplication of 5 * x * y is represented by a Mult object containing 5, 'x', 'y'.
Each node is immutable, but the tree itself can be traversed and manipulated using
the 'zipper' structure in core/zipper.py.

Typically, functions traverse the tree recursively, making changes as necessary.
All functions that yield steps are written as generators and literally 'yield'
steps as it solves a problem. Thus, MB makes heavy use of generator delegation
and the Python 3 'yield from' keyword.


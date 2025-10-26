code style advice:

- use high code locality
- try to avoid state and side effects and use a functional programming style, avoid global variables if possible
- do not make functions too small
- try to seperate logic pieces from data pieces

run it once with `$ uv run snake.py --cli --runs 5`

you want to minimize the number of steps taken to reach the goal and never reach less than the max possible score

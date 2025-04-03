import turtle

from snake.world import Position, World


class Draw:
    def __init__(self, screen: turtle.Screen):
        self.screen = screen
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.screen.tracer(0)
        self.cell_size = 20
        self.grid_size = 32

    def transform_coordinates(self, x:int, y:int):
        screen_x = x * self.cell_size
        screen_y = - y * self.cell_size
        return screen_x, screen_y

    def draw_block(self, x:int, y:int, color: str) -> None:
        screen_x, screen_y = self.transform_coordinates(x, y)
        self.pen.penup()
        self.pen.goto(screen_x, screen_y)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.fillcolor(color)
        for _ in range(4):
            self.pen.forward(self.cell_size)
            self.pen.right(90)
        self.pen.end_fill()

    def draw_score(self, score: int) -> None:
        self.pen.penup()
        self.pen.goto(10, -10)
        self.pen.pendown()
        self.pen.write(f"Score: {score}", font=("Arial", 14, "normal"))

    def draw_apple(self, apple_position: Position) -> None:
        screen_x, screen_y = self.transform_coordinates(apple_position.x, apple_position.y)
        self.pen.penup()
        self.pen.goto(screen_x + self.cell_size // 2, screen_y - self.cell_size // 2)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.fillcolor("red")
        self.pen.circle(self.cell_size // 2)
        self.pen.end_fill()

    def draw_fence(self) -> None:
        for x in range(self.grid_size):
            self.draw_block(x, 0)
            self.draw_block(x, self.grid_size - 1)

        for y in range(self.grid_size):
            self.draw_block(0, y)
            self.draw_block(self.grid_size-1, y)

    def draw(self, world:World) -> None:
        self.screen.clear()
        self.draw_fence()
        self.draw_apple(world.apple)
        for seg in world.tail:
            self.draw_block(seg.x, seg.y, "dark_green")
        self.draw_block(world.head.x, world.head.y, "green")
        self.draw_score(world.score)
        self.screen.update()

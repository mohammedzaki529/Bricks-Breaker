import turtle
import time
screen = turtle.Screen()
screen.title("Bricks Breaker")
screen.bgcolor("black")
screen.setup(width=700, height=600)
turtle.tracer(0)

paused = False
def toggle_pause():
    global paused
    paused = not paused

level = 1
score  = 0
lives = 3


lives_pen = turtle.Turtle()
lives_pen.speed(0)
lives_pen.color("Red")
lives_pen.up()
lives_pen.hideturtle()
lives_pen.goto(-250 , 260)
lives_pen.write("Lives : 3" , align="center", font=("Arial", 20 , "bold") )

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.up()
score_pen.hideturtle()
score_pen.goto(0,260)
score_pen.write("Score : 0", align="center" , font=("Arial" , 20, "bold"))

paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("cyan")
paddle.shapesize(stretch_wid=1, stretch_len=6)
paddle.penup()
paddle.goto(0 , -250)

def paddle_left():
    x = paddle.xcor()
    if x > -300:
        paddle.setx(paddle.xcor() - 40)
def paddle_right():
    x = paddle.xcor()
    if x < 300:
        paddle.setx(paddle.xcor() + 40)

screen.listen()
screen.onkeypress(paddle_left,"Left")
screen.onkeypress(paddle_right,"Right")
screen.onkeypress(toggle_pause, "space")


ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.shapesize(1.5)
ball.up()
ball.goto(0 , -100)

ball.dx = 2
ball.dy = 2

def create_level(level):
    bricks = []

    if level == 1:
        rows = 1
    elif level == 2:
        rows = 2
    elif level == 3:
        rows = 3
        paddle.shapesize(stretch_wid=1, stretch_len=8)
    else:
        rows = 3
    cols = 7
    colors = ["red","orange","yellow","blue","green","purple","cyan"]
    
    x_start = -280
    y_start = 200

    for r in range(rows):
        for c in range(cols):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color(colors[(r+c) % len(colors)])
            brick.shapesize(stretch_wid=1,stretch_len=4)
            brick.up()
            brick.goto(x_start + c*90, y_start - r*40)
            bricks.append(brick)
    return bricks
bricks = create_level(level)
while True:
    
    if paused:
        turtle.update()
        continue


    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #wall bounce
    if ball.xcor() > 330 or ball.xcor() < -330:
        ball.dx *= -1
    #top bounce
    if ball.ycor() > 280:
        ball.dy *= -1
    #paddle bounce
    if (ball.ycor() < -230 and ball.ycor() > -260) and (ball.xcor() > paddle.xcor() - 60 and ball.xcor() < paddle.xcor() + 60):
        ball.dy *= -1

    if ball.ycor() < -290:
        lives -= 1
        lives_pen.clear()
        lives_pen.write(f"Lives : {lives}", align="center",font=("arial" , 20, "bold"))
        #reset count
        ball.goto(0,-100)
        ball.dx = 2
        ball.dy = 2
        #khatam hai mamla
        if lives == 0:
            score_pen.goto(0,0)
            score_pen.write("Game Over", align="center", font=("Arial" , 20, "bold"))
            break

    all_gone = True
    for brick in bricks:
        if brick.isvisible():
            all_gone = False
            break
    if all_gone:
        level += 1
        ball.goto(0,-100)
        ball.dx = 2
        ball.dy = 2
        if level > 3:
            score_pen.goto(0,0)
            score_pen.write("You Win", align="center" , font=("Arial",20,"bold"))
            break
        bricks = create_level(level)
    #brick ka khatamaa
    for brick in bricks:
        if brick.isvisible():
            if (brick.xcor() - 40 < ball.xcor() < brick.xcor() + 40) and (brick.ycor() - 20 < ball.ycor() < brick.ycor() + 20):
                brick.hideturtle()
                ball.dy *= -1

                score += 1
                score_pen.clear()
                score_pen.write(f"Score : {score}", align="center" , font=("Arial", 20, "bold"))
    turtle.update()
    time.sleep(0.01)

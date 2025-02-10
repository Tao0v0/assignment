from turtle import *

def draw_cat():
    # Set up the screen
    bgcolor("white")
    speed(5)
    pensize(3)

    # Draw the head
    penup()
    goto(0, -50)
    pendown()
    fillcolor("gray")
    begin_fill()
    circle(50)
    end_fill()

    # Draw the ears
    penup()
    goto(-30, 50)
    pendown()
    seth(160)
    fillcolor("gray")
    begin_fill()
    circle(-30, 180)
    end_fill()

    penup()
    goto(30, 50)
    pendown()
    seth(20)
    fillcolor("gray")
    begin_fill()
    circle(-30, 180)
    end_fill()

    # Draw the eyes
    penup()
    goto(-20, 20)
    pendown()
    dot(10, "white")

    penup()
    goto(20, 20)
    pendown()
    dot(10, "white")

    # Draw the nose
    penup()
    goto(0, 0)
    pendown()
    dot(10, "pink")

    # Draw the mouth
    penup()
    goto(-10, -10)
    pendown()
    seth(-60)
    circle(10, 120)

    # Draw the whiskers
    penup()
    goto(-30, 0)
    pendown()
    seth(-30)
    fd(30)

    penup()
    goto(-30, 0)
    pendown()
    seth(-120)
    fd(30)

    penup()
    goto(30, 0)
    pendown()
    seth(-150)
    fd(30)

    penup()
    goto(30, 0)
    pendown()
    seth(-60)
    fd(30)

    # Draw the body
    penup()
    goto(-50, -50)
    pendown()
    seth(0)
    fillcolor("gray")
    begin_fill()
    fd(100)
    circle(-50, 180)
    fd(100)
    circle(-50, 180)
    end_fill()

    # Draw the legs
    penup()
    goto(-40, -150)
    pendown()
    seth(-90)
    fillcolor("gray")
    begin_fill()
    fd(30)
    circle(-15, 180)
    fd(30)
    circle(-15, 180)
    end_fill()

    penup()
    goto(40, -150)
    pendown()
    seth(-90)
    fillcolor("gray")
    begin_fill()
    fd(30)
    circle(-15, 180)
    fd(30)
    circle(-15, 180)
    end_fill()

    # Draw the tail
    penup()
    goto(-50, -100)
    pendown()
    seth(-135)
    fillcolor("gray")
    begin_fill()
    circle(50, 180)
    end_fill()

    # Finish
    hideturtle()
    done()

# Call the function to draw the cat
draw_cat()

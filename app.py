import random
from flask import Flask, render_template, request

app = Flask(__name__)

list1 = [0]
while len(list1) < 5:
    a = random.randint(1, 9)
    found = False
    target = a
    for number in list1:
        if number == target:
            found = True
            break
    if found == False:
        list1.append(a)

list1.remove(0)

count1 = 1
history = []
game_over = False


@app.route("/", methods=["GET", "POST"])
def game():
    global count1
    global history
    global game_over

    if request.method == "POST" and not game_over:

        try:
            answer = int(request.form["answer"])

            answerlist = [0]
            answerlist.append(answer//1000)
            answerlist.append(answer%1000//100)
            answerlist.append(answer%1000%100//10)
            answerlist.append(answer%1000%100%10)
            answerlist.remove(0)

            one = answer//1000
            two = answer%1000//100
            thr = answer%1000%100//10
            fou = answer%1000%100%10

            g = 0
            strike = 0
            ball = 0

            if answerlist == list1:
                history.append(
                    f'정답입니다! (시도 횟수: {count1}회)'
                )
                game_over = True

            else:
                for g in range(1, 4):
                    if list1[g-1] == answerlist[g-1]:
                        strike += 1

                if answerlist[0] == list1[1] or answerlist[0] == list1[2] or answerlist[0] == list1[3]:
                    ball += 1

                if answerlist[1] == list1[0] or answerlist[1] == list1[2] or answerlist[1] == list1[3]:
                    ball += 1

                if answerlist[2] == list1[0] or answerlist[2] == list1[1] or answerlist[2] == list1[3]:
                    ball += 1

                if answerlist[3] == list1[0] or answerlist[3] == list1[1] or answerlist[3] == list1[2]:
                    ball += 1

                history.append(
                    f'{count1}회 → {ball}b {strike}s'
                )

                count1 += 1

        except:
            history.append("숫자 이외의 값은 에러 처리됩니다.")

    return render_template(
        "index.html",
        history=history,
        game_over=game_over
    )


if __name__ == "__main__":
    app.run(debug=True)
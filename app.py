import random
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# 세션을 사용하기 위한 비밀키
app.secret_key = "number-baseball-secret-key"


def make_number():
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

    return list1


def start_game():
    session["answer"] = make_number()
    session["count1"] = 1
    session["history"] = []
    session["game_over"] = False


@app.route("/", methods=["GET", "POST"])
def game():

    # 처음 접속했을 때 게임 생성
    if "answer" not in session:
        start_game()

    if request.method == "POST" and not session["game_over"]:

        try:
            answer = int(request.form["answer"])

            answerlist = [0]
            answerlist.append(answer // 1000)
            answerlist.append(answer % 1000 // 100)
            answerlist.append(answer % 1000 % 100 // 10)
            answerlist.append(answer % 1000 % 100 % 10)
            answerlist.remove(0)

            strike = 0
            ball = 0

            if answerlist == session["answer"]:

                session["history"].append(
                    f'정답입니다! (시도 횟수: {session["count1"]}회)'
                )

                session["game_over"] = True

            else:

                # 기존 코드의 스트라이크 판정 방식 유지
                for g in range(1, 4):
                    if session["answer"][g - 1] == answerlist[g - 1]:
                        strike += 1

                if answerlist[0] == session["answer"][1] or answerlist[0] == session["answer"][2] or answerlist[0] == session["answer"][3]:
                    ball += 1

                if answerlist[1] == session["answer"][0] or answerlist[1] == session["answer"][2] or answerlist[1] == session["answer"][3]:
                    ball += 1

                if answerlist[2] == session["answer"][0] or answerlist[2] == session["answer"][1] or answerlist[2] == session["answer"][3]:
                    ball += 1

                if answerlist[3] == session["answer"][0] or answerlist[3] == session["answer"][1] or answerlist[3] == session["answer"][2]:
                    ball += 1

                session["history"].append(
                    f'{session["count1"]}회 → {ball}b {strike}s'
                )

                session["count1"] += 1

            session.modified = True

        except:
            session["history"].append(
                "숫자 이외의 값은 에러 처리됩니다."
            )
            session.modified = True

    return render_template(
        "index.html",
        history=session["history"],
        game_over=session["game_over"]
    )


@app.route("/new")
def new_game():

    start_game()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

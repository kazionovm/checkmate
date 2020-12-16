from flask import Flask, Response, request, redirect, url_for
from evaluation import *

s = State()
#v = Valuator()
v = ClassicValuator()

def to_svg(s):
    return base64.b64encode(chess.svg.board(board=s.board).encode('utf-8')).decode('utf-8')

app = Flask(__name__)

@app.route("/")
def index():
    ret = open("../index.html").read()
    return ret.replace('start', s.board.fen())

def computer_move(s, v):
    # computer move
    move = sorted(explore_leaves(s, v),
                key=lambda x: x[0], reverse=s.board.turn)
    if len(move) == 0:
        return
    print("top 3:")
    for i, m in enumerate(move[0:3]):
        print("  ", m)
    print(s.board.turn, "moving", move[0][1])
    s.board.push(move[0][1])

@app.route("/selfplay")
def selfplay():
    s = State()

    ret = '<html><head>'
    # self play
    while not s.board.is_game_over():
        computer_move(s, v)
        ret += '<img style="margin-bottom: 10px;" width=600 height=600 src="data:image/svg+xml;base64,%s"></img><br/>' % to_svg(
            s)
    print(s.board.result())

    return ret

# move given in algebraic notation
@app.route("/move")
def move():
    if not s.board.is_game_over():
        move = request.args.get('move', default="")
        if move is not None and move != "":
            print("human moves", move)
            try:
                s.board.push_san(move)
                computer_move(s, v)
            except Exception:
                traceback.print_exc()
            response = app.response_class(
                response=s.board.fen(),
                status=200
            )
            return response
    else:
        print("GAME IS OVER")
        response = app.response_class(
            response="game over",
            status=200
        )
        return response
    print("hello ran")
    return hello()


# moves given as coordinates of piece moved
@app.route("/move_coordinates")
def move_coordinates():
    if not s.board.is_game_over():
        source = int(request.args.get('from', default=''))
        target = int(request.args.get('to', default=''))
        promotion = True if request.args.get(
            'promotion', default='') == 'true' else False

        move = s.board.san(chess.Move(
            source, target, promotion=chess.QUEEN if promotion else None))

        if move is not None and move != "":
            print("human moves", move)
            try:
                s.board.push_san(move)
                computer_move(s, v)
            except Exception:
                traceback.print_exc()
        response = app.response_class(
            response=s.board.fen(),
            status=200
        )
        return response

    print("GAME IS OVER")
    response = app.response_class(
        response="game over",
        status=200
    )
    return response


@app.route("/newgame")
def newgame():
    s.board.reset()
    response = app.response_class(
        response=s.board.fen(),
        status=200
    )
    return redirect(url_for('index'))


if __name__ == "__main__":
    if os.getenv("SELFPLAY") is not None:
        s = State()
        while not s.board.is_game_over():
            computer_move(s, v)
            print(s.board)
        print(s.board.result())
    else:
        app.run(debug=True)

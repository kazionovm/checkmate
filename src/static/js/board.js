const board = ChessBoard("board", {
  position: "start",
  draggable: true,
  onDrop: onDrop,
});

function onDrop(source, target, piece) {
  let pn = piece.includes("b")
    ? piece.toLowerCase().substring(1, 2)
    : piece.substring(1, 2);
  pn = piece.includes("P") ? "" : pn;
  let move = piece.includes("P")
    ? source + target
    : pn + source.substring(0, 1) + target;
  move =
    piece.includes("P") && target.includes("8")
      ? target.substring(0, 1) + "8Q"
      : move; // pawn promotion

  $.get("/move", { move: move }, function (r) {
    if (r.includes("game over")) {
      document.querySelector("p").innerText = "game over";
    } else {
      document.querySelector("p").innerText = "";
      board.position(r);
    }
  });
}

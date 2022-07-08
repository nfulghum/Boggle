"use strict";

let score = 0;

let time = 60;
$("#timer").html(time);

let words = new Set();

$("form").on("submit", handleSubmit);

async function handleSubmit(evt) {
    evt.preventDefault();

    // create a variable that equals the word submitted on the form
    let word = $("input").val();

    // do nothing if the form is empty
    if (!word) return;

    // send this word to the server to have it check if it is an appropriate response
    const res = await axios.get("/check-word", { params: { word: word } });

    let response = res.data.response;

    // display response in the dom
    $("#response").html(response);

    // reset form
    $("form").trigger("reset");

    // if the word is on the board, not in our Set, add to the set, update score value
    if (response === "ok") {
        if (words.has(word)) {
            return;
        }
        words.add(word);
        score += word.length;
        $("#score").html(`Score: ${score}`);
    }

    console.log(response);
}

let countDown = setInterval(function () {
    time--;
    $("#timer").html(time);

    stopTimer();
}, 1000);

function stopTimer() {
    if (time < 1) {
        clearInterval(countDown);
        $("form").hide();
        $(".container").append($("<span>").html("Game Over!"));
        endGame();
    }
}

async function endGame() {
    await axios.post("/end-game", { score: score });
}
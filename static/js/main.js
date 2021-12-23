function submitWord() {
    let wordToTry = $('#wordinput').val();
    $('#wordinput').val('');
    console.log('trying', wordToTry);

    $.post("try/" + wordToTry,
        function(data, status){
            if (status != 'success') {
                console.log('failed');
                return;
            }
            if (data == 'bad') {
                updateStatus("Implausible", true);
            } else if (data == 'good') {
                updateStatus("Plausible word", false);
                scoreWord(wordToTry);
            } else if (data == 'real') {
                updateStatus("Actual word", true);
            } else if (data == 'wrong') {
                updateStatus("Wrong letters", true);
            }
        });
}

$(document).ready(function() {
    getLetters();
    updateScoreboard();
});

$(document).on("keypress", function (e) {
    if (e.keyCode == 13 || e.which == 13) {
        submitWord();
    } else if (e.keyCode == 32 || e.which == 32) {
        shuffleHexagon();
        $("#wordinput").blur();
    } else {
        $("#wordinput").focus();
    }
});


function updateStatus(message, error) {
    if (error) {
        $("#status" ).effect("shake");
        $("#status" ).removeClass("status")
        $("#status" ).addClass("status-red")
    } else {
        $("#status" ).removeClass("status-red")
        $("#status" ).addClass("status")
    }
    $('#status').text(message);
}

var savedLetters = null;

function shuffleHexagon() {
    if (savedLetters != null) {
        refreshHexagon(savedLetters);
    }
}

function getLetters() {
    $.get("letters",
        function(data, status){
            if (status != 'success') {
                console.log('failed');
                return;
            }
            savedLetters = data;
            refreshHexagon(savedLetters);
        });
}

function refreshHexagon(letters) {
    $('#mid_letter').text(letters[0]);

    // shuffle the other letters
    let arr = shuffle([1, 2, 3, 4, 5, 6])
    for (let i = 0; i < arr.length; i++) {
        let j = arr[i]
        $('#letter' + (i + 1)).text(letters[j]);
    }
}

var words = []
var points = 0

function scoreWord(word) {
    $("#wordlist").append('<li>' + word + '</li>');
    points += word.length
    updateScoreboard();
}

function updateScoreboard() {
    if (points > 110) {
        $("#rank").text('Oaf---Lummox---Picaroon---Fumbler---[[Blunderbuss]]');
    } else if (points > 90) {
        $("#rank").text('Oaf---Lummox---Picaroon---[[Fumbler]]---Blunderbuss');
    } else if (points > 60) {
        $("#rank").text('Oaf---Lummox---[[Picaroon]]---Fumbler---Blunderbuss');
    } else if (points > 30) {
        $("#rank").text('Oaf---[[Lummox]]---Picaroon---Fumbler---Blunderbuss');
    } else {
        $("#rank").text('[[Oaf]]---Lummox---Picaroon---Fumbler---Blunderbuss');
    }
    $("#points").text(points)
}

function shuffle(array) {
  let currentIndex = array.length,  randomIndex;

  // While there remain elements to shuffle...
  while (currentIndex != 0) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }

  return array;
}


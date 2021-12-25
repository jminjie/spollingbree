function submitWord() {
    let wordToTry = $('#wordinput').val().toLowerCase();
    if (wordToTry.length < 4) {
        return;
    }
    $('#wordinput').val('');
    console.log('trying', wordToTry);

    if (allWords.includes(wordToTry)) {
        updateStatus("Already found", true);
        return;
    }

    $.post("try/" + wordToTry,
        function(data, status){
            if (status != 'success') {
                console.log('failed');
                return;
            }
            if (data == 'bad') {
                updateStatus("Implausible", true);
            } else if (data == 'good') {
                scoreWord(wordToTry, false);
                updateStatus("Plausible word (+" + getPoints(wordToTry, false) + ")", false);
            } else if (data == 'pangram') {
                updateStatus("Pangram! (+" + getPoints(wordToTry, true) + ")", false);
                scoreWord(wordToTry, true);
            } else if (data == 'real') {
                updateStatus("Actual word", true);
            } else if (data == 'wrong') {
                updateStatus("Wrong letters", true);
            }
        });
}

function getPoints(word, pangram) {
    if (word.length == 4) {
        return 1;
    } else if (pangram) {
        return word.length + 7;
    } else {
        return word.length;
    }
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
        $('#wordinput').attr("placeholder", "");
    }
});

function showRankUp() {
    $('.rankstatus').stop();
    $('.rankstatus').css('visibility', 'visible');
    $('.rankstatus').css('opacity', '1');
    $('.rankstatus').animate({'opacity': 0}, 1500, function(){
        $('.rankstatus').css('opacity', '1');
        $('.rankstatus').css('visibility', 'hidden');
    });
}

function updateStatus(message, error) {
    $('#status').text(message);
    $('#status').stop();
    $('#status').css('visibility', 'visible');
    $('#status').css('opacity', '1');
    if (error) {
        $('#status').effect("shake");
        $('#status').addClass("status-bad")

        $('#status').animate({'opacity': 0}, 1500, function(){
            $('#status').css('opacity', '1');
            $('#status').css('visibility', 'hidden');
        });
    } else {
        $('#status').removeClass("status-bad")

        $('#status').animate({'opacity': 0}, 1500, function(){
            $('#status').css('opacity', '1');
            $('#status').css('visibility', 'hidden');
        });
    }
}

var savedLetters = null;

function shuffleHexagon() {
    if (savedLetters != null) {
        for (let i = 1; i < 7; i++) {
            $('#letter' + i ).animate({'opacity': 0}, 150, function(){
                refreshHexagon(savedLetters);
                $('#letter' + i).animate({'opacity': 1}, 300);
            });
        }
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

var words = [];
var points = 0;
var numWords = 0;
var allWords = []

const RANK_NAMES = ['Oaf', 'Lummox', 'Picaroon', 'Fumbler', 'Blunderbuss'];
const RANK_THRESHOLDS = [0, 15, 30, 45, 60]

function scoreWord(word, pangram) {
    $("#wordlist").append('<li>' + word + '</li>');
    allWords.push(word);
    let additionalPoints = getPoints(word, pangram);
    for (let i = 1; i < RANK_THRESHOLDS.length; i++) {
        if (points < RANK_THRESHOLDS[i] && points+additionalPoints >= RANK_THRESHOLDS[i]) {
            showRankUp();
        }
    }

    let highestThreshold = RANK_THRESHOLDS[RANK_THRESHOLDS.length - 1];
    if (points < highestThreshold && points+additionalPoints >= highestThreshold) {
        console.log("Trigger fireworks!");
        alert("Congratulations you've done it you absolute fool!!!");
        setTimeout(function () {
            console.log("Stop fireworks!");
        }, 3000)
    }
    points += getPoints(word, pangram);
    numWords += 1;
    updateScoreboard();
}

function formatRankName(rank) {
    var formattedString=
        ((rank == 0) ? '[[' + RANK_NAMES[0] + ']]' : RANK_NAMES[0]) + '---' +
        ((rank == 1) ? '[[' + RANK_NAMES[1] + ']]' : RANK_NAMES[1]) + '---' +
        ((rank == 2) ? '[[' + RANK_NAMES[2] + ']]' : RANK_NAMES[2]) + '---' +
        ((rank == 3) ? '[[' + RANK_NAMES[3] + ']]' : RANK_NAMES[3]) + '---' +
        ((rank == 4) ? '[[' + RANK_NAMES[4] + ']]' : RANK_NAMES[4]);

    return formattedString;
}

function updateScoreboard() {
    if (points >= RANK_THRESHOLDS[4]) {
        $("#rank").text(formatRankName(4));
    } else if (points >= RANK_THRESHOLDS[3]) {
        $("#rank").text(formatRankName(3));
    } else if (points >= RANK_THRESHOLDS[2]) {
        $("#rank").text(formatRankName(2));
    } else if (points >= RANK_THRESHOLDS[1]) {
        $("#rank").text(formatRankName(1));
    } else if (points >= RANK_THRESHOLDS[0]) {
        $("#rank").text(formatRankName(0));
    }
    $("#points").text(points)
    if (numWords != 1) {
        $("#numwords").text(numWords + " words")
    } else {
        $("#numwords").text(numWords + " word")
    }
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


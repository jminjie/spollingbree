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
});

function closeInfo() {
    document.querySelector('.info-overlay').classList.add('d-none');
}

$(document).on('keypress', function (e) {
    if (e.keyCode == 13 || e.which == 13) {
        submitWord();
    } else if (e.keyCode == 32 || e.which == 32) {
        e.preventDefault();
        shuffleHexagon();
        $('#wordinput').blur();
    } else {
        $('#wordinput').focus();
        $('#wordinput').attr('placeholder', '');
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

            loadWords(savedLetters);
            loadPoints(savedLetters);

            refreshHexagon(savedLetters);

            setPoints();
            setRankString(0);
            setRankLine(0);
            for (let i = 0; i < allWords.length; i++) {
                $("#wordlist").append('<li>' + allWords[i] + '</li>');
            }
            updateScoreboard();

            $("#rankline").click(function() {
                console.log('clicked rankline')
                document.querySelector('.info-overlay').classList.remove('d-none');
            });

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

var points = 0;
var numWords = 0;
var allWords = []

const RANK_NAMES = ['Beginner', 'Moving Down', 'Oaf', 'Lummox', 'Picaroon', 'Fumbler', 'Blunderbuss'];
const RANK_THRESHOLDS = [0, 1, 15, 30, 45, 60, 75]

window.onbeforeunload = function(){
    saveCookies()
};


function loadWords(lettersKey) {
    if (document.cookie.indexOf(lettersKey + "words=") < 0) {
        return;
    } else {
        let words = readCookie(lettersKey + "words").split(',')
        for (let i = 0; i < words.length; i++) {
            if (words[i] != '') {
                allWords.push(words[i]);
            }
        }
        numWords = allWords.length;
    }
}

function loadPoints(lettersKey) {
    if (document.cookie.indexOf(lettersKey + "points=") < 0) {
        return;
    } else {
        let p = readCookie(lettersKey + "points");
        points = parseInt(p)
    }
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}


function saveCookies() {
    var words = "";
    for (let i = 0; i < allWords.length; i++) {
        words += allWords[i] + ',';
    }
    document.cookie = savedLetters + "words=" + words + ";";
    document.cookie = savedLetters + "points=" + points + ";";
}

function scoreWord(word, pangram) {
    $("#wordlist").append('<li>' + word + '</li>');
    allWords.push(word);

    points += getPoints(word, pangram);
    numWords += 1;
    updateScoreboard();

}

function setRankString(rank) {
    $("#rankstring").empty();

    for (var i = 0; i < RANK_NAMES.length; i++) {
        var separatorSpan = $('<span />').addClass('separator_span').html(' &mdash; ');
        var span = null;
        if (i == rank) {
            span = $('<span />').addClass('current_rank').html(RANK_NAMES[i]);
        } else {
            //span = $('<span />').addClass('other_rank').html(RANK_NAMES[i]);
        }
        $("#rankstring").append(span);
    }
}

function setRankLine(rank) {
    // left dots
    $("#ldots").empty();
    for (var i = 0; i < rank; i++) {
        var dot = $('<i/>').addClass('fas fa-dot-circle');
        $("#ldots").append(dot);
    }
       
    //right dots
    $("#rdots").empty();
    var nbsp = $('<span/>').html('&nbsp;');
    $("#rdots").append(nbsp);
    for (var i = 0; i < RANK_NAMES.length - (rank + 1); i++) {
        var dot = $('<i/>').addClass('fas fa-dot-circle');
        $("#rdots").append(dot);
    }
}


function setPoints() {
    $("#points").text(points)
}

var prevPoints = 0;

function updateScoreboard() {

    if (numWords != 1) {
        $("#numwords").text(numWords + " words")
    } else {
        $("#numwords").text(numWords + " word")
    }

    var delayedSetPoints = false;

    for (let i = 0; i < RANK_THRESHOLDS.length; i++) {
        if (prevPoints < RANK_THRESHOLDS[i] && points >= RANK_THRESHOLDS[i]) {
            delayedSetPoints = true;
            $('#points').animate({'opacity': 0}, 300, function(){
                setRankLine(i);
                $('#points').animate({'opacity': 1}, 300);
                setPoints();
            });
            $('#rankstring').animate({'opacity': 0}, 300, function(){
                setRankString(i);
                $('#rankstring').animate({'opacity': 1}, 300);
            });
            showRankUp();
        }
    }

    if (!delayedSetPoints) {
        setPoints();
    }

    let highestThreshold = RANK_THRESHOLDS[RANK_THRESHOLDS.length - 1];

    if (prevPoints < highestThreshold && points >= highestThreshold) {
        const jsConfetti = new JSConfetti();
        jsConfetti.addConfetti();
    }

    prevPoints = points;
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

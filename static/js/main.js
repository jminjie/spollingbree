function submitWord() {
    let wordToTry = $('#wordinput').val();
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
                updateStatus("Plausible", false);
                addWord(wordToTry);
            } else if (data == 'real') {
                updateStatus("Actual word", true);
            } else if (data == 'wrong') {
                updateStatus("Wrong letters", true);
            }
        });
}

$( document ).ready(function() {
   getLetters();
});


function updateStatus(message, shake) {
    if (shake) {
        $("#status" ).effect("shake");
    }
    $('#status').text(message);
}

var letters = 'xxxxxx'

function getLetters() {
    console.log('getting letters');

    $.get("letters",
        function(data, status){
            if (status != 'success') {
                console.log('failed');
                return;
            }
            letters = data;
            refreshHexagon(letters);
        });
}

function refreshHexagon(letters) {
    console.log("the letters are", letters);
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

function addWord(word) {
    $("#score").append('<li>' + word + '</li>');
    points += word.length
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


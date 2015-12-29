var mic;

var myRec = new p5.SpeechRec(); // new P5.SpeechRec object
myRec.continuous = true; // do continuous recognition
myRec.interimResults = true; // allow partial recognition (faster, less accurate)
posted = false;

var rcb;  // will be filled later with user input

var words = [];

function setup() {
  document.getElementById("recipient").innerHTML = "Text or Call a contact";
  mic = new p5.AudioIn();
  mic.start();
  myRec.onResult = resultCallback(); // recognition callback
  myRec.start(); // start engine
  
}

var iter = 0;

window.onload = function() {  
    // sets the "search" bar to most recent word/sentence          
    function getInput() {
      var mostrecentword = myRec.resultString;

      if (mostrecentword != null) {
        document.getElementById("recipient").innerHTML = mostrecentword;
        words.push(mostrecentword);
      } 

      size = words.length;
      if (size > 20) {
        if ( !posted && words[size-1] == words[size-4] && words[size-3] == words[size-7] && words[size-2] == words[size-8]) {
          message = words[size-2];
          posted = true;  
          $.ajax({
            type: 'POST',
            url: 'contactList',
            data: {'sequence': message},
            success: function() {
              console.log("final list exported as " + message);
            }
          });
        }
      }

      // reloads page if the length of words exeeds 100
      if (words.length > 25) {
        location.reload();
      }

      return mostrecentword;
    }

    setInterval(getInput, 200);
}


function resultCallback() {
  var mostrecentword = myRec.resultString;
}








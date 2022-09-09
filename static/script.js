//Script purpose is to disable all input boxes on API Testing page except the input box associated with the checked radio button.

//Variable Declarations
var listOfRadioButtons = document.getElementsByClassName("radio-button");
var searchTermInput = document.getElementById('searchTermInput');
var bookInput = document.getElementById('bookInput');
var searchLinkInput = document.getElementById('searchLinkInput');
var bookRadio = document.getElementById('bookRadio')
var queryTermRadio = document.getElementById('queryTermRadio')
var queryLinkRadio = document.getElementById('queryLinkRadio')
var defaultPlaceholder = "You can only test one input type at a time.";
var enabledOption;
var disabledOption1;
var disabledOption2;

//Function to disable an input box.
function disableInputBox(option){
    option.setAttribute("disabled", true);
    option.value = "";
    option.setAttribute("placeholder", defaultPlaceholder);
}

//Loop to put listeners on every radio button that will enable the input box of the checked radio button and disable the rest.
for (i = 0; i < listOfRadioButtons.length; i++){
  listOfRadioButtons[i].onclick = function () {
    if (bookRadio.checked){
        enabledOption = bookInput;
        disabledOption1 = searchTermInput;
        disabledOption2 = searchLinkInput;
        enabledOption.setAttribute("placeholder", "https://www.gutenberg.org/ebooks/1342");

      }
    else if (queryLinkRadio.checked){
        enabledOption = searchLinkInput;
        disabledOption1 = searchTermInput;
        disabledOption2 = bookInput;
        enabledOption.setAttribute("placeholder", "https://www.gutenberg.org/ebooks/search/?query=pride+and+prejudice&submit_search=Go%21");
      }
    else {
        enabledOption = searchTermInput;
        disabledOption1 = searchLinkInput;
        disabledOption2 = bookInput;
        enabledOption.setAttribute("placeholder", "Pride and Prejudice");
    }
    enabledOption.removeAttribute("disabled");
    disableInputBox(disabledOption1);
    disableInputBox(disabledOption2);
  }
}
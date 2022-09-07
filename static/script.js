var listOfRadioButtons = document.getElementsByClassName("radio-button");

for (i = 0; i < listOfRadioButtons.length; i++){
  listOfRadioButtons[i].onclick = function () {
    if (document.getElementById('bookRadio').checked){
        document.getElementById('bookInput').removeAttribute("disabled");
        document.getElementById('bookInput').setAttribute("placeholder", "https://www.gutenberg.org/")
        document.getElementById('searchInput').setAttribute("disabled", true);
        document.getElementById('searchInput').value = ""
        document.getElementById('searchInput').setAttribute("placeholder", "You can only test one input type at a time.")
      }
    else {
        document.getElementById('searchInput').removeAttribute("disabled");
        document.getElementById('searchInput').setAttribute("placeholder", "Pride and Prejudice")
        document.getElementById('bookInput').setAttribute("disabled", true);
        document.getElementById('bookInput').value = ""
        document.getElementById('bookInput').setAttribute("placeholder", "You can only test one input type at a time.")
      }
  }
}

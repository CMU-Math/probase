$(function() {
    var inp = document.getElementById("myInput");
    var inputContainer = document.getElementById("inputContainer");
    var container = document.getElementById("tagContainer");
    var dropdown = document.getElementById("dropdown");
    var tagText = document.getElementById("tagText");
    var tagList = [];
    var inputval;
    var currentFocus;
    inp.addEventListener("input", function(e) {
        inputval = this.value;
        currentFocus = -1;
        dropdown.innerHTML = "";
        for (let i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, inputval.length).toUpperCase() == inputval.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                let b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].substr(0, inputval.length) + "</strong>";
                b.innerHTML += arr[i].substr(inputval.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function(e) {
                    addTag(this.getElementsByTagName("input")[0].value);
                });
                dropdown.appendChild(b);
            }
        }
    });

    inp.addEventListener("keydown", function(e) {
        items = dropdown.getElementsByTagName("div");
        if (e.keyCode == 40) { // down
            currentFocus++;
            if (currentFocus >= items.length)
                currentFocus = -1;
            addActive(items);
        } else if (e.keyCode == 38) { // up
            e.preventDefault(); // don't move cursor to the start of input
            currentFocus--;
            if (currentFocus < -1)
                currentFocus = items.length - 1;
            addActive(items);
        } else if (e.keyCode == 13) { // enter
            e.preventDefault(); // don't submit form
            if (inp.value != "")
                addTag(inp.value);
        } else if (e.keyCode == 8 && inp.value == "") {
            if (tagList.length > 0) {
                tagList.pop();
                container.removeChild(inputContainer.previousSibling);
                tagText.value = tagList.toString();
            }
        }
    });

    function addTag(text) {
        let newTag = document.createElement("DIV");
        let t = document.createTextNode(text);
        newTag.appendChild(t);
        newTag.classList.add("tag");
        container.insertBefore(newTag, inputContainer);
        inp.value = "";
        inputval = "";
        dropdown.innerHTML = "";
        tagList.push(text);
        tagText.value = tagList.toString();
    }

    function addActive(items) {
        for (var i = 0; i < items.length; i++) {
          items[i].classList.remove("autocomplete-active");
        }
        if (currentFocus > -1) {
            items[currentFocus].classList.add("autocomplete-active");
            inp.value = items[currentFocus].getElementsByTagName("input")[0].value;
        } else {
            inp.value = inputval;
        }
    }

    document.addEventListener("click", function (e) {
        if (e.target != inp)
            dropdown.innerHTML = "";
    });

    for (let i = 0; i < initialTags.length; i++) {
        addTag(initialTags[i]);
    }
});

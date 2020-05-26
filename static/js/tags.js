$(function() {
    var inp = document.getElementById("tagInput");
    var inputContainer = document.getElementById("inputContainer");
    var container = document.getElementById("tagContainer");
    var dropdown = document.getElementById("dropdown");
    var form = document.getElementById("tagForm");
    var tagText = document.getElementById("tagText");
    var tagList = [];
    var inputval;
    var currentFocus;
    var backspacePause;

    for (let i = 0; i < initialTags.length; i++) {
        displayTag(initialTags[i]);
    }

    inp.addEventListener("input", update);

    function update() {
        inputval = inp.value;
        currentFocus = -1;
        dropdown.innerHTML = "";
        for (let i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, inputval.length).toLowerCase() == inputval.toLowerCase()) {
                /*create a DIV element for each matching element:*/
                let item = document.createElement("div")
                item.setAttribute("class", "mydropdown-item");
                item.innerHTML = arr[i];
                item.addEventListener("click", function(e) {
                    addTag(this.innerHTML);
                });
                dropdown.appendChild(item);
            }
        }
        if (dropdown.innerHTML == "")
            dropdown.classList.remove("show");
        else
            dropdown.classList.add("show");
    }

    function addTag(text) {
        text = text.toLowerCase();
        $.ajax({
            url: form.action,
            type: "POST",
            data: {
                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
                'submit': 'addTag',
                'tag': text,
            },
            success: function() {
                displayTag(text);
            },
            error: function() {
                alert("An error occurred when adding the tag: " + text);
            }
        });
    }

    function removeTag(tag) {
        $.ajax({
            url: form.action,
            type: "POST",
            data: {
                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
                'submit': 'removeTag',
                'tag': tag.textContent,
            },
            success: function() {
                console.log(tag.innerHTML);
                container.removeChild(tag);
            },
            error: function() {
                alert("An error occurred when adding the tag: " + text);
            }
        });
    }

    function displayTag(text) {
        let newTag = document.createElement("div");
        let t = document.createTextNode(text);
        newTag.appendChild(t);
        let close = document.createElement("i");
        close.setAttribute("class", "fas fa-times");
        close.addEventListener("click", function(e) {
            removeTag(newTag);
        });
        newTag.appendChild(close);
        newTag.classList.add("tag");
        container.insertBefore(newTag, inputContainer);
        inp.value = "";
        inputval = "";
        tagList.push(text);
    }

    inp.addEventListener("keydown", function(e) {
        items = dropdown.getElementsByTagName("div");
        if (e.keyCode == 40) { // down
            currentFocus++;
            if (currentFocus >= items.length)
                currentFocus = -1;
            setActive(items);
        } else if (e.keyCode == 38) { // up
            e.preventDefault(); // don't move cursor to the start of input
            currentFocus--;
            if (currentFocus < -1)
                currentFocus = items.length - 1;
            setActive(items);
        } else if (e.keyCode == 13) { // enter
            e.preventDefault(); // don't submit form
            if (inp.value != "") {
                addTag(inp.value);
                dropdown.classList.remove("show");
            }
        } else if (e.keyCode == 8 && !backspacePause) { // backspace
            if (inp.value == 0 && tagList.length > 0) {
                removeTag(inputContainer.previousSibling);
                tagList.pop();
                backspacePause = true;
            }
            else if (inp.value.length == 1)
                backspacePause = true;
        }
    });

    inp.addEventListener("keyup", function(e) {
        if (e.keyCode == 8) { //backspace
            backspacePause = false;
        }
    });

    function setActive(items) {
        for (var i = 0; i < items.length; i++) {
            items[i].classList.remove("active");
        }
        if (currentFocus > -1) {
            items[currentFocus].classList.add("active");
            inp.value = items[currentFocus].innerHTML;
        } else {
            inp.value = inputval;
        }
    }

    $(document).on('click', function(e) {
        if (e.target != inp)
            dropdown.classList.remove("show");
    });
});

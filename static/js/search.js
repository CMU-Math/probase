window.onload = () => {
	let textFilter = "";
	let authorFilter = [];
	let tagFilter = [];

	const getProblems = () => Array.from($(".card[data-type=problem]"));

	const authorElem = $("#filterAuthor")[0];

	const tagEleList = $('.tag_filter');

	const alltagsEle = $('#all-tags')[0];

	// Retrieve list of tags for filter
	const getTagList = () => {
		let tagList = [];
		for(var i = 0; i < tagEleList.length; i++){
			if(tagEleList[i].checked){
				tagList.push(tagEleList[i].value);
			}
		}
		return tagList;
	}

	// Gets list of tags for each problem from string
	const extractTags = (tagString) => {
		let tagArray = tagString.split("'");
		let resArray = [];
		for (var i = 1; i < tagArray.length; i += 2){
			resArray.push(tagArray[i]);
		}
		return resArray;
	}

	// Big Filter Function
	const applyFilter = () => {
		const matches = getProblems()
			.filter(e => {
				if (textFilter !== "") {
					return e.innerText.toLowerCase().includes(textFilter);
				}
				return true;
			})
			.filter(e => {
				if (authorFilter.length !== 0) {
					return authorFilter.includes(e.dataset.author);
				}
				return true;
			})
			.filter(e => {
				if (tagFilter.length !== 0) { 
					if(alltagsEle.checked){return true;}
					var curTags = extractTags(e.dataset.tag);
					for(var i = 0; i < curTags.length; i ++){
						if(tagFilter.includes(curTags[i])){
							return true;
						}
					}
					return false;
				}
				return true;
			});

		getProblems().forEach(e => {
			e.hidden = !matches.includes(e);
		});
	}

	// Text Filter handler
	$("#filterText")[0].oninput = function () {
		textFilter = this.value.toLowerCase();
		applyFilter();
	}

	// Creates the options for author change box
	getProblems().map(e => e.dataset.author)
		.filter((e, i, arr) => arr.indexOf(e) === i)
		.forEach(author => {
			const opt = document.createElement("option");
			opt.value = author;
			opt.innerText = author;
			authorElem.appendChild(opt);
		});

	// Handler for Author Change box 
	authorElem.onchange = function () {
		authorFilter = Array.from(this.children)
			.filter(a => a.selected)
			.filter(a => a.value !== "")
			.map(a => a.value);
		applyFilter();
	};

	// Handlers for tag checkboxes
	for(var i = 0; i < tagEleList.length; i++){
		tagEleList[i].onchange = function () {
			alltagsEle.checked = false;
			tagFilter = getTagList();
			applyFilter();
		};
	}

	// Adds Handler for Clear Tags Button
	$("#ClearTags")[0].onclick = function () {
		for(var i = 0; i < tagEleList.length; i++){
			tagEleList[i].checked = false;
			
		}
		alltagsEle.checked = true;
		applyFilter();
	};
	

}

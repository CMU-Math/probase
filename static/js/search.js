window.onload = () => {
	let textFilter = "";
	let authorFilter = [];

	const getProblems = () => Array.from($(".card[data-type=problem]"));


	const authorElem = $("#filterAuthor")[0];
	const applyFilter = () => {
		const matches = getProblems()
			.filter(e => {
				if (textFilter !== "") {
					return e.innerText.includes(textFilter);
				}
				return true;
			})
			.filter(e => {
				if (authorFilter.length !== 0) {
					return authorFilter.includes(e.dataset.author);
				}
				return true;
			});

		getProblems().forEach(e => {
			e.hidden = !matches.includes(e);
		});
	}
	$("#filterText")[0].oninput = function () {
		textFilter = this.value;
		applyFilter();
	}

	getProblems().map(e => e.dataset.author)
		.filter((e, i, arr) => arr.indexOf(e) === i)
		.forEach(author => {
			const opt = document.createElement("option");
			opt.value = author;
			opt.innerText = author;
			authorElem.appendChild(opt);
		});

	authorElem.onchange = function () {
		authorFilter = Array.from(this.children)
			.filter(a => a.selected)
			.filter(a => a.value !== "")
			.map(a => a.value);
		applyFilter();
	}

}

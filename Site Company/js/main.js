(function () {
	const scrollLinks = document.querySelectorAll("a.nav-link");

	for (let i = 0; i < scrollLinks.length; i++) {
		scrollLinks[i].addEventListener("click", event => {
			event.preventDefault();
			const id = scrollLinks[i].getAttribute("href");
			document.querySelector(id).scrollIntoView({
				behavior: 'smooth',
				block: 'start'
			});
		});
	}
})();
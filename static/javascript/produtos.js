document.addEventListener("DOMContentLoaded", function () {
	// Recupera as recomendações do atributo de dados
	var recommendationsContainer = document.getElementById(
		"recommendations-container"
	);
	var recommendationsData = JSON.parse(
		recommendationsContainer.dataset.recommendations
	);

	// Seleciona a lista de recomendações
	var recommendationsList = document.getElementById("recomendacoes");

	// Popula a lista de recomendações
	recommendationsData.forEach(function (recommendation) {
		var li = document.createElement("li2");
		li.className = "titulo";

		var imagemProd = document.createElement("img");
		imagemProd.className = "roupa";

		var titulo = recommendation.title
			.toLowerCase()
			.replace(/\s+/g, "")
			.replace(/-/g, "");
		var tipoRoupa = [
			"tshirt",
			"short",
			"bikini",
			"tanktop",
			"jumpsuits",
			"femme",
			"top",
			"robe",
			"cap",
			"pant",
		];

		var hasImage = false;
		tipoRoupa.forEach(function (tipo) {
			if (titulo.includes(tipo) || titulo.includes(tipo + "s")) {
				imagemProd.src =
					"/static/assets/clothes/" +
					tipo +
					"-" +
					recommendation.color +
					".jpg";
				hasImage = true;
			}
		});

		if (!hasImage) {
			return;
		}

		imagemProd.alt = "Imagem do produto";
		li.appendChild(imagemProd);

		var hr = document.createElement("hr");
		li.appendChild(hr);

		var corProdutoSpan = document.createElement("span");
		corProdutoSpan.innerHTML =
			"<b>Cor do produto:</b> " + recommendation.color + "<br>";
		li.appendChild(corProdutoSpan);

		var tituloSpan = document.createElement("span");
		tituloSpan.innerHTML = "<b>Nome:</b> " + recommendation.title + "<br>";
		li.appendChild(tituloSpan);

		var classificacaoSpan = document.createElement("span");
		classificacaoSpan.innerHTML =
			"<b>Classificação:</b> " + recommendation.rating + "<br>";
		li.appendChild(classificacaoSpan);

		var precoSpan = document.createElement("span");
		precoSpan.innerHTML = "<b>Preço:</b> " + recommendation.price;
		li.appendChild(precoSpan);

		li.onclick = function () {
			redirecionarProduto(recommendation, imagemProd);
		};

		recommendationsList.appendChild(li);
	});
});

function redirecionarProduto(recommendation, imagemProd) {
	const queryString = new URLSearchParams({
		title: recommendation["title"],
		color: recommendation["color"],
		rating: recommendation["rating"],
		price: recommendation["price"],
		imagem: imagemProd.src,
	}).toString();
	console.log(queryString);
	window.location.href = `/produto?${queryString}`;
}

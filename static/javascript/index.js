// Função para alternar a exibição do dropdown
function toggleDropdown(id) {
	const dropdown = document.getElementById(id);
	dropdown.classList.toggle("show");
}

// Mapeamento de cores do português para o inglês
const colorMap = {
	"Azul Marinho": "navyblue",
	Amarelo: "yellow",
	Vermelho: "red",
	Branco: "white",
	Preto: "black",
	Azul: "blue",
	Cinza: "gray",
	Verde: "green",
	Rosa: "pink",
};

// Função para alterar a cor selecionada
function changeColor(color) {
	const dropdownSummary = document.getElementById("dropdownSummary");
	dropdownSummary.textContent = "Cor: " + color;

	const selectedColor = document.getElementById("selectedColor");
	selectedColor.value = colorMap[color] || color;
}

// Função para validar o formulário
function validarFormulario() {
	const precoMinimo = parseFloat(document.getElementById("preco-minimo").value);
	const precoMaximo = parseFloat(document.getElementById("preco-maximo").value);
	const selectedColor = document.getElementById("selectedColor").value;

	if (!selectedColor) {
		alert("Por favor, selecione uma cor.");
		return false;
	}

	if (precoMinimo < 0 || precoMaximo < 0) {
		alert("Os preços não podem ser negativos.");
		return false;
	}

	if (precoMinimo >= precoMaximo) {
		alert("O preço mínimo deve ser menor que o preço máximo.");
		return false;
	}

	gerarRecomendacoes();
	return false;
}

// Função para renderizar um item de recomendação
function renderizarItem(recommendation, recommendationsList) {
	const li = document.createElement("li");
	li.className = "titulo";

	const imagemProd = document.createElement("img");
	imagemProd.className = "roupa";
	const tipoRoupa = [
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
	const titulo = recommendation.title
		.toLowerCase()
		.replace(/\s+/g, "")
		.replace(/-/g, "");

	tipoRoupa.forEach(function (tipo) {
		if (titulo.includes(tipo) || titulo.includes(tipo + "s")) {
			imagemProd.src = `/static/assets/clothes/${tipo}-${recommendation.color}.jpg`;
		}
	});

	if (!imagemProd.src) {
		return; // Não renderizar o item se não houver imagem correspondente
	}

	imagemProd.alt = "Imagem do produto";
	li.appendChild(imagemProd);

	const hr = document.createElement("hr");
	li.appendChild(hr);

	const labels = {
		id: "Código",
		title: "Título",
		color: "Cor",
		rating: "Classificação",
		price: "Preço",
	};

	Object.keys(labels).forEach((key) => {
		const span = document.createElement("span");
		let value = recommendation[key];
		if (key === "rating") {
			value += " estrelas";
		} else if (key === "price") {
			value = `$ ${value}`;
		}
		span.innerHTML = `<b>${labels[key]}: </b> ${value} <br>`;
		li.appendChild(span);
	});

	li.onclick = function () {
		redirecionarProduto(recommendation, imagemProd);
	};

	recommendationsList.appendChild(li);
}

// Função para redirecionar para a página do produto
function redirecionarProduto(recommendation, imagemProd) {
	const recommendationsList = document.getElementById("recomendacoes");
	recommendationsList.innerHTML = "";
	const loading = document.getElementById("loading");
	loading.style.visibility = "visible";

	const queryString = new URLSearchParams({
		id: recommendation.id,
		title: recommendation.title,
		color: recommendation.color,
		rating: recommendation.rating,
		price: recommendation.price,
		imagem: imagemProd.src,
	}).toString();
	window.location.href = `/produto?${queryString}`;
}

// Função para gerar recomendações
function gerarRecomendacoes() {
	const recommendationsList = document.getElementById("recomendacoes");
	recommendationsList.innerHTML = "";

	const loading = document.getElementById("loading");
	loading.style.visibility = "visible";

	const formData = new FormData(document.getElementById("formulario"));

	const xhr = new XMLHttpRequest();
	xhr.open("POST", "/recomendacao", true);
	xhr.onreadystatechange = function () {
		if (xhr.readyState == 4) {
			// Verifica se a requisição foi concluída
			loading.style.visibility = "hidden";
			if (xhr.status == 200) {
				try {
					const recommendations = JSON.parse(xhr.responseText);
					renderizarRecomendacoes(recommendations);
				} catch (e) {
					console.error("Failed to parse JSON response: ", e);
					renderizarRecomendacoes([]);
				}
			} else {
				console.error("Failed to fetch recommendations: ", xhr.status);
				renderizarRecomendacoes([]);
			}
		}
	};

	xhr.send(formData);
}

// Função para renderizar todas as recomendações
function renderizarRecomendacoes(recommendations) {
	const recommendationsList = document.getElementById("recomendacoes");
	recommendationsList.innerHTML = "";

	if (recommendations.length === 0) {
		const noProductsMessage = document.createElement("div");
		noProductsMessage.className = "titulo-sem-produto";
		noProductsMessage.textContent =
			"Não há produtos disponíveis com os critérios selecionados.";

		recommendationsList.appendChild(noProductsMessage);

		return;
	}

	recommendations.forEach(function (recommendation) {
		renderizarItem(recommendation, recommendationsList);
	});
}

// Inicialização quando o DOM estiver pronto
document.addEventListener("DOMContentLoaded", function () {
	const currentURL = window.location.pathname; // Obtém a URL atual da página
	if (currentURL === "/produto") {
		// Verifica se a URL corresponde à rota /produto
		const recommendationsData = JSON.parse(
			document.getElementById("recommendations-container").dataset
				.recommendations
		);
		try {
			renderizarRecomendacoes(recommendationsData.slice(0, 100));
		} catch (error) {
			console.log("Error:", error);
		}
	}
});

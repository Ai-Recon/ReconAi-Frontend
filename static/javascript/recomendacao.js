function toggleDropdown(id) {
  var dropdown = document.getElementById(id);
  dropdown.classList.toggle("show");
}

function changeColor(color) {
  // Mapear as cores do português para o inglês
  var colorMap = {
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
  // Verificar se a cor está mapeada
  if (colorMap[color]) {
    // Se estiver, definir a cor no dropdownSummary e no selectedColor
    document.getElementById("dropdownSummary").textContent = "Cor: " + color;
    document.getElementById("selectedColor").value = colorMap[color];
  } else {
    // Caso contrário, manter a cor original
    document.getElementById("dropdownSummary").textContent = "Cor: " + color;
    document.getElementById("selectedColor").value = color;
  }
}

function validarFormulario() {
  var precoMinimo = document.getElementById("preco-minimo").value;
  var precoMaximo = document.getElementById("preco-maximo").value;
  var selectedColor = document.getElementById("selectedColor").value;

  if (!selectedColor) {
    alert("Por favor, selecione uma cor.");
    return false;
  }

  if (precoMinimo < 0) {
    alert("O preço mínimo não pode ser negativo.");
    return false;
  }

  if (precoMaximo < 0) {
    alert("O preço máximo não pode ser negativo.");
    return false;
  }

  if (parseInt(precoMinimo) >= parseInt(precoMaximo)) {
    alert("O preço mínimo deve ser menor que o preço máximo.");
    return false;
  }

  gerarRecomendacoes();
  return false;
}
function gerarRecomendacoes() {
  var formulario = document.getElementById("formulario");
  var formData = new FormData(formulario);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/recomendacao", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      try {
        var recommendations = JSON.parse(xhr.responseText);
        renderizarRecomendacoes(recommendations);
      } catch (e) {
        console.error("Failed to parse JSON response: ", e);
        renderizarRecomendacoes([]);
      }
    }
  };

  xhr.send(formData);
}

function renderizarRecomendacoes(recommendations) {
  var recommendationsList = document.getElementById("recomendacoes");
  recommendationsList.innerHTML = "";

  if (recommendations.length === 0) {
    var noProductsMessage2 = document.createElement("div");
    noProductsMessage2.className = "titulo";
    noProductsMessage2.textContent =
      "Não há produtos disponíveis com os critérios selecionados.";

    recommendationsList.appendChild(noProductsMessage2);
    return;
  }

  recommendations.forEach(function (recommendation) {
    var li2 = document.createElement("li2");
    li2.className = "titulo";

    var imagemProd = document.createElement("img");
    imagemProd.className = "roupa";
    let titulo = recommendation["title"]
      .toLowerCase()
      .replace(/\s+/g, "")
      .replace(/-/g, "");

    const arrayTipoRoupa = [
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
    arrayTipoRoupa.forEach((tipo) => {
      if (titulo.includes(tipo) || titulo.includes(tipo + "s")) {
        imagemProd.src = `/static/assets/clothes/${tipo}-${recommendation["color"]}.jpg`;
        hasImage = true;
      }
    });

    if (!hasImage) {
      return;
    }

    imagemProd.alt = "Imagem do produto";
    li2.appendChild(imagemProd);

    var hr = document.createElement("hr");
    li2.appendChild(hr);

    var corProdutoSpan = document.createElement("span");
    corProdutoSpan.innerHTML =
      "<b>Cor do produto:</b> " + recommendation["color"] + "<br>";
    li2.appendChild(corProdutoSpan);

    var tituloSpan = document.createElement("span");
    tituloSpan.innerHTML = "<b>Nome:</b> " + recommendation["title"] + "<br>";
    li2.appendChild(tituloSpan);

    var classificacaoSpan = document.createElement("span");
    classificacaoSpan.innerHTML =
      "<b>Classificação:</b> " + recommendation["rating"] + "<br>";
    li2.appendChild(classificacaoSpan);

    var precoSpan = document.createElement("span");
    precoSpan.innerHTML = "<b>Preço:</b> " + recommendation["price"];
    li2.appendChild(precoSpan);

    recommendationsList.appendChild(li2);
  });
}

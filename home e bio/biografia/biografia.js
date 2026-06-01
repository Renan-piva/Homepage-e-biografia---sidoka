

const imagens = [
    "sensitivo homepage.jpg",
    "sidokahomepage.webp",
    "tudu roxo homepage.jpg"
];

let index = 0;

const slide = document.getElementById("slide");

if(slide){

    setInterval(() => {

        index++;

        if(index >= imagens.length){
            index = 0;
        }

        slide.src = imagens[index];

    }, 3000);

}



const prev = document.querySelector(".prev");
const next = document.querySelector(".next");

if(prev && next){

    prev.addEventListener("click", () => {

        index--;

        if(index < 0){
            index = imagens.length - 1;
        }

        slide.src = imagens[index];

    });

    next.addEventListener("click", () => {

        index++;

        if(index >= imagens.length){
            index = 0;
        }

        slide.src = imagens[index];

    });

}


const fotos = document.querySelectorAll(".foto");
const modal = document.getElementById("modal");
const modalImg = document.getElementById("imgModal");
const fechar = document.getElementById("fechar");

fotos.forEach(foto => {

    foto.addEventListener("click", () => {

        modal.style.display = "block";
        modalImg.src = foto.src;

    });

});

if(fechar){

    fechar.onclick = () => {
        modal.style.display = "none";
    }

}


const formulario = document.getElementById("formulario");

if(formulario){

    formulario.addEventListener("submit", (e) => {

        e.preventDefault();

        const nome = document.getElementById("nome").value;
        const email = document.getElementById("email").value;
        const telefone = document.getElementById("telefone").value;

        if(nome == "" || email == "" || telefone == ""){

            alert("Preencha todos os campos.");

            return;
        }

        if(!email.includes("@")){

            alert("Digite um e-mail válido.");

            return;
        }

        alert("Formulário enviado com sucesso!");

    });

}
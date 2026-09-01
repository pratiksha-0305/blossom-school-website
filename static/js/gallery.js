const images = document.querySelectorAll(".gallery img");

const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");

const closeBtn = document.getElementById("close");
const nextBtn = document.getElementById("next");
const prevBtn = document.getElementById("prev");

let currentIndex = 0;


// When any photo is clicked
images.forEach((image, index) => {

    image.onclick = function() {

        currentIndex = index;
        lightboxImg.src = image.src;

        lightbox.style.display = "flex";
    };

});


// Next photo
nextBtn.onclick = function() {

    currentIndex++;

    if(currentIndex >= images.length){
        currentIndex = 0;
    }

    lightboxImg.src = images[currentIndex].src;

};


// Previous photo
prevBtn.onclick = function() {

    currentIndex--;

    if(currentIndex < 0){
        currentIndex = images.length - 1;
    }

    lightboxImg.src = images[currentIndex].src;

};


// Close popup
closeBtn.onclick = function(){

    lightbox.style.display = "none";

};


// Close by clicking outside image
lightbox.onclick = function(event){

    if(event.target == lightbox){
        lightbox.style.display = "none";
    }

};
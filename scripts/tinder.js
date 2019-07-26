
const hiddenDiv = document.querySelector('.hidden-images');
const dogPicLis = hiddenDiv.querySelectorAll('.dogpic');

let dogPicUrls = [];

for (i = 0; i < dogPicLis.length; i++) {
  dogPicUrls.push(dogPicLis[i].innerText);
}

let currentDog = document.querySelector(".current-dog-img");
currentDog.src = dogPicUrls.pop();

const keyClick = document.querySelector('.love-button');
keyClick.addEventListener('click', (event) => {
  currentDog.src = dogPicUrls.pop();
});

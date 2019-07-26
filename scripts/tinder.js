
const hiddenDiv = document.querySelector('.hidden-images');
const dogPicLis = hiddenDiv.querySelectorAll('.dogpic');
document.onkeydown = checkKey;
let dogPicUrls = [];

for (i = 0; i < dogPicLis.length; i++) {
  dogPicUrls.push(dogPicLis[i].innerText);
}

let currentDog = document.querySelector(".current-dog-img");
currentDog.src = dogPicUrls.pop();

let dogHistoryContainer = document.querySelector(".history");

function checkKey(e) {
   e = e || window.event;
   if (e.keyCode == '37') {
     currentDog.src = dogPicUrls.pop();
   }
   else if (e.keyCode == '39') {
    let likedDogUrl = dogPicUrls.pop();
    currentDog.src = likedDogUrl
   }
}

// const keyClick = document.querySelector('.love-button');
//     keyClick.addEventListener('keypress', (event) => {
//       console.log(event)
//       // currentDog.src = dogPicUrls.pop();
//     });

// keyClick.addEventListener('keypress', (event) => {
//   currentDog.src = dogPicUrls.pop();
// });

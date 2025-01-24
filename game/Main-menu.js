//Get all of the necessary elements

let first_round
const video = document.getElementById("videoBackground");
const sound = document.getElementById("sound");
const links = document.querySelectorAll("ul a");
const audioClick = document.getElementById("audioClick");
const audioHover = document.getElementById("audioHover");

//Add click event Listener to the sound icon
sound.addEventListener("click", () => {

    //Toggle icon on click
    sound.classList.toggle("fa-volume-up");

//Mute / Unmute video sound
    if (video.muted === false) {
        video.muted = true;
    } else {
        video.muted = false;
    }

//Add the sound effect
    clickSound();
});

//Add hover event listener on the sound icon
sound.addEventListener("mouseenter", hoverSound);

//Select all links
for (let i= 0; i < links.length; i++) {

//Add click event listener on the links
    links[i].addEventListener("click", clickSound);

//Add hover event listener on the Links
    links[i].addEventListener("mouseenter", hoverSound);
}

//Click sound effect
function clickSound() {
    audioClick.play();
}
//Hover sound effect
function hoverSound() {
    audioHover.play();
}

const new_player = document.getElementById('new-player')
const old_player = document.getElementById('old-player')
new_player.addEventListener('click', function(evt){
    first_round = 'true'
    let url = 'game.html?first_round=' + first_round
    document.getElementById('new-player').href = url

})
old_player.addEventListener('click', function(evt){
    first_round = 'false'
    let url = 'game.html?first_round=' + first_round
    document.getElementById('old-player').href = url
})


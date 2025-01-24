'use strict';

// Check url to see if new or returning player
const url = new URLSearchParams(window.location.search)
const urlinfo = url.get('first_round')
let first_round
if (urlinfo==='true'){
  first_round = true
} else {
  first_round = false
  document.querySelector('#player-modal').classList.add('hide')
}

// Create a map to display airport locations
const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 25], 3);
let currentMarkersLayer = null;


// Function to add markers to the map
function createMapMarkers(jsonData) {
  // Clear existing markers
  if (currentMarkersLayer) {
    currentMarkersLayer.clearLayers();
  }

  var markers = [];

  jsonData.forEach(function(markerData) {
    var marker = L.marker([markerData.lat, markerData.lon])
      .bindPopup(`
        <b>${markerData.name}</b><br>${markerData.country_name}, ${markerData.continent}<br>Distance: ${markerData['distance_km']} km
      `);
    markers.push(marker);
  });

  currentMarkersLayer = L.layerGroup(markers);
  currentMarkersLayer.addTo(map);

  return currentMarkersLayer;
}



// Global variables
let game_over = false
let story
const delay = 100
let selected_user
const getAirports = 'get_airports';
const chosenAirport = 'chosen_airport';
const getFreight = 'get_freight';
const chosenFreight = 'chosen_freight';
const chargeBattery = 'charge_battery';
const gameWindow = document.querySelector('.game-window');


// Runs function under if menu button is pressed
document.getElementById('menu-button').addEventListener('click', function(evt){
reset_basevalues()
})

// Function to reset values saved in python if menu button is pressed
async function reset_basevalues(){
    try {
        await fetch (`http://127.0.0.1:3000/reset_values`)
    } catch(error){
        console.log(error.message)
    } finally {
        console.log('base values reset')
    }
}

// Form for player name
async function newUser(username){
    try{
    const resp = await fetch(`http://127.0.0.1:3000/newuser/${username}`)
        const jsondata = resp.json()
        return jsondata

    }
    catch(error){
        console.error(`ERROR: ${error}`)
    }
}
function create_newUser_form() {

  const form = document.getElementById('player-form')

  form.addEventListener('submit', function(event) {
    event.preventDefault()
    let formData = new FormData(form)
    let user = formData.get('username')
    newUser(user).then((jsondata) => {
      console.log(user+' was created: '+jsondata.success);
      if (jsondata.success === "True") {
        document.querySelector('#player-name').innerHTML = user
        document.querySelector('#player-modal').classList.add('hide')
          update_data()
          firstround()
      } else if (jsondata.success === "False") {
        alert("Username already in use. Enter a new username")
      }
    });
  })
}

//Function for creating a selection of old players names
function userlist(){
  async function get_userlist(){
    try{
      const answer = await fetch('http://127.0.0.1:3000/userlist')
        const jsonanswer = await answer.json()
        return jsonanswer
     }catch (error) {
        console.log(error.message)
    } finally {
        console.log('userlist loaded')
    }
  }
  get_userlist().then((jsonanswer) => {
    const gamewindow = document.querySelector('.game-window')
    let selection = '<select id="users">'
    if (!jsonanswer.success){
        gamewindow.innerHTML = `<a>No users found. 
        Go back to menu to create a new user</a>`
    }
    else{
        gamewindow.innerHTML = '<a>Select user:</a>'
      let userlist = jsonanswer.names
      for (let i=0;i<userlist.length;i++){
        selection += '<option>'+userlist[i]+'</option>'
      }
      selection += '</select>'
      gamewindow.innerHTML += selection
      gamewindow.innerHTML += `<button id="submit">Submit</button>`
      let selector = document.getElementById('users')
      let submit = document.getElementById('submit')
      submit.addEventListener('click', function(evt){
                    selected_user = selector.options[selector.selectedIndex].text
                    olduser(selected_user)
      })
}
})
}

//Function for fetching old player data
function olduser(name) {
  async function get_olduser(name) {
    try {
      const answer = await fetch(`http://127.0.0.1:3000/olduser/${name}`)
      const jsonanswer = await answer.json()
        return jsonanswer
    }catch (error) {
        console.log(error.message)
    } finally {
        console.log('old userdata loaded')
    }
  }
  get_olduser(name).then((jsonanswer)=> {
    document.querySelector('#player-name').innerHTML = name
    document.querySelector('#money').innerHTML = jsonanswer.money
    document.querySelector('#battery').innerHTML = jsonanswer.charge_left
    document.querySelector('#rounds-left').innerHTML = jsonanswer.rounds_left
      gameWindow.innerHTML = ''
      proceedbutton('airport')
})
}

// Function to fetch data from API and update it on screen
function update_data(){

async function getdata(){
     try {

        const answer = await fetch('http://127.0.0.1:3000/getdata')
        const jsonanswer = await answer.json()
        return jsonanswer
     }catch (error) {
        console.log(error.message)
    } finally {
        console.log('display data loaded')
    }
}
getdata().then((jsonanswer) => {
    document.querySelector('#money').innerHTML = jsonanswer.money
    document.querySelector('#battery').innerHTML = jsonanswer.charge_left
    document.querySelector('#rounds-left').innerHTML = jsonanswer.rounds_left
})
}

// Function to update game status into database and check if game has ended
async function endround() {
        try {
            const answer = await fetch('http://127.0.0.1:3000/endround')
            const jsonanswer = await answer.json()
            if (jsonanswer.result === 'crashed') {
                gameWindow.innerHTML = ''
                getStory().then((json) => {
                story = json
                displayTextWithDelay(story.crashlanding, delay)})
                game_over = true
                return
            }
            if (jsonanswer.result === 'goodend') {
                gameWindow.innerHTML = ''
                getStory().then((json) => {
                story = json
                displayTextWithDelay(story.goodend, delay)})
                game_over = true
                return
            }
            if (jsonanswer.result === 'badend') {
                gameWindow.innerHTML = ''
                getStory().then((json) => {
                story = json
                displayTextWithDelay(story.badend, delay)})
                game_over = true
                return
            }
            if (jsonanswer.result === 'neutralend') {
                gameWindow.innerHTML = ''
                getStory().then((json) => {
                story = json
                displayTextWithDelay(story.neutralend, delay)})
                game_over = true
                return
            }
            if (jsonanswer.result === 'Game saved') {
                console.log('round ended successfully')
                update_data()
                gamerounds()
            }
        } catch (error) {
            console.log(error.message)
        } finally {
            console.log('endround loaded')
        }
    }

// Function to run events
async function start_event(){
    let gameWindow = document.querySelector('.game-window')

    try {
        const answer = await fetch('http://127.0.0.1:3000/event/a/start')
        const jsonanswer = await answer.json()

        gameWindow.innerHTML = `<p id="scenario">${jsonanswer.eventtext}</p>`
        if (jsonanswer.choices.length > 0){
            for (let i=1;i<4;i++){
                gameWindow.innerHTML += `
                 <button type="button" class="option-button" id="option${i}">${jsonanswer.choices[i-1][0]}</button>
                `
            }
            const button1 = document.querySelector('#option1')
                button1.addEventListener('click', function(evt){
                    event_choice(1)
                    proceedbutton('airport')
                })
            const button2 = document.querySelector('#option2')
                button2.addEventListener('click', function(evt){
                    event_choice(2)
                    proceedbutton('airport')
                })
            const button3 = document.querySelector('#option3')
            button3.addEventListener('click', function(evt){
                event_choice(3)
                proceedbutton('airport')
            })
        } else {
            proceedbutton('airportwithbutton')
        }

    } catch (error) {
        console.log(error.message)
    } finally {
        console.log('event loaded')
    }
}

async function event_choice(choice){
    try {
        await fetch(`http://127.0.0.1:3000/event/${choice}/choice`)
    } catch (error) {
        console.log(error.message)
    } finally {
        console.log('event choice loaded')
    }
}

//Functions to choose airport and freight
async function airporteventlisteners (ident) {
    const optionNumber1 = document.getElementById('option1');
    optionNumber1.addEventListener('click', function () {
        console.log('You clicked the "option1" button.');
        choises(ident[0].ident, chosenAirport);

        setTimeout(() => {
           choose_freight()
        }, 100);
    });
    const optionNumber2 = document.getElementById('option2');
    optionNumber2.addEventListener('click', function () {
        console.log('You clicked the "option2" button.');
        choises(ident[1].ident, chosenAirport);

        setTimeout(() => {
           choose_freight()
        }, 100);
    });
    const optionNumber3 = document.getElementById('option3');
    optionNumber3.addEventListener('click', function () {
        console.log('You clicked the "option3" button.');
        choises(ident[2].ident, chosenAirport);

        setTimeout(() => {
           choose_freight()
        }, 100);
    });
    const optionNumber4 = document.getElementById('option4');
    optionNumber4.addEventListener('click', function () {
        console.log('You clicked the "option4" button.');
        choises(ident[3].ident, chosenAirport);

        setTimeout(() => {
           choose_freight()
        }, 100);
    });
    const optionNumber5 = document.getElementById('option5');
    optionNumber5.addEventListener('click', function () {
        console.log('You clicked the "option5" button.');
        choises(ident[4].ident, chosenAirport);

        setTimeout(() => {
           choose_freight()
        }, 100);
    });
}


async function freighteventlisteners (freight) {
    const optionNumber1 = document.getElementById('option1');
    optionNumber1.addEventListener('click', function () {
        console.log('You clicked the "option1" button.');
        choises([freight[0].price, freight[0].karma], chosenFreight);

        setTimeout(() => {
           charge_battery()
        }, 100);
    });
    const optionNumber2 = document.getElementById('option2');
    optionNumber2.addEventListener('click', function () {
        console.log('You clicked the "option2" button.');
        choises([freight[1].price, freight[1].karma], chosenFreight);

        setTimeout(() => {
           charge_battery()
        }, 100);
    });
    const optionNumber3 = document.getElementById('option3');
    optionNumber3.addEventListener('click', function () {
        console.log('You clicked the "option3" button.');
        choises([freight[2].price, freight[2].karma], chosenFreight);

        setTimeout(() => {
           charge_battery()
        }, 100);
    });
    const optionNumber4 = document.getElementById('option4');
    optionNumber4.addEventListener('click', function () {
        console.log('You clicked the "option4" button.');
        choises([freight[3].price, freight[3].karma], chosenFreight);

        setTimeout(() => {
           charge_battery()
        }, 100);
    });
    const optionNumber5 = document.getElementById('option5');
    optionNumber5.addEventListener('click', function () {
        console.log('You clicked the "option5" button.');
        choises([freight[4].price, freight[4].karma], chosenFreight);

        setTimeout(() => {
           charge_battery()
        }, 100);
    });
}

function addtext(array, process) {
    let texts = []
    if (process === 'get_airports') {
        for (let i = 0; i < 5; i++) {
            let text = `<h2>${i + 1}:</h2>
                                <p>Name: ${array[i].name}</p>
                                <p>Country: ${array[i].country_name}</p>
                                <p>Distance: ${array[i].distance_km}km</p>`
            texts.push(text)
        }
        return texts
    }
    if (process === 'get_freight') {
        for (let i = 0; i < 5; i++) {
            let text = `<h2>${i + 1}:</h2>
                                <p>Name: ${array[i].name}</p>
                                <p>Price: ${array[i].price}</p>`
            texts.push(text)
        }
        return texts
    }
}

async function airportServices(process) {
    try {
        const answer = await fetch(`http://127.0.0.1:3000/airport/empty/${process}`);
        const jsonAnswer = await answer.json();
        if (process === getAirports || process === getFreight) {
            let text = addtext(jsonAnswer, process)
            gameWindow.innerHTML = '<p id="make-choice">Make your choice!</p>'
            for (let i = 1; i < 6; i++) {
                gameWindow.innerHTML += `<button type="button" class="option-button" id="option${i}">${text[i - 1]}</button>`
            }
        }
        return jsonAnswer
    } catch (error) {
    console.log(error.message);
  } finally {
        console.log('airport data loaded');
    }
}

async function choises (playerinput, process) {
    try {
        await fetch(`http://127.0.0.1:3000/airport/${playerinput}/${process}`)
    } catch (error) {
        console.log(error.message)
    } finally {
        console.log('choice sent to endpoint')
    }
}

async function choose_airport () {
    const airports = await airportServices(getAirports);
    createMapMarkers(airports)
    await airporteventlisteners(airports);
}

async function choose_freight () {
    const freight = await airportServices(getFreight);
    await freighteventlisteners(freight);
}

async function charge_battery () {
    gameWindow.innerHTML = 'Would you like to charge your battery?';
    gameWindow.innerHTML += '<button type="button" class="option-button" id="option1">Yes</button>' +
                            '<button type="button" class="option-button" id="option2">No</button>';

    const optionNumber1 = document.getElementById('option1');
    optionNumber1.addEventListener('click', async function () {
        console.log('player chose to charge battery');
        const charge = await airportServices(chargeBattery);
        gameWindow.innerHTML = charge.text;
        endround()
        gamerounds()
    });

    const optionNumber2 = document.getElementById('option2');
    optionNumber2.addEventListener('click', function () {
        console.log('player chose not to charge battery');
        gameWindow.innerHTML = ''
        endround()
        gamerounds()
    });
}
//Functions to get story text and read it slowly
async function getStory() {
    try {
        const response = await fetch('http://127.0.0.1:3000/get_story');
        const jsonAnswer = await response.json();
        return jsonAnswer

    } catch (error) {
        console.log(error.message);
        return null;
    } finally {
        console.log('story loaded');
    }
}

// to give the story feed some delay
function displayTextWithDelay(text, delay) {
    const words = text.split(' ');
    let index = 0;
    let lastTimestamp = 0;

    function displayNextWord(timestamp) {
        if (!lastTimestamp) {
            lastTimestamp = timestamp;
        }

        if (timestamp - lastTimestamp >= delay && index < words.length) {
            document.querySelector('.game-window').innerHTML += words[index] + ' ';
            index++;
            lastTimestamp = timestamp;
        }

        if (index < words.length) {
            requestAnimationFrame(displayNextWord);
        }
    }

    requestAnimationFrame(displayNextWord);
}

//Function to create a button to pace the game round correctly
function proceedbutton (process) {
    if (process === 'airport') {
        choose_airport()
    } else {
        gameWindow.innerHTML += '<button type="button" class="option-button" id="proceed">Proceed</button>'

        const proceed = document.getElementById('proceed');
        proceed.addEventListener('click', async function () {
            gameWindow.innerHTML = ''
            if (process === 'first') {
                displayTextWithDelay(story.firstevent, delay)
                setTimeout(() => {
                    proceedbutton('airportwithbutton')
                }, 14000)
            }
            if (process === 'airportwithbutton'){
                proceedbutton('airport')
            }


        })
    }
}

// Function for completing the first round of a new player
function firstround (){
    getStory().then((json) => {
    story = json
    displayTextWithDelay(story.story, delay)
        setTimeout(() => {
            proceedbutton('first')
        }, 47000)
})
}

// Run the correct function depending on player being new or not
    if (first_round) {
        create_newUser_form()
    } else {
        userlist()
    }

// This is the main function that starts running the rounds after the first one for new players is completed
function gamerounds(){
        if (game_over){
            return
        }
        start_event().then(()=>{
            update_data()
        })
}

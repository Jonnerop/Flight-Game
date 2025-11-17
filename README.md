# Flight Game

Flight Game is a dynamic aviation simulation game developed as a first-year software project at Metropolia University of Applied Sciences. It combines real-world airport data with engaging storytelling and decision-making mechanics, offering players an immersive and educational experience.

---

## Features

- **Real-World Airport Database**: Utilizes a **MariaDB** database for accurate airport details and locations.  
- **Dynamic Storytelling**: Engaging narrative with karma-based decision-making and multiple endings.  
- **Event-Driven Gameplay**: Randomized in-game events affecting player progress and outcomes.  
- **Fuel and Range Management**: Calculates fuel consumption and range based on real-world distances.  
- **Interactive Frontend**: Built with JavaScript for a dynamic and visually appealing interface.  
- **Scalable Backend**: Flask-based server managing game logic, events, and player state.  

---

## Technical Specifications

- **Backend**: Python with Flask for game state management and server logic.  
- **Database**: MariaDB for storing airport data, player progress, and decisions.  
- **Frontend**: JavaScript-powered interactive game interface.  
- **Libraries and Tools**:  
  - **geopy** for distance calculations.  
  - **Flask-CORS** for cross-origin requests.  
  - **MySQL Connector** for database interactions.  

---

## Components

- Python Backend  
- JavaScript Frontend  
- MariaDB Database  
- Real-World Airport Dataset  

---

## Getting Started

### Prerequisites  
- Python 3.x  
- Flask Framework  
- MariaDB Server  

### Setup  

1. **Clone the Repository**:  
   ```bash  
   git clone https://github.com/your-repo/flight_game.git  
   cd flight_game  
   ```  

2. **Set Up the Database**:  
   - Import the provided SQL schema into your MariaDB server.  
   - Update database credentials in `functions.py`.  

3. **Run the Flask Server**:  
   ```bash  
   python flaskserver.py  
   ```  

4. **Launch the Frontend**:  
   - Open `game.html` in a browser to access the game.  

---

## Usage

1. **Start a New Game**: Enter a username and begin the journey.  
2. **Make Decisions**: Navigate events and make choices to influence outcomes.  
3. **Manage Resources**: Track fuel, money, and karma for successful flights.  
4. **Reach an Ending**: Complete the game with one of multiple narrative outcomes.  

---

## Troubleshooting

- **Database Issues**: Ensure the MariaDB server is running, and credentials are correctly configured.  
- **Frontend Errors**: Verify the JavaScript console for errors and ensure all files are loaded correctly.  
- **Server Not Responding**: Check Flask server logs for issues.  

---

## Contributors
 
- Eetu Oinonen
- Topias Aho
- Tommi Halla
- Jonne Roponen  

---

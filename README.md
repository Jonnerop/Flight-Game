# Flight Game

Flight Game is a dynamic aviation simulation game developed as a first-year software project at Metropolia University of Applied Sciences. It combines real-world airport data with storytelling and decision-making mechanics, offering players an immersive and fun experience.

---

## Features

- **Real-World Airport Data**: Includes accurate airport details and locations used throughout gameplay.  
- **Dynamic Storytelling**:  Narrative with karma-based decisions and multiple endings.  
- **Event-Driven Gameplay**: Randomized events influencing player progress and outcomes.  
- **Fuel and Range Management**: Calculates consumption and range using real-world distances.  
- **Interactive Gameplay**: Responsive user interactions and visual feedback.  
- **Scalable Architecture**: Reliable server logic handling events, state, and progression.  

---

## Technical Specifications

- **Frontend Stack**: JavaScript for rendering the UI and handling user interactions.  
- **Backend Framework**: Python (Flask) for server logic and game state management.  
- **Database Layer**: MariaDB for storing airport data, player progress, and decisions.  
- **Key Libraries & Tools**:  
  - **geopy** for distance calculations  
  - **Flask-CORS** for cross-origin communications  
  - **MySQL Connector** for database operations

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
   git clone https://github.com/Jonnerop/Flight-Game.git  
   cd Flight-Game  
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

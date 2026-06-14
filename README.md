
# Backend for Blood Donation Management System
The Blood Request module enables hospitals or authorized medical personnel to submit requests for specific blood types when blood is needed for patients. The module records important details such as the requested blood group, number of units required, urgency level, patient information (if applicable), and request date.

Once a request is submitted, it is stored in the database and can be viewed by donors, administrators, or blood bank personnel depending on their access rights. The system helps streamline the process of locating suitable donors and managing blood inventory efficiently.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [TechStack](#TechStack)

## Installation
1. Clone the repository:
```bash
 git clone https://github.com/adisacodes/blood-donation-backend.git
```
2. Install dependencies:
```bash
 npm install
 ```

## Usage
```
uvicorn app.main:app --reload
```
## Tech Stack
- Python 3.12
- FastAPI
- SQLite
- SQLAlchemy

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.

## License
This project is a school project.



# Cinematch

Cinematch is a movie recommendation system that helps users discover new movies based on their preferences. The system uses machine learning to provide personalized movie recommendations.

## Features

- User authentication (login/register)
- Movie recommendations based on user preferences
- Favorite movies list
- Popular and top-rated movies
- Beautiful and responsive UI

## Technologies Used

- Python
- Django
- MySQL
- Machine Learning (for recommendations)
- HTML/CSS
- JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cinematch.git
cd cinematch
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
mysql -u root -e "CREATE DATABASE cinematchdb;"
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Register a new account or login
2. Browse popular and top-rated movies
3. Get personalized movie recommendations
4. Add movies to your favorites
5. View and manage your favorite movies in your profile

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
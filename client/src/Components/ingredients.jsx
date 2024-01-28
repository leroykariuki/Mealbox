import React, { useEffect, useState } from 'react';

function Ingredients() {
  const [ingredients, setIngredients] = useState([]);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    fetch('http://127.0.0.1:5555/ingredients')
      .then((response) => response.json())
      .then((data) => {
        setIngredients(data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const theme = isDarkMode ? darkTheme : lightTheme;

  return (
    <div style={{ ...styles.container, ...theme.container }}>
      <header style={styles.header}>
        <h1 style={styles.heading}>Ingredient List</h1>
        <button onClick={toggleDarkMode} style={theme.toggleButton}>
          {isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        </button>
      </header>
      <ul style={styles.list}>
        {ingredients.map((ingredient) => (
          <li key={ingredient.id} style={{ ...styles.listItem, ...theme.listItem }}>
            <p style={{ ...styles.ingredientName, ...theme.ingredientName }}>{ingredient.name}</p>
            <p style={styles.ingredientDetail}>
              Quantity: {ingredient.quantity} {ingredient.unit}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}

const lightTheme = {
  container: {
    backgroundColor: '#F9F9F9',
    color: '#333',
    transition: 'background-color 0.3s ease, color 0.3s ease',
  },
  header: {
    backgroundColor: '#EFEFEF',
    padding: '10px',
    borderRadius: '8px',
    marginBottom: '20px',
  },
  toggleButton: {
    backgroundColor: '#3498db',
    color: '#fff',
  },
  listItem: {
    borderBottom: '1px solid #ccc',
    padding: '15px 0',
  },
  ingredientName: {
    fontSize: '22px',
    fontWeight: 'bold',
    marginBottom: '8px',
    color: '#E44D26',
  },
  ingredientDetail: {
    fontSize: '16px',
    color: '#555',
  },
};

const darkTheme = {
  container: {
    backgroundColor: '#333',
    color: '#fff',
    transition: 'background-color 0.3s ease, color 0.3s ease',
  },
  header: {
    backgroundColor: '#555',
    padding: '10px',
    borderRadius: '8px',
    marginBottom: '20px',
  },
  toggleButton: {
    backgroundColor: '#3498db',
    color: '#fff',
  },
  listItem: {
    borderBottom: '1px solid #666',
    padding: '15px 0',
  },
  ingredientName: {
    fontSize: '22px',
    fontWeight: 'bold',
    marginBottom: '8px',
    color: '#FFD700',
  },
  ingredientDetail: {
    fontSize: '16px',
    color: '#ddd',
  },
};

const styles = {
  container: {
    maxWidth: '100%',
    margin: '0 auto',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  heading: {
    fontSize: '32px',
    fontWeight: 'bold',
    textTransform: 'uppercase',
  },
  list: {
    listStyle: 'none',
    padding: '0',
  },
};

export default Ingredients;

import React, { useEffect, useState } from 'react';

function Meals() {
  const [meals, setMeals] = useState([]);
  const [isExpanded, setIsExpanded] = useState(null);

  useEffect(() => {
    // Make a GET request to your Flask API
    fetch('http://127.0.0.1:5555//meal')
      .then((response) => response.json())
      .then((data) => {
        setMeals(data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const toggleDescription = (id) => {
    setIsExpanded(isExpanded === id ? null : id);
  };

  return (
    <div style={{ ...styles.container, ...getBackgroundPattern() }}>
      <h1 style={styles.heading}>Explore Delicious Meals</h1>
      <ul style={styles.list}>
        {meals.map((meal) => (
          <li key={meal.id} style={styles.listItem}>
            <div style={styles.mealHeader}>
              <h2 style={styles.mealTitle}>{meal.title}</h2>
              <button onClick={() => toggleDescription(meal.id)} style={styles.toggleButton}>
                {isExpanded === meal.id ? 'Collapse' : 'Expand'}
              </button>
            </div>
            {isExpanded === meal.id && (
              <div style={styles.description}>
                <p>{meal.description}</p>
                <p>Category: {meal.category}</p>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

const getBackgroundPattern = () => {
  const patterns = [
    { background: 'linear-gradient(45deg, #3498db, #2ecc71)' },
    { background: 'linear-gradient(45deg, #e74c3c, #3498db)' },
    { background: 'radial-gradient(circle, #e74c3c, #2ecc71)' },
    { background: 'radial-gradient(circle, #3498db, #e74c3c)' },
  ];

  return patterns[Math.floor(Math.random() * patterns.length)];
};

const styles = {
  container: {
    maxWidth: '100%',
    margin: '0 auto',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  },
  heading: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: '20px',
  },
  list: {
    listStyle: 'none',
    padding: '0',
  },
  listItem: {
    borderBottom: '1px solid #ccc',
    padding: '15px 0',
  },
  mealHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
  },
  mealTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#fff',
  },
  toggleButton: {
    backgroundColor: '#3498db',
    color: '#fff',
    padding: '8px 12px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  description: {
    marginTop: '10px',
    color: '#fff',
  },
};

export default Meals;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AddMealForm = () => {
  const [mealData, setMealData] = useState({
    title: '',
    description: '',
    category: '',
  });
  const nav = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setMealData({
      ...mealData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
  
    const formData = new FormData();
    formData.append('title', mealData.title);
    formData.append('description', mealData.description);
    formData.append('category', mealData.category);
  
    fetch('http://127.0.0.1:5000/meal', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Meal added successfully:', data);
        nav('/meal');
      })
      .catch((error) => {
        console.error('Error adding meal:', error);
      });
  };

  return (
    <div
      className="hero"
      style={{
        width: '100%',
        height: '100vh',
        backgroundImage: 'url("/image4.jpg")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        objectFit: 'cover',
        position: 'relative',
      }}
    >
      <div className="overlay">
        <div className="feedback-form">
          <h2>Add a Meal</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Title:</label>
              <input
                type="text"
                name="title"
                required
                value={mealData.title}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label>Description:</label>
              <textarea
                name="description"
                required
                value={mealData.description}
                onChange={handleInputChange}
              ></textarea>
            </div>
            <div className="form-group">
              <label>Category:</label>
              <input
                type="text"
                name="category"
                required
                value={mealData.category}
                onChange={handleInputChange}
              />
            </div>
            <button type="submit">Add Meal</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AddMealForm
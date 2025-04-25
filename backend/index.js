const express = require('express');
const axios = require('axios');  
const app = express();
const port = 3031;

axios.get('http://mlflow:5000')
  .then(response => {
    console.log('MLflow is running:', response.data);  
  })
  .catch(error => {
    console.error('Error connecting to MLflow:', error.message);  
  });

app.use(express.json());

app.post('/predict', async (req, res) => {
  try {
    const { sepalWidth } = req.body;

    if (typeof sepalWidth !== 'number') {
      return res.status(400).send('La largeur du sépale doit être un nombre');
    }

    const response = await axios.post('http://localhost:5000/invocations', {
    data: [[sepalWidth]],  
      dtype: 'float32',
    });

    const predictedLength = response.data;
    res.json({ predictedLength });  
  } catch (error) {
    console.error('Erreur lors de la prédiction :', error);
    res.status(500).send('Erreur serveur');
  }
});

app.listen(port, () => {
  console.log(`Serveur API démarré sur http://localhost:${port}`);
});

const { Pool } = require('pg'); 

const pool = new Pool({
  user: 'Esteban',         
  host: 'db',                
  database: 'mldb',          
  password: 'pass',          
  port: 5432,                
});

pool.connect()
  .then(() => {
    console.log('Connected to the database');
  })
  .catch((err) => {
    console.error('Error connecting to the database:', err.stack);
  });

module.exports = pool;  

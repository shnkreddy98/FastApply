const express = require('express');
const cors = require('cors');
const path = require('path');
const app = express();

// CORS configuration
const corsOptions = {
    origin: 'http://localhost:3000',
    methods: ['POST', 'GET', 'OPTIONS'],
    allowedHeaders: ['Content-Type'],
    credentials: true
};

app.use(cors(corsOptions));
app.use(express.json());

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

app.post('/process', (req, res) => {
    const { job_description } = req.body;
    console.log('Received job description:', job_description);

    const fs = require('fs')
    // Write data in 'Output.txt' .
    fs.writeFile('outputs/jd.txt', job_description, (err) => {
        // In case of a error throw err.
        if (err) throw err;
    })
});

// Start the server
app.listen(3000, () => {
    console.log(`Server is running at http://localhost:3000`);
});
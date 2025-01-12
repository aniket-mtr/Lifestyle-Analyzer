const express = require('express')
const { spawn } = require('child_process'); // To run the Python script
const path = require('path')
const PORT = 5000
const app = express()

app.use(express.static(path.join(__dirname, '../frontend')));
app.use(express.urlencoded({ extended: true }))

app.get('/', (req, res)=>{
    res.sendFile('../frontend/index.html')
})

app.post('/submit', (req, res) => {
    const formData = req.body;

    // Prepare data for Python script
    const { core_circle, bmi, steps, sleep, wlb } = formData;
    const inputData = [core_circle, bmi, steps, sleep, wlb];

    // Run the Python script and pass the data
    const pythonProcess = spawn('C:\\ProgramData\\anaconda3\\python', ['./backend/predict.py', ...inputData]);

    let predictionResult = '';

    // Collect Python script output
    pythonProcess.stdout.on('data', (data) => {
        predictionResult += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            // Redirect to result page with the prediction as a query parameter
            res.redirect(`/result.html?result=${predictionResult.trim()}`);
        } else {
            res.status(500).send('An error occurred while processing your request.');
        }
    });
});

app.listen(PORT, ()=>{
    console.log(`server running on port ${PORT}`)
})
// const express = require('express');
// const mongoose = require('mongoose');
// const bcrypt = require('bcryptjs');
// const bodyParser = require('body-parser');
// const { exec } = require('child_process');
// const path = require('path');

// const app = express();
// const PORT = 3000;

// // Middleware
// app.use(bodyParser.json());
// app.use(bodyParser.urlencoded({ extended: true }));
// app.use(express.static(path.join(__dirname, 'public')));

// // MongoDB Connection
// mongoose.connect('mongodb+srv://shakthinathan34:bNaoFXBAYrkRGOGs@cluster0.oucekiy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', {
//     useNewUrlParser: true,
//     useUnifiedTopology: true
// });
// const db = mongoose.connection;
// db.on('error', console.error.bind(console, 'Connection error:'));
// db.once('open', () => console.log('Connected to MongoDB'));

// // User Schema
// const userSchema = new mongoose.Schema({
//     name: String,
//     email: { type: String, unique: true },
//     password: String,
//     phone: String
// });
// const User = mongoose.model('User', userSchema);

// // Serve success.html when server starts
// app.get('/', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'success.html'));
// });

// // Register Route
// app.post('/signup', async (req, res) => {
//     try {
//         const { name, email, password, phone } = req.body;
//         const hashedPassword = await bcrypt.hash(password, 10);
//         const newUser = new User({ name, email, password: hashedPassword, phone });
//         await newUser.save();
//         res.redirect('/success.html'); // Redirect to success page
//     } catch (error) {
//         console.error(error);
//         res.status(500).send('Error registering user');
//     }
// });

// // Login Route
// app.post('/login', async (req, res) => {
//     try {
//         const { email, password } = req.body;
//         const user = await User.findOne({ email });
//         if (user && await bcrypt.compare(password, user.password)) {
//             res.sendFile(path.join(__dirname, 'public', 'success.html'));
//         } else {
//             res.send('Invalid email or password');
//         }
//     } catch (error) {
//         console.error(error);
//         res.status(500).send('Login error');
//     }
// });

// // Route to start the Python scripts
// const runPythonScript = (scriptName, res) => {
//     const scriptPath = `"E:\\MINI PROJECT\\EYE DET\\Eye-Blink-Detector-Mine\\${scriptName}"`;
//     exec(`python ${scriptPath}`, (error, stdout, stderr) => {
//         if (error) {
//             console.error(`Error: ${error.message}`);
//             res.status(500).send(`Error running ${scriptName}`);
//             return;
//         }
//         if (stderr) {
//             console.error(`stderr: ${stderr}`);
//             res.status(500).send(`Error running ${scriptName}`);
//             return;
//         }
//         console.log(`stdout: ${stdout}`);
//         res.send(`${scriptName} executed successfully.`);
//     });
// };

// // Routes for executing Python scripts
// app.get('/start-drowsiness', (req, res) => runPythonScript('basic.py', res));
// app.get('/start-face-detection', (req, res) => runPythonScript('facedetect.py', res));
// app.get('/view-existing', (req, res) => runPythonScript('new.py', res));

// // Start Server
// app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, 'public')));

// MongoDB Connection
mongoose.connect('mongodb+srv://shakthinathan34:bNaoFXBAYrkRGOGs@cluster0.oucekiy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'Connection error:'));
db.once('open', () => console.log('Connected to MongoDB'));

// User Schema
const userSchema = new mongoose.Schema({
    name: String,
    email: { type: String, unique: true },
    password: String,
    phone: String
});
const User = mongoose.model('User', userSchema);

// ✅ Serve DASH.html as the homepage
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'DASH.html'));
});

// ✅ Register Route (Signup)
app.post('/signup', async (req, res) => {
    try {
        const { name, email, password, phone } = req.body;
        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = new User({ name, email, password: hashedPassword, phone });
        await newUser.save();
        res.redirect('/login.html'); // ✅ Redirect to login page after signup
    } catch (error) {
        console.error(error);
        res.status(500).send('Error registering user');
    }
});

// ✅ Login Route
app.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const user = await User.findOne({ email });
        if (user && await bcrypt.compare(password, user.password)) {
            res.redirect('/success.html'); // ✅ Redirect to success page only after login
        } else {
            res.send('Invalid email or password');
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('Login error');
    }
});

// Start Server
app.listen(3000, () => console.log('Server running on port 3000'));

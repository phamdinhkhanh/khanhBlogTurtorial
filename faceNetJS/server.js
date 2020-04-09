const PORT = process.env.PORT || 3000;
const HOSTNAME = '0.0.0.0';

const express = require('express');
const path = require('path');
const cors = require('cors');
const {get} = require('request');


let app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const viewsDir = path.join(__dirname);

// Bypass CORS error
// var whitelist = ['https://gogul09.github.io/models/mobilenet/model.json']
var corsOptions = {
  origin: '*'
}

// Cấu hình root mặc định.
app.use(express.static(viewsDir));
app.use(express.static(path.join(__dirname, './public')));
app.use(express.static(path.join(__dirname, './images')));
app.use(express.static(path.join(__dirname, './models')));
app.use(express.static(path.join(__dirname, './medias')));

app.get('/age_and_gender_recognition', (req, res) => res.sendFile(path.join(viewsDir, 'ageAndGenderRecognition.html')));


// app.get("/", cors(corsOptions), (req, res, next) => {
// 	// res.header("Access-Control-Allow-Origin", "https://0.0.0.0:5000"); // update to match the domain you will make the request from
//   	res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
// 	res.sendFile(path.join(__dirname+"/index.html"));
// 	next();
// });

app.listen(PORT, (err) => {
	if (err) {
		console.log(err);
	} else {
		console.log("Website is Up on PORT %d and HOSTNAME %s !", PORT, app.get('env'));
	}
});
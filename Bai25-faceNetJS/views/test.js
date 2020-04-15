const PORT = process.env.PORT || 5000;
const HOSTNAME = '127.0.0.1';

const express = require('express');
const path = require('path');
const cors = require('cors');

let app = express();


// Bypass CORS error
// var whitelist = ['https://gogul09.github.io/models/mobilenet/model.json']
var corsOptions = {
  origin: '*'
}

// Cấu hình root mặc định.
app.use(express.static(__dirname));

app.get("/", cors(corsOptions), (req, res, next) => {
	res.header("Access-Control-Allow-Origin", "https://127.0.0.1:5000"); // update to match the domain you will make the request from
  	res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	res.sendFile(path.join(__dirname+"/index.html"));
	next();
});

app.listen(PORT, HOSTNAME, (err) => {
	if (err) {
		console.log(err);
	} else {
		console.log("Website is Up on PORT %d and HOSTNAME %s !", PORT, app.get('env'));
	}
});
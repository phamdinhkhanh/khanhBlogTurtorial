let model;
let IMAGE_WIDTH = 300;


async function loadModel() {
	console.log("model loading mobilenet model kdfah ...");
	loader = document.getElementById("progress-box");
	load_button = document.getElementById("load-button");
	loader.style.display = "block";
	modelName = "mobilenet";
	model = undefined;
	
	model = await tf.loadLayersModel('models/mobilenet/model.json');

	if (typeof model !== "undefined") {
		loader.style.display = "none";
		load_button.disabled = true;		
		load_button.innerHTML = "Loaded Model";
		console.log("model loaded..");
	}
};

function loadImageLocal() {
	console.log("Click into selected file image");
  	document.getElementById("select-file-box").style.display = "table-cell";
  	document.getElementById("predict-box").style.display = "table-cell";
  	document.getElementById("prediction").innerHTML = "Click predict to find my label!";
    renderImage(this.files);
};




function renderImage(file) {
  var reader = new FileReader();
  reader.onload = function(event) {
    let output = document.getElementById('test-image');
  	output.src = reader.result;
  	output.width = IMAGE_WIDTH;
  }
  
  if(event.target.files[0]){
	reader.readAsDataURL(event.target.files[0]);
  }
}

async function predictImage(){
	console.log("Click predict button");
	if (model == undefined) {
		alert("Please load the model first..")
	}
	if (document.getElementById("predict-box").style.display == "none") {
		alert("Please load an image using 'Upload Image' button..")
	}
	
	let image  = document.getElementById("test-image");
	let tensor = preprocessImage(image, modelName);
	let predictions = await model.predict(tensor).data();
	let results = Array.from(predictions)
		.map(function (p, i) {
			return {
				probability: p,
				className: IMAGENET_CLASSES[i]
			};
		}).sort(function (a, b) {
			return b.probability - a.probability;
		}).slice(0, 5);

	document.getElementById("predict-box").style.display = "block";
	document.getElementById("prediction").innerHTML = "MobileNet prediction <br><b>" + results[0].className + "</b>";

	var ul = document.getElementById("predict-list");
	ul.innerHTML = "";
	results.forEach(function (p) {
		console.log(p.className + " " + p.probability.toFixed(6));
		var li = document.createElement("LI");
		li.innerHTML = p.className + " " + p.probability.toFixed(6);
		ul.appendChild(li);
	})

	if (typeof predictions !== "undefined"){
		document.getElementById("progress-box").style.display = "none";
	}
}

function preprocessImage(image, modelName) {
	let tensor = tf.browser.fromPixels(image)
		.resizeNearestNeighbor([224, 224])
		.toFloat();

	if (modelName === undefined) {
		return tensor.expandDims();
	} else if (modelName === "mobilenet") {
		let offset = tf.scalar(127.5);
		return tensor.sub(offset)
			.div(offset)
			.expandDims();
	} else {
		alert("Unknown model name..")
	}
}

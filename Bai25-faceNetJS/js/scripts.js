// B1. Load model
(async () => {
	// Load model
	await faceapi.nets.ssdMobilenetv1.loadFromUri("/models"); 
	await faceapi.nets.faceRecognitionNet.loadFromUri("/models"); 
	await faceapi.nets.faceLandmark68Net.loadFromUri("/models");
})();


// B2. Face Landmark Detection
(async () => { 
	// Load model 
	await faceapi.nets.ssdMobilenetv1.loadFromUri("/models"); 
	await faceapi.nets.faceRecognitionNet.loadFromUri("/models"); 
	await faceapi.nets.faceLandmark68Net.loadFromUri("/models"); // Detect Face 
	const input = document.getElementById("myImg"); 

	// Face detection SingleFace
	const result = await faceapi 
		.detectSingleFace(input, new faceapi.SsdMobilenetv1Options()) 
		.withFaceLandmarks() 
		.withFaceDescriptor(); 

	const displaySize = { width: input.width, height: input.height }; 

	// resize the overlay canvas to the input dimensions 
	const canvas = document.getElementById("myCanvas"); 
	faceapi.matchDimensions(canvas, displaySize); 
	const resizedDetections = faceapi.resizeResults(result, displaySize); 
	console.log(resizedDetections);
})();


// Face Recognition
async function detectNancyFace() {
	const label = "Nancy";
	const numberImage = 5;
	const descriptions = [];

	for (let i = 1; i <= numberImage; i++) {
		//B1: Get image
		const img = await faceapi.fetchImage( 
		`http://localhost:5500/data/Nancy/${i}.jpg`
		);
		
		//B2: Detect image
		const detection = await faceapi
			.detectSingleFace(img)
			.withFaceLandmarks()
			.withFaceDescriptor(); 
		
		//B3: Add image into descriptions
		descriptions.push(detection.descriptor);
	}

	return new faceapi.LabeledFaceDescriptors(label, descriptions);
}
 
// Detect many faces
async function detectAllLabeledFaces() {
const labels = ["Nancy", "Yeonwoo"];
	return Promise.all(
		labels.map(async label => {
			const descriptions = [];
			for (let i = 1; i <= 2; i++) {
				const img = await faceapi.fetchImage( 
				`http://localhost:5500/data/${label}/${i}.jpg`
				);
				const detection = await faceapi
					.detectSingleFace(img)
					.withFaceLandmarks()
					.withFaceDescriptor(); 
				descriptions.push(detection.descriptor);
			}
			return new faceapi.LabeledFaceDescriptors(label, descriptions);
		})
	);
}
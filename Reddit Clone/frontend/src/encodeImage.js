// encodeImage.js encodes a file to base64 to allow the API to
// process the image
// z5259931

const encode = () => {
    const reader = new FileReader();
    // grabs the name of the image being uploaded 
    const file = document.querySelector("input[type=file]").files[0];

    if (file) {
        reader.readAsDataURL(file);
    }

    reader.addEventListener('load', () => {
        window.encodedImage = reader.result;
        // replaces the result to return only the encoded section
        window.encodedImage = window.encodedImage.replace(/data.*,/gi, '');
    })
}

export { encode };
const inputFile = document.getElementById("id_image");

inputFile.addEventListener('change', previewPhoto);

const previewPhoto = () => {
    const file = inputFile.files;
    if (file) {
        const fileReader = new FileReader();
        const preview = document.getElementById('preview');
        fileReader.onload = event => {
            preview.setAttribute('src', event.target.result);
        }
        fileReader.readAsDataURL(file[0]);
    }
}


const inputFile = document.getElementById("image");

const previewPhoto = () => {
    const file = inputFile.files;
    if (file) {
        const fileReader = new FileReader();
        const preview = document.getElementById('preview');
        fileReader.onload = event => {
            preview.setAttribute('src', event.target.result);
        }
        fileReader.readAsDataURL(file[0]);
        document.getElementById('previewDiv').classList.remove("hidden");

    }
}

inputFile.addEventListener('change', previewPhoto);


let autocomplete;

function initMap() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById("address"),
        {
            types: ['establishment'],
            componentRestrictions: { country: ["us"] },
            fields: ["place_id","address_components", "geometry", "icon", "name"],
        }
    );
    autocomplete.addListener('place_change', onPlaceChange)
}

function onPlaceChange() {
    var place = autocomplete.getPlace();

    if (!place.geometry) {
        
    } else {
        placeid = document.getElementById("placeid")
        placeid.value = place.place_id
    }
}



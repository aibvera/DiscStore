window.addEventListener("load", async() => {
    await initialLoad();
});

const initialLoad = async() => {
    await catalog();
};

const catalog = async() => {
    try {
        const response = await fetch("/albums");
        const data = await response.json();
        if (data.message == "Success") {

            // Inicio de acciones
            let album_divs = ``;
            data.albums.forEach((album) => {
                album_divs += `
                    <div class="album_container">
                        <ul class="catalog_album">
                        <li>Album: ${album.Album_Name}</li>
                        <li>Artista: ${album.Id_Artist__Artist_Name}</li>
                        <li>Genero principal: ${album.Album_MainGenre}</li>
                        <li>Precio: S/ ${album.Album_Price}</li>
                        </ul>
                    </div>
                `
            });
            catalog_div.innerHTML = album_divs;
            // Fin

        } else {
            alert('No se encontraron álbumes...')
        }
    } catch (error){
        console.log(error)
    }
};
document.getElementById("uploadForm").onsubmit = async function(event) {
    event.preventDefault();

    let formData = new FormData(this);
    let response = await fetch(this.action, {
        method: this.method,
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });

    if (response.ok) {
        let result = await response.json();
        if (result.download_link) {
            fetch(result.download_link)
                .then(res => res.blob())
                .then(blob => {
                    JSZip.loadAsync(blob).then(function(zip) {
                        let imageContainer = document.getElementById("images");
                        let sheetContainer = document.getElementById("sheets");

                        zip.forEach(function(relativePath, zipEntry) {
                            if (relativePath.startsWith("images/")) {
                                zipEntry.async("blob").then(function(data) {
                                    let img = document.createElement("img");
                                    img.src = URL.createObjectURL(data);
                                    imageContainer.appendChild(img);
                                });
                            } else if (relativePath.startsWith("sheets/")) {
                                zipEntry.async("string").then(function(data) {
                                    let parser = new DOMParser();
                                    let doc = parser.parseFromString(data, "application/xml");
                                    let table = document.createElement("table");
                                    let headerRow = table.insertRow();

                                    // Assuming first row contains column names
                                    Array.from(doc.getElementsByTagName("Column")).forEach(column => {
                                        let th = document.createElement("th");
                                        th.textContent = column.textContent;
                                        headerRow.appendChild(th);
                                    });

                                    Array.from(doc.getElementsByTagName("Row")).forEach(row => {
                                        let tableRow = table.insertRow();
                                        Array.from(row.getElementsByTagName("Cell")).forEach(cell => {
                                            let td = tableRow.insertCell();
                                            td.textContent = cell.textContent;
                                        });
                                    });

                                    sheetContainer.appendChild(table);
                                });
                            }
                        });
                    });
                });
        }
    } else {
        let error = await response.json();
        alert(error.error);
    }
}

async function post(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    // Error
    if (!response.ok) {
        console.log(response)
        const jsonData = await response.json()
        alert(jsonData.message)


        throw new Error(`HTTP error! status: ${response.status}`);
    }
    // Return data
    let jsonData = await response.json();
    return jsonData;
}




// --- Players page -----



    // document.addEventListener("DOMContentLoaded", function () {
    //     winners()
    // });

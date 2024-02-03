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


function players() {
    let data = { "type": "players" };
    let url = '/api/get/players';

    let response = post(url, data).then(response => {

        var customMutatorDate = function (value, data, type, params, component) {
            let currentDate = new Date(data.date_joined);
            let date = currentDate.getDate();
            let month = currentDate.getMonth();
            let year = currentDate.getFullYear();
            let dateMonthYear = date + "/" + month + "/" + year;
            return dateMonthYear
        }

        var players_table = new Tabulator("#players_table", {
            data: response, //set initial table data
            // layout: "fitDataStretch",
            layout: "fitColumns",
            resizableColumnFit: true,
            selectable: 1,


            columns: [
                { title: "#", field: "id", resizable: true, visible: false },
                { title: "VOORNAAM", field: "firstname", resizable: true },
                { title: "ACHTERNAAM", field: "lastname", resizable: true },
                { title: "BIJNAAM", field: "nickname", resizable: true },
                { title: "ARCADE NAAM", field: "arcadename", resizable: true },
                { title: "EMAIL", field: "email", resizable: true },
                { title: "DATE", field: "date_joined", resizable: true, mutator: customMutatorDate }
            ]
        });

        players_table.on("rowSelected", function (row) {
            var selectedData = players_table.getSelectedData();

            document.getElementById("removeButton").value = selectedData[0].id;

            document.getElementById("Formid").value = selectedData[0].id;
            document.getElementById("FormFirstname").value = selectedData[0].firstname;
            document.getElementById("FormLastname").value = selectedData[0].lastname;
            document.getElementById("FormNickname").value = selectedData[0].nickname;
            document.getElementById("FormArcadename").value = selectedData[0].arcadename;
            document.getElementById("FormEmail").value = selectedData[0].email;

            var myModal = new bootstrap.Modal(document.getElementById('editPlayerModal'))
            myModal.show()

        });
    });
}

function addPlayer() {
    var myModal = new bootstrap.Modal(document.getElementById('addPlayerModal'))
    myModal.show()
}

function removePlayer(playerId) {
    if (confirm('Weet je het zeker dat je deze speler wil verwijderen.')) {
        let data = { playerid: playerId };
        let url = '/api/remove/player';

        post(url, data)
        window.location.reload();

    } else {
        // Do nothing!
        console.log('Player not removed.');
    }
}




    // document.addEventListener("DOMContentLoaded", function () {
    //     winners()
    // });

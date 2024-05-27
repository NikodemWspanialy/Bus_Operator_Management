fetch("table.json")
.then(function(response){
    return response.json();
})
.then(function(table){
    let placeholder = document.querySelector("#data-output");
    let out = "";
    for(let i of table){
        out += `
        <tr>
            <td>${i.username}</td>
            <td>${i.identifier}</td>
            <td>${i.firstName}</td>
            <td>${i.lastName}</td>
        </tr>
        `;
    }

    placeholder.innerHTML = out;
})
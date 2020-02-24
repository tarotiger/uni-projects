// searchSeddit.js allows user to go search for posts via text and title 

// will go through each user you have followed and search their posts 
const seddit = (apiUrl, query) => {
    // displays the number of results found
    const numQueries = document.createElement("div");
    numQueries.style.padding = "5px 0px";
    numQueries.textContent = `${window.queries} result/s found with query '${query}'`;
    document.getElementById("feed").appendChild(numQueries);

    // goes through each user that you're following and returns the posts they have made 
    window.follows.forEach(element => {
        fetch(`${apiUrl}/user/?username=${element}`, {
                headers: {
                    'Authorization': `Token ${window.token}`
                }
            })
            .then((response) => response.json())
            .then((user) => {
                console.log(user);
                matchQuery(apiUrl, query, numQueries);
            })
    });
}

export { seddit };
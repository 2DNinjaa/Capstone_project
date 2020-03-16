var scroller = document.querySelector("#scroller");
var template = document.querySelector('#post_template');
var sentinel = document.querySelector('#sentinel');
var counter = 0;

function loadItems() {
    var title = $(document).find("title").text();

    // Use fetch to request data and pass the counter value in the QS
    fetch(`/load?c=${counter}?t=${title}`).then((response) => {

        // Convert the response data to JSON
        response.json().then((data) => {
            if (!data.length) {

                // Replace the spinner with "No more posts"
                sentinel.innerHTML = "No more jobs";
                return;
            }

            // Iterate over the items in the response
            for (var i = 0; i < data.length; i++) {
                let template_clone = template.content.cloneNode(true);
                if (title.includes('Bookmark')){
                    template_clone.querySelector("#postLink")["href"] = "bookmarkPage/" + `${data[i][0]}`;
                } else {
                    template_clone.querySelector("#postLink")["href"] = "jobPage/" + `${data[i][0]}`;
                }
                //template_clone.querySelector("#postLink")["href"] =
                //   Flask.url_for('jobPage', { cnt: `${data[i][0]}`});

                if (`${data[i][2]}` == 'Jobs') {
                    template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]['jobTitle']}`;
                    template_clone.querySelector("#company").innerHTML = `${data[i][1]['company']}`;
                    template_clone.querySelector("#location").innerHTML = `${data[i][1]['location']}` + ', ';
                    template_clone.querySelector("#pay").innerHTML = `${data[i][1]['salary']}`;

                } else {
                    template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]['userName']}`;
                    template_clone.querySelector("#company").innerHTML = `${data[i][1]['skills']}`;
                    template_clone.querySelector("#location").innerHTML = `${data[i][1]['location']}` + ', ';
                    //template_clone.querySelector("#pay").innerHTML = `${data[i][1]['salary']}`;
                }
                // Append template to dom
                scroller.appendChild(template_clone);

                // Increment the counter
                counter += 1;

            }
        })
    })
}

// Create a new IntersectionObserver instance
var intersectionObserver = new IntersectionObserver(entries => {
    // If intersectionRatio is 0, the sentinel is out of view
    // and we don't need to do anything. Exit the function
    if (entries[0].intersectionRatio <= 0) {
        return;
    }

    // Call the loadItems function
    loadItems();
});

// Instruct the IntersectionObserver to watch the sentinel
intersectionObserver.observe(sentinel);